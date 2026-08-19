#!/usr/bin/env python3
"""Forja de sites en Railway: consume la cola del panel y construye demos completos.

POR QUE EXISTE (2026-08-14): la forja en la nube de Anthropic corre por slots (~7 min),
reclama lotes que a veces mueren a mitad, y su IP no llega bien a Instagram. Este worker
vive en Railway (misma plataforma que ig-photo-service, que ya demostro llegar a IG),
sondea la cola cada 25 segundos y procesa de UNO en uno, reportando progreso real.

FLUJO por item:
  1. reclamar (progress research) apenas se toma; los demas quedan pending
  2. resolver el input a un handle de IG (si viene un nombre, Claude + web_search lo busca)
  3. research_ig.py: fotos + bio + telefono + contact sheet (Playwright local del container)
  4. UNA llamada a Claude (vision): curacion del sheet + content.json + dm, con reglas
     anti-invencion; despues un guard PROGRAMATICO: todo numero del copy debe existir en
     los hechos, toda foto referenciada debe existir en disco
  5. derive.py + gate.py (los mismos del repo, empaquetados aqui)
  6. subir al repo por la API de GitHub -> Workers Builds deploya solo
  7. esperar el 200 del demo, registrar en el panel (registry-upsert) y marcar done

REGLAS QUE HEREDA DEL FORGE-BRIEF: solo datos reales (los hechos vienen del research);
sin resenas ni precios inventados (modo razones); menos de 5 fotos usables = failed;
nunca dos items a la vez; el research degradado NO condena al negocio (se deja con nota
para reintento, no se marca failed por ceguera).
"""
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

PANEL = os.environ.get('PANEL_URL', 'https://siteforge-panel.odd-forest-9504.workers.dev')
DEMOS = 'https://siteforge-demos.odd-forest-9504.workers.dev'
GH_REPO = os.environ.get('GH_REPO', 'luiso2/webistecreator')
GH_TOKEN = os.environ['GITHUB_TOKEN']
# Proveedor LLM: DeepSeek si hay key (decision del usuario 2026-08-18); Anthropic como
# alternativa si su variable esta presente. DeepSeek NO tiene vision ni busqueda web:
# la curacion usa los alt-texts de las fotos (IG marca los flyers con "text that says")
# y los items por NOMBRE se dejan para la rutina cloud, que si puede buscar.
DEEPSEEK_KEY = os.environ.get('DEEPSEEK_API_KEY')
ANTHROPIC_KEY = os.environ.get('ANTHROPIC_API_KEY')
MODELO = os.environ.get('LLM_MODEL', 'claude-sonnet-5')  # modelo del camino Anthropic
if not (DEEPSEEK_KEY or ANTHROPIC_KEY):
    raise SystemExit('Falta DEEPSEEK_API_KEY o ANTHROPIC_API_KEY')
POLL_S = int(os.environ.get('POLL_SECONDS', '25'))
FORBID = 'Pure Artistry,pure.artistrysk,Booksy,booksy,121705,silk press,locs,K-Tip,W Grant,Chianita,Hair Studio'

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)


def http(url, data=None, headers=None, method=None, timeout=90):
    req = urllib.request.Request(url, method=method or ('POST' if data is not None else 'GET'))
    # Cloudflare bloquea el UA por defecto de Python (Python-urllib) desde IPs de datacenter:
    # el worker recibia 403 en /api/public/queue. Un UA identificable y con forma de navegador pasa.
    req.add_header('User-Agent', 'Mozilla/5.0 (compatible; siteforge-forja/1.0; +railway)')
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    body = json.dumps(data).encode() if isinstance(data, (dict, list)) else data
    if body is not None:
        req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, body, timeout=timeout) as r:
        return json.loads(r.read().decode())


def panel(ruta, data=None):
    try:
        return http(f'{PANEL}{ruta}', data)
    except Exception as e:
        print(f'  panel {ruta}: {e}', flush=True)
        return None


def progreso(item_id, stage, note=None):
    panel('/api/public/queue/progress', {'id': item_id, 'stage': stage, **({'note': note} if note else {})})


