#!/usr/bin/env python3
"""Detecta el MISMO negocio registrado bajo dos slugs distintos en data/processed.json.

Uso: python3 scripts/dedup_check.py            -> exit 1 si hay duplicados contactables
     python3 scripts/dedup_check.py --all      -> tambien lista los ya resueltos

Por que existe (caso real 2026-07-21): "305 Esthetics" quedo registrado como `305esthetics` y
como `threezerofiveesthetics`, mismo IG y mismo email, los dos en `pending_manual`. Aprobar ese
lote habria mandado DOS cold emails al mismo dueno, que rompe la regla dura #3 del README.
La dedup del pipeline es por slug, y el slug se deriva del nombre: dos corridas pueden derivar
slugs distintos para el mismo negocio. La identidad real es el email o el handle de IG.

Correr esto ANTES de aprobar cualquier lote de outreach.
"""
import argparse
import collections
import json
import re
import sys

RUTA = 'data/processed.json'
# Estados que ya no van a generar un email: no cuentan como riesgo de doble contacto.
INACTIVOS = {'sent', 'skip_duplicate'}


def norm(v):
    return (v or '').strip().lower().lstrip('@')


def clave_nombre(x):
    return (re.sub(r'[^a-z0-9]', '', (x.get('name') or '').lower()),
            re.sub(r'[^a-z0-9]', '', (x.get('city') or '').lower()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true', help='incluir duplicados ya resueltos')
    a = ap.parse_args()

    registros = json.load(open(RUTA, encoding='utf-8'))
    activos = [x for x in registros if x.get('outreach') not in INACTIVOS]
    universo = registros if a.all else activos

    hallazgos = []
    for campo, extraer in (('email', lambda x: norm(x.get('email'))),
                           ('ig', lambda x: norm(x.get('ig'))),
                           ('nombre+ciudad', clave_nombre)):
        grupos = collections.defaultdict(list)
        for x in universo:
            k = extraer(x)
            if k and (not isinstance(k, tuple) or all(k)):
                grupos[k].append(x['slug'])
        for k, slugs in grupos.items():
            if len(slugs) > 1:
                hallazgos.append((campo, k, sorted(slugs)))

    # Un mismo par de slugs puede caer por email Y por ig: reportar el par una sola vez.
    vistos, unicos = set(), []
    for campo, k, slugs in hallazgos:
        par = tuple(slugs)
        if par in vistos:
            continue
        vistos.add(par)
        unicos.append((campo, k, slugs))

    if not unicos:
        print(f'DEDUP OK: {len(activos)} negocios contactables, ninguno repetido')
        return
    print(f'DEDUP FAIL ({len(unicos)}): mismo negocio bajo slugs distintos')
    for campo, k, slugs in unicos:
        print(f' - por {campo}: {k} -> {slugs}')
    print('\nResolver: dejar UN slug canonico y marcar el otro con')
    print('  "outreach": "skip_duplicate", "status": "duplicate", "duplicate_of": "<slug canonico>"')
    sys.exit(1)


if __name__ == '__main__':
    main()
