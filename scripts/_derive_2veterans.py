import re

SLUG = 'output/2-veterans-handyman-service/index.html'
h = open(SLUG, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    cnt = h.count(a)
    assert cnt >= n, f'NO (found {cnt}, need {n}): {a[:90]!r}'
    h = h.replace(a, b, n)

def rep_all(a, b, expect=None):
    global h
    cnt = h.count(a)
    if expect is not None:
        assert cnt == expect, f'expected {expect}, found {cnt}: {a[:90]!r}'
    else:
        assert cnt > 0, f'NO: {a[:90]!r}'
    h = h.replace(a, b)

# ---------- 1. Protect the Merktop badge block ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'merktop badge block not found'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ---------- 2. Palette: gold -> forest green ----------
PALETTE = [
    ('#0f0b07', '#0a120d'),   # bg
    ('#171207', '#0f1b15'),   # bg-2
    ('rgba(245,239,227,', 'rgba(238,247,241,'),  # ink alpha base (ink-60/40 use this prefix)
    ('#f5efe3', '#eef5f0'),   # ink solid
    ('#d4a84b', '#3f9867'),   # accent-deep
    ('#b8934a', '#2f7d55'),   # accent-mid
    ('#241c0e', '#0f2017'),   # accent-soft
    ('rgba(212,168,75,', 'rgba(63,152,103,'),  # accent-deep alpha (ghost, borders, glows) -- badge protected already
    ('rgba(122,90,30,0.28)', 'rgba(31,92,60,0.28)'),  # orb-b
    ('rgba(180,140,60,0.18)', 'rgba(90,170,120,0.18)'),  # orb-c
    ('#f0dc9e', '#bfe8cf'),   # text-shine light stop / scroll-progress end
    ('#9a7431', '#1f5c3c'),   # text-shine dark stop / step-num dark stop
    ('#e5c374', '#7fd1a0'),   # text-shine stop / step-num light stop
    ('#e8c476', '#7fd1a0'),   # btn-3d / book-float gradient top
    ('#c9a04a', '#3f9867'),   # btn-3d / book-float gradient mid/bottom
    ('#96742c', '#1f5c3c'),   # btn-3d gradient bottom / scroll-progress start
    ('#1c1408', '#07140d'),   # btn-3d / book-float-label text color
    ('rgba(80,58,18,0.4)', 'rgba(20,60,38,0.4)'),   # btn-3d inset shadow
    ('rgba(80,58,18,0.45)', 'rgba(20,60,38,0.45)'),  # btn-3d active inset shadow
    ('#6b5222', '#1f5c3c'),   # btn-3d / book-float solid shadow offset
    ('rgba(232,210,160,0.16)', 'rgba(150,220,180,0.16)'),  # dark-band accent-ghost
    ('#e8cf96', '#9fe3b8'),   # dark-band text-shine stop
    ('#f8eed3', '#ecfbf1'),   # dark-band text-shine light stop
    ('#bfa060', '#5fae7d'),   # dark-band text-shine dark stop
    ('#f0dcae', '#bdeecb'),   # dark-band text-shine stop
    ('rgba(232,207,150,', 'rgba(150,220,180,'),  # dark-band orb-a / ghost / stars shadow / foot-mark stroke
    ('rgba(185,138,128,0.14)', 'rgba(100,180,140,0.14)'),  # dark-band orb-b
    ('#faf1dc', '#f0faf3'),   # dark-band btn-3d gradient top
    ('#ecd9a8', '#cdeedb'),   # dark-band btn-3d gradient mid
    ('#c9ab6b', '#8fcaa8'),   # dark-band btn-3d gradient bottom
    ('rgba(110,85,35,0.35)', 'rgba(30,90,58,0.35)'),  # dark-band btn-3d inset shadow
    ('rgba(110,85,35,0.4)', 'rgba(30,90,58,0.4)'),    # dark-band btn-3d active inset shadow
    ('#8a744a', '#4a8f68'),   # dark-band btn-3d shadow offset
    ('#e9c3ab', '#9fe3b8'),   # dark-band stars color
    ('#191307', '#0f1b15'),   # cta-final bg gradient top
    ('#100c05', '#060d09'),   # cta-final bg gradient bottom
    ('#0c0905', '#060d09'),   # footer bg
    ('#f4eee2', '#f4eee2'),   # merktop text (unchanged, kept for clarity)
]
for old, new in PALETTE:
    assert old in h, f'palette anchor missing: {old}'
    h = h.replace(old, new)

# ---------- 3. Restore the protected badge ----------
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

open(SLUG, 'w', encoding='utf-8').write(h)
print('STEP 1-3 OK, length', len(h))
