#!/usr/bin/env python3
"""Dossier de un negocio de GlossGenius (subdominio <slug>.glossgenius.com).

Uso: python3 scripts/glossgenius_dossier.py <glossgenius_url> <slug>

GlossGenius embebe TODO en __NEXT_DATA__ (props.serverContext.publicUser): nombre,
telefono, email, direccion, IG, website propio, "about", y servicios con precio,
duracion e IMAGEN. Extrae eso a output/<slug>/data.json, descarga las fotos de servicio
+ cover como galeria (static.glossgenius.com) y genera el contact sheet.

OJO: GlossGenius NO expone reseñas verbatim en el payload (estan en Google via
`review_with_google_url`). El campo d['reviews'] queda vacio; conseguir reseñas reales
es paso aparte (busqueda Google) y NUNCA se inventan. Si `website_url` existe -> has_own_site.
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
SOCIAL = ('facebook.com', 'instagram.com', 'glossgenius.com', 'tiktok.com', 'twitter.com', 'x.com', 'yelp.com', 'youtube.com')


def curl(url, out=None, timeout=30):
    cmd = ['curl', '-sL', '--max-time', str(timeout), '-H', f'User-Agent: {UA}', url]
    if out:
        cmd += ['-o', out]
        return subprocess.run(cmd, capture_output=True).returncode == 0
    return subprocess.run(cmd, capture_output=True, text=True).stdout


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
        print('ERROR: no __NEXT_DATA__ (GlossGenius cambio de estructura o URL invalida)')
        sys.exit(1)
    try:
        pu = json.loads(m.group(1))['props']['serverContext']['publicUser']
    except Exception as e:
        print('ERROR parseando publicUser:', e)
        sys.exit(1)

    d = {'source': 'glossgenius', 'url': url, 'slug': slug}
    d['name'] = pu.get('business_name')
    d['phone'] = pu.get('business_phone') or pu.get('phone')
    d['email'] = pu.get('business_email')
    d['address_raw'] = pu.get('business_address')
    d['about'] = (pu.get('about') or '').strip()
    ig = pu.get('instagram_url') or ''
    m2 = re.search(r'instagram\.com/([A-Za-z0-9_.]+)', ig)
    d['instagram'] = m2.group(1) if m2 else (ig if re.match(r'^[A-Za-z0-9_.]{2,30}$', ig) else None)
    web = (pu.get('website_url') or '').strip()
    d['website'] = web or None
    d['has_own_site'] = bool(web and not any(s in web for s in SOCIAL))

    users = pu.get('users') or [{}]
    svcs = users[0].get('services') or []
    servicios, img_urls = [], []
    for s in svcs:
        dur = s.get('total_duration') or s.get('start_duration')
        servicios.append({
            'name': (s.get('name') or '').replace('—', ': ').strip(),
            'price': s.get('price'),
            'duration_min': dur,
        })
        if s.get('image'):
            img_urls.append(s['image'])
    d['services'] = servicios
    d['reviews'] = []  # GlossGenius no expone reseñas verbatim (estan en Google)

    # fotos: cover + imagenes de servicio (dedupe)
    fotos = []
    for k in ('cover_image_original', 'cover_image_medium'):
        if pu.get(k):
            fotos.append(pu[k])
            break
    seen = set()
    for u in img_urls:
        base = u.split('/')[-1].split('.')[0]
        if base not in seen:
            seen.add(base)
            fotos.append(u)
    ok = 0
    for i, u in enumerate(fotos[:16], 1):
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

    json.dump(d, open(f'output/{slug}/data.json', 'w'), indent=1, ensure_ascii=False)
    print(f'dossier: output/{slug}/data.json')
    print(f"  {d['name']} | tel: {d['phone']} | email: {d['email']} | ig: @{d['instagram']} | addr: {d['address_raw']}")
    print(f"  servicios: {len(servicios)} | fotos validas: {ok} | reseñas: 0 (GlossGenius no expone verbatim, buscar en Google)")
    if d['has_own_site']:
        print(f"  YA TIENE WEBSITE PROPIO: {web} (angulo rediseño o SKIP)")

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
