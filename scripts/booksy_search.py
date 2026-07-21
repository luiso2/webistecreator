#!/usr/bin/env python3
"""Enumera TODOS los negocios de Booksy por categoria + ciudad (para descubrir candidatos sin website).

Uso:
  python3 scripts/booksy_search.py                 # corre la matriz por defecto (categorias x ciudades de Miami)
  python3 scripts/booksy_search.py nail-salon 15889 miami   # una sola categoria+ciudad

Salida: agrega las URLs de negocio (deduplicadas por Booksy ID) a data/booksy_candidates.txt.
Las paginas de categoria de Booksy son SPAs: se renderizan con Playwright (mismo venv .venv-pw que
ig_photos), se scrollea para cargar mas resultados, y se extraen los links /en-us/<id>_<slug>_...
NO llama a Instagram (no hay rate-limit). El dossier real (booksy_dossier.py) valida despues
has_own_site/rating por cada negocio; este script solo DESCUBRE la lista completa.
"""
import os
import re
import subprocess
import sys

VENV_PY = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.venv-pw', 'bin', 'python'))
CAND_PATH = 'data/booksy_candidates.txt'

# Matriz por defecto: categorias x ciudades del area de Miami (id_slug de Booksy).
CATEGORIES = ['nail-salon', 'hair-salon', 'barber-shop', 'brows-lashes', 'eyelash-extensions',
              'skin-care', 'makeup', 'hair-removal', 'wellness-day-spa', 'microblading']
# Por ahora: area de Miami + area de Tampa (Florida).
CITIES = [('15889', 'miami'), ('15886', 'hialeah'), ('122701', 'doral'), ('15890', 'miami-beach'),
          ('15891', 'miami-gardens'), ('122705', 'miami-lakes'), ('15892', 'north-miami-beach'),
          ('122715', 'south-miami'), ('122695', 'west-miami'),
          ('15761', 'tampa'), ('131663', 'new-tampa'), ('119797', 'st-petersburg'), ('15980', 'clearwater')]

_DRIVER = r'''
import sys, json
from playwright.sync_api import sync_playwright
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
cat, cid, cslug = sys.argv[1], sys.argv[2], sys.argv[3]
url = f'https://booksy.com/en-us/s/{cat}/{cid}_{cslug}'
found = {}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--no-sandbox'])
    pg = b.new_page(user_agent=UA, viewport={'width':1280,'height':2200})
    try:
        pg.goto(url, wait_until='domcontentloaded', timeout=45000)
        pg.wait_for_timeout(3500)
        # scroll para cargar mas negocios (lazy list); recolectar en cada paso
        for _ in range(14):
            links = pg.evaluate("() => [...document.querySelectorAll('a')].map(a=>a.getAttribute('href')||'').filter(h=>/\\/en-us\\/\\d+_/.test(h))")
            for h in links:
                m = __import__('re').search(r'/en-us/(\d+)_([a-z0-9-]+)_([a-z-]+)_(\d+)_([a-z-]+)', h)
                if m:
                    found[m.group(1)] = f"https://booksy.com/en-us/{m.group(1)}_{m.group(2)}_{m.group(3)}_{m.group(4)}_{m.group(5)}"
            pg.mouse.wheel(0, 2600); pg.wait_for_timeout(1100)
    except Exception as e:
        print('ERR ' + str(e)[:120], file=sys.stderr)
    b.close()
print(json.dumps(list(found.values())))
'''


def scrape(cat, cid, cslug):
    driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_booksy_search_driver.py')
    with open(driver, 'w') as f:
        f.write(_DRIVER)
    out = subprocess.run([VENV_PY, driver, cat, cid, cslug], capture_output=True, text=True, timeout=180)
    try:
        import json
        return json.loads(out.stdout.strip().splitlines()[-1])
    except Exception:
        sys.stderr.write(out.stderr[-300:] + '\n')
        return []


def main():
    combos = [(sys.argv[1], sys.argv[2], sys.argv[3])] if len(sys.argv) >= 4 else [(c, cid, cs) for c in CATEGORIES for (cid, cs) in CITIES]
    seen = set()
    if os.path.exists(CAND_PATH):
        for line in open(CAND_PATH):
            m = re.search(r'/en-us/(\d+)_', line)
            if m:
                seen.add(m.group(1))
    total_new = 0
    with open(CAND_PATH, 'a') as out:
        for cat, cid, cslug in combos:
            urls = scrape(cat, cid, cslug)
            new = [u for u in urls if re.search(r'/en-us/(\d+)_', u).group(1) not in seen]
            for u in new:
                seen.add(re.search(r'/en-us/(\d+)_', u).group(1))
                out.write(u + '\n')
            out.flush()
            total_new += len(new)
            print(f'  {cat} @ {cslug}: {len(urls)} vistos, {len(new)} nuevos (acum {len(seen)})', flush=True)
    print(f'TOTAL nuevos agregados: {total_new} | total unicos en {CAND_PATH}: {len(seen)}')


if __name__ == '__main__':
    main()
