#!/usr/bin/env python3
"""Descarga la galeria de un perfil de Booksy y genera el contact sheet para curacion visual.

Uso: python3 scripts/booksy_gallery.py <booksy_url> <slug> [max_fotos]

- Extrae las fotos biz_photo de cloudfront (dedupe por hash, prefiere 'large').
- html.unescape OBLIGATORIO (las URLs vienen con &#38;; sin esto el CDN da 403).
- Redimensiona a max 1300px con PIL (sin sips: corre igual en macOS y Linux/cloud).
- Borra archivos que no decodifican como imagen.
- Escribe output/<slug>/assets/raw/bk-N.jpg y el sheet en output/<slug>/_sheet.jpg
  (el _sheet.jpg esta en .assetsignore: NO se deploya; el agente lo LEE para curar).
- Imprime metadata detectada (nombre, rating, reviews, telefono) del payload de la pagina.
"""
import html
import io
import os
import re
import subprocess
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'], check=True)
    from PIL import Image, ImageDraw

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'


def curl(url, out=None, timeout=30):
    cmd = ['curl', '-s', '--max-time', str(timeout), '-H', f'User-Agent: {UA}', url]
    if out:
        cmd += ['-o', out]
        return subprocess.run(cmd, capture_output=True).returncode == 0
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    url, slug = sys.argv[1], sys.argv[2]
    max_fotos = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    d = f'output/{slug}/assets/raw'
    os.makedirs(d, exist_ok=True)

    page = html.unescape(curl(url))
    if len(page) < 5000:
        print('ERROR: pagina de Booksy vacia o bloqueada, len', len(page))
        sys.exit(1)

    # metadata util para el build
    for label, pat in [('nombre', r'"name"\s*:\s*"([^"]{3,80})"'),
                       ('rating', r'"ratingValue"\s*:\s*"?([0-9.]+)'),
                       ('reviews', r'"reviewCount"\s*:\s*"?(\d+)'),
                       ('telefono', r'"telephone"\s*:\s*"([^"]+)"'),
                       ('telefono2', r'"phone"\s*:\s*"([^"]+)"')]:
        m = re.search(pat, page)
        if m:
            print(f'meta {label}: {m.group(1)}')
    igs = sorted(set(re.findall(r'instagram\.com/([A-Za-z0-9_.]+)', page)) - {'booksybiz'})
    if igs:
        print('meta instagram:', igs[:3])

    urls = re.findall(r'https://d2zdpiztbgorvt\.cloudfront\.net/[^"\'\s\\]*', page)
    por = {}
    for u in urls:
        m = re.search(r'biz_photo/([a-f0-9]+)', u)
        base = m.group(1) if m else u.split('/')[-1][:24]
        score = len(u) + (100 if 'large' in u else 0) - (100 if ('small' in u or 'thumb' in u) else 0)
        prev = por.get(base)
        if not prev or score > prev[1]:
            por[base] = (u, score)

    ok = 0
    for i, (u, _s) in enumerate(list(por.values())[:max_fotos], 1):
        p = f'{d}/bk-{i}.jpg'
        curl(u, out=p, timeout=25)
        try:
            im = Image.open(p)
            im.verify()
            im = Image.open(p).convert('RGB')
            im.thumbnail((1300, 1300))
            im.save(p, 'JPEG', quality=84)
            ok += 1
        except Exception:
            if os.path.exists(p):
                os.remove(p)
    print('fotos validas:', ok)

    files = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
    if files:
        cols, tw, th, label = 7, 150, 190, 16
        rows = (len(files) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * 154 + 4, rows * (th + label + 4) + 4), 'white')
        dr = ImageDraw.Draw(sheet)
        for idx, f in enumerate(files):
            im = Image.open(f'{d}/{f}').convert('RGB')
            im.thumbnail((tw, th))
            x = 4 + (idx % cols) * 154
            y = 4 + (idx // cols) * (th + label + 4)
            sheet.paste(im, (x, y))
            dr.text((x, y + th + 2), f, fill='black')
        sheet.save(f'output/{slug}/_sheet.jpg', quality=80)
        print(f'contact sheet: output/{slug}/_sheet.jpg (LEERLO y curar ANTES de elegir fotos)')


if __name__ == '__main__':
    main()
