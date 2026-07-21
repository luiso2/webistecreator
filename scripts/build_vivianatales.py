import re

h = open('output/vivianatales/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:120]
    h = h.replace(a, b, n)

# 1. Proteger el badge Merktop
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# 2. Paleta: plum-pink (Lash Bloom) -> rosewood/terracota (Viviana Tales)
palette = [
    ('#faf2f6', '#f8efe9'),
    ('#f3e0ea', '#f0e0d8'),
    ('#33222c', '#2f2420'),
    ('#a04a72', '#8c3f52'),
    ('#c47a9c', '#b66f80'),
    ('rgba(160,74,114,0.14)', 'rgba(140,63,82,0.14)'),
    ('rgba(160,74,114,0.16)', 'rgba(140,63,82,0.16)'),
    ('rgba(160,74,114,0.32)', 'rgba(140,63,82,0.34)'),
    ('rgba(160,74,114,0.08)', 'rgba(140,63,82,0.1)'),
    ('rgba(160,74,114,0.3)', 'rgba(140,63,82,0.32)'),
    ('rgba(160,74,114,0.35)', 'rgba(140,63,82,0.37)'),
    ('rgba(160,74,114,0.7)', 'rgba(140,63,82,0.72)'),
    ('rgba(160,74,114,0.25)', 'rgba(140,63,82,0.27)'),
    ('#f2d5e3', '#f0d8ce'),
    ('#d9a8c2', '#d9b0a0'),
    ('#e5c1d4', '#e5cabb'),
    ('#c9789f 30%, #5f2c48 52%, #a04a72 75%, #b25a85', '#b66f80 30%, #4a2030 52%, #8c3f52 75%, #a35a6b'),
    ('#c47a9c 0%, #a04a72 48%, #7d3457 100%', '#b66f80 0%, #8c3f52 48%, #632a3c 100%'),
    ('#5c2140', '#421f2c'),
    ('#c47a9c, #5f2c48', '#b66f80, #4a2030'),
    ('rgba(212,168,75,0.45)', 'rgba(212,168,75,0.45)'),  # badge (no-op, protegido igual)
    ('#dc9dbe', '#c98a95'),
    ('#7d3457 0%, #a04a72 45%', '#632a3c 0%, #8c3f52 45%'),
    ('rgba(240,190,215,0.16)', 'rgba(227,176,168,0.16)'),
    ('rgba(240,190,215,0.14)', 'rgba(227,176,168,0.16)'),
    ('rgba(240,190,215,0.35)', 'rgba(227,176,168,0.37)'),
    ('rgba(240,190,215,0.7)', 'rgba(227,176,168,0.72)'),
    ('rgba(240,190,215,0.08)', 'rgba(227,176,168,0.1)'),
    ('rgba(240,190,215,0.4)', 'rgba(227,176,168,0.42)'),
    ('rgba(240,190,215,0.18)', 'rgba(227,176,168,0.2)'),
    ('#f0bed7 0%, #f8dfeb 30%, #d9a8c2 52%, #f0bed7 75%, #f2cfe0 100%',
     '#e3b0a8 0%, #f2ded9 30%, #b9808a 52%, #e3b0a8 75%, #dcbdb5 100%'),
    ('#f0bed7', '#e3b0a8'),
    ('#fbeff5 0%, #efd0e0 48%, #d3a2bc 100%', '#f7ece8 0%, #e8cfc7 48%, #c99a94 100%'),
    ('#8a5573', '#8a6055'),
    ('rgba(125,52,87,0.35)', 'rgba(120,60,60,0.35)'),
    ('rgba(125,52,87,0.4)', 'rgba(120,60,60,0.4)'),
    ('rgba(250,242,246,0.85)', 'rgba(248,239,233,0.85)'),
    ('rgba(253,246,250,0.7)', 'rgba(250,241,236,0.7)'),
    ('rgba(253,246,250,0.88)', 'rgba(250,241,236,0.88)'),
    ('#2a1722 0%, #1f0f18 100%', '#241512 0%, #180d0b 100%'),
    ('#1c0f16', '#160d0b'),
]
for a, b in palette:
    h = h.replace(a, b)

# Restaurar badge
h = h.replace('@@BADGE@@', badge_block, 1)

# 3. Globales: Booksy, IG
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/941017_viviana-tales-lash-studio_brows-lashes_15889_miami'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/vivianataleslashstudio/'
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@_lashbloom', '@vivianataleslashstudio')

open('output/vivianatales/index.html', 'w').write(h)
print('paleta + globales OK, lineas:', h.count(chr(10)))
