#!/usr/bin/env python3
"""Publica un demo ya construido: gate -> deploy -> verificar live -> registrar.

Uso: python3 scripts/publish.py <slug> --lang es|en|fr [--forbid "A,B"] [--name "..."]
                                [--city "..."] [--ig "@handle"] [--dry-run]

Por que existe: estos 4 pasos se hacian a mano y en ese orden esta el riesgo. Registrar un
negocio ANTES de comprobar que el demo responde 200 crea "tarjetas fantasma" en el panel
(un link que el dueno abre y no carga). Aqui el registro ocurre SOLO si el live respondio 200.

Es idempotente: re-publicar el mismo slug actualiza su registro, nunca lo duplica, y jamas
pisa un negocio con outreach 'sent' o 'skip_duplicate'.
"""
import argparse
import json
import os
import subprocess
import sys
import time

BASE_DEMOS = 'https://siteforge-demos.odd-forest-9504.workers.dev'
REGISTRO = 'data/processed.json'


def paso(txt):
    print(f'\n=== {txt}')


def correr(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def http_code(url, intentos=6, espera=5):
    """El CDN tarda en propagar: reintenta antes de dar por fallido el deploy."""
    code = '000'
    for i in range(intentos):
        r = correr(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                    '--max-time', '15', '-L', url])
        code = (r.stdout or '').strip() or '000'
        if code == '200':
            return code
        if i < intentos - 1:
            time.sleep(espera)
    return code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('--lang', required=True, choices=['es', 'en', 'fr'])
    ap.add_argument('--forbid', default='')
    ap.add_argument('--name', default=None)
    ap.add_argument('--city', default=None)
    ap.add_argument('--ig', default=None)
    ap.add_argument('--dry-run', action='store_true', help='gate y verificacion, sin deploy ni registro')
    a = ap.parse_args()

    if not os.path.exists(f'output/{a.slug}/index.html'):
        print(f'FAIL: no existe output/{a.slug}/index.html')
        sys.exit(1)

    # datos del research, si los hay
    data = {}
    ruta_data = f'output/{a.slug}/data.json'
    if os.path.exists(ruta_data):
        data = json.load(open(ruta_data, encoding='utf-8'))

    paso('1/4 GATE de calidad')
    g = correr([sys.executable, 'scripts/gate.py', a.slug, '--lang', a.lang, '--forbid', a.forbid])
    print(g.stdout.strip() or g.stderr.strip())
    if g.returncode != 0:
        print('\nABORTADO: el gate no pasa. No se deploya nada.')
        sys.exit(1)

    paso('2/4 Chequeo de duplicados en el registro')
    dd = correr([sys.executable, 'scripts/dedup_check.py'])
    print(dd.stdout.strip())
    if dd.returncode != 0:
        print('\nABORTADO: hay negocios duplicados sin resolver. Resolverlos antes de publicar.')
        sys.exit(1)

    if a.dry_run:
        print('\n--dry-run: no se deploya ni se registra.')
        return

    paso('3/4 Deploy a Cloudflare Workers')
    d = correr(['npx', 'wrangler', 'deploy', '-c', 'demos/wrangler.jsonc'])
    salida = (d.stdout or '') + (d.stderr or '')
    print('\n'.join(salida.strip().splitlines()[-6:]))
    if d.returncode != 0:
        print('\nFAIL: el deploy fallo. Nada se registra.')
        sys.exit(1)

    url = f'{BASE_DEMOS}/{a.slug}/'
    code = http_code(url)
    if code != '200':
        print(f'\nFAIL: el demo no responde 200 (HTTP {code}). NO se registra para no crear una tarjeta fantasma.')
        sys.exit(1)
    print(f'  live OK: {url}')

    paso('4/4 Registro en data/processed.json')
    registro = json.load(open(REGISTRO, encoding='utf-8'))
    idx = next((i for i, x in enumerate(registro) if x['slug'] == a.slug), None)
    if idx is not None and registro[idx].get('outreach') in ('sent', 'skip_duplicate'):
        print(f'  {a.slug} ya tiene outreach "{registro[idx]["outreach"]}": se respeta, solo se refresca la URL.')
        registro[idx]['url_demo'] = url
    else:
        fotos = data.get('fotos') or []
        entrada = {
            'slug': a.slug,
            'name': a.name or data.get('name') or a.slug,
            'city': a.city or data.get('city'),
            'ig': a.ig or data.get('ig'),
            'url_demo': url,
            'has_own_site': bool(data.get('has_own_site')),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'outreach': 'pending_manual',
            'fecha': time.strftime('%Y-%m-%d'),
            'language': a.lang,
            'status': 'staging',
        }
        if fotos:
            entrada['thumb'] = f'{url}assets/raw/{fotos[0]}'
        if idx is None:
            registro.append(entrada)
            print(f'  nuevo registro: {a.slug}')
        else:
            registro[idx] = {**registro[idx], **{k: v for k, v in entrada.items() if v is not None}}
            print(f'  registro actualizado: {a.slug}')
    json.dump(registro, open(REGISTRO, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    dd = correr([sys.executable, 'scripts/dedup_check.py'])
    print('  ' + dd.stdout.strip().splitlines()[0])
    print(f'\nPUBLICADO: {url}')
    print('Outreach: queda en pending_manual. NINGUN mensaje se envia desde aqui.')


if __name__ == '__main__':
    main()
