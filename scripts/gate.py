#!/usr/bin/env python3
"""Puerta de calidad de un demo site. Falla (exit 1) si algo no pasa.

Uso: python3 scripts/gate.py <slug> --lang es|en [--forbid "Str1,Str2,..."]

Checks (los mismos que el proceso manual probado):
1. em-dash (U+2014) == 0 en index.html
2. toda ruta assets/ referenciada existe, pesa >0 y decodifica como imagen (PIL)
3. JSON-LD parsea como JSON valido
4. markers motion v2+v3 presentes (text-shine, orb, glass, btn-3d, reveal, preloader,
   marquee, data-count, merktop-badge, data-es, split-word, sec-num, tile-cap,
   cursor-ring, foot-mark, heroInner, assets/tailwind.js)
5. applyLang default y <html lang> coherentes con --lang
6. strings prohibidos ausentes (nombres del negocio anterior del esqueleto, ciudad vieja, etc.)
7. sin referencias a localhost ni a templates/
"""
import argparse
import json
import os
import re
import sys

try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'], check=True)
    from PIL import Image

MARKERS = ['text-shine', 'orb', 'glass', 'btn-3d', 'reveal', 'preloader', 'marquee',
           'data-count', 'merktop-badge', 'data-es', 'split-word', 'sec-num', 'tile-cap',
           'cursor-ring', 'foot-mark', 'heroInner', 'assets/tailwind.js', 'Powered by']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('--lang', required=True, choices=['es', 'en'])
    ap.add_argument('--forbid', default='')
    a = ap.parse_args()

    path = f'output/{a.slug}/index.html'
    if not os.path.exists(path):
        print(f'FAIL: no existe {path}')
        sys.exit(1)
    h = open(path, encoding='utf-8').read()
    fails = []

    n = h.count('—')
    if n:
        fails.append(f'em-dash x{n} (PROHIBIDO)')

    for ruta in sorted(set(re.findall(r'assets/[A-Za-z0-9./_-]+', h))):
        p = f'output/{a.slug}/{ruta}'
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            fails.append(f'asset roto o vacio: {ruta}')
        elif ruta.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            try:
                Image.open(p).verify()
            except Exception:
                fails.append(f'asset no decodifica: {ruta}')

    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, flags=re.S)
    if not m:
        fails.append('falta JSON-LD')
    else:
        try:
            json.loads(m.group(1))
        except Exception as e:
            fails.append(f'JSON-LD invalido: {e}')

    for mk in MARKERS:
        if mk not in h:
            fails.append(f'falta marker: {mk}')

    ml = re.search(r"applyLang\(lang === '(\w\w)' \? '\w\w' : '(\w\w)'\)", h)
    if not ml:
        fails.append('no se encontro applyLang default')
    else:
        default = ml.group(2)
        if default != a.lang:
            fails.append(f'applyLang default es "{default}", esperado "{a.lang}"')
    mh = re.search(r'<html lang="(\w\w)"', h)
    if mh and mh.group(1) != a.lang:
        fails.append(f'<html lang="{mh.group(1)}"> esperado "{a.lang}"')

    for s in [x.strip() for x in a.forbid.split(',') if x.strip()]:
        c = h.count(s)
        if c:
            fails.append(f'string prohibido "{s}" x{c} (leftover del esqueleto)')

    if 'localhost' in h or 'templates/' in h:
        fails.append('referencia a localhost o templates/')

    if fails:
        print(f'GATE FAIL ({len(fails)}):')
        for f in fails:
            print(' -', f)
        sys.exit(1)
    print(f'GATE OK: {a.slug} ({a.lang})')


if __name__ == '__main__':
    main()