def terminar(item_id, **result):
    panel('/api/public/queue/done', {'id': item_id, **result})


def llm(prompt, max_tokens=8000, imagen_b64=None):
    """DeepSeek primero (eleccion del usuario); si falla (p.ej. sin saldo, comprobado
    2026-08-18: 'Insufficient Balance'), cae a Anthropic para que la forja no se detenga.
    En cuanto DeepSeek tenga saldo vuelve a ser el que responde, sin redeploy."""
    if DEEPSEEK_KEY:
        try:
            data = {'model': 'deepseek-chat', 'max_tokens': max_tokens,
                    'messages': [{'role': 'user', 'content': prompt}]}
            r = http('https://api.deepseek.com/chat/completions', data,
                     headers={'Authorization': f'Bearer {DEEPSEEK_KEY}'}, timeout=300)
            return r['choices'][0]['message']['content']
        except Exception as e:
            if not ANTHROPIC_KEY:
                raise
            print(f'  deepseek fallo ({str(e)[:80]}); usando anthropic', flush=True)
    contenido = [{'type': 'text', 'text': prompt}]
    if imagen_b64:
        contenido.insert(0, {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/jpeg', 'data': imagen_b64}})
    r = http('https://api.anthropic.com/v1/messages',
             {'model': MODELO, 'max_tokens': max_tokens, 'messages': [{'role': 'user', 'content': contenido}]},
             headers={'x-api-key': ANTHROPIC_KEY, 'anthropic-version': '2023-06-01'}, timeout=300)
    return '\n'.join(b.get('text', '') for b in r.get('content', []) if b.get('type') == 'text')


def subir_github(ruta_local, ruta_repo, intento=0):
    """Sube un archivo por la API de contents. Reintenta el 409 de SHA (commits concurrentes)."""
    with open(ruta_local, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    url = f'https://api.github.com/repos/{GH_REPO}/contents/{ruta_repo}'
    hdr = {'Authorization': f'Bearer {GH_TOKEN}', 'Accept': 'application/vnd.github+json'}
    sha = None
    try:
        sha = http(url + '?ref=main', headers=hdr).get('sha')
    except Exception:
        pass
    data = {'message': f'forja-railway: {ruta_repo}', 'content': b64, 'branch': 'main', **({'sha': sha} if sha else {})}
    try:
        http(url, data, headers=hdr, method='PUT', timeout=120)
        return True
    except Exception as e:
        if intento < 2:
            time.sleep(4)
            return subir_github(ruta_local, ruta_repo, intento + 1)
        print(f'  subida fallo {ruta_repo}: {e}', flush=True)
        return False


def parece_handle(s):
    s = s.strip()
    return bool(re.fullmatch(r'@?[A-Za-z0-9._]{2,30}', s)) and ' ' not in s


# Sin busqueda web (DeepSeek): un item por NOMBRE no se puede resolver a handle sin
# adivinar, y adivinar esta prohibido. Esos items se SALTAN sin reclamarlos, para que la
# rutina cloud (que si busca) los tome. Esta forja procesa los que traen @handle.


PROMPT_CONTENIDO = """Eres el curador y redactor de la forja Siteforge. NO puedes ver las fotos:
trabajas con sus ALT-TEXTS de Instagram (campo fotos_utilizables de los hechos; las que IG
marco como graficos con texto ya fueron descartadas). Elige por el alt, se conservador: si
un alt sugiere retrato, selfie, meme o producto, NO va en galeria.

HECHOS (unica fuente de verdad):
%s

TAREA, responde UN SOLO JSON:
{"construible": true|false, "motivo": "...",
 "fotos": {"hero": "bk-N.jpg", "nosotros": ["...","..."], "galeria": ["..." x6], "contacto": "..."},
 "dm": "mensaje de primer contacto, 300-400 chars, formato: ELLOS primero -> link -> sin riesgo -> pregunta",
 "content": { ...content.json completo con el MISMO schema del ejemplo de abajo... }}

CURACION (regla dura): en galeria SOLO fotos reales del TRABAJO del negocio. PROHIBIDO:
flyers o graficos con texto, memes, retratos/selfies, fotos de otras cuentas, stock,
capturas con caption encima. Si tras descartar no quedan 5 usables: construible=false y
motivo detallado (no fuerces un demo pobre). El logo del avatar es logo.jpg.

CONTENIDO (regla dura): ni UN dato factual fuera de los HECHOS. Sin precios, resenas,
ratings, anos de experiencia, zonas ni credenciales salvo que esten en los hechos. Los
posts de IG se llaman "publicaciones", NUNCA "proyectos" ni "trabajos" (N posts no son N
trabajos). social_proof modo "razones". contacto sin mapa (usa contacto.imagen). Bilingue
es/en en cada texto; lang principal = idioma_principal de los hechos. cta_url del canal de
los hechos. slug, base="dark-v2".

SCHEMA de ejemplo (copiar estructura exacta, cambiar solo contenido):
%s"""


def fotos_curables(hechos):
    """Prefiltro DETERMINISTICO con los alt-texts de IG: los flyers y capturas con caption
    vienen marcados con 'text that says'. Sin vision, esto es la primera linea de curacion."""
    fotos = hechos.get('fotos', [])
    caps = hechos.get('captions', [])
    limpias, sucias = [], []
    for i, f in enumerate(fotos):
        alt = (caps[i] if i < len(caps) else '') or ''
        (sucias if 'text that says' in alt.lower() else limpias).append({'foto': f, 'alt': alt[:160]})
    return limpias, sucias


def curar_y_redactar(slug, hechos):
    with open(f'{AQUI}/ejemplo-content.json', encoding='utf-8') as f:
        ejemplo = f.read()
    limpias, sucias = fotos_curables(hechos)
    if len(limpias) < 5:
        return {'construible': False,
                'motivo': f'Solo {len(limpias)} fotos sin texto encima segun los alt de IG '
                          f'({len(sucias)} marcadas como graficos/flyers). Liston: 5.'}
    hechos = dict(hechos)
    hechos['fotos_utilizables'] = limpias
    hechos['fotos_descartadas_por_texto'] = [s['foto'] for s in sucias]
    salida = llm(PROMPT_CONTENIDO % (json.dumps(hechos, ensure_ascii=False, indent=1), ejemplo),
                 max_tokens=16000)
    m = re.search(r'\{.*\}', salida, re.S)
    return json.loads(m.group(0)) if m else None


def guard_anti_invencion(content, hechos, slug):
    """Deterministico: numeros del copy respaldados y fotos existentes. Devuelve lista de fallos."""
    fallos = []
    hechos_txt = re.sub(r'[^0-9]', '', json.dumps(hechos))
    for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', json.dumps(content, ensure_ascii=False)):
        for num in re.findall(r'\d[\d,.]{1,}\d', m.group(1)):
            limpio = re.sub(r'[^0-9]', '', num)
            if len(limpio) >= 2 and limpio not in hechos_txt:
                fallos.append(f'numero sin respaldo: {num}')
    for foto in set(re.findall(r'(?:bk-\d+|logo)\.jpg', json.dumps(content))):
        if not os.path.exists(f'output/{slug}/assets/raw/{foto}'):
            fallos.append(f'foto inexistente: {foto}')
    return sorted(set(fallos))


def procesar(item):
    iid, entrada = item['id'], item['input'].strip()
    print(f'== {entrada}', flush=True)
    progreso(iid, 'research', 'forja-railway')

    handle = entrada.lstrip('@')
    slug = re.sub(r'[^a-z0-9-]', '', handle.lower().replace('.', '-').replace('_', '-'))[:40]

    r = subprocess.run([sys.executable, 'scripts/research_ig.py', handle, slug],
                       capture_output=True, text=True, timeout=300)
    ruta_data = f'output/{slug}/data.json'
    if not os.path.exists(ruta_data):
        terminar(iid, failed=True, motivo=f'Research sin datos: {(r.stdout or r.stderr)[-180:]}')
        return
    hechos = json.load(open(ruta_data, encoding='utf-8'))
    if hechos.get('research_degradado') or len(hechos.get('fotos', [])) < 5:
        # ceguera != negocio malo: se deja con nota; el rescate de 40 min lo reofrece
        progreso(iid, 'research', f'IG dio {len(hechos.get("fotos", []))} fotos desde Railway; reintento luego')
        return
    hechos['slug'] = slug
    hechos['idioma_principal'] = 'es'  # Claude puede cambiarlo si la bio es EN; el gate valida coherencia

    progreso(iid, 'build')
    plan = curar_y_redactar(slug, hechos)
    if not plan:
        terminar(iid, failed=True, motivo='La curacion no devolvio JSON valido')
        return
    if not plan.get('construible'):
        terminar(iid, failed=True, motivo=f'Curacion visual: {plan.get("motivo", "?")[:200]}')
        return
    content = plan['content']
    content['slug'], content['base'] = slug, 'dark-v2'
    fallos = guard_anti_invencion(content, hechos, slug)
    if fallos:
        terminar(iid, failed=True, motivo=f'Guard anti-invencion: {"; ".join(fallos[:4])}')
        return
    json.dump(content, open(f'output/{slug}/content.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    subprocess.run(['cp', 'templates/.assetsignore-template', f'output/{slug}/.assetsignore'])

    if subprocess.run([sys.executable, 'scripts/derive.py', slug], capture_output=True).returncode != 0:
        terminar(iid, failed=True, motivo='derive.py fallo (ancla rota)')
        return
    progreso(iid, 'verify')
    lang = content.get('lang', 'es')
    g = subprocess.run([sys.executable, 'scripts/gate.py', slug, '--lang', lang, '--forbid', FORBID],
                       capture_output=True, text=True)
    if g.returncode != 0:
        terminar(iid, failed=True, motivo=f'GATE: {g.stdout[-200:]}')
        return

    progreso(iid, 'commit')
    fotos_usadas = sorted(set(re.findall(r'(?:bk-\d+|logo)\.jpg', open(f'output/{slug}/content.json').read())))
    ok = subir_github(f'output/{slug}/index.html', f'output/{slug}/index.html')
    for f in ['content.json', 'data.json', '.assetsignore']:
        ok &= subir_github(f'output/{slug}/{f}', f'output/{slug}/{f}')
    for f in fotos_usadas:
        ok &= subir_github(f'output/{slug}/assets/raw/{f}', f'output/{slug}/assets/raw/{f}')
    if not ok:
        terminar(iid, failed=True, motivo='Subida a GitHub incompleta')
        return

    url = f'{DEMOS}/{slug}/'
    for _ in range(30):  # Workers Builds tarda 2-10 min segun cola
        time.sleep(25)
        try:
            if urllib.request.urlopen(url, timeout=15).status == 200:
                break
        except Exception:
            pass
    else:
        terminar(iid, failed=True, motivo='El demo no respondio 200 tras el deploy (no se registra)')
        return

    panel('/api/public/registry-upsert', {
        'slug': slug, 'name': content.get('brand', {}).get('name', slug),
        'city': (hechos.get('ciudad') or ''), 'ig': f'@{handle}', 'url_demo': url,
        'phone': hechos.get('phone'), 'language': lang, 'has_own_site': bool(hechos.get('has_own_site')),
        'thumb': f'{url}assets/raw/{plan["fotos"]["hero"]}', 'dm_message': plan.get('dm', '')[:500],
    })
    terminar(iid, slug=slug, name=content.get('brand', {}).get('name', slug), url_demo=url)
    print(f'  LISTO {url}', flush=True)


def main():
    print(f'forja-railway arrancada (poll {POLL_S}s, modelo {MODELO})', flush=True)
    while True:
        q = panel('/api/public/queue') or {}
        pendientes = q.get('pending', [])
        mios = [p for p in pendientes if parece_handle(p.get('input', ''))]
        if mios:
            try:
                procesar(mios[0])  # de UNO en uno, regla del brief; los de nombre son de la rutina cloud
            except Exception as e:
                print(f'  error procesando: {e}', flush=True)
                try:
                    terminar(mios[0]['id'], failed=True, motivo=f'Excepcion en forja-railway: {str(e)[:160]}')
                except Exception:
                    pass
        time.sleep(POLL_S)


if __name__ == '__main__':
    main()
