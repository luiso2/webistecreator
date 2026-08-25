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
nunca dos items a la vez; el research degradado cierra rápido con un motivo transitorio
para reintento, nunca deja un item fantasma en processing.
"""
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

import contenido_script as cs
from scripts.maps_common import instagram_handle

PANEL = os.environ.get('PANEL_URL', 'https://siteforge-panel.odd-forest-9504.workers.dev')
DEMOS = 'https://siteforge-demos.odd-forest-9504.workers.dev'
GH_REPO = os.environ.get('GH_REPO', 'luiso2/webistecreator')
GH_TOKEN = os.environ['GITHUB_TOKEN']
# SIN IA (decision del usuario 2026-08-18): curacion por reglas y plantillas por nicho,
# todo en contenido_script.py. Cero costo por site, cero dependencia de APIs de modelos.
# Los items por NOMBRE se resuelven con la ficha pública de Google Maps; antes se dejaban
# sin reclamar y por eso se acumulaban indefinidamente cuando la rutina cloud estaba llena.
POLL_S = int(os.environ.get('POLL_SECONDS', '10'))
try:
    DISCOVERY_BUILD_WORKERS = max(1, min(int(os.environ.get('DISCOVERY_BUILD_WORKERS', '3')), 3))
except (TypeError, ValueError):
    DISCOVERY_BUILD_WORKERS = 3
# Una forja nunca puede dejar una fila viva indefinidamente. Se reserva margen para
# cerrar el item en el panel antes de los diez minutos que ve el usuario.
try:
    FORGE_DEADLINE_SECONDS = max(300, min(int(os.environ.get('FORGE_DEADLINE_SECONDS', '510')), 540))
except (TypeError, ValueError):
    FORGE_DEADLINE_SECONDS = 510
FORBID = 'Pure Artistry,pure.artistrysk,Booksy,booksy,121705,silk press,locs,K-Tip,W Grant,Chianita,Hair Studio'

# "negocio local" llega con frecuencia cuando el usuario pide solo una ciudad.
# Google Maps no trata esa frase como un nicho de búsqueda útil; usarla literalmente
# devuelve cero fichas o resultados no relacionados. Rotamos nichos concretos, sin
# relajar nunca la comprobación de website propio, rating, reseñas ni fotos.
GENERIC_DISCOVERY_NICHES = {
    'negocio', 'negocios', 'negocio local', 'negocios locales', 'empresa', 'empresas',
    'business', 'businesses', 'local business', 'local businesses', 'small business',
}
DISCOVERY_FALLBACK_NICHES = (
    'handyman', 'plumber', 'electrician', 'landscaper', 'auto repair',
    'cleaning service', 'barbershop', 'catering',
)

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


class ForgeDeadlineExceeded(RuntimeError):
    """La fila agotó su presupuesto; se cierra como fallo concreto, nunca queda processing."""


def timeout_for(deadline, cap):
    """Devuelve un timeout acotado al presupuesto restante de una fila."""
    if deadline is None:
        return cap
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise ForgeDeadlineExceeded(f'La forja superó el límite de {FORGE_DEADLINE_SECONDS} segundos.')
    return max(1, min(cap, int(remaining)))


def sleep_for(seconds, deadline=None):
    if deadline is None:
        time.sleep(seconds)
        return
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise ForgeDeadlineExceeded(f'La forja superó el límite de {FORGE_DEADLINE_SECONDS} segundos.')
    time.sleep(min(seconds, remaining))


def deploy_marker(slug):
    """Incluye un cambio bajo demos/ para activar Workers Builds aunque haya path filters."""
    path = f'/tmp/siteforge-deploy-{slug}.txt'
    with open(path, 'w', encoding='utf-8') as marker:
        marker.write(f'{slug}\n{int(time.time())}\n')
    return path, 'demos/.forge-deploy'


def discovery_niches(niche: str) -> list[str]:
    normalized = re.sub(r'\s+', ' ', niche.strip().lower())
    if normalized in GENERIC_DISCOVERY_NICHES:
        return list(DISCOVERY_FALLBACK_NICHES)
    return [niche]


def panel(ruta, data=None, timeout=20):
    try:
        return http(f'{PANEL}{ruta}', data, timeout=timeout)
    except Exception as e:
        print(f'  panel {ruta}: {e}', flush=True)
        return None


def progreso(item_id, stage, note=None, token=None):
    # Enviar cadena vacía cuando una etapa no trae nota limpia el mensaje de la etapa
    # anterior (por ejemplo, no dejar "Workers Builds sigue desplegando" tras terminar).
    payload = {'id': item_id, 'stage': stage, 'note': note or ''}
    if token:
        payload['token'] = token
    panel('/api/public/queue/progress', payload)


def esperar_demo(item_id, url, max_seconds=420, token=None, deadline=None, expected_marker=None):
    """Espera el deploy, comprobando contenido y respetando el deadline de la fila."""
    inicio = time.monotonic()
    ultimo_heartbeat = inicio
    ultimo_status = 'sin respuesta'
    if deadline is not None:
        max_seconds = min(max_seconds, max(0, deadline - time.monotonic()))
    while time.monotonic() - inicio < max_seconds:
        try:
            # Usa una consulta no cacheada y un UA de navegador: Cloudflare puede
            # servir una respuesta cacheada distinta a Railway si se consulta el
            # mismo slug sin headers, justo durante la propagacion de Builds.
            sep = '&' if '?' in url else '?'
            check = urllib.request.Request(
                f'{url}{sep}forge_check={int(time.time())}',
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; siteforge-forja/1.0; +railway)',
                    'Cache-Control': 'no-cache',
                },
            )
            with urllib.request.urlopen(check, timeout=timeout_for(deadline, 15)) as response:
                ultimo_status = str(response.status)
                # Un 200 del mismo slug puede ser una versión vieja cacheada. Cuando
                # conocemos el nombre esperado, exigimos verlo en el HTML antes de
                # registrar el demo como terminado.
                body = response.read(512 * 1024).decode('utf-8', errors='ignore') if expected_marker else ''
            markers = [expected_marker] if expected_marker else []
            if expected_marker and '&' in expected_marker:
                markers.append(expected_marker.replace('&', '&amp;'))
            if ultimo_status == '200' and (not markers or any(marker in body for marker in markers)):
                return True
        except urllib.error.HTTPError as exc:
            ultimo_status = f'HTTP {exc.code}'
        except Exception:
            ultimo_status = 'error de red'
        ahora = time.monotonic()
        if ahora - ultimo_heartbeat >= 60:
            progreso(item_id, 'commit', f'Workers Builds sigue desplegando (último check: {ultimo_status})', token=token)
            ultimo_heartbeat = ahora
        sleep_for(10, deadline)
    return False


def terminar(item_id, token=None, **result):
    payload = {'id': item_id, **result}
    if token:
        payload['token'] = token
    panel('/api/public/queue/done', payload)


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


def reservar_candidatos(item_id, token, candidates):
    """Reserva identidades bajo el claim activo; si el panel falla, no construye a ciegas."""
    result = panel('/api/public/queue/candidates/reserve', {
        'id': item_id,
        'token': token,
        'candidates': candidates,
    }, timeout=25)
    if not isinstance(result, dict) or not result.get('ok'):
        return [], [], 'No se pudo reservar la identidad del negocio; se evita un build duplicado.'
    return result.get('reserved') or [], result.get('skipped') or [], None


def liberar_candidato(item_id, token, candidate):
    if item_id and token and candidate:
        panel('/api/public/queue/candidates/release', {
            'id': item_id, 'token': token, 'candidate': candidate,
        })


def completar_candidato(item_id, token, candidate, site):
    if not item_id or not token or not candidate:
        return {'ok': False, 'error': 'reserva incompleta'}
    return panel('/api/public/queue/candidates/complete', {
        'id': item_id, 'token': token, 'candidate': candidate, 'site': site,
    }) or {'ok': False, 'error': 'el panel no confirmó la identidad publicada'}


def resultado_existente(skipped):
    """Extrae un demo ya publicado de una respuesta de deduplicación."""
    for entry in skipped or []:
        existing = entry.get('existing') if isinstance(entry, dict) else None
        if isinstance(existing, dict) and existing.get('slug') and existing.get('url_demo'):
            return {
                'slug': existing['slug'],
                'name': existing.get('name') or existing['slug'],
                'url_demo': existing['url_demo'],
                'reused': True,
            }
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


def subir_sitio_github(slug, archivos, intento=0, deadline=None):
    """Publica un sitio completo en un solo commit de GitHub.

    La API Contents crea un commit por archivo. Con las cuatro replicas de Railway
    eso producia una carrera de SHA (409) y Builds podia arrancar con un sitio
    incompleto. Git Data API permite crear blobs, un arbol y un commit atomico; si
    otra forja avanzo ``main`` durante la operacion se vuelve a leer el head y se
    reintenta el commit completo.
    """
    hdr = {
        'Authorization': f'Bearer {GH_TOKEN}',
        'Accept': 'application/vnd.github+json',
    }
    base = f'https://api.github.com/repos/{GH_REPO}'
    try:
        ref = http(f'{base}/git/ref/heads/main', headers=hdr, timeout=timeout_for(deadline, 30))
        head_sha = ref['object']['sha']
        head_commit = http(f'{base}/git/commits/{head_sha}', headers=hdr, timeout=timeout_for(deadline, 30))
        def crear_blob(par):
            local, repo_path = par
            timeout_for(deadline, 30)
            with open(local, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode()
            blob = http(f'{base}/git/blobs', {
                'content': encoded,
                'encoding': 'base64',
            }, headers=hdr, timeout=timeout_for(deadline, 30))
            return {
                'path': repo_path,
                'mode': '100644',
                'type': 'blob',
                'sha': blob['sha'],
            }

        # Los blobs no dependen entre sí. GitHub sigue recibiendo un solo árbol y
        # un solo commit, pero las fotos dejan de sumar una latencia de red cada una.
        with ThreadPoolExecutor(max_workers=min(4, max(1, len(archivos)))) as pool:
            entries = list(pool.map(crear_blob, archivos))
        tree = http(f'{base}/git/trees', {
            'base_tree': head_commit['tree']['sha'],
            'tree': entries,
        }, headers=hdr, timeout=timeout_for(deadline, 30))
        commit = http(f'{base}/git/commits', {
            'message': f'forja-railway: publish {slug}',
            'tree': tree['sha'],
            'parents': [head_sha],
        }, headers=hdr, timeout=timeout_for(deadline, 30))
        # force=false conserva cambios de otras forjas; un 409 significa que
        # simplemente debemos repetir con el nuevo head.
        http(f'{base}/git/refs/heads/main', {
            'sha': commit['sha'],
            'force': False,
        }, headers=hdr, method='PATCH', timeout=timeout_for(deadline, 30))
        return True
    except ForgeDeadlineExceeded:
        raise
    except urllib.error.HTTPError as exc:
        # GitHub responde 409 o 422 segun el endpoint cuando otra replica
        # avanzo main entre la lectura del head y el PATCH de la referencia.
        if exc.code in (409, 422) and intento < 5:
            sleep_for(2 + intento * 2, deadline)
            return subir_sitio_github(slug, archivos, intento + 1, deadline)
        print(f'  publicacion atomica fallo ({exc.code}) {slug}: {exc}', flush=True)
        return False
    except Exception as exc:
        if intento < 2:
            sleep_for(2 + intento * 2, deadline)
            return subir_sitio_github(slug, archivos, intento + 1, deadline)
        print(f'  publicacion atomica fallo {slug}: {exc}', flush=True)
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


def procesar(item, deadline=None):
    iid, entrada = item['id'], item['input'].strip()
    token = item.get('claim_token')
    report = lambda stage, note=None: progreso(iid, stage, note, token=token)
    reserved_candidate = None

    def finish(**result):
        nonlocal reserved_candidate
        if result.get('failed'):
            liberar_candidato(iid, token, reserved_candidate)
        elif reserved_candidate:
            completed = completar_candidato(iid, token, reserved_candidate, result)
            if not completed.get('ok'):
                conflict = completed.get('existing')
                if isinstance(conflict, dict) and conflict.get('slug') and conflict.get('url_demo'):
                    result = {
                        'slug': conflict['slug'],
                        'name': conflict.get('name') or conflict['slug'],
                        'url_demo': conflict['url_demo'],
                        'reused': True,
                    }
                else:
                    result = {'failed': True, 'motivo': f'No se confirmó la identidad publicada: {completed.get("error", "error desconocido")}'[:300]}
        terminar(iid, token=token, **result)

    print(f'== {entrada}', flush=True)
    report('research', 'forja-railway')

    handle = entrada.lstrip('@')
    slug = re.sub(r'[^a-z0-9-]', '', handle.lower().replace('.', '-').replace('_', '-'))[:40]
    reserved, skipped, reserve_error = reservar_candidatos(iid, token, [{
        'name': handle, 'slug': slug, 'location': 'Instagram', 'niche': 'Instagram',
    }])
    existing = resultado_existente(skipped)
    if existing:
        terminar(iid, token=token, **existing)
        print(f'  REUTILIZADO {existing["url_demo"]}', flush=True)
        return
    if reserve_error or not reserved:
        finish(failed=True, motivo=reserve_error or 'No se construyó para evitar un negocio duplicado.')
        return
    reserved_candidate = reserved[0]

    r = subprocess.run([sys.executable, 'scripts/research_ig.py', handle, slug],
                       capture_output=True, text=True, timeout=timeout_for(deadline, 300))
    ruta_data = f'output/{slug}/data.json'
    if not os.path.exists(ruta_data):
        finish(failed=True, motivo=f'Research sin datos: {(r.stdout or r.stderr)[-180:]}')
        return
    hechos = json.load(open(ruta_data, encoding='utf-8'))
    if hechos.get('research_degradado') or len(hechos.get('fotos', [])) < 5:
        # No dejar el item processing mientras el research degradado espera al
        # rescatador. Se cierra rápido con motivo transitorio y el panel permite
        # reintentar hasta cinco veces para que otra ejecución pueda completar las fotos.
        fotos = len(hechos.get('fotos', []))
        finish(failed=True, motivo=f'Research Instagram incompleto ({fotos} fotos); reintenta para volver a consultar el perfil.')
        return
    hechos['slug'] = slug
    hechos['idioma_principal'] = 'es'  # el gate valida la coherencia del copy generado

    report('build')
    # Sin IA (decision del usuario 2026-08-18): curacion por reglas + plantillas por nicho
    fotos_sel, motivo = cs.curar(hechos)
    if not fotos_sel:
        finish(failed=True, motivo=f'Curacion por reglas: {motivo[:220]}')
        return
    content, dm, nicho = cs.construir(hechos, fotos_sel)
    print(f'  nicho={nicho}', flush=True)
    plan = {'fotos': fotos_sel, 'dm': dm}
    fallos = guard_anti_invencion(content, hechos, slug)
    if fallos:
        finish(failed=True, motivo=f'Guard anti-invencion: {"; ".join(fallos[:4])}')
        return
    json.dump(content, open(f'output/{slug}/content.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    subprocess.run(['cp', 'templates/.assetsignore-template', f'output/{slug}/.assetsignore'])

    if subprocess.run([sys.executable, 'scripts/derive.py', slug], capture_output=True,
                      timeout=timeout_for(deadline, 60)).returncode != 0:
        finish(failed=True, motivo='derive.py fallo (ancla rota)')
        return
    report('verify')
    lang = content.get('lang', 'es')
    g = subprocess.run([sys.executable, 'scripts/gate.py', slug, '--lang', lang, '--forbid', FORBID],
                       capture_output=True, text=True, timeout=timeout_for(deadline, 60))
    if g.returncode != 0:
        finish(failed=True, motivo=f'GATE: {g.stdout[-200:]}')
        return

    report('commit')
    fotos_usadas = sorted(set(re.findall(r'(?:bk-\d+|logo)\.jpg', open(f'output/{slug}/content.json').read())))
    archivos = [(f'output/{slug}/index.html', f'output/{slug}/index.html')]
    archivos += [(f'output/{slug}/{f}', f'output/{slug}/{f}')
                 for f in ['content.json', 'data.json', '.assetsignore']]
    archivos += [(f'output/{slug}/assets/raw/{f}', f'output/{slug}/assets/raw/{f}')
                 for f in fotos_usadas]
    archivos.append(deploy_marker(slug))
    ok = subir_sitio_github(slug, archivos, deadline=deadline)
    if not ok:
        finish(failed=True, motivo='Subida a GitHub incompleta')
        return

    url = f'{DEMOS}/{slug}/'
    if not esperar_demo(iid, url, token=token, deadline=deadline,
                        expected_marker=content.get('brand', {}).get('name')):
        finish(failed=True, motivo='El demo no respondio 200 tras el deploy (no se registra)')
        return

    registry_result = panel('/api/public/registry-upsert', {
        'slug': slug, 'name': content.get('brand', {}).get('name', slug),
        'city': (hechos.get('ciudad') or ''), 'ig': f'@{handle}', 'url_demo': url,
        'phone': hechos.get('phone'), 'language': lang, 'has_own_site': bool(hechos.get('has_own_site')),
        'business_key': reserved_candidate.get('business_key'),
        'source': 'instagram',
        'thumb': f'{url}assets/raw/{plan["fotos"]["hero"]}', 'dm_message': plan.get('dm', '')[:900], 'message_version': 2,
    })
    if not isinstance(registry_result, dict) or not registry_result.get('ok'):
        finish(failed=True, motivo='El demo publicó, pero el registro del panel no confirmó el negocio.')
        return
    duplicate = registry_result.get('existing') if registry_result.get('duplicate') else None
    if isinstance(duplicate, dict) and duplicate.get('slug') and duplicate.get('url_demo'):
        finish(slug=duplicate['slug'], name=duplicate.get('name') or duplicate['slug'], url_demo=duplicate['url_demo'])
    else:
        finish(slug=slug, name=content.get('brand', {}).get('name', slug), url_demo=url,
               business_key=reserved_candidate.get('business_key'))
    print(f'  LISTO {url}', flush=True)


CONTENT_PATCH_ROOTS = {
    'slug', 'base', 'lang', 'cta_url', 'cta_icono', 'cta_label', 'ig_url', 'ig_handle',
    'paleta', 'brand', 'head', 'jsonld', 'nav', 'hero', 'strip', 'marquee', 'nosotros',
    'proceso', 'servicios', 'galeria', 'social_proof', 'contacto', 'footer', 'seo',
}


def _clean_update_value(value, depth=0, state=None):
    """Limpia y limita un patch del Control Plane antes de tocar content.json."""
    state = state or {'keys': 0}
    if depth > 6:
        raise ValueError('patch demasiado profundo')
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return re.sub(r'[<>\x00-\x1f\x7f]', '', value)[:2000]
    if isinstance(value, list):
        if len(value) > 40:
            raise ValueError('una lista del patch no puede superar 40 elementos')
        return [_clean_update_value(item, depth + 1, state) for item in value]
    if not isinstance(value, dict):
        raise ValueError('valor de patch inválido')
    result = {}
    for key, item in value.items():
        state['keys'] += 1
        if state['keys'] > 120:
            raise ValueError('patch demasiado grande')
        key = str(key)
        if (not key or '__' in key or key in {'constructor', 'prototype'}
                or len(key) > 80 or re.search(r'[<>\x00-\x1f\x7f]', key)):
            raise ValueError(f'clave de patch no permitida: {key[:80]}')
        result[key] = _clean_update_value(item, depth + 1, state)
    return result


def _merge_update(base, patch):
    """Deep merge determinista: objetos se fusionan, listas/valores se reemplazan."""
    if not isinstance(base, dict) or not isinstance(patch, dict):
        return patch
    result = dict(base)
    for key, value in patch.items():
        result[key] = _merge_update(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else value
    return result


def procesar_actualizacion(item, deadline=None):
    """Aplica una revisión de SiteSpec al content.json existente y la publica.

    El GPT nunca escribe HTML ni ejecuta comandos: solo entrega un patch JSON
    validado por el Control Plane. El mismo derive.py/gate.py que usa la forja
    inicial conserva la calidad y la compatibilidad de los sitios existentes.
    """
    iid = item['id']
    token = item.get('claim_token')
    request = item.get('request') or {}
    slug = str(request.get('slug') or '').strip().lower()
    if not re.fullmatch(r'[a-z0-9-]{1,40}', slug):
        terminar(iid, token=token, failed=True, motivo='site_update con slug inválido.')
        return

    def report(stage, note=None):
        progreso(iid, stage, note, token=token)

    def fail(motivo):
        terminar(iid, token=token, failed=True, motivo=motivo[:300])

    content_path = f'output/{slug}/content.json'
    if not os.path.exists(content_path):
        fail(f'No existe content.json para {slug}; no se modifica el website.')
        return
    try:
        content = json.load(open(content_path, encoding='utf-8'))
        patch = request.get('content_patch') or {}
        if not isinstance(patch, dict):
            raise ValueError('content_patch debe ser un objeto')
        unknown = set(patch) - CONTENT_PATCH_ROOTS
        if unknown:
            raise ValueError(f'raíces no permitidas: {", ".join(sorted(unknown))}')
        patch = _clean_update_value(patch)
        if len(json.dumps(patch, ensure_ascii=False)) > 16000:
            raise ValueError('content_patch supera 16 KB')
        updated = _merge_update(content, patch)
        json.dump(updated, open(content_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    except Exception as exc:
        fail(f'Patch de contenido rechazado: {exc}')
        return

    report('build', f'Revisión {request.get("spec_revision", "?")} · derive determinista')
    derived = subprocess.run([sys.executable, 'scripts/derive.py', slug], capture_output=True, text=True,
                             timeout=timeout_for(deadline, 60))
    if derived.returncode != 0:
        fail(f'derive.py fallo en actualización: {(derived.stdout or derived.stderr)[-220:]}')
        return

    lang = updated.get('lang', 'en')
    gate = subprocess.run([sys.executable, 'scripts/gate.py', slug, '--lang', lang, '--forbid', FORBID],
                          capture_output=True, text=True, timeout=timeout_for(deadline, 60))
    if gate.returncode != 0:
        fail(f'GATE en actualización: {gate.stdout[-220:]}')
        return
    report('verify', 'SiteSpec y contenido verificados')

    photos = sorted(set(re.findall(r'(?:gmaps-\d+|bk-\d+|logo)\.jpg', json.dumps(updated))))
    files = [(f'output/{slug}/index.html', f'output/{slug}/index.html'),
             (content_path, content_path)]
    if os.path.exists(f'output/{slug}/.assetsignore'):
        files.append((f'output/{slug}/.assetsignore', f'output/{slug}/.assetsignore'))
    files.extend((f'output/{slug}/assets/raw/{photo}', f'output/{slug}/assets/raw/{photo}')
                 for photo in photos if os.path.exists(f'output/{slug}/assets/raw/{photo}'))
    files.append(deploy_marker(slug))
    report('commit', 'Publicando revisión atómica')
    if not subir_sitio_github(slug, files, deadline=deadline):
        fail('Subida a GitHub incompleta en actualización.')
        return

    url = f'{DEMOS}/{slug}/'
    expected = updated.get('brand', {}).get('name') or slug
    if not esperar_demo(iid, url, token=token, deadline=deadline, expected_marker=expected):
        fail('El demo no respondió 200 tras publicar la actualización.')
        return
    terminar(iid, token=token, slug=slug, name=expected, url_demo=url,
             revision=request.get('spec_revision'), updated=True)
    print(f'  ACTUALIZADO {url} (revision {request.get("spec_revision", "?")})', flush=True)


def procesar_nombre(item, cerrar=True, progress_id=None, deadline=None):
    """Construye entradas directas (nombre + ciudad) desde Google Maps.

    Google Maps entrega nombre, rating, contacto, website declarado y fotos públicas sin
    adivinar un handle de Instagram. Menos de cinco fotos propias se cierra con motivo
    concreto en vez de dejar el item pendiente para siempre.
    """
    iid, entrada = item['id'], item['input'].strip()
    token = item.get('claim_token')
    report_id = progress_id or iid
    candidate = None

    def report(stage, note=None):
        progreso(report_id, stage, note, token=token)

    def fail(motivo):
        if item.get('business_reserved') and candidate:
            liberar_candidato(report_id, token, candidate)
            item['business_reserved'] = False
        if cerrar:
            terminar(iid, token=token, failed=True, motivo=motivo)
        return {'failed': True, 'motivo': motivo}

    print(f'== {entrada} (Google Maps)', flush=True)
    report('research', 'ficha publica de Google Maps')
    m = re.match(r'^(.*?)\s*\(([^)]+)\)\s*$', entrada)
    nombre = (m.group(1) if m else entrada).strip()
    ciudad = (m.group(2) if m else 'Florida').strip()
    # El panel acepta slugs de hasta 40 caracteres; respetar el mismo límite aquí
    # evita terminar todo el build y dejar el item atascado al llamar a /done.
    slug = re.sub(r'[^a-z0-9-]', '', nombre.lower().replace('&', ' and ').replace('.', '-').replace('_', '-').replace(' ', '-'))[:40].strip('-')
    source_candidate = item.get('candidate') if isinstance(item.get('candidate'), dict) else {}
    candidate = {
        **source_candidate,
        'name': nombre,
        'slug': slug,
        'location': source_candidate.get('location') or ciudad,
        'city': ciudad,
        'niche': item.get('nicho') or source_candidate.get('niche'),
    }
    candidate['location'] = candidate.get('location') or ciudad
    if not item.get('business_reserved'):
        reserved, skipped, reserve_error = reservar_candidatos(report_id, token, [candidate])
        existing = resultado_existente(skipped)
        if existing:
            if cerrar:
                terminar(iid, token=token, **existing)
            print(f'  REUTILIZADO {existing["url_demo"]}', flush=True)
            return existing
        if reserve_error or not reserved:
            reason = reserve_error or ((skipped[0].get('reason') if skipped else None) or 'identidad no disponible')
            return fail(f'No se construyó para evitar duplicados: {reason}')
        candidate = reserved[0]
        item['candidate'] = candidate
        item['business_reserved'] = True
    ruta_data = f'output/{slug}/data.json'
    # Nunca reutilizar datos/fotos de una corrida anterior con el mismo slug.
    try:
        os.unlink(ruta_data)
    except FileNotFoundError:
        pass
    raw_dir = f'output/{slug}/assets/raw'
    for old_photo in os.listdir(raw_dir) if os.path.isdir(raw_dir) else []:
        if old_photo.startswith('gmaps-') and old_photo.endswith('.jpg'):
            try:
                os.unlink(os.path.join(raw_dir, old_photo))
            except OSError:
                pass
    r = None
    best_research = None
    for attempt in range(2):
        research_cmd = [sys.executable, 'scripts/maps_research.py', f'{nombre}, {ciudad}', slug]
        if candidate.get('maps_url'):
            research_cmd += ['--maps-url', candidate['maps_url']]
        r = subprocess.run(research_cmd,
                           capture_output=True, text=True, timeout=timeout_for(deadline, 150))
        if os.path.exists(ruta_data):
            try:
                current_research = json.load(open(ruta_data, encoding='utf-8'))
            except (OSError, json.JSONDecodeError):
                current_research = None
            if current_research and (
                best_research is None
                or len(current_research.get('fotos') or []) > len(best_research.get('fotos') or [])
            ):
                best_research = current_research
            if current_research and len(current_research.get('fotos') or []) >= 5:
                break
        if attempt == 0:
            report('research', 'Google Maps: reintentando galeria incompleta')
            sleep_for(4, deadline)
    if best_research is None:
        return fail(f'Research Google Maps sin datos: {(r.stdout or r.stderr)[-180:]}')
    hechos = best_research
    json.dump(hechos, open(ruta_data, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if hechos.get('status') == 'PERMANENTLY_CLOSED':
        return fail('La ficha de Google Maps figura como permanentemente cerrada.')
    if hechos.get('has_own_site'):
        return fail('La ficha ya tiene un website propio; se respeta el filtro sin website.')
    # Maps no devuelve el contexto de la consulta dentro de data.json. Persistirlo antes
    # del builder evita que todos los negocios manuales aparezcan como Hialeah, Florida.
    hechos['nombre'] = hechos.get('name') or nombre
    hechos['ciudad'] = ciudad
    hechos['nicho'] = item.get('nicho') or candidate.get('niche') or hechos.get('nicho') or nombre
    hechos['idioma_principal'] = 'en'
    hechos['maps_url'] = hechos.get('maps_url') or candidate.get('maps_url')
    hechos['business_key'] = candidate.get('business_key')
    json.dump(hechos, open(ruta_data, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    fotos = hechos.get('fotos') or []
    if len(fotos) < 5:
        return fail(f'Google Maps solo expone {len(fotos)} fotos propias; se necesitan al menos 5 para una galeria real.')
    report('build', f'{len(fotos)} fotos publicas verificadas')
    b = subprocess.run([sys.executable, 'scripts/build_maps_site.py', slug], capture_output=True,
                       text=True, timeout=timeout_for(deadline, 90))
    if b.returncode != 0:
        return fail(f'build_maps_site fallo: {(b.stdout or b.stderr)[-220:]}')
    d = subprocess.run([sys.executable, 'scripts/derive.py', slug], capture_output=True,
                       text=True, timeout=timeout_for(deadline, 60))
    if d.returncode != 0:
        return fail('derive.py fallo para item por nombre')
    subprocess.run(['cp', 'templates/assets/tailwind.js', f'output/{slug}/assets/tailwind.js'], check=False)
    g = subprocess.run([sys.executable, 'scripts/gate.py', slug, '--lang', 'en', '--forbid', FORBID],
                       capture_output=True, text=True, timeout=timeout_for(deadline, 60))
    if g.returncode != 0:
        return fail(f'GATE: {g.stdout[-220:]}')
    report('verify')
    fotos_usadas = sorted(set(re.findall(r'(?:gmaps-|bk-)\d+\.jpg', open(f'output/{slug}/content.json').read())))
    archivos = [(f'output/{slug}/index.html', f'output/{slug}/index.html')]
    archivos += [(f'output/{slug}/{f}', f'output/{slug}/{f}')
                 for f in ['content.json', 'data.json', '.assetsignore', 'assets/tailwind.js']]
    archivos += [(f'output/{slug}/assets/raw/{f}', f'output/{slug}/assets/raw/{f}')
                 for f in fotos_usadas]
    archivos.append(deploy_marker(slug))
    ok = subir_sitio_github(slug, archivos, deadline=deadline)
    if not ok:
        return fail('Subida a GitHub incompleta')
    url = f'{DEMOS}/{slug}/'
    if not esperar_demo(report_id, url, token=token, deadline=deadline,
                        expected_marker=hechos.get('name') or nombre):
        return fail('El demo no respondio 200 tras el deploy')
    report('commit')
    dm = cs.generar_dm({**hechos, 'nombre': hechos.get('name') or nombre, 'ciudad': ciudad,
                        'idioma_principal': 'en'}, url, item.get('nicho') or hechos.get('nicho'))
    verified_instagram = instagram_handle(
        hechos.get('instagram_handle') or hechos.get('profile_url') or hechos.get('website')
    )
    registry_result = panel('/api/public/registry-upsert', {
        'slug': slug, 'name': hechos.get('name') or nombre, 'city': ciudad,
        **({'ig': f'@{verified_instagram}'} if verified_instagram else {}),
        'source': 'google_maps', 'url_demo': url, 'has_own_site': bool(hechos.get('has_own_site')),
        'email': None, 'phone': hechos.get('phone'), 'language': 'en', 'dm_message': dm[:900], 'message_version': 2,
        'maps_url': hechos.get('maps_url'), 'business_key': candidate.get('business_key'),
        'thumb': f'{url}assets/raw/{fotos_usadas[0]}',
    })
    if not isinstance(registry_result, dict) or not registry_result.get('ok'):
        return fail('El demo publicó, pero el registro del panel no confirmó el negocio.')
    existing = registry_result.get('existing') if registry_result.get('duplicate') else None
    site = existing if isinstance(existing, dict) and existing.get('url_demo') else {
        'slug': slug,
        'name': hechos.get('name') or nombre,
        'city': ciudad,
        'phone': hechos.get('phone'),
        'url_demo': url,
        'maps_url': hechos.get('maps_url'),
        'business_key': candidate.get('business_key'),
    }
    completed_identity = completar_candidato(report_id, token, candidate, site)
    if not completed_identity.get('ok'):
        conflict = completed_identity.get('existing')
        if isinstance(conflict, dict) and conflict.get('slug') and conflict.get('url_demo'):
            site = conflict
        else:
            return fail(f'El demo publicó, pero no se confirmó su identidad: {completed_identity.get("error", "error desconocido")}')
    result = {'slug': site['slug'], 'name': site.get('name') or nombre, 'url_demo': site['url_demo'], 'dm': dm}
    if cerrar:
        terminar(iid, token=token, **result)
    print(f'  LISTO {url}', flush=True)
    return result


def procesar_descubrimiento(item, deadline=None):
    """Resuelve una búsqueda manual de nicho + ciudad sin esperar al Cron.

    El panel guarda estas búsquedas como un único item de cola. Se reclama de forma
    atómica y aquí mismo se descubren y construyen hasta cinco candidatos. Cada candidato
    reutiliza el pipeline de Google Maps (fotos, gate, GitHub y demo), mientras el item
    original solo se cierra cuando todos los resultados posibles ya fueron procesados.
    """
    iid = item['id']
    token = item.get('claim_token')
    request = item.get('request') or {}
    niche = str(request.get('niche') or '').strip()
    location = str(request.get('location') or '').strip()
    count = max(1, min(int(request.get('count') or 1), 5))
    if not niche or not location:
        terminar(iid, token=token, failed=True, motivo='Búsqueda manual sin nicho o ciudad.')
        return

    print(f'== {item.get("input", "descubrimiento")} (búsqueda manual prioritaria)', flush=True)
    candidates = []
    seen_candidates = set()
    discovery_errors = []
    # Para un nicho concreto solo se hace una consulta. Si el usuario dejó el
    # nicho vacío/genérico, probamos categorías locales concretas hasta reunir
    # suficientes candidatos; nunca convertimos un negocio con dominio propio.
    search_niches = discovery_niches(niche)
    generic_search = len(search_niches) > 1
    # Dos categorías genéricas se consultan juntas y, como máximo, se prueban cuatro.
    # Esto acota discovery a ~150 s incluso cuando Maps no devuelve nada útil, dejando
    # más de cinco minutos para construir, validar y desplegar.
    search_niches = search_niches[:4] if generic_search else search_niches
    needed_candidates = max(count * 6, 12) if generic_search else max(count * 2, count)

    def run_discovery(search_niche):
        try:
            discovery = subprocess.run(
                [sys.executable, 'scripts/maps_discover.py', '--niche', search_niche, '--location', location,
                 '--limit', str(max(count * 4, 8))],
                capture_output=True, text=True, timeout=timeout_for(deadline, 75),
            )
        except ForgeDeadlineExceeded as exc:
            return search_niche, [], str(exc)
        except Exception as exc:
            return search_niche, [], str(exc)[:120]

        raw = (discovery.stdout or '').strip()
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {}
        found = payload.get('results') if isinstance(payload, dict) else None
        if not isinstance(found, list):
            found = []
        error = payload.get('error') if isinstance(payload, dict) else None
        return search_niche, found, str(error or '')[:120]

    query_workers = 2 if generic_search else 1
    for offset in range(0, len(search_niches), query_workers):
        batch_niches = search_niches[offset:offset + query_workers]
        progreso(iid, 'research', f'Google Maps: {" + ".join(batch_niches)} en {location}', token=token)
        with ThreadPoolExecutor(max_workers=len(batch_niches)) as pool:
            discoveries = list(pool.map(run_discovery, batch_niches))
        for search_niche, found, discovery_error in discoveries:
            if discovery_error:
                discovery_errors.append(discovery_error)
        # Defensa en profundidad: aunque el descubridor ya filtre perfiles, no se procesa
        # un candidato si otra versión del script devuelve un website propio.
            for candidate in found:
                if not isinstance(candidate, dict) or not candidate.get('name'):
                    continue
                if candidate.get('website') or candidate.get('has_own_site'):
                    continue
                key = re.sub(r'[^a-z0-9]', '', str(candidate.get('name')).lower())
                if not key or key in seen_candidates:
                    continue
                seen_candidates.add(key)
                candidate = {**candidate, 'niche': candidate.get('niche') or search_niche}
                candidates.append(candidate)
        if len(candidates) >= needed_candidates:
            break

    if not candidates:
        detail = '; '.join(discovery_errors) if discovery_errors else 'Google Maps no devolvió candidatos'
        terminar(iid, token=token, failed=True, motivo=f'No se encontraron negocios sin website propio en {location}. {detail}'.strip()[:300])
        return

    reservation_input = [{**candidate, 'index': index} for index, candidate in enumerate(candidates[:20])]
    candidates, skipped_duplicates, reserve_error = reservar_candidatos(iid, token, reservation_input)
    if reserve_error:
        terminar(iid, token=token, failed=True, motivo=reserve_error)
        return
    if not candidates:
        reasons = sorted({str(entry.get('reason') or '') for entry in skipped_duplicates if isinstance(entry, dict)})
        detail = ', '.join(reason for reason in reasons if reason) or 'todos ya estaban registrados'
        terminar(iid, token=token, failed=True,
                 motivo=f'No hay negocios nuevos para construir: {detail}. No se crearon duplicados.'[:300])
        return

    selected = []
    seen = set()
    failed_candidates = []
    # Reservar candidatos de reemplazo evita que una ficha con pocas fotos convierta
    # una búsqueda de 1 negocio en un fallo total. El resultado padre sigue limitado
    # exactamente a ``count`` demos.
    target_candidates = min(len(candidates), count * 2)
    for candidate in candidates:
        if len(selected) >= target_candidates:
            break
        name = str(candidate.get('name') or '').strip()
        key = re.sub(r'[^a-z0-9]', '', name.lower())
        if not name or key in seen:
            continue
        seen.add(key)
        selected.append({
            'index': len(selected),
            'name': name,
            'child': {
                'id': f'{iid}:{candidate.get("slug") or key[:48]}',
                'input': f'{name} ({candidate.get("location") or location})',
                'nicho': candidate.get('niche') or niche,
                'claim_token': token,
                'candidate': candidate,
                'business_reserved': True,
            },
        })

    # Los candidatos de una búsqueda son independientes. Construir una tanda del
    # tamaño solicitado en paralelo evita esperas seriales; si alguno falla, la tanda
    # siguiente usa los reemplazos sin publicar más de ``count`` demos.
    if selected:
        progreso(iid, 'build', f'Iniciando hasta {count} forjas en paralelo (máximo {DISCOVERY_BUILD_WORKERS})', token=token)

    def build_candidate(entry):
        name = entry['name']
        result = {'failed': True, 'motivo': 'fallo desconocido'}
        # Maps/Workers pueden devolver una ficha incompleta en el primer intento
        # aunque el candidato sea válido. Repetir solo los candidatos fallidos evita
        # falsos errores sin ralentizar los builds que ya funcionan.
        for attempt in range(2):
            try:
                result = procesar_nombre(entry['child'], cerrar=False, progress_id=iid, deadline=deadline)
            except ForgeDeadlineExceeded as exc:
                result = {'failed': True, 'motivo': str(exc)}
                break
            except Exception as exc:
                print(f'  candidato {name} intento {attempt + 1} fallo: {exc}', flush=True)
                result = {'failed': True, 'motivo': str(exc)[:180]}
            if result and not result.get('failed'):
                break
            if attempt == 0:
                progreso(iid, 'research', f'Reintentando ficha: {name}', token=token)
        return entry['index'], result

    completed = []
    remaining_candidates = list(selected)
    while remaining_candidates and len(completed) < count:
        batch_size = min(count - len(completed), len(remaining_candidates))
        batch = remaining_candidates[:batch_size]
        remaining_candidates = remaining_candidates[batch_size:]
        with ThreadPoolExecutor(max_workers=min(DISCOVERY_BUILD_WORKERS, len(batch))) as pool:
            futures = [pool.submit(build_candidate, entry) for entry in batch]
            for future in as_completed(futures):
                index, result = future.result()
                if result and not result.get('failed'):
                    completed.append((index, {k: result[k] for k in ('slug', 'name', 'url_demo') if k in result}))
                elif result:
                    failed_candidates.append(f'{result.get("motivo") or "fallo sin detalle"}')

    sites = [result for _index, result in sorted(completed, key=lambda pair: pair[0])][:count]

    if sites:
        terminar(iid, token=token, sites=sites, slug=sites[0].get('slug'), name=sites[0].get('name'), url_demo=sites[0].get('url_demo'))
        print(f'  DESCUBRIMIENTO LISTO: {len(sites)} demo(s)', flush=True)
    else:
        detail = '; '.join(failed_candidates[:3])
        motivo = 'Los candidatos encontrados no superaron research, fotos o validación.'
        if detail:
            motivo += f' Detalle: {detail}'
        terminar(iid, token=token, failed=True, motivo=motivo[:300])


def main():
    print(f'forja-railway arrancada (poll {POLL_S}s, deadline {FORGE_DEADLINE_SECONDS}s, '
          f'workers {DISCOVERY_BUILD_WORKERS}, sin IA: plantillas por nicho)', flush=True)
    while True:
        q = panel('/api/public/queue') or {}
        pendientes = q.get('pending', [])
        # Las búsquedas manuales tienen prioridad sobre los nombres que mete el Cron:
        # una persona no debe esperar a que se vacíe la cola automática para ver su demo.
        updates = [p for p in pendientes if (p.get('request') or {}).get('type') == 'site_update']
        discoveries = [p for p in pendientes if (p.get('request') or {}).get('type') == 'discovery']
        mios = [p for p in pendientes if not p.get('request') and parece_handle(p.get('input', ''))]
        nombres = [p for p in pendientes if not p.get('request') and not parece_handle(p.get('input', ''))]
        # Una modificación solicitada desde el GPT tiene prioridad absoluta:
        # el propietario no debe esperar a que termine el descubrimiento diario.
        if updates:
            item = None
            deadline = None
            try:
                item = tomar_siguiente(updates)
                if item:
                    deadline = time.monotonic() + FORGE_DEADLINE_SECONDS
                    procesar_actualizacion(item, deadline=deadline)
            except Exception as e:
                print(f'  error procesando actualización: {e}', flush=True)
                try:
                    if item:
                        terminar(item['id'], token=item.get('claim_token'), failed=True,
                                 motivo=f'Excepcion en actualización: {str(e)[:160]}')
                except Exception:
                    pass
        elif discoveries:
            item = None
            deadline = None
            try:
                item = tomar_siguiente(discoveries)
                if item:
                    deadline = time.monotonic() + FORGE_DEADLINE_SECONDS
                    procesar_descubrimiento(item, deadline=deadline)
            except Exception as e:
                print(f'  error procesando búsqueda manual: {e}', flush=True)
                try:
                    if item:
                        terminar(item['id'], token=item.get('claim_token'), failed=True, motivo=f'Excepcion en búsqueda manual: {str(e)[:160]}')
                except Exception:
                    pass
        elif mios:
            item = None
            deadline = None
            try:
                item = tomar_siguiente(mios)
                if item:
                    deadline = time.monotonic() + FORGE_DEADLINE_SECONDS
                    procesar(item, deadline=deadline)
            except Exception as e:
                print(f'  error procesando: {e}', flush=True)
                try:
                    if item:
                        terminar(item['id'], token=item.get('claim_token'), failed=True, motivo=f'Excepcion en forja-railway: {str(e)[:160]}')
                except Exception:
                    pass
        elif nombres:
            item = None
            deadline = None
            try:
                item = tomar_siguiente(nombres)
                if item:
                    deadline = time.monotonic() + FORGE_DEADLINE_SECONDS
                    procesar_nombre(item, deadline=deadline)
            except Exception as e:
                print(f'  error procesando nombre: {e}', flush=True)
                try:
                    if item:
                        terminar(item['id'], token=item.get('claim_token'), failed=True, motivo=f'Excepcion en research Google Maps: {str(e)[:160]}')
                except Exception:
                    pass
        time.sleep(POLL_S)


if __name__ == '__main__':
    main()
