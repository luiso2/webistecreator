import re

h = open('output/iloveawaxingmiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- Quitar seccion GALERIA completa (curaduria: pool dominado por graficas de
# marketing con texto superpuesto; solo 2 fotos reales de calidad sobrevivieron y ya se usan
# en hero + experiencia. Mejor sin galeria dedicada que rellenar con graficas descalificadas. ----------
gallery_block = re.search(
    r'  <!-- GALERIA -->\n  <section id="galeria".*?</section>\n\n',
    h, flags=re.S
)
assert gallery_block, 'seccion galeria no encontrada'
h = h.replace(gallery_block.group(0), '', 1)

# Quitar los links de nav a #galeria (desktop + mobile)
rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '')

# Renumerar sec-num: opiniones 05->04, ubicacion 06->05 (galeria 04 ya no existe)
rep('''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>''',
    '''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">04</span>''')
rep('''<section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>''',
    '''<section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">05</span>''')

open('output/iloveawaxingmiami/index.html', 'w').write(h)
print('galeria removida + nav + sec-num renumerado OK')
