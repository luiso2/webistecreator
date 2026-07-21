#!/usr/bin/env python3
"""Descarga las fotos REALES del perfil publico de Instagram de un negocio, via Playwright.

Uso: python3 scripts/ig_photos.py <ig_username> <slug> [start_index]

AUTO-BOOTSTRAP (clave para la nube): el script se instala Playwright + chromium SOLO si no
estan, en un venv local `.venv-pw`, y se re-ejecuta con ese interprete. Asi corre igual en tu
Mac que en la nube de Anthropic (forja) o cualquier maquina, SIN depender de una instalacion
previa. La primera corrida en un entorno nuevo tarda ~1-2 min (instala chromium); las
siguientes en el mismo entorno son de segundos.

Por que Playwright y no curl: Instagram carga las fotos con JS (curl vuelve vacio) y la API
oficial solo da tu propia cuenta. Un navegador real anonimo (headless) SI ve los primeros
~12 posts del perfil publico, SIN login y SIN riesgo de ban para ninguna cuenta.
NUNCA inventa nada: solo baja lo que el perfil publica. Curar el _sheet.jpg (descartar covers
de reels y graficos con texto) antes de elegir.
"""
import os
import subprocess
import sys

VENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.venv-pw')
VENV = os.path.normpath(VENV)
VENV_PY = os.path.join(VENV, 'bin', 'python')


def ensure_playwright_and_reexec():
    """Si playwright no importa, crea/usa .venv-pw, instala, y re-ejecuta con su python."""
    try:
        import playwright.sync_api  # noqa: F401
        return  # ya disponible en este interprete
    except ImportError:
        pass
    # ¿ya existe el venv con playwright? re-ejecutar con el
    if os.path.exists(VENV_PY) and os.path.realpath(sys.executable) != os.path.realpath(VENV_PY):
        r = subprocess.run([VENV_PY, '-c', 'import playwright.sync_api'], capture_output=True)
        if r.returncode == 0:
            os.execv(VENV_PY, [VENV_PY] + sys.argv)
    # crear venv e instalar (idempotente)
    print('bootstrap: instalando Playwright + chromium (una sola vez por entorno)...', flush=True)
    if not os.path.exists(VENV_PY):
        subprocess.run([sys.executable, '-m', 'venv', VENV], check=True)
    subprocess.run([VENV_PY, '-m', 'pip', 'install', '--quiet', '--upgrade', 'pip'], check=False)
    subprocess.run([VENV_PY, '-m', 'pip', 'install', '--quiet', 'playwright', 'pillow'], check=True)
    subprocess.run([VENV_PY, '-m', 'playwright', 'install', 'chromium'], check=True)
    os.execv(VENV_PY, [VENV_PY] + sys.argv)


ensure_playwright_and_reexec()

from playwright.sync_api import sync_playwright  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

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
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page(user_agent=UA, viewport={'width': 1280, 'height': 2200})
        page.goto(url, wait_until='networkidle', timeout=45000)
        page.wait_for_timeout(2500)
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
        print('AVISO: Instagram mostro pared de login (cuenta privada o rate-limit). 0 fotos.')
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
        print(f'contact sheet: output/{slug}/_sheet.jpg (curar VISUALMENTE)')


if __name__ == '__main__':
    main()
