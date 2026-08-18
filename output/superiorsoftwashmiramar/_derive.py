import re

h = open('output/superiorsoftwashmiramar/index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f'NO (found {c}, need {n}): {a[:90]}'
    h = h.replace(a, b, n)


def rep_all(a, b):
    global h
    c = h.count(a)
    assert c > 0, 'NO (0 matches): ' + a[:90]
    h = h.replace(a, b)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de repintar la paleta
# ---------------------------------------------------------------------------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque merktop-badge'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lash bloom) -> aqua/teal soft-wash
# ---------------------------------------------------------------------------
HEX_PAIRS = [
    ('a04a72', '1f6b73'),
    ('c47a9c', '4fb3bd'),
    ('c9789f', '57b8c2'),
    ('5f2c48', '123a40'),
    ('b25a85', '2f8891'),
    ('7d3457', '184f57'),
    ('5c2140', '0f2e33'),
    ('f2d5e3', 'd7f0f1'),
    ('d9a8c2', 'a9dde2'),
    ('e5c1d4', 'c8e9ec'),
    ('f0bed7', '8fe3ea'),
    ('f8dfeb', 'd7f5f7'),
    ('f2cfe0', 'bdeef1'),
    ('fbeff5', 'eafbfb'),
    ('efd0e0', 'bdeaec'),
    ('d3a2bc', '7dd3da'),
    ('8a5573', '1c5d64'),
    ('dc9dbe', '79d6de'),
    ('fbf3f8', 'eafbfc'),
    ('33222c', '1b2c2e'),
    ('faf2f6', 'f3fafa'),
    ('f3e0ea', 'e3f3f4'),
    ('f6f1ea', 'eef7f6'),
    ('2a1722', '12282a'),
    ('1f0f18', '0b1e20'),
    ('1c0f16', '0b1e20'),
]
for old, new in HEX_PAIRS:
    c = h.count('#' + old)
    assert c > 0, 'hex no encontrado: #' + old
    h = h.replace('#' + old, '#' + new)

RGB_TRIPLE_PAIRS = [
    ('160,74,114', '31,107,115'),
    ('51,34,44', '27,44,46'),
    ('240,190,215', '143,227,234'),
    ('233,205,186', '143,227,234'),
    ('185,138,128', '58,138,148'),
    ('70,25,50', '10,45,50'),
    ('125,52,87', '24,79,87'),
    ('40,16,30', '11,30,32'),
    ('253,246,250', '244,251,251'),
    ('250,242,246', '243,250,250'),
]
for old, new in RGB_TRIPLE_PAIRS:
    c = h.count(old)
    assert c > 0, 'rgb no encontrado: ' + old
    h = h.replace(old, new)

# Restaurar el badge Merktop (siempre dorado)
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

print('OK: paso 1-2 paleta+badge')
open('output/superiorsoftwashmiramar/index.html', 'w', encoding='utf-8').write(h)
