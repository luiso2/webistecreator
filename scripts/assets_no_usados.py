#!/usr/bin/env python3
"""Lista las fotos de output/*/assets/ que NO usa nadie, para excluirlas del deploy.

Uso: python3 scripts/assets_no_usados.py [--escribir]
     --escribir actualiza output/.assetsignore (por defecto solo informa)

NO BORRA NADA. Las fotos siguen en disco y en git: solo se dejan de PUBLICAR en el worker.
Los originales hacen falta para recurar un sitio o regenerarlo, y el ahorro de peso en el
deploy es el mismo que borrando.

QUE CUENTA COMO "EN USO" (los 7 criterios salieron de una auditoria con tres lentes
independientes mas un pase adversarial; cada uno es un caso real que un grep ingenuo pierde):
 1. index.html: src/srcset/poster/icon/og:image/background-image Y el "image" del JSON-LD,
    que es sintaxis JSON y no atributo HTML (15 sitios dependian solo de eso).
 2. URLs ABSOLUTAS al worker (https://siteforge-demos.../<slug>/assets/...): la unica forma
    que no empieza por "assets/".
 3. thumb de data/processed.json.
 4. thumb del REGISTRO EN KV: invisible a cualquier grep del repo y es el que sirve el panel.
    Puede estar STALE (apuntar a una foto que el sitio ya no usa), y aun asi hay que respetarlo.
 5. data.json / content.json / captions.json leidos como TEXTO, nunca con json.load: hay al
    menos un data.json malformado, y parsearlo lanzaria excepcion y daria sus 11 fotos por
    huerfanas. Incluye los nombres DESNUDOS ("bk-3.jpg" sin la ruta delante).
 6. scripts/build_*.py, para que un rebuild siga encontrando sus fotos.
 7. Slugs en LISTA NEGRA (rangos en prosa tipo "bk-1.jpg..bk-12.jpg", irresolubles por regex)
    y slugs sin index.html: se dejan intactos por precaucion.
"""
import argparse
import json
import os
import re
import glob

RAIZ = 'output'
IGNORE = os.path.join(RAIZ, '.assetsignore')
KV_REGISTRY = '/tmp/kv_registry.json'  # volcado de: wrangler kv key get registry

# Slugs que no se tocan: su data.json describe las fotos con rangos en prosa que no se
# pueden resolver, asi que no hay forma segura de saber cuales sobran.
LISTA_NEGRA = {'meinbeautystudio', 'emery-beauty-bar-cape-coral'}

CABECERA = """# Material de TRABAJO: no se publica en el worker (se sigue guardando en git).
# Sin este archivo el research de cada negocio quedaba accesible desde internet:
# comprobado 2026-08-11, 94 data.json con el email del negocio, 76 con notas internas y
# 58 con borradores de outreach respondian 200 a cualquiera que supiera la URL.
**/data.json
**/content.json
**/captions.json
**/ig_profile.json
**/_sheet.jpg
**/wrangler.jsonc
**/.assetsignore
**/site_check/

# ---------------------------------------------------------------------------
# Fotos descargadas que NINGUN sitio usa. Se quedan en disco y en git (hacen falta para
# recurar o regenerar un sitio), pero no se suben al worker: son peso muerto en cada deploy.
# Generado por scripts/assets_no_usados.py, que cruza 7 fuentes distintas de referencias.
# Para regenerarlo:
#   npx wrangler kv key get registry --namespace-id <ns> --remote > /tmp/kv_registry.json
#   python3 scripts/assets_no_usados.py --escribir
"""

RE_ASSET = re.compile(r'assets/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp|gif|mp4|svg)', re.I)
RE_ABS = re.compile(r'https?://[^"\'\s)]*?/([a-z0-9-]{1,40})/(assets/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp|gif|mp4|svg))', re.I)
RE_DESNUDO = re.compile(r'\b([A-Za-z0-9][A-Za-z0-9._-]*\.(?:jpg|jpeg|png|webp|gif|mp4))\b', re.I)


def norm(*p):
    return os.path.normpath(os.path.join(*p))


def leer(ruta):
    try:
        return open(ruta, encoding='utf-8', errors='replace').read()
    except Exception:
        return ''


