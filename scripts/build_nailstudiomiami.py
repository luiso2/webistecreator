import re

h = open('output/nailstudiomiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:120]
    h = h.replace(a, b, n)

# 1. Proteger el badge Merktop (contiene rgba(212,168,75,...) que debe seguir dorado)
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# 2. Paleta: dorado (Pure Artistry) -> zafiro (The Nail Studio Miami)
palette = [
    ('#0f0b07', '#0a0e15'),
    ('#171207', '#0f1520'),
    ('#d4a84b', '#4a72ad'),
    ('#b8934a', '#3d5d8f'),
    ('#241c0e', '#161f2e'),
    ('rgba(212,168,75,0.16)', 'rgba(74,114,173,0.18)'),
    ('rgba(212,168,75,0.2)', 'rgba(74,114,173,0.22)'),
    ('rgba(122,90,30,0.28)', 'rgba(38,62,102,0.3)'),
    ('rgba(180,140,60,0.18)', 'rgba(96,138,190,0.2)'),
    ('rgba(212,168,75,0.35)', 'rgba(120,160,210,0.4)'),
    ('rgba(212,168,75,0.32)', 'rgba(120,160,210,0.36)'),
    ('rgba(212,168,75,0.08)', 'rgba(74,114,173,0.1)'),
    ('rgba(212,168,75,0.14)', 'rgba(74,114,173,0.16)'),
    ('rgba(212,168,75,0.25)', 'rgba(120,160,210,0.28)'),
    ('rgba(212,168,75,0.45)', 'rgba(140,175,220,0.5)'),
    ('rgba(212,168,75,0.7)', 'rgba(140,175,220,0.75)'),
    ('#d4a84b 0%, #f0dc9e 30%, #9a7431 52%, #d4a84b 75%, #e5c374 100%',
     '#5a86c4 0%, #a8c4e8 30%, #2f4a73 52%, #5a86c4 75%, #7fa8d9 100%'),
    ('#e8c476 0%, #c9a04a 48%, #96742c 100%', '#8fb3e0 0%, #4a72ad 48%, #2a3f60 100%'),
    ('#6b5222', '#1c2b47'),
    ('#e5c374, #9a7431', '#8fb3e0, #2f4a73'),
    ('#d4a84b', '#4a72ad'),  # any remaining literal accent (stars, step-num fallback)
    ('#96742c 0%, #d4a84b 45%, #f0dc9e 100%', '#2a3f60 0%, #4a72ad 45%, #a8c4e8 100%'),
    ('rgba(232,207,150,0.16)', 'rgba(140,175,220,0.18)'),
    ('rgba(185,138,128,0.14)', 'rgba(100,130,175,0.14)'),
    ('#e8cf96 0%, #f8eed3 30%, #bfa060 52%, #e8cf96 75%, #f0dcae 100%',
     '#a8c4e8 0%, #e2edf9 30%, #6f92c0 52%, #a8c4e8 75%, #bcd6f0 100%'),
    ('#faf1dc 0%, #ecd9a8 48%, #c9ab6b 100%', '#eef3fb 0%, #c3d7ef 48%, #82a5d0 100%'),
    ('#8a744a', '#4d6f9e'),
    ('rgba(110,85,35,0.35)', 'rgba(60,90,140,0.35)'),
    ('rgba(110,85,35,0.4)', 'rgba(60,90,140,0.4)'),
    ('rgba(232,207,150,0.35)', 'rgba(140,175,220,0.4)'),
    ('rgba(232,207,150,0.7)', 'rgba(140,175,220,0.75)'),
    ('rgba(232,207,150,0.08)', 'rgba(140,175,220,0.1)'),
    ('rgba(232,207,150,0.18)', 'rgba(140,175,220,0.2)'),
    ('#e9c3ab', '#a8c4e8'),
    ('rgba(232,207,150,0.4)', 'rgba(140,175,220,0.45)'),
    ('rgba(212,168,75,0.16) 0%, rgba(212,168,75,0.08) 42%', 'rgba(140,175,220,0.16) 0%, rgba(74,114,173,0.1) 42%'),
    ('rgba(232,207,150,0.14) 0%, rgba(212,168,75,0.08) 42%', 'rgba(140,175,220,0.16) 0%, rgba(74,114,173,0.1) 42%'),
    ('rgba(232,207,150,0.09)', 'rgba(140,175,220,0.1)'),
    ('rgba(15,11,7,0.85)', 'rgba(10,14,21,0.85)'),
]
for a, b in palette:
    h = h.replace(a, b)

# Restaurar badge dorado
h = h.replace('@@BADGE@@', badge_block, 1)

# 3. Globales: Booksy, IG
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/418314_the-nail-studio-miami_nail-salon_15889_miami'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/thenailstudiomiami/'
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@pure.artistrysk', '@thenailstudiomiami')

open('output/nailstudiomiami/index.html', 'w').write(h)
print('paleta + globales OK, lineas:', h.count(chr(10)))
