#!/usr/bin/env python3
"""Paleta automatica por negocio a partir de sus fotos reales.

Uso: python3 scripts/paleta_auto.py <slug>

Lee output/<slug>/assets/raw/*.jpg (fotos + logo) y calcula el hue dominante
ponderado por saturacion (ignora grises, blancos y negros puros). Asi cada site
toma el color de la identidad real del negocio en vez de un color fijo.

Para que no salgan varios sites seguidos del mismo color, consulta
data/processed.json: si el hue elegido esta a menos de 25 grados de uno usado
en los ultimos 12 builds, lo desplaza +45 grados.

Guarda el resultado en output/<slug>/content.json -> {"paleta": {"hue": H}}.
Si content.json ya existe (textos escritos por el agente), solo fusiona la clave
"paleta" sin tocar nada mas. El agente siempre puede sobreescribir el hue a mano.
"""
import colorsys
import glob
import json
import os
import sys

MIN_SAT = 0.18
VAR_MIN_DIST = 25
VAR_NUDGE = 45
RECIENTES = 12
REGISTRO = 'data/processed.json'


def hue_dominante(paths):
    from PIL import Image
    hist = [0.0] * 360
    for p in paths:
        try:
            im = Image.open(p).convert('RGB').resize((120, 120))
        except Exception:
            continue
        px = im.load()
        w, h = im.size
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                r, g, b = px[x, y]
                hh, ll, ss = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
                if ss < MIN_SAT or ll < 0.12 or ll > 0.92:
                    continue
                hist[int(hh * 360) % 360] += ss * ss
    if sum(hist) <= 0:
        return None
    suav = [0.0] * 360
    for i in range(360):
        suav[i] = (hist[i - 2] + hist[i - 1] * 2 + hist[i] * 3
                   + hist[(i + 1) % 360] * 2 + hist[(i + 2) % 360]) / 9.0
    return max(range(360), key=lambda i: suav[i])


def dist_circular(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def hues_recientes():
    if not os.path.exists(REGISTRO):
        return []
    try:
        reg = json.load(open(REGISTRO, encoding='utf-8'))
    except Exception:
        return []
    hues = []
    for e in reg[-RECIENTES:]:
        h = e.get('paleta_hue')
        if isinstance(h, (int, float)):
            hues.append(h % 360)
    return hues


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    slug = sys.argv[1]
    fotos = sorted(glob.glob(f'output/{slug}/assets/raw/*.jpg'))
    if not fotos:
        print(f'FAIL: no hay fotos en output/{slug}/assets/raw/')
        sys.exit(1)

    hue = hue_dominante(fotos)
    if hue is None:
        print('AVISO: fotos sin color aprovechable (grises); no se fija paleta.')
        sys.exit(0)
    origen = hue

    for h in hues_recientes():
        if dist_circular(hue, h) < VAR_MIN_DIST:
            hue = (hue + VAR_NUDGE) % 360
            break

    ruta = f'output/{slug}/content.json'
    contenido = {}
    if os.path.exists(ruta):
        contenido = json.load(open(ruta, encoding='utf-8'))
    contenido['paleta'] = {'hue': hue, 'sat_mult': 1.0, 'light_mult': 1.0}
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    json.dump(contenido, open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    nota = f'hue {origen}' if hue == origen else f'hue {origen} -> {hue} (variedad)'
    print(f'{slug}: paleta automatica {nota} | {len(fotos)} fotos | guardada en {ruta}')


if __name__ == '__main__':
    main()
