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

BK = 'https://booksy.com/en-us/212857_class-a-barber-studio-llc_barber-shop_15761_tampa'
IG = 'https://www.instagram.com/classabarberstudiollc/'

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">CA</span>
    <span class="pre-word">Class A Barber Studio</span>
    <span class="pre-line"></span>
  </div>

  '''

# ============================================================
# NAV
# ============================================================
NEW_NAV = f'''<!-- NAV -->
  <header id="nav" class="fixed top-0 inset-x-0 z-50">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 h-[72px] flex items-center justify-between">
      <a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/bk-2.jpg" alt="Class A Barber Studio logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(107,39,55,0.35)] bg-white" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Class A <span class="text-[color:var(--accent-deep)]">Barber</span></span>
      </a>
      <nav class="hidden md:flex items-center gap-7 text-sm font-light">
        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>
        <a class="nav-link" href="#metodo" data-es="El Método" data-en="The Process">El Método</a>
        <a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>
        <a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>
        <a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>
        <a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>
      </nav>
      <div class="flex items-center gap-3">
        <button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Change language">EN</button>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>
        <button id="menuBtn" class="md:hidden w-10 h-10 flex flex-col items-center justify-center gap-[5px]" aria-label="Open menu">
          <span class="w-6 h-px bg-[color:var(--ink)]"></span>
          <span class="w-6 h-px bg-[color:var(--ink)]"></span>
          <span class="w-4 h-px bg-[color:var(--accent-deep)] self-end mr-2"></span>
        </button>
      </div>
    </div>
    <div id="mobileMenu" class="md:hidden hidden glass mx-4 mt-1 rounded-2xl overflow-hidden">
      <nav class="flex flex-col p-4 text-sm">
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Process">El Método</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>
      </nav>
    </div>
  </header>

  '''

print('OK: preloader + nav definidos')

# ============================================================
# HERO
# ============================================================
NEW_HERO = f'''<!-- HERO -->
  <section id="top" class="relative min-h-screen flex items-center grain overflow-hidden pt-28 pb-16">
    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Tampa, FL · Barbería" data-en="Tampa, FL · Barbershop">Tampa, FL · Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Fades nítidos. Líneas limpias. Siempre." data-en="Sharp fades. Clean lines. Every time.">Sharp fades. Clean lines. Every time.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, líneas de barba y" data-en="Fades, beard lines and">Fades, beard lines and</span><br /><span data-es="grooming hecho " data-en="grooming done ">grooming done </span><span class="text-shine" data-es="bien" data-en="right">right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Fades de precisión, line-ups nítidos, diseño de barba e instalación de hair units con el barbero Danny Olivera. Una barbería de barrio en Tampa con 491 reseñas y una calificación casi perfecta de 5.0." data-en="Precision fades, sharp line-ups, beard sculpting and hair unit installs with barber Danny Olivera. A neighborhood shop in Tampa with 491 reviews and a nearly perfect 5.0 rating.">Precision fades, sharp line-ups, beard sculpting and hair unit installs with barber Danny Olivera. A neighborhood shop in Tampa with 491 reviews and a nearly perfect 5.0 rating.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 491 reseñas en Booksy" data-en="5.0 · 491 reviews on Booksy">5.0 · 491 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @classabarberstudiollc
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-3.jpg" alt="Client with a sharp fade and clean beard line-up at Class A Barber Studio" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">The Fire Fade</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $40 · 30min" data-en="From $40 · 30min">From $40 · 30min</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# STRIP DE CONFIANZA
# ============================================================
NEW_STRIP = '''<!-- STRIP DE CONFIANZA -->
  <section class="relative border-y border-[color:var(--accent-ghost)] bg-[color:var(--bg-2)]">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="491">491</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Beards</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Line-ups · Afeitadas · Arreglos" data-en="Line-ups · Shaves · Trims">Line-ups · Shaves · Trims</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Hair Units" data-en="Hair Units">Hair Units</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Instalación y mantenimiento" data-en="Custom install &amp; maintenance">Custom install &amp; maintenance</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1011 W Mohawk Ave</p></div>
    </div>
  </section>

  '''

