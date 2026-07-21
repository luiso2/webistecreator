import re

h = open('output/vivianatales/index.html').read()

m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

def swap1(match):
    return f'rgba(140,63,82,{match.group(1)})'
h = re.sub(r'rgba\(160,74,114,([0-9.]+)\)', swap1, h)

def swap2(match):
    return f'rgba(227,176,168,{match.group(1)})'
h = re.sub(r'rgba\(240,190,215,([0-9.]+)\)', swap2, h)

h = h.replace('#a04a72', '#8c3f52').replace('#c47a9c', '#b66f80')

h = h.replace('@@BADGE@@', badge_block, 1)

open('output/vivianatales/index.html', 'w').write(h)

leftovers = ['Lash Bloom', 'West Palm Beach', 'Cresthaven', '519855', '_lashbloom', 'Yesi', 'hybrid', 'Hybrid', 'bottom lashes', 'Bottom Lashes', 'logo.jpg', 'hero-1.jpg', 'about-2.jpg', 'gallery-7.jpg', 'gallery-2.jpg']
for lo in leftovers:
    c = h.count(lo)
    if c:
        print(f'LEFTOVER "{lo}": {c}')
print('barrido de color OK')
