#!/usr/bin/env python3
"""Descarga las fotos REALES del perfil publico de Instagram de un negocio.

Uso: python3 scripts/ig_photos.py <ig_username> <slug> [start_index]

ARQUITECTURA (todo en la nube, 2026-07-20):
- Por defecto llama al microservicio en Railway `ig-photo-service` (corre Playwright headless
  desde una IP que SI llega a IG; la nube de Anthropic/forja NO llega a IG por firewall de
  egress, pero SI llega a Railway). El servicio devuelve las URLs de las fotos del perfil.
- Este script (cliente HTTP) descarga esas URLs + genera el contact sheet. Corre en cualquier
  lado (tu Mac, la forja cloud) porque solo necesita HTTP al servicio, no un navegador local.
- Override del endpoint con env IG_SERVICE_URL / IG_SERVICE_KEY.

IG rate-limitea BURSTS por IP: el servicio es una sola IP, asi que ESPACIAR las llamadas
(la forja construye ~1 negocio/7min, que se queda bajo el limite). NUNCA inventar nada:
solo baja lo que el perfil publica. Curar el _sheet.jpg (descartar covers de reels y graficos).
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

IG_SERVICE_URL = os.environ.get('IG_SERVICE_URL', 'https://ig-photo-service-production.up.railway.app')
IG_SERVICE_KEY = os.environ.get('IG_SERVICE_KEY', 'igsvc_pub_2026')  # gate suave; el dato es publico
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

try:
    from PIL import Image, ImageDraw
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', '--break-system-packages', 'pillow'], check=False)
    from PIL import Image, ImageDraw


def fetch_via_service(username):
    q = urllib.parse.urlencode({'u': username.lstrip('@').strip('/'), 'key': IG_SERVICE_KEY, 'tries': '4'})
    url = f'{IG_SERVICE_URL}/ig?{q}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def fetch_via_local(username):
    """Fallback: Playwright local (IP residencial, confiable). Auto-instala si falta."""
    venv_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.venv-pw', 'bin', 'python')
    venv_py = os.path.normpath(venv_py)
    driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ig_local_driver.py')
    if not os.path.exists(venv_py):
        import venv as _venv
        _venv.create(os.path.dirname(os.path.dirname(venv_py)), with_pip=True)
        subprocess.run([venv_py, '-m', 'pip', 'install', '--quiet', 'playwright'], check=True)
        subprocess.run([venv_py, '-m', 'playwright', 'install', 'chromium'], check=True)
    with open(driver, 'w') as f:
        f.write(_LOCAL_DRIVER)
    out = subprocess.run([venv_py, driver, username.lstrip('@').strip('/')], capture_output=True, text=True, timeout=120)
    try:
        return json.loads(out.stdout.strip().splitlines()[-1])
    except Exception:
        return {'urls': [], '_local_err': out.stderr[-200:]}


_LOCAL_DRIVER = r'''
import sys, json
from playwright.sync_api import sync_playwright
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
def extract():
    return """() => {
      const imgs = Array.from(document.querySelectorAll('img'));
      const posts = imgs.filter(i => /cdninstagram|fbcdn/.test(i.src) && i.naturalWidth>250 && !/profile picture/i.test(i.alt||'')).map(i => ({src:i.src, alt:(i.alt||'').replace(/\s+/g,' ').slice(0,80)}));
      const seen=new Set(); const u=[];
      for(const p of posts){const k=p.src.split('/').pop().split('?')[0].slice(0,30); if(!seen.has(k)){seen.add(k);u.push(p);}}
      return {login_wall: !!document.querySelector('input[name=\"username\"]'), urls:u};
    }"""
u=sys.argv[1]
with sync_playwright() as p:
    import os as _os
    _exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
    _kw = {'headless': True, 'args': ['--no-sandbox']}
    if _os.path.exists(_exe):
        _kw['executable_path'] = _exe
    _px = _os.environ.get('HTTPS_PROXY') or _os.environ.get('https_proxy')
    if _px:
        _kw['proxy'] = {'server': _px}
    b=p.chromium.launch(**_kw)
    pg=b.new_page(user_agent=UA, viewport={'width':1280,'height':2200})
    pg.goto(f'https://www.instagram.com/{u}/', wait_until='networkidle', timeout=45000)
    pg.wait_for_timeout(2500)
    try: pg.mouse.wheel(0,1800); pg.wait_for_timeout(1800)
    except Exception: pass
    d=pg.evaluate(extract()); b.close()
print(json.dumps(d))
'''


def fetch_urls(username):
    # Cloud-first (para la forja), local-fallback (confiable en IP residencial).
    try:
        d = fetch_via_service(username)
    except Exception as e:
        d = {'urls': [], '_svc_err': str(e)}
    if len(d.get('urls', [])) >= 5:
        return d
    # OJO: un login_wall del servicio NO debe cortar el fallback. El servicio sale por IP de
    # datacenter, que es justo la que IG gatea con la pared de login; la IP residencial local
    # suele pasar. Antes se retornaba aqui y se perdian fotos que el local si conseguia.
    motivo = 'pared de login' if d.get('login_wall') else f'{len(d.get("urls", []))} fotos'
    print(f'  servicio dio {motivo}; probando Playwright local...', flush=True)
    try:
        dl = fetch_via_local(username)
        if len(dl.get('urls', [])) > len(d.get('urls', [])):
            return dl
    except Exception as e:
        print('  fallback local fallo:', str(e)[:120])
    return d


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    username, slug = sys.argv[1], sys.argv[2]
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    d_dir = f'output/{slug}/assets/raw'
    os.makedirs(d_dir, exist_ok=True)

    try:
        data = fetch_urls(username)
    except Exception as e:
        print(f'ERROR llamando al servicio IG ({IG_SERVICE_URL}): {e}')
        sys.exit(1)
    if data.get('login_wall'):
        print('AVISO: Instagram mostro pared de login (cuenta privada o rate-limit). 0 fotos.')
        sys.exit(1)
    urls = data.get('urls', [])
    print(f'posts publicos vistos: {len(urls)} (via {IG_SERVICE_URL})')
    if not urls:
        print('0 fotos (perfil vacio/privado, o IG le sirvio pagina sin contenido a la IP del servicio).')
        sys.exit(1)

    ok = 0
    for i, x in enumerate(urls[:16], start):
        p = f'{d_dir}/bk-{i}.jpg'
        subprocess.run(['curl', '-s', '--max-time', '25', '-H', f'User-Agent: {UA}',
                        '-e', 'https://www.instagram.com/', '-o', p, x['src']], capture_output=True)
        try:
            Image.open(p).verify()
            im = Image.open(p).convert('RGB')
            im.thumbnail((1300, 1300))
            im.save(p, 'JPEG', quality=84)
            ok += 1
        except Exception:
            if os.path.exists(p):
                os.remove(p)
    print(f'fotos validas descargadas: {ok} (bk-{start}..)')
    print('alts:', [x.get('alt', '') for x in urls[:6]])

    # Orden NATURAL (bk-2 antes que bk-10): con sorted() lexicografico el contact sheet quedaba
    # desordenado y la curacion visual elegia por nombre el archivo equivocado.
    def orden_natural(f):
        m = re.search(r'(\d+)', f)
        return (int(m.group(1)) if m else 0, f)

    files = sorted((f for f in os.listdir(d_dir) if f.endswith('.jpg')), key=orden_natural)
    if files:
        cols, tw, th, label = 7, 150, 190, 16
        rows = (len(files) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * 154 + 4, rows * (th + label + 4) + 4), 'white')
        dr = ImageDraw.Draw(sheet)
        for idx, f in enumerate(files):
            im = Image.open(f'{d_dir}/{f}').convert('RGB')
            im.thumbnail((tw, th))
            xx = 4 + (idx % cols) * 154
            yy = 4 + (idx // cols) * (th + label + 4)
            sheet.paste(im, (xx, yy))
            dr.text((xx, yy + th + 2), f, fill='black')
        sheet.save(f'output/{slug}/_sheet.jpg', quality=80)
        print(f'contact sheet: output/{slug}/_sheet.jpg (curar VISUALMENTE)')


if __name__ == '__main__':
    main()
