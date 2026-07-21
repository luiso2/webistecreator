import re

h = open('output/nailstudiomiami/index.html').read()

m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# barrido de cualquier rgba/hex dorado remanente fuera del badge
def swap_alpha(match):
    alpha = match.group(1)
    return f'rgba(74,114,173,{alpha})'
h = re.sub(r'rgba\(212,168,75,([0-9.]+)\)', swap_alpha, h)

def swap_alpha2(match):
    alpha = match.group(1)
    return f'rgba(140,175,220,{alpha})'
h = re.sub(r'rgba\(232,207,150,([0-9.]+)\)', swap_alpha2, h)

h = h.replace('#d4a84b', '#4a72ad').replace('#b8934a', '#3d5d8f')

h = h.replace('@@BADGE@@', badge_block, 1)

open('output/nailstudiomiami/index.html', 'w').write(h)

# reporte de leftovers de texto (nombre/ciudad/nicho viejo)
leftovers = ['Pure Artistry', 'Orlando', '121705', 'Silk Press', 'K-Tip', 'silk press', 'knotless', 'Knotless', 'braids', 'Braids', 'retwist', 'Retwist', 'hair-salon', '80 W Grant']
for lo in leftovers:
    c = h.count(lo)
    if c:
        print(f'LEFTOVER "{lo}": {c}')
print('barrido de color OK')
