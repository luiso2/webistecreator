#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/classabarberstudio/index.html
Class A Barber Studio LLC, Tampa FL. Paleta borgona/vino (#6b2737 / #9c4a5c).
"""
import re

SRC = 'templates/dark-v2/index.html'
DST = 'output/classabarberstudio/index.html'

h = open(SRC, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'ANCLA ROTA: ' + a[:120]
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    c = h.count(a)
    assert c > 0, 'ANCLA ROTA (0 matches): ' + a[:120]
    if expect is not None:
        assert c == expect, f'ANCLA "{a[:60]}" x{c}, esperaba {expect}'
    h = h.replace(a, b)


# ============================================================
# 1. PROTEGER EL BADGE MERKTOP (dorado, no debe cambiar)
# ============================================================
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque merktop-badge/mkPulse'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ============================================================
# 2. PALETA: gold -> borgona/vino profundo
# ============================================================
# 2a. Swaps de hex puntuales (fuera del badge, ya protegido)
# gradiente compuesto: reemplazar ANTES de tocar los hex individuales que lo forman
rep_all(
    'linear-gradient(90deg, #96742c 0%, #d4a84b 45%, #f0dc9e 100%)',
    'linear-gradient(90deg, #5c2030 0%, #6b2737 45%, #c97a8c 100%)',
)

PALETTE = [
    # accent principal
    ('#d4a84b', '#6b2737'),
    ('#b8934a', '#9c4a5c'),
    # bg
    ('#0f0b07', '#120709'),
    ('#171207', '#1c0d10'),
    ('#241c0e', '#2a1116'),
    # btn-3d gradient (claro->oscuro) + sombras
    ('#e8c476', '#c97a8c'),
    ('#c9a04a', '#9c4a5c'),
    ('#96742c', '#5c2030'),
    ('#6b5222', '#3d1420'),
    ('#1c1408', '#22090d'),
    # shimmer
    ('#f0dc9e', '#e8b4c0'),
    ('#9a7431', '#4a1520'),
    ('#e5c374', '#c97a8c'),
    # dark-band shimmer/orb/btn
    ('#e8cf96', '#e3a9b8'),
    ('#f8eed3', '#f6dde3'),
    ('#bfa060', '#a85a70'),
    ('#f0dcae', '#eec3cf'),
    ('#faf1dc', '#f6dde3'),
    ('#ecd9a8', '#e3a9b8'),
    ('#c9ab6b', '#b06478'),
    ('#8a744a', '#6b3040'),
    ('#e9c3ab', '#e3a9b8'),
    # nav scrolled bg
    ('rgba(15,11,7,0.85)', 'rgba(18,7,9,0.85)'),
    # cta band + footer bg
    ('linear-gradient(180deg, #191307 0%, #100c05 100%)',
     'linear-gradient(180deg, #1c0d10 0%, #0f0709 100%)'),
    ('#0c0905', '#0f0709'),
]
for old, new in PALETTE:
    rep_all(old, new)

# 2b. rgba() por familia de color: swap de hue via regex (cubre TODAS las
# variantes de alpha sin enumerarlas una a una; el badge ya esta protegido).
RGBA_FAMILIES = [
    ((212, 168, 75), (107, 39, 55)),   # accent-deep dorado -> vino profundo
    ((232, 207, 150), (201, 122, 140)),  # dark-band accent claro -> rosa-vino
    ((232, 210, 160), (201, 122, 140)),  # dark-band accent-ghost
    ((122, 90, 30), (74, 21, 32)),     # orb-b
    ((180, 140, 60), (156, 74, 92)),   # orb-c
    ((185, 138, 128), (140, 60, 70)),  # dark-band orb-b
    ((110, 85, 35), (90, 30, 45)),     # dark-band btn-3d inset shadow
    ((54, 42, 38), (61, 20, 32)),      # btn-ghost hover shadow neutro
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda m: f'rgba({r2},{g2},{b2},{m.group(1)})', h)

# restaurar el badge dorado intacto
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/212857_class-a-barber-studio-llc_barber-shop_15761_tampa'
rep_all(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/classabarberstudiollc/'
rep_all(OLD_IG_URL, NEW_IG_URL)

rep_all('@pure.artistrysk', '@classabarberstudiollc')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Class A Barber Studio · Barbershop in Tampa, FL | Fades, Beard Trims &amp; Hair Units | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Class A Barber Studio, Tampa FL: precision fades, beard trims, line-ups and hair unit installs with barber Danny Olivera. 5.0 rating across 491 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Class A Barber Studio · Barbershop in Tampa, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Precision fades, beard trims and hair units with Danny Olivera. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-3.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Class A Barber Studio LLC",
    "description": "Barbershop in Tampa, FL: precision fades, beard trims, line-ups, shaves and hair unit installs with barber Danny Olivera.",
    "address": { "@type": "PostalAddress", "streetAddress": "1011 W Mohawk Ave", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33603", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.997475023595037, "longitude": -82.47340923430025 },
    "sameAs": ["https://booksy.com/en-us/212857_class-a-barber-studio-llc_barber-shop_15761_tampa", "https://www.instagram.com/classabarberstudiollc/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.97", "reviewCount": "491", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barber services", "itemListElement": [
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Fire Fade" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Elite cut & beard" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gentleman's trio/ haircut, beard, brows" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Black mask facial with haircut" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: badge + paleta + globales + head/JSON-LD')

# ============================================================
# 5. IDIOMA: el esqueleto dark-v2 ya es EN default -> sin cambios
# ============================================================
assert "applyLang(lang === 'es' ? 'es' : 'en')" in h
assert '<html lang="en"' in h

# ============================================================
# 6. RECONSTRUCCION DE SECCIONES POR ANCLAS (comentarios HTML unicos)
# ============================================================
def idx(marker, start=0):
    i = h.find(marker, start)
    assert i != -1, 'MARCADOR NO ENCONTRADO: ' + marker
    return i


i_preloader = idx('<!-- PRELOADER DE MARCA -->')
i_scroll = idx('<!-- BARRA DE PROGRESO DE SCROLL -->')
i_nav = idx('<!-- NAV -->')
i_hero = idx('<!-- HERO -->')
i_strip = idx('<!-- STRIP DE CONFIANZA -->')
i_marquee1 = idx('<!-- MARQUEE -->')
i_experiencia = idx('<!-- LA EXPERIENCIA -->')
i_metodo = idx('<!-- EL METODO -->')
i_servicios = idx('<!-- SERVICIOS -->')
i_galeria = idx('<!-- GALERIA -->')
i_marquee2 = idx('<!-- MARQUEE -->', i_experiencia)
i_opiniones = idx('<!-- OPINIONES -->')
i_ubicacion = idx('<!-- UBICACION -->')
i_cta = idx('<!-- CTA FINAL -->')
i_footer = idx('<!-- FOOTER -->')
i_bookfloat = idx('<!-- Boton flotante de reserva -->')
i_cursorring = idx('<div id="cursorRing"')

seg_head = h[:i_preloader]
seg_preloader = h[i_preloader:i_scroll]
seg_scroll = h[i_scroll:i_nav]
seg_nav = h[i_nav:i_hero]
seg_hero = h[i_hero:i_strip]
seg_strip = h[i_strip:i_marquee1]
seg_marquee1 = h[i_marquee1:i_experiencia]
seg_experiencia = h[i_experiencia:i_metodo]
seg_metodo = h[i_metodo:i_servicios]
seg_servicios = h[i_servicios:i_galeria]
seg_galeria = h[i_galeria:i_marquee2]
seg_marquee2 = h[i_marquee2:i_opiniones]
seg_opiniones = h[i_opiniones:i_ubicacion]
seg_ubicacion = h[i_ubicacion:i_cta]
seg_cta = h[i_cta:i_footer]
seg_footer = h[i_footer:i_bookfloat]
seg_bookfloat = h[i_bookfloat:i_cursorring]
seg_tail = h[i_cursorring:]

print('OK: segmentacion por anclas de comentario')

with open('/tmp/stage1.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('etapa 1 escrita en /tmp/stage1.html, len=', len(h))
