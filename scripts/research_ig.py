#!/usr/bin/env python3
"""Research COMPLETO de un negocio a partir de su Instagram, en UNA sola pasada.

Uso: .venv-pw/bin/python scripts/research_ig.py <ig_handle> [slug]
Salida: output/<slug>/data.json + assets/raw/bk-N.jpg + assets/raw/logo.jpg + _sheet.jpg

QUE SUSTITUYE (y por que es mas rapido, medido 2026-07-29):
El research anterior abria Instagram 4 veces: ig_photos.py (fotos), ig_contact.py (bio y
contacto), una pasada para la foto de perfil y otra para los captions. Cada navegacion
cuesta ~5.6s, o sea ~22s solo en IG. Este script hace UNA navegacion y saca todo de ella.
Ademas descarga las fotos en paralelo (12 fotos: 3.8s secuencial -> 0.4s, 8.7x) y, en local,
no gasta 4.5s llamando primero al servicio de Railway (que suele devolver <5 fotos porque
sale por IP de datacenter y IG se la gatea).

Beneficio mayor que el tiempo: 1 sola visita a IG en vez de 4 baja a la cuarta parte el
riesgo de rate limit, que es lo que de verdad hace fallar un build.

REGLA: no inventa nada. Solo devuelve lo que el perfil publica. Los campos que no
encuentra quedan en null para que el build sepa que NO tiene ese dato.
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')
IG_SERVICE_URL = os.environ.get('IG_SERVICE_URL', 'https://ig-photo-service-production.up.railway.app')
IG_SERVICE_KEY = os.environ.get('IG_SERVICE_KEY', 'igsvc_pub_2026')
MAX_FOTOS = 16

try:
    from PIL import Image, ImageDraw
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', '--break-system-packages', 'pillow'], check=False)
    from PIL import Image, ImageDraw

# Driver de UNA pasada: perfil + bio + contacto + foto de perfil + fotos + captions.
_DRIVER = r'''
import sys, json
from playwright.sync_api import sync_playwright
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
h=sys.argv[1]
EXTRAER = """() => {
  const header = document.querySelector('header');
  const bio = header ? header.innerText : '';
  // Los links se sacan SOLO del header (la bio). Con querySelectorAll('a') de toda la
  // pagina entraban about.meta.com y threads.com del pie de Instagram y el negocio
  // quedaba marcado con "website propio" siendo falso.
  const links = header ? [...header.querySelectorAll('a')].map(a => a.href).filter(Boolean) : [];
  const meta = document.querySelector('meta[name="description"]');
  const pp = [...document.querySelectorAll('img')].find(i => /profile picture/i.test(i.alt||''));
  const imgs = [...document.querySelectorAll('img')];
  const posts = imgs
    .filter(i => /cdninstagram|fbcdn/.test(i.src) && i.naturalWidth > 250 && !/profile picture/i.test(i.alt||''))
    .map(i => ({src: i.src, alt: (i.alt||'').replace(/\s+/g,' ').slice(0,220)}));
  const seen = new Set(); const urls = [];
  for (const p of posts) {
    const k = p.src.split('/').pop().split('?')[0].slice(0,30);
    if (!seen.has(k)) { seen.add(k); urls.push(p); }
  }
  return {
    login_wall: !!document.querySelector('input[name="username"]'),
    bio, links, profile_pic: pp ? pp.src : '', urls,
    // el conteo de posts no esta en el header, si en la meta description
    meta_desc: meta ? meta.content : '',
    title: document.title
  };
}"""
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, args=['--no-sandbox'])
    pg=b.new_page(user_agent=UA, viewport={'width':1280,'height':2400})
    # domcontentloaded + espera corta: networkidle en IG cuesta segundos extra y no aporta
    pg.goto(f'https://www.instagram.com/{h}/', wait_until='domcontentloaded', timeout=45000)
    pg.wait_for_timeout(2200)
    try: pg.mouse.wheel(0, 2200); pg.wait_for_timeout(1600)
    except Exception: pass
    d=pg.evaluate(EXTRAER)
    b.close()
print(json.dumps(d))
'''

RE_EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]{2,}')
# Telefono US con o sin +1, con parentesis/guiones/espacios/puntos
RE_TEL = re.compile(r'(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}')


def venv_python():
    ruta = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.venv-pw', 'bin', 'python'))
    return ruta if os.path.exists(ruta) else None


def scrape_local(handle):
    """Playwright local: IP residencial, es el que de verdad pasa el gate de IG."""
    py = venv_python()
    if not py:
        return None
    driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ig_research_driver.py')
    with open(driver, 'w') as f:
        f.write(_DRIVER)
    out = subprocess.run([py, driver, handle], capture_output=True, text=True, timeout=150)
    try:
        return json.loads(out.stdout.strip().splitlines()[-1])
    except Exception:
        print('  local fallo:', (out.stderr or '')[-200:])
        return None


def scrape_servicio(handle):
    """Fallback para entornos sin navegador (forja cloud). Solo trae fotos, no bio."""
    q = urllib.parse.urlencode({'u': handle, 'key': IG_SERVICE_KEY, 'tries': '4'})
    try:
        req = urllib.request.Request(f'{IG_SERVICE_URL}/ig?{q}', headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode())
        d.setdefault('bio', '')
        d.setdefault('links', [])
        d.setdefault('profile_pic', '')
        return d
    except Exception as e:
        print('  servicio fallo:', str(e)[:120])
        return None


def obtener(handle):
    """Local primero cuando hay navegador (es el que funciona y evita 4.5s de servicio inutil).
    Sin navegador (cloud), el servicio es lo unico que hay."""
    if venv_python():
        d = scrape_local(handle)
        if d and (len(d.get('urls', [])) >= 5 or d.get('login_wall')):
            return d, 'playwright-local'
        alt = scrape_servicio(handle)
        if alt and len(alt.get('urls', [])) > len((d or {}).get('urls', [])):
            return alt, 'servicio-railway'
        return d, 'playwright-local'
    return scrape_servicio(handle), 'servicio-railway'


def descargar_paralelo(urls, destino, start=1):
    """12 fotos: 3.8s secuencial -> 0.4s en paralelo (medido)."""
    procs = []
    for i, x in enumerate(urls[:MAX_FOTOS], start):
        ruta = f'{destino}/bk-{i}.jpg'
        procs.append((ruta, subprocess.Popen(
            ['curl', '-s', '--max-time', '25', '-H', f'User-Agent: {UA}',
             '-e', 'https://www.instagram.com/', '-o', ruta, x['src']],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)))
    validas = []
    for ruta, p in procs:
        p.wait()
        try:
            Image.open(ruta).verify()
            im = Image.open(ruta).convert('RGB')
            im.thumbnail((1300, 1300))
            im.save(ruta, 'JPEG', quality=84)
            validas.append(ruta)
        except Exception:
            if os.path.exists(ruta):
                os.remove(ruta)
    return validas


def contact_sheet(destino, slug):
    def natural(f):
        m = re.search(r'(\d+)', f)
        return (int(m.group(1)) if m else 0, f)

    files = sorted((f for f in os.listdir(destino) if f.endswith('.jpg') and f.startswith('bk-')), key=natural)
    if not files:
        return None
    cols, tw, th, label = 7, 150, 190, 16
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 154 + 4, rows * (th + label + 4) + 4), 'white')
    dr = ImageDraw.Draw(sheet)
    for idx, f in enumerate(files):
        im = Image.open(f'{destino}/{f}').convert('RGB')
        im.thumbnail((tw, th))
        xx, yy = 4 + (idx % cols) * 154, 4 + (idx // cols) * (th + label + 4)
        sheet.paste(im, (xx, yy))
        dr.text((xx, yy + th + 2), f, fill='black')
    ruta = f'output/{slug}/_sheet.jpg'
    sheet.save(ruta, quality=80)
    return ruta


def desenvolver(url):
    """El link de la bio sale envuelto en el redirector de IG
    (l.instagram.com/?u=<url-encodeada>&e=...). Devuelve la URL real."""
    if 'l.instagram.com' not in url:
        return url
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    return urllib.parse.unquote(q['u'][0]) if q.get('u') else url


def check_websites(handle, links):
    """Regla dura #2: saber si YA tienen website propio cambia el angulo del outreach.
    Se prueban los candidatos EN PARALELO (antes era una consulta detras de otra)."""
    base = re.sub(r'[^a-z0-9]', '', handle.lower())
    candidatos = [f'{base}.com', f'{base}.net', f'{base}.us']
    PLATAFORMAS = ('instagram.com', 'facebook.com', 'tiktok.com', 'threads.net', 'linktr.ee',
                   'booksy.com', 'glossgenius.com', 'square.site', 'fresha.com', 'vagaro.com',
                   'wa.me', 'api.whatsapp', 'youtube.com', 'twitter.com', 'x.com', 'l.instagram.com')
    for l in links:
        host = urllib.parse.urlparse(l).netloc.lower()
        if host and not any(p in host for p in PLATAFORMAS) and host not in candidatos:
            candidatos.append(host)
    procs = [(c, subprocess.Popen(
        ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '8', '-L', f'https://{c}'],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)) for c in candidatos[:6]]
    vivos = []
    for c, p in procs:
        out, _ = p.communicate()
        if (out or b'').decode().strip() == '200':
            vivos.append(f'https://{c}')
    return vivos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    handle = sys.argv[1].lstrip('@').strip('/')
    slug = sys.argv[2] if len(sys.argv) > 2 else re.sub(r'[^a-z0-9-]', '', handle.lower())
    destino = f'output/{slug}/assets/raw'
    os.makedirs(destino, exist_ok=True)

    print(f'research de @{handle} -> output/{slug}/')
    d, via = obtener(handle)
    if not d:
        print('ERROR: no se pudo leer el perfil (ni local ni servicio).')
        sys.exit(1)
    if d.get('login_wall'):
        print('AVISO: Instagram mostro pared de login (perfil privado o rate limit). Reintentar mas tarde.')
        sys.exit(1)
    urls = d.get('urls', [])
    if not urls:
        print('0 fotos: perfil vacio, privado, o IG sirvio pagina sin contenido.')
        sys.exit(1)

    validas = descargar_paralelo(urls, destino)
    logo = None
    if d.get('profile_pic'):
        logo = f'{destino}/logo.jpg'
        subprocess.run(['curl', '-s', '--max-time', '20', '-H', f'User-Agent: {UA}',
                        '-e', 'https://www.instagram.com/', '-o', logo, d['profile_pic']],
                       capture_output=True)
        try:
            Image.open(logo).verify()
        except Exception:
            os.remove(logo)
            logo = None

    bio = d.get('bio', '') or ''
    # La meta description trae "N Followers, N Following, N Posts"; el header no trae posts.
    metricas = f"{bio}\n{d.get('meta_desc', '') or ''}"
    emails = RE_EMAIL.findall(bio)
    tels = RE_TEL.findall(bio)
    seguidores = re.search(r'([\d.,]+)\s*(?:followers|seguidores)', metricas, re.I)
    posts = re.search(r'([\d.,]+)\s*(?:posts|publicaciones)', metricas, re.I)
    externos = [desenvolver(l) for l in d.get('links', []) if 'l.instagram.com' in l or
                (urllib.parse.urlparse(l).netloc and 'instagram.com' not in urllib.parse.urlparse(l).netloc)]
    sitios = check_websites(handle, externos)

    data = {
        'slug': slug,
        'ig': f'@{handle}',
        'ig_url': f'https://www.instagram.com/{handle}/',
        'fuente': via,
        'bio_raw': bio,
        'email': emails[0] if emails else None,
        'phone': tels[0].strip() if tels else None,
        'followers': seguidores.group(1) if seguidores else None,
        'posts': posts.group(1) if posts else None,
        'links_externos': externos[:6],
        'website_candidates_vivos': sitios,
        'has_own_site': bool(sitios),
        'logo': 'assets/raw/logo.jpg' if logo else None,
        'fotos': [os.path.basename(v) for v in validas],
        'captions': [x.get('alt', '') for x in urls[:MAX_FOTOS]],
    }
    with open(f'output/{slug}/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    sheet = contact_sheet(destino, slug)

    print(f'  via: {via}')
    print(f'  fotos validas: {len(validas)} | logo: {"si" if logo else "NO"}')
    print(f'  telefono: {data["phone"]} | email: {data["email"]}')
    print(f'  seguidores: {data["followers"]} | posts: {data["posts"]}')
    print(f'  website propio: {sitios if sitios else "NO (angulo: no tienen website)"}')
    print(f'  data.json + {sheet} listos. CURAR EL SHEET VISUALMENTE antes de construir.')


if __name__ == '__main__':
    main()
