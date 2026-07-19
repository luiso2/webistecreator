#!/usr/bin/env python3
"""Dossier COMPLETO de un negocio de Booksy en un solo comando (segundos, no minutos).

Uso: python3 scripts/booksy_dossier.py <booksy_url> <slug>

Extrae de UNA sola descarga de la pagina:
- JSON-LD: nombre, tipo schema, direccion, geo, rating, reviewCount, TODOS los servicios
  con precio, horarios, staff (nombre+descripcion), sameAs (IG/FB), 3 reseñas con autor.
- DOM renderizado: hasta 10 reseñas verbatim + nombres de autor, duraciones de servicios.
- Telefono si esta publicado (telephone/phone/tel: link).
- Heuristica de idioma (es/en) sobre las reseñas.
- Candidatos a website propio (sameAs no-social; el agente confirma con 1 busqueda).

Escribe output/<slug>/data.json y luego corre booksy_gallery.py (fotos + contact sheet).
El agente construye DIRECTO desde data.json: cero rondas de WebFetch para menu/reviews.
"""
import html
import json
import os
import re
import subprocess
import sys

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
SOCIAL = ('facebook.com', 'instagram.com', 'booksy.com', 'tiktok.com', 'youtube.com', 'twitter.com', 'x.com')


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    url, slug = sys.argv[1], sys.argv[2]
    os.makedirs(f'output/{slug}', exist_ok=True)
    page = subprocess.run(['curl', '-s', '--max-time', '30', '-H', f'User-Agent: {UA}', url],
                          capture_output=True, text=True).stdout
    if len(page) < 5000:
        print('ERROR: pagina vacia o bloqueada, len', len(page))
        sys.exit(1)

    d = {'booksy_url': url, 'slug': slug}

    ld = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, flags=re.S):
        try:
            j = json.loads(m.group(1))
            if isinstance(j, dict) and j.get('makesOffer') is not None:
                ld = j
                break
        except Exception:
            continue
    if not ld:
        print('ERROR: no se encontro JSON-LD con makesOffer. Booksy pudo renombrar el negocio')
        print('(la URL vieja redirige al LISTADO: verificar el nombre y buscar la URL nueva).')
        sys.exit(1)

    d['name'] = ld.get('name')
    d['schema_type'] = ld.get('@type')
    d['address'] = ld.get('address', {})
    d['geo'] = ld.get('geo')
    agg = ld.get('aggregateRating', {})
    d['rating'] = round(float(agg.get('ratingValue', 0)), 1)
    d['reviews_count'] = agg.get('reviewCount')
    d['hours'] = ld.get('openingHoursSpecification')
    d['staff'] = [{'name': e.get('name'), 'description': e.get('description')}
                  for e in ld.get('employee', [])]
    d['same_as'] = ld.get('sameAs', [])
    d['instagram'] = next((u.rstrip('/').split('/')[-1] for u in d['same_as'] if 'instagram.com' in u), None)
    if not d['instagram']:
        # Booksy a veces publica el handle pelado como sameAs ("https://Yulipach")
        for u in d['same_as']:
            tail = re.sub(r'^https?://', '', u).strip('/')
            if '.' not in tail and re.match(r'^[A-Za-z0-9_.]{2,30}$', tail):
                d['instagram'] = tail
                break
    d['website_candidates'] = [u for u in d['same_as']
                               if not any(s in u for s in SOCIAL)
                               and '.' in re.sub(r'^https?://', '', u).split('/')[0]]

    # telefono (varias fuentes)
    tel = ld.get('telephone')
    if not tel:
        m = re.search(r'href="tel:([^"]+)"', page) or re.search(r'"(?:telephone|phone)"\s*:\s*"([^"]{7,20})"', page)
        tel = m.group(1) if m else None
    d['phone'] = tel

    # duraciones: filas renderizadas "$precio|duracion", emparejadas con la oferta por precio/orden
    dom = html.unescape(page)
    rows = re.findall(r'\$([\d,]+(?:\.\d\d)?)\s*\+?\s*(?:</[^>]*>|<[^>]*>|\s){0,8}(\d+h(?:\s?\d+min)?|\d+\s?min)\b', dom)
    dur_por_precio = {}
    for precio, dur in rows:
        p = precio.replace(',', '')
        dur_por_precio.setdefault(p.split('.')[0], dur)
    servicios = []
    for o in ld.get('makesOffer', []):
        precio = o.get('price')
        servicios.append({'name': o.get('name'), 'price': precio,
                          'duration': dur_por_precio.get(str(precio))})
    d['services'] = servicios

    # reseñas: 3 del LD (autor + body) + hasta 10 bodies renderizados con nombres del payload
    revs = []
    for r in ld.get('review', []):
        revs.append({'author': (r.get('author') or {}).get('name'),
                     'body': r.get('reviewBody'), 'rating': (r.get('reviewRating') or {}).get('ratingValue')})
    bodies = re.findall(r'<div class="text-gray-900"><span>([^<]{4,400})</span>', page)
    nombres = re.findall(r'"([A-Za-z][A-Za-z .\'-]{1,24})","([A-Z])…"', page)
    ya = {r['body'] for r in revs}
    for i, b in enumerate([html.unescape(x) for x in bodies]):
        if b in ya:
            continue
        autor = f'{nombres[i][0]}' if i < len(nombres) else None
        revs.append({'author': autor, 'body': b, 'rating': None})
    d['reviews'] = revs[:12]

    # idioma predominante (heuristica sobre reseñas)
    texto = ' '.join(r['body'] or '' for r in revs).lower()
    es_hits = sum(texto.count(w) for w in [' el ', ' la ', ' que ', ' muy ', ' mejor', ' uñas', ' trabajo', ' excelente', ' gracias'])
    en_hits = sum(texto.count(w) for w in [' the ', ' and ', ' best', ' great', ' always', ' love', ' amazing', ' service'])
    d['language'] = 'es' if es_hits > en_hits else 'en'

    out = f'output/{slug}/data.json'
    json.dump(d, open(out, 'w'), indent=1, ensure_ascii=False)
    print(f'dossier: {out}')
    print(f"  {d['name']} ({d['schema_type']}) | {d['rating']} x {d['reviews_count']} | tel: {d['phone']} | ig: @{d['instagram']} | lang: {d['language']}")
    print(f"  servicios: {len(servicios)} (con duracion: {sum(1 for s in servicios if s['duration'])}) | reseñas: {len(d['reviews'])} | staff: {len(d['staff'])}")
    if d['website_candidates']:
        print(f"  POSIBLE WEBSITE PROPIO: {d['website_candidates']} (verificar: cambia el angulo)")

    # fotos + contact sheet
    subprocess.run([sys.executable, 'scripts/booksy_gallery.py', url, slug], check=False)


if __name__ == '__main__':
    main()
