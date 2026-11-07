#!/usr/bin/env python3
"""Descarga fotos de Google Maps a output/<slug>/assets/raw/gmaps-N.jpg, verifica con PIL
y genera el contact sheet _sheet.jpg para curaduria visual (leccion Iconic: mirar cada foto).

Uso: python3 scripts/_gmaps_photos.py <slug> <urls.json>
  urls.json = ["https://lh3.googleusercontent.com/...", ...]
"""
import json
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
MAX_LADO = 1000
CALIDAD = 82


def descargar(slug, urls, max_n=16):
    destino = f'output/{slug}/assets/raw'
    os.makedirs(destino, exist_ok=True)
    validas = []
    for i, u in enumerate(urls[:max_n], 1):
        ruta = f'{destino}/gmaps-{i}.jpg'
        r = subprocess.run(['curl', '-sS', '-m', '20', '-A', UA, '-o', ruta, u],
                            capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(ruta) or os.path.getsize(ruta) < 3000:
            if os.path.exists(ruta):
                os.remove(ruta)
            continue
        try:
            im = Image.open(ruta)
            im.verify()
            im = Image.open(ruta).convert('RGB')
            im.thumbnail((MAX_LADO, MAX_LADO))
            im.save(ruta, 'JPEG', quality=CALIDAD, optimize=True, progressive=True)
            validas.append(f'gmaps-{i}.jpg')
        except Exception:
            if os.path.exists(ruta):
                os.remove(ruta)
    return validas


def contact_sheet(slug, files):
    destino = f'output/{slug}/assets/raw'
    if not files:
        return None

    def natural(f):
        m = re.search(r'(\d+)', f)
        return int(m.group(1)) if m else 0
    files = sorted(files, key=natural)
    cols, tw, th, label = 6, 160, 200, 16
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 164 + 4, rows * (th + label + 4) + 4), 'white')
    dr = ImageDraw.Draw(sheet)
    for idx, f in enumerate(files):
        im = Image.open(f'{destino}/{f}').convert('RGB')
        im.thumbnail((tw, th))
        xx, yy = 4 + (idx % cols) * 164, 4 + (idx // cols) * (th + label + 4)
        sheet.paste(im, (xx, yy))
        dr.text((xx, yy + th + 2), f, fill='black')
    ruta = f'output/{slug}/_sheet.jpg'
    sheet.save(ruta, quality=80)
    return ruta


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    slug, urls_path = sys.argv[1], sys.argv[2]
    urls = json.load(open(urls_path, encoding='utf-8'))
    files = descargar(slug, urls)
    print(f'{slug}: {len(files)} fotos validas de {len(urls)} URLs')
    sheet = contact_sheet(slug, files)
    if sheet:
        print(f'contact sheet: {sheet} (MIRARLO antes de elegir tiles de galeria)')
    print(json.dumps(files))


if __name__ == '__main__':
    main()
