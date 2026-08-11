#!/usr/bin/env python3
"""Escaneo rapido (sin descargar fotos) de un candidato Booksy: rating, reviews, website propio.
Uso: python3 scripts/_scan_candidate.py <booksy_url>
Imprime una linea JSON con {url, name, rating, reviews_count, website_candidates, address, phone, category}
"""
import json
import re
import subprocess
import sys

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
SOCIAL = ('facebook.com', 'instagram.com', 'booksy.com', 'tiktok.com', 'youtube.com', 'twitter.com', 'x.com')


def main():
    url = sys.argv[1]
    try:
        page = subprocess.run(['curl', '-s', '--max-time', '20', '-H', f'User-Agent: {UA}', url],
                              capture_output=True, text=True, timeout=25).stdout
    except Exception as e:
        print(json.dumps({'url': url, 'error': str(e)}))
        return
    if len(page) < 5000:
        print(json.dumps({'url': url, 'error': 'empty_or_blocked'}))
        return

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
        print(json.dumps({'url': url, 'error': 'no_ld'}))
        return

    def num(v):
        if v is None:
            return None
        try:
            return float(str(v).replace(',', '.'))
        except (TypeError, ValueError):
            return None

    agg = ld.get('aggregateRating') or {}
    rv = num(agg.get('ratingValue'))
    same_as = ld.get('sameAs', [])
    website_candidates = [u for u in same_as
                          if not any(s in u for s in SOCIAL)
                          and '.' in re.sub(r'^https?://', '', u).split('/')[0]]
    tel = ld.get('telephone')
    if not tel:
        m = re.search(r'href="tel:([^"]+)"', page)
        tel = m.group(1) if m else None
    out = {
        'url': url,
        'name': ld.get('name'),
        'rating': round(rv, 1) if rv is not None else None,
        'reviews_count': agg.get('reviewCount'),
        'website_candidates': website_candidates,
        'address': ld.get('address'),
        'phone': tel,
        'schema_type': ld.get('@type'),
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    main()