def recoger():
    usadas, slugs_intactos = set(), set(LISTA_NEGRA)
    dirs = [d for d in glob.glob(f'{RAIZ}/*/') if os.path.isdir(d)]

    for d in dirs:
        slug = os.path.basename(d.rstrip('/'))
        idx = os.path.join(d, 'index.html')
        if not os.path.exists(idx):
            # Sin index.html no se puede saber que usa: no se toca nada de ese slug.
            slugs_intactos.add(slug)
            continue
        h = leer(idx)
        # (1) rutas relativas, incluidas las del JSON-LD
        for r in RE_ASSET.findall(h):
            usadas.add(norm(d, r))
        # (2) URLs absolutas al worker: pueden apuntar a OTRO slug, hay que resolver por la URL
        for s_url, r in RE_ABS.findall(h):
            usadas.add(norm(RAIZ, s_url, r))

    # (5) json de trabajo, como TEXTO (hay al menos uno malformado)
    for f in glob.glob(f'{RAIZ}/*/*.json'):
        d = os.path.dirname(f)
        t = leer(f)
        for r in RE_ASSET.findall(t):
            usadas.add(norm(d, r))
        for s_url, r in RE_ABS.findall(t):
            usadas.add(norm(RAIZ, s_url, r))
        # nombres desnudos: solo valen si existe el archivo en ese slug
        for n in RE_DESNUDO.findall(t):
            for sub in ('assets/raw', 'assets'):
                p = norm(d, sub, n)
                if os.path.exists(p):
                    usadas.add(p)

    # (3) thumbs del registro en disco
    if os.path.exists('data/processed.json'):
        for x in json.load(open('data/processed.json', encoding='utf-8')):
            for s_url, r in RE_ABS.findall(str(x.get('thumb') or '')):
                usadas.add(norm(RAIZ, s_url, r))

    # (4) thumbs del registro en KV (los que sirve el panel; invisibles al grep)
    if os.path.exists(KV_REGISTRY):
        for x in json.load(open(KV_REGISTRY, encoding='utf-8')):
            for s_url, r in RE_ABS.findall(str(x.get('thumb') or '')):
                usadas.add(norm(RAIZ, s_url, r))
    else:
        print('AVISO: no hay volcado del KV; se aborta para no ignorar thumbs del panel.')
        raise SystemExit(1)

    # (6) scripts de build, para que un rebuild siga encontrando sus fotos
    for f in glob.glob('scripts/build_*.py'):
        t = leer(f)
        m = re.search(r'output/([a-z0-9-]{1,40})/', t)
        slug = m.group(1) if m else None
        for r in RE_ASSET.findall(t):
            if slug:
                usadas.add(norm(RAIZ, slug, r))
            else:
                # sin slug resoluble: se protege ese nombre en TODOS los slugs (conservador)
                base = os.path.basename(r)
                for d in dirs:
                    for sub in ('assets/raw', 'assets'):
                        p = norm(d, sub, base)
                        if os.path.exists(p):
                            usadas.add(p)
    return usadas, slugs_intactos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--escribir', action='store_true')
    a = ap.parse_args()

    usadas, intactos = recoger()
    todas = {norm(p) for p in glob.glob(f'{RAIZ}/*/assets/**/*', recursive=True) if os.path.isfile(p)}
    fotos = {p for p in todas if p.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4'))}
    huerfanas = sorted(
        p for p in fotos - usadas
        if p.split(os.sep)[1] not in intactos
    )
    mb = sum(os.path.getsize(p) for p in huerfanas) / 1024 / 1024
    print(f'  fotos totales           : {len(fotos)}')
    print(f'  en uso (7 criterios)    : {len(fotos & usadas)}')
    print(f'  slugs intactos          : {len(intactos)} (sin index.html o en lista negra)')
    print(f'  NO usadas por nadie     : {len(huerfanas)}  ({mb:.0f} MB que dejan de subirse)')

    if not a.escribir:
        print('\n  (informativo: usa --escribir para actualizar output/.assetsignore)')
        return
    rutas = [p[len(RAIZ) + 1:] for p in huerfanas]  # relativas a output/
    with open(IGNORE, 'w', encoding='utf-8') as f:
        f.write(CABECERA + '\n'.join(rutas) + '\n')
    print(f'\n  escrito {IGNORE} con {len(rutas)} exclusiones')


if __name__ == '__main__':
    main()
