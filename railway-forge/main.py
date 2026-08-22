#!/usr/bin/env python3
"""Forja de sites en Railway: consume la cola del panel y construye demos completos.

POR QUE EXISTE (2026-08-14): la rutina cloud anterior corría por slots (~7 min),
reclamaba lotes que a veces morían a mitad y dejaba nombres sin construir. Este worker
vive en Railway, sondea la cola cada 10 segundos y procesa de UNO en uno, reportando
progreso real.

FLUJO por item:
  1. reclamar (progress research) apenas se toma; los demas quedan pending
  2. research del input: Instagram para handles o Google Maps para nombre + ciudad
  3. research_ig.py / maps_research.py: fotos, datos públicos y contact sheet (Playwright local del container)
  4. curación por reglas + plantillas por nicho; después un guard PROGRAMATICO: todo
     numero del copy debe existir en los hechos y toda foto referenciada debe existir
     en disco
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
import urllib.error
import urllib.request

import contenido_script as cs

PANEL = os.environ.get('PANEL_URL', 'https://siteforge-panel.odd-forest-9504.workers.dev')
DEMOS = 'https://siteforge-demos.odd-forest-9504.workers.dev'
GH_REPO = os.environ.get('GH_REPO', 'luiso2/webistecreator')
GH_TOKEN = os.environ['GITHUB_TOKEN']
# SIN IA (decision del usuario 2026-08-18): curacion por reglas y plantillas por nicho,
# todo en contenido_script.py. Cero costo por site, cero dependencia de APIs de modelos.
# Los items por NOMBRE se resuelven con la ficha pública de Google Maps; antes se dejaban
# sin reclamar y por eso se acumulaban indefinidamente cuando la rutina cloud estaba llena.
POLL_S = int(os.environ.get('POLL_SECONDS', '10'))
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


def reclamar(item):
    """Reclama un item de forma atomica antes de hacer research o build.

    El endpoint publico responde 409 cuando otra instancia ya lo tomó. Sin este
    paso dos workers de Railway podían investigar y publicar el mismo negocio.
    """
    try:
        result = http(f'{PANEL}/api/public/queue/claim', {'id': item['id']})
        return result.get('item') if isinstance(result, dict) else None
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            print(f'  item ya reclamado por otra forja: {item.get("input")}', flush=True)
        else:
            print(f'  claim HTTP {exc.code}: {item.get("input")}', flush=True)
    except Exception as exc:
        print(f'  claim fallo: {exc}', flush=True)
    return None


def tomar_siguiente(candidatos):
    """Reintenta dentro de la misma lectura si otra réplica ganó el primer claim."""
    for candidato in candidatos:
        item = reclamar(candidato)
        if item:
            return item
    return None


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
    hechos['idioma_principal'] = 'es'  # el gate valida la coherencia del copy generado

    progreso(iid, 'build')
    # Sin IA (decision del usuario 2026-08-18): curacion por reglas + plantillas por nicho
    fotos_sel, motivo = cs.curar(hechos)
    if not fotos_sel:
        terminar(iid, failed=True, motivo=f'Curacion por reglas: {motivo[:220]}')
        return
    content, dm, nicho = cs.construir(hechos, fotos_sel)
    print(f'  nicho={nicho}', flush=True)
    plan = {'fotos': fotos_sel, 'dm': dm}
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
    for _ in range(72):  # Workers Builds tarda 2-10 min segun cola; sondeo corto reduce latencia
        time.sleep(10)
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


def procesar_nombre(item, cerrar=True, progress_id=None):
    """Construye entradas directas (nombre + ciudad) desde Google Maps.

    Google Maps entrega nombre, rating, contacto, website declarado y fotos públicas sin
    adivinar un handle de Instagram. Menos de cinco fotos propias se cierra con motivo
    concreto en vez de dejar el item pendiente para siempre.
    """
    iid, entrada = item['id'], item['input'].strip()
    report_id = progress_id or iid

    def report(stage, note=None):
        progreso(report_id, stage, note)

    def fail(motivo):
        if cerrar:
            terminar(iid, failed=True, motivo=motivo)
        return {'failed': True, 'motivo': motivo}

    print(f'== {entrada} (Google Maps)', flush=True)
    report('research', 'ficha publica de Google Maps')
    m = re.match(r'^(.*?)\s*\(([^)]+)\)\s*$', entrada)
    nombre = (m.group(1) if m else entrada).strip()
    ciudad = (m.group(2) if m else 'Florida').strip()
    # El panel acepta slugs de hasta 40 caracteres; respetar el mismo límite aquí
    # evita terminar todo el build y dejar el item atascado al llamar a /done.
    slug = re.sub(r'[^a-z0-9-]', '', nombre.lower().replace('&', ' and ').replace('.', '-').replace('_', '-').replace(' ', '-'))[:40].strip('-')
    r = subprocess.run([sys.executable, 'scripts/maps_research.py', f'{nombre}, {ciudad}', slug], capture_output=True, text=True, timeout=360)
    ruta_data = f'output/{slug}/data.json'
    if not os.path.exists(ruta_data):
        return fail(f'Research Google Maps sin datos: {(r.stdout or r.stderr)[-180:]}')
    hechos = json.load(open(ruta_data, encoding='utf-8'))
    if hechos.get('status') == 'PERMANENTLY_CLOSED':
        return fail('La ficha de Google Maps figura como permanentemente cerrada.')
    if hechos.get('has_own_site'):
        return fail('La ficha ya tiene un website propio; se respeta el filtro sin website.')
    fotos = hechos.get('fotos') or []
    if len(fotos) < 5:
        return fail(f'Google Maps solo expone {len(fotos)} fotos propias; se necesitan al menos 5 para una galeria real.')
    report('build', f'{len(fotos)} fotos publicas verificadas')
    b = subprocess.run([sys.executable, 'scripts/build_maps_site.py', slug], capture_output=True, text=True, timeout=120)
    if b.returncode != 0:
        return fail(f'build_maps_site fallo: {(b.stdout or b.stderr)[-220:]}')
    d = subprocess.run([sys.executable, 'scripts/derive.py', slug], capture_output=True, text=True, timeout=120)
    if d.returncode != 0:
        return fail('derive.py fallo para item por nombre')
    subprocess.run(['cp', 'templates/assets/tailwind.js', f'output/{slug}/assets/tailwind.js'], check=False)
    g = subprocess.run([sys.executable, 'scripts/gate.py', slug, '--lang', 'en', '--forbid', FORBID], capture_output=True, text=True)
    if g.returncode != 0:
        return fail(f'GATE: {g.stdout[-220:]}')
    report('verify')
    fotos_usadas = sorted(set(re.findall(r'gmaps-\d+\.jpg', open(f'output/{slug}/content.json').read())))
    ok = subir_github(f'output/{slug}/index.html', f'output/{slug}/index.html')
    for f in ['content.json', 'data.json', '.assetsignore', 'assets/tailwind.js']:
        ok &= subir_github(f'output/{slug}/{f}', f'output/{slug}/{f}')
    for f in fotos_usadas:
        ok &= subir_github(f'output/{slug}/assets/raw/{f}', f'output/{slug}/assets/raw/{f}')
    if not ok:
        return fail('Subida a GitHub incompleta')
    url = f'{DEMOS}/{slug}/'
    for _ in range(72):
        time.sleep(10)
        try:
            if urllib.request.urlopen(url, timeout=15).status == 200:
                break
        except Exception:
            pass
    else:
        return fail('El demo no respondio 200 tras el deploy')
    report('commit')
    dm = (f'Hello! I prepared a website concept for {nombre} using the public Google Maps listing. '
          f'See it here: {url} It is free to review and does not change your current operations.')
    panel('/api/public/registry-upsert', {
        'slug': slug, 'name': hechos.get('name') or nombre, 'city': ciudad,
        'ig': 'Google Maps', 'url_demo': url, 'has_own_site': bool(hechos.get('has_own_site')),
        'email': None, 'phone': hechos.get('phone'), 'language': 'en', 'dm_message': dm[:500],
        'thumb': f'{url}assets/raw/{fotos_usadas[0]}',
    })
    result = {'slug': slug, 'name': hechos.get('name') or nombre, 'url_demo': url, 'dm': dm}
    if cerrar:
        terminar(iid, **result)
    print(f'  LISTO {url}', flush=True)
    return result


def procesar_descubrimiento(item):
    """Resuelve una búsqueda manual de nicho + ciudad sin esperar al Cron.

    El panel guarda estas búsquedas como un único item de cola. Se reclama de forma
    atómica y aquí mismo se descubren y construyen hasta tres candidatos. Cada candidato
    reutiliza el pipeline de Google Maps (fotos, gate, GitHub y demo), mientras el item
    original solo se cierra cuando todos los resultados posibles ya fueron procesados.
    """
    iid = item['id']
    request = item.get('request') or {}
    niche = str(request.get('niche') or '').strip()
    location = str(request.get('location') or '').strip()
    count = max(1, min(int(request.get('count') or 1), 3))
    if not niche or not location:
        terminar(iid, failed=True, motivo='Búsqueda manual sin nicho o ciudad.')
        return

    progreso(iid, 'research', f'Google Maps: {niche} en {location}')
    print(f'== {item.get("input", "descubrimiento")} (búsqueda manual prioritaria)', flush=True)
    try:
        discovery = subprocess.run(
            [sys.executable, 'scripts/maps_discover.py', '--niche', niche, '--location', location,
             '--limit', str(max(count * 4, 8))],
            capture_output=True, text=True, timeout=240,
        )
    except Exception as exc:
        terminar(iid, failed=True, motivo=f'Descubrimiento Google Maps falló: {str(exc)[:180]}')
        return

    raw = (discovery.stdout or '').strip()
    try:
        payload = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        payload = {}
    candidates = payload.get('results') if isinstance(payload, dict) else None
    if not isinstance(candidates, list):
        candidates = []
    # Defensa en profundidad: aunque el descubridor ya filtre perfiles, no se procesa
    # un candidato si otra versión del script devuelve un website propio.
    candidates = [c for c in candidates if isinstance(c, dict) and c.get('name')
                  and not c.get('website') and not c.get('has_own_site')]
    if not candidates:
        detail = payload.get('error') if isinstance(payload, dict) else ''
        terminar(iid, failed=True, motivo=f'No se encontraron negocios sin website propio en {location}. {detail}'.strip()[:300])
        return

    sites = []
    seen = set()
    for candidate in candidates:
        if len(sites) >= count:
            break
        name = str(candidate.get('name') or '').strip()
        key = re.sub(r'[^a-z0-9]', '', name.lower())
        if not name or key in seen:
            continue
        seen.add(key)
        child = {
            'id': f'{iid}:{candidate.get("slug") or key[:48]}',
            'input': f'{name} ({candidate.get("location") or location})',
        }
        progreso(iid, 'build', f'Construyendo {len(sites) + 1}/{count}: {name}')
        try:
            result = procesar_nombre(child, cerrar=False, progress_id=iid)
        except Exception as exc:
            print(f'  candidato {name} fallo: {exc}', flush=True)
            result = {'failed': True, 'motivo': str(exc)[:180]}
        if result and not result.get('failed'):
            sites.append({k: result[k] for k in ('slug', 'name', 'url_demo') if k in result})

    if sites:
        terminar(iid, sites=sites, slug=sites[0].get('slug'), name=sites[0].get('name'), url_demo=sites[0].get('url_demo'))
        print(f'  DESCUBRIMIENTO LISTO: {len(sites)} demo(s)', flush=True)
    else:
        terminar(iid, failed=True, motivo='Los candidatos encontrados no superaron research, fotos o validación.')


def main():
    print(f'forja-railway arrancada (poll {POLL_S}s, sin IA: plantillas por nicho)', flush=True)
    while True:
        q = panel('/api/public/queue') or {}
        pendientes = q.get('pending', [])
        # Las búsquedas manuales tienen prioridad sobre los nombres que mete el Cron:
        # una persona no debe esperar a que se vacíe la cola automática para ver su demo.
        discoveries = [p for p in pendientes if (p.get('request') or {}).get('type') == 'discovery']
        mios = [p for p in pendientes if not p.get('request') and parece_handle(p.get('input', ''))]
        nombres = [p for p in pendientes if not p.get('request') and not parece_handle(p.get('input', ''))]
        if discoveries:
            try:
                item = tomar_siguiente(discoveries)
                if item:
                    procesar_descubrimiento(item)
            except Exception as e:
                print(f'  error procesando búsqueda manual: {e}', flush=True)
                try:
                    terminar(discoveries[0]['id'], failed=True, motivo=f'Excepcion en búsqueda manual: {str(e)[:160]}')
                except Exception:
                    pass
        elif mios:
            try:
                item = tomar_siguiente(mios)
                if item:
                    procesar(item)
            except Exception as e:
                print(f'  error procesando: {e}', flush=True)
                try:
                    terminar(mios[0]['id'], failed=True, motivo=f'Excepcion en forja-railway: {str(e)[:160]}')
                except Exception:
                    pass
        elif nombres:
            try:
                item = tomar_siguiente(nombres)
                if item:
                    procesar_nombre(item)
            except Exception as e:
                print(f'  error procesando nombre: {e}', flush=True)
                try:
                    terminar(nombres[0]['id'], failed=True, motivo=f'Excepcion en research Google Maps: {str(e)[:160]}')
                except Exception:
                    pass
        time.sleep(POLL_S)


if __name__ == '__main__':
    main()