print('OK: hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Trims</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Line-Ups</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hair Units</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hot Towel Shaves</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Tampa, FL</span><span class="marquee-star">✦</span>
      </div>
'''
NEW_MARQUEE1 = '''<!-- MARQUEE -->
  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
''' + MARQUEE_SEQ + MARQUEE_SEQ + '''    </div>
  </div>

  '''
NEW_MARQUEE2 = '''<!-- MARQUEE -->
  <div class="marquee marquee-reverse" aria-hidden="true">
    <div class="marquee-track">
''' + MARQUEE_SEQ + MARQUEE_SEQ + '''    </div>
  </div>

  '''

# ============================================================
# LA EXPERIENCIA
# ============================================================
NEW_EXPERIENCIA = '''<!-- LA EXPERIENCIA -->
  <section id="experiencia" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">01</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-14 items-center">
      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-9.jpg" alt="Barber Danny Olivera lining up a client's haircut with a trimmer" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-7.jpg" alt="Danny Olivera fading a haircut under the studio's ring light" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="resultados nítidos" data-en="sharp results">sharp results</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Class A Barber Studio es la barbería de Danny Olivera en Tampa: fades de precisión, líneas de barba limpias e instalación de hair units, todo con la misma atención de cerca, silla tras silla." data-en="Class A Barber Studio is Danny Olivera's shop in Tampa: precision fades, clean beard lines and hair unit installs, all done with the same close attention chair after chair.">Class A Barber Studio is Danny Olivera's shop in Tampa: precision fades, clean beard lines and hair unit installs, all done with the same close attention chair after chair.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientes vuelven por una razón: un corte fresco cada vez, además del tipo de conversación que hace que la silla se sienta como en casa. 491 reseñas en Booksy, con un 5.0 casi perfecto." data-en="His clients keep coming back for one reason: a fresh cut every time, plus the kind of conversation that makes the chair feel like home. 491 reviews on Booksy, with a nearly perfect 5.0.">His clients keep coming back for one reason: a fresh cut every time, plus the kind of conversation that makes the chair feel like home. 491 reviews on Booksy, with a nearly perfect 5.0.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="491">491</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Class A Barber Studio logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,74,92,0.3)] bg-white" loading="lazy" />
            <span class="text-sm font-light">Danny Olivera · <span class="text-[color:var(--ink-40)]" data-es="Dueño y barbero" data-en="Owner &amp; Barber">Owner &amp; Barber</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: marquee x2 + experiencia definidos')

# ============================================================
# EL METODO
# ============================================================
NEW_METODO = '''<!-- EL METODO -->
  <section id="metodo" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">02</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elige tu servicio en Booksy con precio y duración claros: fade, arreglo de barba, afeitada o hair unit, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: fade, beard trim, shave or hair unit, and confirm instantly.">Pick your service on Booksy with clear price and duration: fade, beard trim, shave or hair unit, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, el crecimiento y el estilo que buscas definen el plan: un fade o line-up nítido empieza con una idea clara." data-en="Your hair type, growth pattern and the look you want set the plan: a sharp fade or line-up starts with a clear vision.">Your hair type, growth pattern and the look you want set the plan: a sharp fade or line-up starts with a clear vision.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde un line-up rápido hasta la instalación completa de un hair unit: cada cliente recibe atención completa en la silla, sin apuros ni atajos." data-en="From a quick line-up to a full hair unit install: every client gets full attention in the chair, no rushing, no shortcuts.">From a quick line-up to a full hair unit install: every client gets full attention in the chair, no rushing, no shortcuts.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un fade limpio, una línea de barba nítida y consejos para mantenerlo fresco en casa. Tu próxima cita queda agendada antes de irte." data-en="You leave with a clean fade, a sharp beard line and tips to keep it fresh at home. Your next appointment gets booked before you go.">You leave with a clean fade, a sharp beard line and tips to keep it fresh at home. Your next appointment gets booked before you go.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (4 cards destacadas + bloques agrupados con el resto)
# card 2 = destacada (border-color accent 0.4 + btn-3d; el resto btn-ghost)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="corte" data-en="cut">cut</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Class A Barber Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Class A Barber Studio on Booksy. Booking confirms instantly.">Prices and durations as published by Class A Barber Studio on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más reservado" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Elite cut &amp; beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un corte completo junto con un diseño de barba de precisión, terminado limpio en una sola sesión." data-en="A full haircut paired with a precision beard sculpt, finished clean in one sitting.">A full haircut paired with a precision beard sculpt, finished clean in one sitting.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(107,39,55,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">The Fire Fade</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El fade nítido y bien fundido que todos los clientes piden por nombre, terminado con un line-up limpio." data-en="The sharp, blended fade every regular asks for by name, finished with a clean line-up.">The sharp, blended fade every regular asks for by name, finished with a clean line-up.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Paquete completo" data-en="Full package">Full package</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gentleman&#8217;s trio</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte, barba y cejas en una sola visita: la rutina de grooming completa, bien hecha." data-en="Haircut, beard and brows in one visit: the complete grooming routine, done right.">Haircut, beard and brows in one visit: the complete grooming routine, done right.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Facial adicional" data-en="Add-on facial">Add-on facial</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Black Mask Facial" data-en="Black Mask Facial">Black Mask Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un corte rematado con un facial de mascarilla negra de limpieza profunda, para un rostro más fresco." data-en="A haircut finished off with a deep-cleaning black mask facial for a fresher, brighter face.">A haircut finished off with a deep-cleaning black mask facial for a fresher, brighter face.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo: 14 servicios, desde $8 hasta $550. Todo se reserva igual, en Booksy." data-en="Full menu: 14 services, from $8 to $550. Everything below books the same way, on Booksy.">Full menu: 14 services, from $8 to $550. Everything below books the same way, on Booksy.</span></p>
      <div class="reveal grid sm:grid-cols-3 gap-5 mt-10" style="transition-delay:120ms">
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Detalles" data-en="Grooming details">Grooming details</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Barber brow clean up <span class="text-[color:var(--ink-40)] text-xs">· 5min</span></span><span class="text-[color:var(--ink)]">$8</span></li>
            <li class="flex justify-between gap-3"><span>Signature nose &amp; ear wax <span class="text-[color:var(--ink-40)] text-xs">· 10min</span></span><span class="text-[color:var(--ink)]">$15</span></li>
            <li class="flex justify-between gap-3"><span>Precision Line-Up</span><span class="text-[color:var(--ink)]">$20</span></li>
            <li class="flex justify-between gap-3"><span>Royal Beard Trim</span><span class="text-[color:var(--ink)]">$20</span></li>
          </ul>
        </div>
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Cortes y afeitadas" data-en="Cuts &amp; shaves">Cuts &amp; shaves</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Master Line-Up &amp; Beard</span><span class="text-[color:var(--ink)]">$30</span></li>
            <li class="flex justify-between gap-3"><span>The boss shave</span><span class="text-[color:var(--ink)]">$30</span></li>
            <li class="flex justify-between gap-3"><span>Young kings cut / 12 and under</span><span class="text-[color:var(--ink)]">$30</span></li>
            <li class="flex justify-between gap-3"><span>Fade &amp; arch <span class="text-[color:var(--ink-40)] text-xs">· 30min</span></span><span class="text-[color:var(--ink)]">$45</span></li>
          </ul>
        </div>
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Hair units" data-en="Hair units">Hair units</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>HairUnit Maintenance/ Men <span class="text-[color:var(--ink-40)] text-xs">· 1h 30min</span></span><span class="text-[color:var(--ink)]">$80</span></li>
            <li class="flex justify-between gap-3"><span>Hair unit install <span class="text-[color:var(--ink-40)] text-xs">· 2h</span></span><span class="text-[color:var(--ink)]">$550</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 5 tiles 3/4)
# ============================================================
NEW_GALERIA = f'''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Cortes" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="cuts">cuts</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @classabarberstudiollc
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Dentro del estudio" data-en="Inside the studio">Inside the studio</span><img src="assets/raw/bk-1.jpg" alt="Lounge and waiting area inside Class A Barber Studio, Tampa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Fade con textura, acabado fresco" data-en="Textured fade, fresh finish">Textured fade, fresh finish</span><img src="assets/raw/bk-4.jpg" alt="Textured haircut finished with a clean fade at Class A Barber Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Precisión, navaja en mano" data-en="Precision, blade in hand">Precision, blade in hand</span><img src="assets/raw/bk-6.jpg" alt="Close-up of a straight razor blade used for a clean line-up" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Line-up limpio, de cerca" data-en="Clean line-up, close up">Clean line-up, close up</span><img src="assets/raw/bk-8.jpg" alt="Close-up of a precise beard line-up being shaved at Class A Barber Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Difuminando el fade" data-en="Fading it in">Fading it in</span><img src="assets/raw/bk-7.jpg" alt="Barber Danny Olivera fading a haircut under the studio ring light" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Enfoque total, líneas nítidas" data-en="Sharp focus, sharp lines">Sharp focus, sharp lines</span><img src="assets/raw/bk-9.jpg" alt="Barber Danny Olivera lining up a client's haircut with a trimmer" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 reseñas reales verbatim)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="los clientes" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 491 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 491 verified reviews on Booksy">5.0 out of 5 · 491 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Fresh cut every time"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joshua F…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Like many of you reading this, I moved down to Tampa needing to find a good barber. Its been a few years now and I don’t plan on switching. With Danny, you’ll not only get a fresh cut, good conversations, but a great experience overall. So stop scrolling and just book that appointment!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Misael a…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The best"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jose D…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 491 reseñas en Booksy" data-en="Read all 491 reviews on Booksy">Read all 491 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

with open('/tmp/stage1.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('etapa 1 escrita en /tmp/stage1.html, len=', len(h))
