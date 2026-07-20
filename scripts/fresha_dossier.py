#!/usr/bin/env python3
"""Dossier de un negocio de Fresha (fresha.com/a/<slug>).

Uso: python3 scripts/fresha_dossier.py <fresha_url> <slug>

Fresha embebe TODO en __NEXT_DATA__ (props.pageProps.data.location): nombre, rating,
reviewsCount, telefono (contactNumber), direccion, servicios (con precio y duracion),
reseñas VERBATIM (reviews.edges) y galeria (images.fresha.com). Extrae a data.json,
descarga fotos + contact sheet. OJO: la galeria publica de Fresha suele ser pequeña
(3-6 fotos); si <5 reales, curar/complementar o marcar failed. NUNCA inventar datos.
"""
import html
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


def curl(url, out=None, timeout=30):
    cmd = ['curl', '-sL', '--max-time', str(timeout), '-H', f'User-Agent: {UA}', url]
    if out:
        cmd += ['-o', out]
        return subprocess.run(cmd, capture_output=True).returncode == 0
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def dur_from_caption(cap):
    # "2 hr - 2 hr, 30 min" -> "2h" ; "45 min" -> "45min"
    if not cap:
        return None
    first = cap.split('-')[0].strip()
    h_ = re.search(r'(\d+)\s*hr', first)
    mn = re.search(r'(\d+)\s*min', first)
    parts = []
    if h_:
        parts.append(f'{h_.group(1)}h')
    if mn:
        parts.append(f'{mn.group(1)}min')
    return ' '.join(parts) or None


def clean(s):
    return (s or '').replace('—', ': ').strip()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    url, slug = sys.argv[1], sys.argv[2]
    d_dir = f'output/{slug}/assets/raw'
    os.makedirs(d_dir, exist_ok=True)
    page = curl(url)
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', page, flags=re.S)
    if not m:
        print('ERROR: no __NEXT_DATA__ (Fresha cambio de estructura o URL invalida)')
        sys.exit(1)
    try:
        data = json.loads(m.group(1))['props']['pageProps']['data']
        loc = data['location']
    except Exception as e:
        print('ERROR parseando location:', e)
        sys.exit(1)

    d = {'source': 'fresha', 'url': url, 'slug': slug}
    d['name'] = clean(loc.get('name'))
    rating = loc.get('rating')
    d['rating'] = round(float(rating), 1) if rating not in (None, 0) else None
    d['reviews_count'] = loc.get('reviewsCount')
    d['phone'] = loc.get('contactNumber')
    d['email'] = loc.get('email')
    # direccion desde directionsUrl (URL-encoded)
    addr = None
    a = loc.get('address')
    if isinstance(a, dict):
        du = a.get('directionsUrl') or ''
        m2 = re.search(r'daddr=([^&]+)', du)
        if m2:
            from urllib.parse import unquote
            addr = unquote(m2.group(1)).strip()
    d['address_raw'] = addr
    d['biz_type'] = (loc.get('primaryBusinessType') or {}).get('name')

    # servicios
    servicios = []
    for g in loc.get('services', []):
        for it in (g.get('items') or []):
            servicios.append({
                'name': clean(it.get('name')),
                'price': it.get('formattedRetailPrice') or (f"${it.get('retailPrice')}" if it.get('retailPrice') else None),
                'duration': dur_from_caption(it.get('caption')),
                'group': g.get('name'),
            })
    d['services'] = servicios

    # reseñas verbatim
    revs = []
    rv = loc.get('reviews') or {}
    for e in (rv.get('edges') or []):
        node = e.get('node') or {}
        body = clean(node.get('comment') or node.get('text') or node.get('reviewText'))
        author = node.get('customerName') or node.get('authorName') or (node.get('customer') or {}).get('firstName')
        if body:
            revs.append({'author': author, 'body': body, 'rating': node.get('rating'), 'author_verified': bool(author)})
    d['reviews'] = revs[:12]
    d['named_reviews'] = [r for r in revs if r['author_verified']]

    # fotos
    fotos = []
    cov = loc.get('coverImage')
    if isinstance(cov, dict) and cov.get('url'):
        fotos.append(cov['url'])
    for k in ('portfolioGallery', 'galleryModalDesktopLargeImages', 'galleryDesktopLargeImages', 'venueSnippetImages'):
        for v in (loc.get(k) or []):
            u = v if isinstance(v, str) else (v.get('url') or v.get('src') if isinstance(v, dict) else None)
            if u:
                fotos.append(u)
    seen, uniq = set(), []
    for u in fotos:
        base = u.split('/')[-1].split('?')[0]
        if base not in seen:
            seen.add(base)
            uniq.append(u)
    ok = 0
    for i, u in enumerate(uniq[:16], 1):
        p = f'{d_dir}/bk-{i}.jpg'
        curl(html.unescape(u), out=p, timeout=25)
        try:
            Image.open(p).verify()
            im = Image.open(p).convert('RGB')
            im.thumbnail((1300, 1300))
            im.save(p, 'JPEG', quality=84)
            ok += 1
        except Exception:
            if os.path.exists(p):
                os.remove(p)

    texto = ' '.join((r['body'] or '') for r in revs).lower()
    es = sum(texto.count(w) for w in [' el ', ' la ', ' que ', ' muy ', ' uñas', ' gracias', ' excelente', ' mejor'])
    en = sum(texto.count(w) for w in [' the ', ' and ', ' best', ' great', ' love', ' amazing', ' she '])
    d['language'] = 'es' if es > en else 'en'

    json.dump(d, open(f'output/{slug}/data.json', 'w'), indent=1, ensure_ascii=False)
    print(f'dossier: output/{slug}/data.json')
    print(f"  {d['name']} ({d['biz_type']}) | {d['rating']} x {d['reviews_count']} | tel: {d['phone']} | lang: {d['language']}")
    print(f"  servicios: {len(servicios)} | reseñas con autor: {len(d['named_reviews'])} | fotos validas: {ok} | addr: {d['address_raw']}")
    if ok < 5:
        print(f"  AVISO: solo {ok} fotos (Fresha limita la galeria publica); curar o complementar.")

    files = sorted(f for f in os.listdir(d_dir) if f.endswith('.jpg'))
    if files:
        cols, tw, th, label = 7, 150, 190, 16
        rows = (len(files) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * 154 + 4, rows * (th + label + 4) + 4), 'white')
        dr = ImageDraw.Draw(sheet)
        for idx, f in enumerate(files):
            im = Image.open(f'{d_dir}/{f}').convert('RGB')
            im.thumbnail((tw, th))
            x = 4 + (idx % cols) * 154
            y = 4 + (idx // cols) * (th + label + 4)
            sheet.paste(im, (x, y))
            dr.text((x, y + th + 2), f, fill='black')
        sheet.save(f'output/{slug}/_sheet.jpg', quality=80)
        print(f'contact sheet: output/{slug}/_sheet.jpg')


if __name__ == '__main__':
    main()
