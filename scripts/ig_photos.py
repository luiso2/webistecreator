#!/usr/bin/env python3
"""Descarga las fotos REALES del perfil publico de Instagram de un negocio, via Playwright.

Uso: .venv-pw/bin/python scripts/ig_photos.py <ig_username> <slug> [start_index]

Por que Playwright y no curl: Instagram carga las fotos con JS (curl vuelve vacio) y la API
oficial solo da tu propia cuenta. Un navegador real anonimo (headless) SI ve los primeros
~12 posts del perfil publico, SIN login (no pide pared de login) y SIN riesgo de ban para
ninguna cuenta (solo mira una pagina publica). Es la solucion al cuello de botella de fotos
de los tenants que estan en Square/GlossGenius (sus plataformas dan menu pero no fotos).

- Extrae del DOM renderizado las <img> de cdninstagram/fbcdn con naturalWidth>250 (excluye la
  foto de perfil). Dedupe por id del post.
- Descarga a output/<slug>/assets/raw/bk-N.jpg (start_index permite complementar fotos ya bajadas).
- Valida que cada archivo decodifica (PIL) y redimensiona a 1300px.
- Genera output/<slug>/_sheet.jpg para la curacion visual OBLIGATORIA (algunos posts son covers de
  reels o graficos con texto: MIRAR el sheet y elegir solo resultados reales).
NUNCA inventa nada: solo baja lo que el perfil publica.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.venv-pw', 'lib'))
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print('ERROR: usar el interprete del venv: .venv-pw/bin/python scripts/ig_photos.py ...')
    sys.exit(2)
try:
    from PIL import Image, ImageDraw
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'], check=False)
    from PIL import Image, ImageDraw

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

EXTRACT_JS = """() => {
  const imgs = Array.from(document.querySelectorAll('img'));
  const posts = imgs
    .filter(i => /cdninstagram|fbcdn/.test(i.src) && i.naturalWidth > 250 && !/profile picture/i.test(i.alt||''))
    .map(i => ({src: i.src, alt: (i.alt||'').replace(/\\s+/g,' ').slice(0,70)}));
  const seen = new Set(); const uniq = [];
  for (const p of posts){ const k = p.src.split('/').pop().split('?')[0].slice(0,30); if(!seen.has(k)){seen.add(k); uniq.push(p);} }
  return {login_wall: !!document.querySelector('input[name=\"username\"]'), urls: uniq};
}"""


def fetch_urls(username):
    url = f'https://www.instagram.com/{username.lstrip("@").strip("/")}/'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA, viewport={'width': 1280, 'height': 2200})
        page.goto(url, wait_until='networkidle', timeout=45000)
        page.wait_for_timeout(2500)
        # un scroll suave para forzar carga de mas posts
        try:
            page.mouse.wheel(0, 1800)
            page.wait_for_timeout(1800)
        except Exception:
            pass
        data = page.evaluate(EXTRACT_JS)
        browser.close()
    return data


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    username, slug = sys.argv[1], sys.argv[2]
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    d_dir = f'output/{slug}/assets/raw'
    os.makedirs(d_dir, exist_ok=True)

    data = fetch_urls(username)
    if data.get('login_wall'):
        print('AVISO: Instagram mostro pared de login para este perfil (posible cuenta privada o rate-limit). 0 fotos.')
        sys.exit(1)
    urls = data.get('urls', [])
    print(f'posts publicos vistos: {len(urls)}')
    if not urls:
        print('0 fotos (perfil vacio, privado o IG cambio el DOM).')
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
    print('alts:', [x['alt'] for x in urls[:6]])

    files = sorted(f for f in os.listdir(d_dir) if f.endswith('.jpg'))
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
        print(f'contact sheet: output/{slug}/_sheet.jpg (curar VISUALMENTE: descartar covers de reels y graficos con texto)')


if __name__ == '__main__':
    main()
