#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/do-not-disturb-nails-miami-beach/index.html
Do Not Disturb Nails, Miami Beach FL. Paleta rojo vino sobre carbon (#8a1f2b / #b23a4a).
Idioma principal: EN (dark-v2 ya es EN default).
"""
import re
import os

SRC = 'templates/dark-v2/index.html'
DST = 'output/do-not-disturb-nails-miami-beach/index.html'

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
# 2. PALETA: gold -> rojo vino sobre carbon
# ============================================================
# 2a. Composites primero (contienen hexes que tambien se remplazan sueltos despues)
rep_all(
    'linear-gradient(90deg, #96742c 0%, #d4a84b 45%, #f0dc9e 100%)',
    'linear-gradient(90deg, #5c141d 0%, #8a1f2b 45%, #e8aab5 100%)',
)
rep_all(
    'linear-gradient(180deg, #191307 0%, #100c05 100%)',
    'linear-gradient(180deg, #1d1213 0%, #110b0c 100%)',
)
rep_all('rgba(15,11,7,0.85)', 'rgba(18,13,13,0.85)')

PALETTE = [
    # accent principal
    ('#d4a84b', '#8a1f2b'),
    ('#b8934a', '#b23a4a'),
    # bg
    ('#0f0b07', '#120d0d'),
    ('#171207', '#1a1112'),
    ('#241c0e', '#2a1518'),
    # btn-3d gradient (claro->oscuro) + sombras + color de texto
    ('#e8c476', '#d98995'),
    ('#c9a04a', '#b23a4a'),
    ('#96742c', '#5c141d'),
    ('#6b5222', '#451018'),
    ('#1c1408', '#200a0d'),
    # shimmer / step-num
    ('#f0dc9e', '#e8aab5'),
    ('#9a7431', '#4a1018'),
    ('#e5c374', '#c9525f'),
    # dark-band shimmer/orb/btn (footer + cta final)
    ('#e8cf96', '#e8b1bb'),
    ('#f8eed3', '#f8e0e3'),
    ('#bfa060', '#a8515f'),
    ('#f0dcae', '#eec3cb'),
    ('#faf1dc', '#f8e0e3'),
    ('#ecd9a8', '#e8b1bb'),
    ('#c9ab6b', '#b0616f'),
    ('#8a744a', '#6b2530'),
    ('#e9c3ab', '#e3aab3'),
    # footer bg
    ('#0c0905', '#110b0c'),
]
for old, new in PALETTE:
    rep_all(old, new)

# 2b. rgba() por familia de color: swap de hue via regex
RGBA_FAMILIES = [
    ((212, 168, 75), (138, 31, 43)),    # accent-deep dorado -> vino profundo
    ((232, 207, 150), (232, 177, 187)),  # dark-band accent claro -> rosa-vino claro
    ((232, 210, 160), (232, 177, 187)),  # dark-band accent-ghost
    ((122, 90, 30), (90, 20, 32)),       # orb-b
    ((180, 140, 60), (178, 58, 74)),     # orb-c
    ((185, 138, 128), (168, 81, 95)),    # dark-band orb-b
    ((110, 85, 35), (107, 37, 48)),      # dark-band btn-3d inset shadow
    ((54, 42, 38), (58, 20, 26)),        # btn-ghost hover shadow neutro
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

# restaurar el badge dorado intacto
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

print('OK: badge protegido + paleta vino aplicada')

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/987275_do-not-disturb-nails_nail-salon_15890_miami-beach'
rep_all(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/donotdisturbnails/'
rep_all(OLD_IG_URL, NEW_IG_URL)

rep_all('@pure.artistrysk', '@donotdisturbnails')

BK = NEW_BOOKSY
IG = NEW_IG_URL

# ============================================================
# 4. HEAD: title, meta, og, theme-color, favicon, JSON-LD
# ============================================================
assert '<meta name="theme-color" content="#120d0d" />' in h, 'theme-color no se actualizo via paleta'
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Do Not Disturb Nails · Nail Studio in Miami Beach, FL | Acrylic, Gel-X &amp; Nail Art | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Do Not Disturb Nails, Miami Beach FL: acrylic and Gel-X full sets, builder gel and hand-painted nail art with nail artist Shauna Griffin. 5.0 rating across 57 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Do Not Disturb Nails · Nail Studio in Miami Beach, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, Gel-X, builder gel and hand-painted nail art with Shauna Griffin. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-14.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-16.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Do Not Disturb Nails",
    "description": "Nail studio in Miami Beach, FL: acrylic and Gel-X full sets, builder gel, manicures, pedicures and hand-painted nail art with nail artist Shauna Griffin.",
    "address": { "@type": "PostalAddress", "streetAddress": "7403 Collins Ave, Suite 113", "addressLocality": "Miami Beach", "addressRegion": "FL", "postalCode": "33141", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.85974, "longitude": -80.1208 },
    "sameAs": ["https://booksy.com/en-us/987275_do-not-disturb-nails_nail-salon_15890_miami-beach", "https://www.instagram.com/donotdisturbnails/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "57", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday"], "opens": "12:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "11:00", "closes": "20:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic FULL SET" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel-X full set" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel manicure with nail art" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Basic pedicure" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: globales + head/JSON-LD')

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
seg_scroll = h[i_scroll:i_nav]
seg_footer_orig = h[i_footer:i_bookfloat]
seg_tail = h[i_cursorring:]

print('OK: segmentacion por anclas de comentario')

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">DND</span>
    <span class="pre-word">Do Not Disturb Nails</span>
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
        <img src="assets/raw/bk-16.jpg" alt="Do Not Disturb Nails logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,31,43,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Do Not Disturb <span class="text-[color:var(--accent-deep)]">Nails</span></span>
      </a>
      <nav class="hidden md:flex items-center gap-7 text-sm font-light">
        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">The Experience</a>
        <a class="nav-link" href="#metodo" data-es="El Método" data-en="The Process">The Process</a>
        <a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>
        <a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Location</a>
      </nav>
      <div class="flex items-center gap-3">
        <button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Change language">EN</button>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Book now</span>
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
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="La Experiencia" data-en="The Experience">The Experience</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Process">The Process</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Location</a>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Book now</a>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami Beach, FL · Estudio de uñas" data-en="Miami Beach, FL · Nail Studio">Miami Beach, FL · Nail Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu tiempo, sin interrupciones." data-en="Your time, uninterrupted.">Your time, uninterrupted.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Acrílico, Gel-X y nail art" data-en="Acrylic, Gel-X and nail art">Acrylic, Gel-X and nail art</span><br /><span data-es="hechos para sentirse " data-en="made to feel ">made to feel </span><span class="text-shine" data-es="sin interrupciones" data-en="uninterrupted">uninterrupted</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos de acrílico y Gel-X, builder gel y nail art pintado a mano con la nail artist Shauna Griffin. Un estudio privado en Miami Beach con una calificación perfecta de 5.0 en 57 reseñas en Booksy." data-en="Acrylic and Gel-X full sets, builder gel and hand-painted nail art with nail artist Shauna Griffin. A private Miami Beach studio with a perfect 5.0 rating across 57 reviews on Booksy.">Acrylic and Gel-X full sets, builder gel and hand-painted nail art with nail artist Shauna Griffin. A private Miami Beach studio with a perfect 5.0 rating across 57 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 57 reseñas en Booksy" data-en="5.0 · 57 reviews on Booksy">5.0 · 57 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @donotdisturbnails
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-14.jpg" alt="Dramatic glossy red nail set, editorial lighting, Do Not Disturb Nails" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Acrylic Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $85 · 2h" data-en="From $85 · 2h">From $85 · 2h</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="57">57</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Gel-X</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos · Nail Art" data-en="Full Sets · Fills · Nail Art">Full Sets · Fills · Nail Art</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Manicura &amp; Pedicura" data-en="Manicure &amp; Pedicure">Manicure &amp; Pedicure</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel · Spa · Clásica" data-en="Gel · Spa · Classic">Gel · Spa · Classic</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">7403 Collins Ave</p></div>
    </div>
  </section>

  '''

print('OK: hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Acrylic Full Sets</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Gel-X</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Builder Gel</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Nail Art</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Spa Pedicure</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami Beach, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-6.jpg" alt="Soft nude nail set resting over a skirt" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-4.jpg" alt="Finished nail set shown resting on a car interior" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una nail artist," data-en="One nail artist,">One nail artist,</span><br /><span class="text-shine" data-es="toda tu atención" data-en="your full attention">your full attention</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Do Not Disturb Nails es el estudio privado de nail art de Shauna Griffin en Collins Ave, Miami Beach: sets completos de acrílico y Gel-X, builder gel y nail art pintado a mano, atendiendo a un cliente a la vez." data-en="Do Not Disturb Nails is Shauna Griffin's private nail studio on Collins Ave in Miami Beach: acrylic and Gel-X full sets, builder gel and hand-painted nail art, done one client at a time.">Do Not Disturb Nails is Shauna Griffin's private nail studio on Collins Ave in Miami Beach: acrylic and Gel-X full sets, builder gel and hand-painted nail art, done one client at a time.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas siguen volviendo y reservando con ella por nombre, tal como promete el estudio: sin distracciones, sin apuro, solo trabajo cuidadoso silla a silla. Una calificación perfecta de 5.0 en 57 reseñas en Booksy lo confirma." data-en="Her clients keep coming back and booking her by name, exactly like the studio promises: no distractions, no rush, just careful work chair-side. A perfect 5.0 rating across 57 reviews on Booksy confirms it.">Her clients keep coming back and booking her by name, exactly like the studio promises: no distractions, no rush, just careful work chair-side. A perfect 5.0 rating across 57 reviews on Booksy confirms it.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="57">57</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-16.jpg" alt="Do Not Disturb Nails logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(178,58,74,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Shauna Griffin · <span class="text-[color:var(--ink-40)]" data-es="Nail Artist" data-en="Nail Artist">Nail Artist</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: marquee x2 + experiencia definidos')

# ============================================================
# EL METODO (4 pasos genericos de nail salon)
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
          <h3 class="font-display text-xl mb-3" data-es="Consulta y diseño" data-en="Consultation &amp; Design">Consultation &amp; Design</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Conversamos sobre forma, largo y cualquier inspiración de nail art antes de tocar tus uñas con la lima." data-en="We talk through shape, length and any nail art inspiration before the first file touches your nails.">We talk through shape, length and any nail art inspiration before the first file touches your nails.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Preparación y limado" data-en="Prep &amp; Filing">Prep &amp; Filing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cuidado de cutículas, forma y limado preparan tu uña natural para un resultado limpio y duradero." data-en="Cuticle care, shaping and filing get your natural nail ready for a clean, long-lasting result.">Cuticle care, shaping and filing get your natural nail ready for a clean, long-lasting result.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Aplicación de gel/acrílico" data-en="Gel/Acrylic Application">Gel/Acrylic Application</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu set completo o relleno se aplica con el sistema que elegiste: acrílico, Gel-X o builder gel." data-en="Your full set or fill goes on with the system you chose: acrylic, Gel-X or builder gel.">Your full set or fill goes on with the system you chose: acrylic, Gel-X or builder gel.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Sellado y top coat" data-en="Seal &amp; Top Coat">Seal &amp; Top Coat</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El nail art se termina y se sella con un top coat duradero para un brillo que se mantiene." data-en="Nail art gets finished and sealed with a durable top coat for shine that lasts.">Nail art gets finished and sealed with a durable top coat for shine that lasts.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (4 cards destacadas + menu completo agrupado, sin acordeon)
# card 2 = destacada (border-color accent 0.4 + btn-3d; el resto btn-ghost)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine">set</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios publicados por Do Not Disturb Nails en Booksy. La reserva se confirma al instante." data-en="Prices as published by Do Not Disturb Nails on Booksy. Booking confirms instantly.">Prices as published by Do Not Disturb Nails on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más reservado" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic FULL SET</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un set completo de acrílico, moldeado y limado al largo que prefieras, hecho para durar." data-en="A full acrylic set shaped and filed to your preferred length, built to last.">A full acrylic set shaped and filed to your preferred length, built to last.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(138,31,43,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel-X full set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tips de Gel-X ligeros armados en un set completo con un acabado brillante y resistente." data-en="Lightweight Gel-X tips built into a full set with a glossy, chip-resistant finish.">Lightweight Gel-X tips built into a full set with a glossy, chip-resistant finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Nail art" data-en="Nail art">Nail art</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel manicure with nail art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una manicura de gel terminada con nail art pintado a mano según lo que quieras." data-en="A gel manicure finished with hand-painted nail art designed around what you want.">A gel manicure finished with hand-painted nail art designed around what you want.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Basic pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una pedicura clásica con forma, cuidado de cutículas y esmalte, de principio a fin." data-en="A classic pedicure with shaping, cuticle care and polish, finished top to bottom.">A classic pedicure with shaping, cuticle care and polish, finished top to bottom.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo: 22 servicios, desde $10 hasta $100. Todo se reserva igual, en Booksy." data-en="Full menu: 22 services, from $10 to $100. Everything below books the same way, on Booksy.">Full menu: 22 services, from $10 to $100. Everything below books the same way, on Booksy.</span></p>
      <div class="reveal grid sm:grid-cols-3 gap-5 mt-10" style="transition-delay:120ms">
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Acrílico" data-en="Acrylic">Acrylic</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Acrylic full set- nail art</span><span class="text-[color:var(--ink)]">$100</span></li>
            <li class="flex justify-between gap-3"><span>Acrylic FULL SET <span class="text-[color:var(--ink-40)] text-xs">· 2h</span></span><span class="text-[color:var(--ink)]">$85</span></li>
            <li class="flex justify-between gap-3"><span>Acrylic FILL</span><span class="text-[color:var(--ink)]">$65</span></li>
            <li class="flex justify-between gap-3"><span>Acrylic fill- nail art</span><span class="text-[color:var(--ink)]">$65</span></li>
          </ul>
        </div>
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Gel-X y Builder Gel" data-en="Gel-X &amp; Builder Gel">Gel-X &amp; Builder Gel</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Gel-x full set - nail art</span><span class="text-[color:var(--ink)]">$100</span></li>
            <li class="flex justify-between gap-3"><span>Gel-X full set <span class="text-[color:var(--ink-40)] text-xs">· 2h</span></span><span class="text-[color:var(--ink)]">$80</span></li>
            <li class="flex justify-between gap-3"><span>Builder Gel full set</span><span class="text-[color:var(--ink)]">$75</span></li>
            <li class="flex justify-between gap-3"><span>Builder full set w/art</span><span class="text-[color:var(--ink)]">$100</span></li>
            <li class="flex justify-between gap-3"><span>Builder gel refill</span><span class="text-[color:var(--ink)]">$60</span></li>
            <li class="flex justify-between gap-3"><span>Builder refill with art</span><span class="text-[color:var(--ink)]">$75</span></li>
            <li class="flex justify-between gap-3"><span>Hard Gel full set</span><span class="text-[color:var(--ink)]">$75</span></li>
            <li class="flex justify-between gap-3"><span>Hard gel fill</span><span class="text-[color:var(--ink)]">$60</span></li>
          </ul>
        </div>
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Manicura, Pedicura y Extras" data-en="Manicure, Pedicure &amp; Extras">Manicure, Pedicure &amp; Extras</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Gel-Manicure <span class="text-[color:var(--ink-40)] text-xs">· 1h 30min</span></span><span class="text-[color:var(--ink)]">$50</span></li>
            <li class="flex justify-between gap-3"><span>Gel manicure with nail art <span class="text-[color:var(--ink-40)] text-xs">· 2h</span></span><span class="text-[color:var(--ink)]">$70</span></li>
            <li class="flex justify-between gap-3"><span>Basic manicure</span><span class="text-[color:var(--ink)]">$20</span></li>
            <li class="flex justify-between gap-3"><span>Spa pedicure</span><span class="text-[color:var(--ink)]">$65</span></li>
            <li class="flex justify-between gap-3"><span>Basic pedicure <span class="text-[color:var(--ink-40)] text-xs">· 1h 30min</span></span><span class="text-[color:var(--ink)]">$50</span></li>
            <li class="flex justify-between gap-3"><span>Nail repair</span><span class="text-[color:var(--ink)]">$10</span></li>
            <li class="flex justify-between gap-3"><span>Regular Polish change</span><span class="text-[color:var(--ink)]">$20</span></li>
            <li class="flex justify-between gap-3"><span>Gel polish change</span><span class="text-[color:var(--ink)]">$30</span></li>
            <li class="flex justify-between gap-3"><span>Soak off with service</span><span class="text-[color:var(--ink)]">$10</span></li>
            <li class="flex justify-between gap-3"><span>Soak off only</span><span class="text-[color:var(--ink)]">$20</span></li>
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
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Nail art" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @donotdisturbnails
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Nail art sobre fondo oscuro" data-en="Nail art on a moody backdrop">Nail art on a moody backdrop</span><img src="assets/raw/bk-9.jpg" alt="Nail art design with a white pattern over a dark background" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Punta francesa con piedras" data-en="French tips with hand-placed stones">French tips with hand-placed stones</span><img src="assets/raw/bk-1.jpg" alt="French tip nail set with rhinestones" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Nail art en rojo y rosa" data-en="Nail art in red and pink tones">Nail art in red and pink tones</span><img src="assets/raw/bk-2.jpg" alt="Nail art design in red and pink tones over a dark background" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Degradado ahumado gris a negro" data-en="Smoky grey-to-black ombre">Smoky grey-to-black ombre</span><img src="assets/raw/bk-10.jpg" alt="Smoky grey and black ombre nail set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Blanco y negro con anillos" data-en="Black and white art with statement rings">Black and white art with statement rings</span><img src="assets/raw/bk-13.jpg" alt="Black and white nail art paired with statement rings" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Degradado de gris a blanco" data-en="Grey-to-white ombre finish">Grey-to-white ombre finish</span><img src="assets/raw/bk-15.jpg" alt="Grey to white ombre nail set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 reseñas reales verbatim, con emojis tal cual)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="las clientas" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 57 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 57 verified reviews on Booksy">5.0 out of 5 · 57 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Shauna is the best!! 🔥🔥"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Claire</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"First time going to Shauna and loved it! She does everything the right way and you feel at ease with her process! Found my new nail tech!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maria P&#8230;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Such an amazing experience. I&#8217;ve been looking for a nail tech I can trust in Miami, happy to say I finally found her!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Idi M&#8230;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 57 reseñas en Booksy" data-en="Read all 57 reviews on Booksy">Read all 57 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

# ============================================================
# UBICACION
# ============================================================
MAPS_Q = '7403+Collins+Ave,+Miami+Beach,+FL+33141'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Beach</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">7403 Collins Ave, Suite 113, Miami Beach, FL 33141</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,31,43,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes: 12:00 PM &#8211; 8:00 PM" data-en="Monday: 12:00 PM &#8211; 8:00 PM">Monday: 12:00 PM &#8211; 8:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes a viernes: 11:00 AM &#8211; 8:00 PM" data-en="Tuesday &#8211; Friday: 11:00 AM &#8211; 8:00 PM">Tuesday &#8211; Friday: 11:00 AM &#8211; 8:00 PM</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,31,43,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira el nail art más reciente y escribe por DM cualquier duda antes de tu cita." data-en="See the latest nail art and DM any questions before your appointment.">See the latest nail art and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,31,43,0.4)]" href="{IG}" target="_blank" rel="noopener">@donotdisturbnails</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Do Not Disturb Nails, 7403 Collins Ave, Miami Beach FL"
          src="https://www.google.com/maps?q={MAPS_Q}&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

  '''

print('OK: ubicacion definida')

# ============================================================
# CTA FINAL
# ============================================================
NEW_CTA = f'''<!-- CTA FINAL -->
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #1d1213 0%, #110b0c 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu tiempo, sin interrupciones." data-en="Your time, uninterrupted.">Your time, uninterrupted.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu set de acrílico, tu Gel-X o ese diseño de nail art que has estado planeando." data-en="Book online in seconds: your acrylic full set, your Gel-X, or that nail art design you have been planning.">Book online in seconds: your acrylic full set, your Gel-X, or that nail art design you have been planning.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>
      </div>
    </div>
  </section>

  '''

print('OK: cta final definida')

# ============================================================
# FOOTER (el merktop-badge original se mantiene intacto)
# ============================================================
m_badge_footer = re.search(r'<a href="https://merktop\.com".*?</a>', seg_footer_orig, flags=re.S)
assert m_badge_footer, 'no se encontro merktop-badge en footer original'
MERKTOP_BADGE_HTML = m_badge_footer.group(0)

NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#110b0c]">
    <span class="foot-mark" aria-hidden="true">Do Not Disturb</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-16.jpg" alt="Do Not Disturb Nails logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,177,187,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Do Not Disturb Nails</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de uñas en Miami Beach, FL. Con cita previa vía Booksy." data-en="Nail studio in Miami Beach, FL. By appointment via Booksy.">Nail studio in Miami Beach, FL. By appointment via Booksy.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>7403 Collins Ave, Suite 113, Miami Beach, FL 33141</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#e3aab3]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#e3aab3]">Instagram · @donotdisturbnails</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Do Not Disturb Nails.</p>
        {MERKTOP_BADGE_HTML}
      </div>
    </div>
  </footer>

  '''

# ============================================================
# BOTON FLOTANTE (mismo markup, solo booksy url + aria-label EN)
# ============================================================
NEW_BOOKFLOAT = f'''<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#200a0d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>

  '''

# ============================================================
# TAIL: cursorRing + back-top + script (aria-label back-top a EN)
# ============================================================
new_seg_tail = seg_tail.replace('aria-label="Volver arriba"', 'aria-label="Back to top"')
assert new_seg_tail != seg_tail, 'no se pudo traducir aria-label de back-top'
seg_tail = new_seg_tail

print('OK: footer + book-float + tail definidos')

# ============================================================
# 7. ENSAMBLADO FINAL
# ============================================================
h_final = (
    seg_head
    + NEW_PRELOADER
    + seg_scroll
    + NEW_NAV
    + NEW_HERO
    + NEW_STRIP
    + NEW_MARQUEE1
    + NEW_EXPERIENCIA
    + NEW_METODO
    + NEW_SERVICIOS
    + NEW_GALERIA
    + NEW_MARQUEE2
    + NEW_OPINIONES
    + NEW_UBICACION
    + NEW_CTA
    + NEW_FOOTER
    + NEW_BOOKFLOAT
    + seg_tail
)

# sanity: los 6 marquee-word deben aparecer exactamente 4 veces cada uno
for word in ['Acrylic Full Sets', 'Gel-X', 'Builder Gel', 'Nail Art', 'Spa Pedicure', 'Miami Beach, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'
assert 'bk-3.jpg' not in h_final, 'PROHIBIDO: bk-3.jpg (selfie) presente'
assert 'bk-11.jpg' not in h_final, 'PROHIBIDO: bk-11.jpg (selfie) presente'

os.makedirs('output/do-not-disturb-nails-miami-beach', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
