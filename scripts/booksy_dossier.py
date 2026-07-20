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

    # Buscar el LocalBusiness en CUALQUIER forma de JSON-LD: dict suelto, array,
    # o dentro de "@graph" (variantes muy comunes). No exigir makesOffer para no dar
    # un falso "negocio renombrado" cuando el nodo esta anidado.
    def es_negocio(x):
        if not isinstance(x, dict):
            return False
        t = x.get('@type', '')
        t = ' '.join(t) if isinstance(t, list) else str(t)
        return bool(x.get('makesOffer')) or bool(x.get('aggregateRating')) or \
            any(k in t for k in ('Salon', 'Barbershop', 'BeautySalon', 'HairSalon', 'NailSalon',
                                 'DaySpa', 'HealthAndBeauty', 'LocalBusiness'))

    def buscar_negocio(obj):
        if isinstance(obj, dict):
            if es_negocio(obj):
                return obj
            if isinstance(obj.get('@graph'), list):
                for x in obj['@graph']:
                    r = buscar_negocio(x)
                    if r:
                        return r
        elif isinstance(obj, list):
            for x in obj:
                r = buscar_negocio(x)
                if r:
                    return r
        return None

    ld = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, flags=re.S):
        try:
            ld = buscar_negocio(json.loads(m.group(1)))
        except Exception:
            ld = None
        if ld:
            break
    if not ld:
        print('ERROR: no se encontro el negocio en el JSON-LD. Booksy pudo renombrar el negocio')
        print('(la URL vieja redirige al LISTADO: verificar el nombre y buscar la URL nueva).')
        sys.exit(1)

    def num(v):
        if v is None:
            return None
        try:
            return float(str(v).replace(',', '.'))
        except (TypeError, ValueError):
            return None

    d['name'] = ld.get('name')
    d['schema_type'] = ld.get('@type')
    d['address'] = ld.get('address', {})
    d['geo'] = ld.get('geo')
    agg = ld.get('aggregateRating') or {}
    rv = num(agg.get('ratingValue'))
    d['rating'] = round(rv, 1) if rv is not None else None  # None, NUNCA 0.0 fabricado
    d['reviews_count'] = agg.get('reviewCount')
    d['hours'] = ld.get('openingHoursSpecification')
    d['staff'] = [{'name': e.get('name'), 'description': e.get('description')}
                  for e in ld.get('employee', [])]
    d['same_as'] = ld.get('sameAs', [])

    def ig_handle(u):
        m = re.search(r'instagram\.com/([A-Za-z0-9_.]{2,30})', u)
        return m.group(1) if m else None
    d['instagram'] = next((h for h in (ig_handle(u) for u in d['same_as'] if 'instagram.com' in u) if h), None)
    if not d['instagram']:
        # Booksy a veces publica el handle pelado como sameAs ("https://Yulipach")
        for u in d['same_as']:
            tail = re.sub(r'^https?://', '', u).strip('/').split('/')[0].split('?')[0]
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

    # Duraciones: emparejar precio->duracion SOLO cuando es inequivoco. Si dos servicios
    # comparten precio con duraciones distintas, no adivinar (duration=None): atribuir la
    # duracion equivocada a un servicio es un dato falso. Precios normalizados a entero.
    dom = html.unescape(page)
    rows = re.findall(r'\$([\d,]+(?:\.\d\d)?)\s*\+?\s*(?:<[^>]*>|\s){0,4}(\d+h(?:\s?\d+min)?|\d+\s?min)\b', dom)

    def pkey(v):
        n = num(v)
        return str(int(round(n))) if n is not None else None
    dur_por_precio = {}
    for precio, dur in rows:
        k = pkey(precio)
        if k is None:
            continue
        dur_por_precio.setdefault(k, set()).add(dur.strip())
    servicios = []
    for o in ld.get('makesOffer', []):
        k = pkey(o.get('price'))
        durs = dur_por_precio.get(k)
        servicios.append({'name': o.get('name'), 'price': o.get('price'),
                          'duration': next(iter(durs)) if durs and len(durs) == 1 else None})
    d['services'] = servicios

    # Reseñas. FUENTE CONFIABLE: el array `review` del JSON-LD empareja autor+body dentro
    # del mismo objeto (correcto por construccion). Es lo que usa la plantilla (3 quotes).
    # Los bodies del DOM se agregan SOLO como material extra y SIN autor: emparejar un nombre
    # por indice entre dos regexes distintos misatribuye en silencio si un conteo diverge,
    # y misatribuir una reseña viola "nunca inventar datos". author=None es preferible.
    # em-dash (U+2014) prohibido en el output; en reseñas verbatim se sustituye por ": "
    # (decision del proyecto, mantiene el sentido y deja el gate en 0). norm = clave de dedup
    # tolerante a espacios/entidades para no duplicar la misma reseña del LD y del DOM.
    def clean_txt(s):
        return (s or '').replace('—', ': ').strip()

    def norm(s):
        return ' '.join((s or '').lower().split())
    revs = []
    ya = set()
    for r in ld.get('review', []):
        body = clean_txt(r.get('reviewBody'))
        revs.append({'author': (r.get('author') or {}).get('name'),
                     'body': body, 'rating': (r.get('reviewRating') or {}).get('ratingValue'),
                     'author_verified': True})
        ya.add(norm(body))
    for raw in re.findall(r'<div class="text-gray-900"><span>([^<]{4,400})</span>', page):
        body = clean_txt(html.unescape(raw))
        if body and norm(body) not in ya:
            ya.add(norm(body))
            revs.append({'author': None, 'body': body, 'rating': None, 'author_verified': False})
    d['reviews'] = revs[:12]
    d['named_reviews'] = [r for r in revs if r['author_verified']]
    # em-dash fuera tambien de nombres de servicio y staff (van al HTML del site)
    for s in d['services']:
        if s.get('name'):
            s['name'] = clean_txt(s['name'])
    for st in d['staff']:
        if st.get('description'):
            st['description'] = clean_txt(st['description'])

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
