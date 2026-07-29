#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/floridafreshcuts/index.html
Florida Fresh Cuts, Miami FL (Flagler/Fontainebleau, zip 33126). Barber/owner: Nelson Diaz.
Paleta oxblood/barbershop-pole red (#c64a52 / #a64c52), distinta de la paleta acero de
vierostudiobarber (otra barberia del mismo batch).
"""
import re

SRC = 'templates/dark-v2/index.html'
DST = 'output/floridafreshcuts/index.html'

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
# 2. PALETA: dorado -> oxblood/rojo de barberia
# ============================================================
# 2a. Swaps de hex puntuales (precomputados: hue-shift a ~356 grados, preservando la
# forma de luminosidad/saturacion, ligeramente desaturado/oscurecido para look oxblood).
PALETTE = [
    ('#6b5222', '#5b2327'),
    ('#d4a84b', '#c64a52'),
    ('#e9c3ab', '#e1a4a8'),
    ('#8a744a', '#7c494c'),
    ('#1c1408', '#0f0506'),
    ('#f5efe3', '#efdadb'),
    ('#f0dc9e', '#e7989d'),
    ('#e8cf96', '#de9096'),
    ('#e8c476', '#dc7279'),
    ('#e5c374', '#d97077'),
    ('#c9a04a', '#bb4850'),
    ('#9a7431', '#87353a'),
    ('#96742c', '#833035'),
    ('#0f0b07', '#040202'),
    ('#fbf6ea', '#f6dfe1'),
    ('#faf1dc', '#f5d2d4'),
    ('#f8eed3', '#f2c9cc'),
    ('#f4eee2', '#eed9da'),
    ('#f0dcae', '#e8a7ab'),
    ('#ecd9a8', '#e3a1a6'),
    ('#c9ab6b', '#bd676d'),
    ('#bfa060', '#b35d62'),
    ('#b8934a', '#a64c52'),
    ('#241c0e', '#180b0c'),
    ('#191307', '#0c0405'),
    ('#171207', '#0b0404'),
    ('#100c05', '#040202'),
    ('#0c0905', '#010101'),
]
for old, new in PALETTE:
    rep_all(old, new)

# 2b. rgba() por familia de color: mismo hue-shift (~356 grados) aplicado via HSL a los
# tonos que en el esqueleto solo existen como rgba(...) (sin contraparte hex). El badge
# ya esta protegido, asi que estas familias no lo tocan.
RGBA_FAMILIES = [
    ((15, 11, 7), (4, 2, 2)),          # == #0f0b07 -> #040202 (nav scrolled bg)
    ((212, 168, 75), (198, 74, 82)),   # == #d4a84b -> #c64a52 (accent-ghost, glass border, orb-a, etc.)
    ((232, 207, 150), (222, 144, 150)),  # == #e8cf96 -> #de9096 (dark-band text-shine/accent)
    ((245, 239, 227), (239, 218, 219)),  # == #f5efe3 -> #efdadb (ink en rgba)
    ((110, 85, 35), (93, 36, 40)),     # dark-band btn-3d inset shadow
    ((122, 90, 30), (104, 33, 38)),    # orb-b
    ((180, 140, 60), (160, 65, 71)),   # orb-c
    ((185, 138, 128), (175, 123, 126)),  # dark-band orb-b
    ((232, 210, 160), (223, 154, 158)),  # dark-band accent-ghost
    ((54, 42, 38), (44, 33, 33)),      # btn-ghost hover shadow neutro
    ((80, 58, 18), (64, 19, 22)),      # btn-3d inset shadow (principal)
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

# restaurar el badge dorado intacto
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/946026_florida-fresh-cuts_barber-shop_15889_miami'
rep_all(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/diaznelson22/'
rep_all(OLD_IG_URL, NEW_IG_URL)

rep_all('@pure.artistrysk', '@diaznelson22')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Florida Fresh Cuts · Barbershop in Miami, FL | Fades, Beard Trims &amp; Line-Ups | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Florida Fresh Cuts, Miami FL: classic haircuts, skin fades, beard trims and the signature Florida Fresh Experience with barber Nelson Diaz. 5.0 rating across 414 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Florida Fresh Cuts · Barbershop in Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Classic cuts, skin fades and beard trims with Nelson Diaz. 5.0 across 414 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-10.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Florida Fresh Cuts",
    "description": "Barbershop in Miami, FL: classic haircuts, skin/bald fades, beard trims and the signature Florida Fresh Experience with barber Nelson Diaz.",
    "address": { "@type": "PostalAddress", "streetAddress": "3931 NW 7th St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.77919, "longitude": -80.26047 },
    "sameAs": ["https://booksy.com/en-us/946026_florida-fresh-cuts_barber-shop_15889_miami", "https://www.instagram.com/diaznelson22/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "414", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "08:00", "closes": "13:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "08:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barbershop services", "itemListElement": [
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic Haircut" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Florida Fresh Experience" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic + Beard" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Skin/Bald Fade" } }
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
seg_scroll = h[i_scroll:i_nav]
seg_tail_before = h[i_bookfloat:i_cursorring]
seg_tail = h[i_cursorring:]

print('OK: segmentacion por anclas de comentario')

BK = 'https://booksy.com/en-us/946026_florida-fresh-cuts_barber-shop_15889_miami'
IG = 'https://www.instagram.com/diaznelson22/'

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">FF</span>
    <span class="pre-word">Florida Fresh Cuts</span>
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
        <img src="assets/raw/bk-2.jpg" alt="Florida Fresh Cuts logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(198,74,82,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Florida Fresh <span class="text-[color:var(--accent-deep)]">Cuts</span></span>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami, FL · Barbería" data-en="Miami, FL · Barbershop">Miami, FL · Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="El barbero que todo Miami conoce." data-en="The barber all of Miami knows.">The barber all of Miami knows.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, líneas de barba y" data-en="Fades, beard lines and">Fades, beard lines and</span><br /><span data-es="cortes clásicos " data-en="classic cuts, ">classic cuts, </span><span class="text-shine" data-es="hechos bien" data-en="done right">done right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Florida Fresh Cuts es la barbería del barbero Nelson Diaz en Flagler/Fontainebleau, Miami: cortes clásicos, skin fades y arreglos de barba con la misma atención cada vez. 5.0 perfecto en 414 reseñas en Booksy." data-en="Florida Fresh Cuts is barber Nelson Diaz's shop in the Flagler/Fontainebleau area of Miami: classic cuts, skin fades and beard trims with the same close attention every time. A perfect 5.0 across 414 reviews on Booksy.">Florida Fresh Cuts is barber Nelson Diaz's shop in the Flagler/Fontainebleau area of Miami: classic cuts, skin fades and beard trims with the same close attention every time. A perfect 5.0 across 414 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 414 reseñas en Booksy" data-en="5.0 · 414 reviews on Booksy">5.0 · 414 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @diaznelson22
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-6.jpg" alt="Finished side-profile fresh cut and fade at Florida Fresh Cuts, Miami" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg" data-es="Florida Fresh Experience" data-en="Florida Fresh Experience">Florida Fresh Experience</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $70 · 1h 35min" data-en="From $70 · 1h 35min">From $70 · 1h 35min</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="414">414</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Beards</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Line-ups · Skin Fades · Arreglos de barba" data-en="Line-ups · Skin Fades · Beard Trims">Line-ups · Skin Fades · Beard Trims</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">3931 NW 7th St</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl" data-es="7 Días" data-en="7 Days">7 Days</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Abierto de domingo a sábado" data-en="Open Sunday to Saturday">Open Sunday to Saturday</p></div>
    </div>
  </section>

  '''

print('OK: hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Classic Cuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Skin Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Trims</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Line-Ups</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Black Mask</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-1.jpg" alt="Barber and client together at Florida Fresh Cuts, Miami" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-2.jpg" alt="Interior of Florida Fresh Cuts barbershop with red chairs and mirrors" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="todo Miami lo conoce" data-en="all of Miami knows">all of Miami knows</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Florida Fresh Cuts es la barbería de Nelson Diaz en el área de Flagler/Fontainebleau, Miami: cortes clásicos, skin fades y arreglos de barba con la misma atención de cerca en cada silla." data-en="Florida Fresh Cuts is barber Nelson Diaz's shop in the Flagler/Fontainebleau area of Miami: classic cuts, skin fades and beard trims, all done with the same close attention chair after chair.">Florida Fresh Cuts is barber Nelson Diaz's shop in the Flagler/Fontainebleau area of Miami: classic cuts, skin fades and beard trims, all done with the same close attention chair after chair.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientes lo confirman: es la barbería que todo Miami conoce, con un 5.0 perfecto en 414 reseñas de Booksy, una de las calificaciones más sólidas de la ciudad." data-en="His clients confirm it: this is the shop everyone in Miami knows, with a perfect 5.0 across 414 reviews on Booksy, one of the strongest trust signals in the city.">His clients confirm it: this is the shop everyone in Miami knows, with a perfect 5.0 across 414 reviews on Booksy, one of the strongest trust signals in the city.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="414">414</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-9.jpg" alt="Nelson Diaz, barber and owner of Florida Fresh Cuts" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(198,74,82,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Nelson Diaz · <span class="text-[color:var(--ink-40)]" data-es="Dueño y barbero" data-en="Owner &amp; Barber">Owner &amp; Barber</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elige tu servicio en Booksy con precio y duración claros: corte clásico, skin fade, arreglo de barba o la Florida Fresh Experience, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: classic cut, skin fade, beard trim or the Florida Fresh Experience, and confirm instantly.">Pick your service on Booksy with clear price and duration: classic cut, skin fade, beard trim or the Florida Fresh Experience, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, el crecimiento y el estilo que buscas definen el plan: un skin fade o line-up nítido empieza con una idea clara." data-en="Your hair type, growth pattern and the look you want set the plan: a sharp skin fade or line-up starts with a clear vision.">Your hair type, growth pattern and the look you want set the plan: a sharp skin fade or line-up starts with a clear vision.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde un corte clásico rápido hasta la Florida Fresh Experience completa: cada cliente recibe atención completa en la silla, sin apuros ni atajos." data-en="From a quick classic cut to the full Florida Fresh Experience: every client gets full attention in the chair, no rushing, no shortcuts.">From a quick classic cut to the full Florida Fresh Experience: every client gets full attention in the chair, no rushing, no shortcuts.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un fade limpio, una línea de barba nítida y el mismo trato que ha llevado a la barbería a 414 reseñas de 5.0. Tu próxima cita queda agendada antes de irte." data-en="You leave with a clean fade, a sharp beard line and the same care that has earned this shop 414 reviews at a perfect 5.0. Your next appointment gets booked before you go.">You leave with a clean fade, a sharp beard line and the same care that has earned this shop 414 reviews at a perfect 5.0. Your next appointment gets booked before you go.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (4 cards reales; card 2 = destacada, 414 reseñas = trust signal)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="corte" data-en="cut">cut</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Florida Fresh Cuts en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Florida Fresh Cuts on Booksy. Booking confirms instantly.">Prices and durations as published by Florida Fresh Cuts on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Todos los días" data-en="Everyday go-to">Everyday go-to</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Classic Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El corte clásico de Florida Fresh Cuts: limpio, rápido y consistente cada vez." data-en="The Florida Fresh Cuts classic: clean, quick and consistent every single time.">The Florida Fresh Cuts classic: clean, quick and consistent every single time.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(198,74,82,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Florida Fresh Experience</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio completo que le da nombre a la barbería: corte, fade y arreglo de barba en una sola sesión extendida, la razón por la que Miami vuelve." data-en="The full service the shop is named after: haircut, fade and beard work in one extended sitting, the reason Miami keeps coming back.">The full service the shop is named after: haircut, fade and beard work in one extended sitting, the reason Miami keeps coming back.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 35min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Paquete completo" data-en="Full package">Full package</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Classic + Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte clásico y arreglo de barba en una sola visita: la rutina completa de grooming, bien hecha." data-en="A classic haircut paired with a full beard trim in one visit: the complete grooming routine, done right.">A classic haircut paired with a full beard trim in one visit: the complete grooming routine, done right.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">55min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Skin/Bald Fade" data-en="Skin/Bald Fade">Skin/Bald Fade</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El fade nítido y bien fundido hasta la piel, terminado con un line-up limpio." data-en="The sharp, blended fade taken down to the skin, finished with a clean line-up.">The sharp, blended fade taken down to the skin, finished with a clean line-up.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en Booksy: Fade + Beard $55/55min, Edge-up / Line-up $20, Black Mask $12. Menú completo y disponibilidad en Booksy." data-en="Also on Booksy: Fade + Beard $55/55min, Edge-up / Line-up $20, Black Mask $12. Full menu and availability on Booksy.">Also on Booksy: Fade + Beard $55/55min, Edge-up / Line-up $20, Black Mask $12. Full menu and availability on Booksy.</span></p>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 5 tiles 3/4; bk-9 NUNCA en galeria)
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
          @diaznelson22
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Fade de precisión, detalle de cerca" data-en="Precision fade, close-up detail">Precision fade, close-up detail</span><img src="assets/raw/bk-10.jpg" alt="Close-up detail of a fresh fade at the back of the head, Florida Fresh Cuts" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Diseño a mano alzada" data-en="Freehand hair design">Freehand hair design</span><img src="assets/raw/bk-11.jpg" alt="Cross-shaved hair design detail at Florida Fresh Cuts" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cortes para toda la familia" data-en="Cuts for the whole family">Cuts for the whole family</span><img src="assets/raw/bk-3.jpg" alt="Barber cutting a kid's hair in close-up at Florida Fresh Cuts" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Buzzcut, líneas limpias" data-en="Buzzcut, clean lines">Buzzcut, clean lines</span><img src="assets/raw/bk-4.jpg" alt="Back-of-head detail of a fresh buzzcut, Florida Fresh Cuts" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Perfil terminado, con capa" data-en="Finished cut, side profile">Finished cut, side profile</span><img src="assets/raw/bk-7.jpg" alt="Side-profile finished haircut with cape at Florida Fresh Cuts" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Manos a la obra, corte de niño" data-en="Hard at work, kid's cut">Hard at work, kid's cut</span><img src="assets/raw/bk-12.jpg" alt="Barber actively cutting a kid's hair at Florida Fresh Cuts" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 reseñas reales, verbatim, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="los clientes" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 414 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 414 verified reviews on Booksy">5.0 out of 5 · 414 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Best barber in Miami!!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Octavio N…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Awesome cut"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Alessandro B…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very nice place did a very good hair cut, definitely will go back"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Steven D…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 414 reseñas en Booksy" data-en="Read all 414 reviews on Booksy">Read all 414 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

# ============================================================
# UBICACION
# ============================================================
MAPS_Q = '25.77919,-80.26047'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">3931 NW 7th St, Miami, FL 33126</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(198,74,82,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sábado: 8:00 am - 6:00 pm · Domingo: 8:00 am - 1:00 pm" data-en="Monday-Saturday: 8:00 am - 6:00 pm · Sunday: 8:00 am - 1:00 pm">Monday-Saturday: 8:00 am - 6:00 pm · Sunday: 8:00 am - 1:00 pm</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:230ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(198,74,82,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and DM any questions before your appointment.">See the latest cuts and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(198,74,82,0.4)]" href="{IG}" target="_blank" rel="noopener">@diaznelson22</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Florida Fresh Cuts, 3931 NW 7th St, Miami FL"
          src="https://www.google.com/maps?q={MAPS_Q}&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

  '''

# ============================================================
# CTA FINAL
# ============================================================
NEW_CTA = f'''<!-- CTA FINAL -->
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #0c0405 0%, #040202 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="El barbero que todo Miami conoce." data-en="The barber all of Miami knows.">The barber all of Miami knows.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo corte" data-en="Your next cut">Your next cut</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu corte clásico, tu skin fade, o la Florida Fresh Experience completa." data-en="Book online in seconds: your classic cut, your skin fade, or the full Florida Fresh Experience.">Book online in seconds: your classic cut, your skin fade, or the full Florida Fresh Experience.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>
      </div>
    </div>
  </section>

  '''

print('OK: ubicacion + cta final definidos')

# ============================================================
# FOOTER (el merktop-badge original se mantiene intacto)
# ============================================================
m_badge_footer = re.search(r'<a href="https://merktop\.com".*?</a>', h[i_footer:i_bookfloat], flags=re.S)
assert m_badge_footer, 'no se encontro merktop-badge en footer original'
MERKTOP_BADGE_HTML = m_badge_footer.group(0)

NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#010101]">
    <span class="foot-mark" aria-hidden="true">Florida Fresh Cuts</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Florida Fresh Cuts logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(223,154,158,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Florida Fresh Cuts</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería en Miami, FL. Con cita previa vía Booksy." data-en="Barbershop in Miami, FL. By appointment via Booksy.">Barbershop in Miami, FL. By appointment via Booksy.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>3931 NW 7th St, Miami, FL 33126</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#e3a1a6]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#e3a1a6]">Instagram · @diaznelson22</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Florida Fresh Cuts.</p>
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
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0f0506" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
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
for word in ['Classic Cuts', 'Skin Fades', 'Beard Trims', 'Line-Ups', 'Black Mask', 'Miami, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# leftover-assertion loop: NADA del esqueleto anterior debe sobrevivir
FORBIDDEN = ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk', 'silk press', 'NBA', 'MLB']
for s in FORBIDDEN:
    assert s.lower() not in h_final.lower(), f'LEFTOVER DEL ESQUELETO: "{s}" sigue presente'

# bk-9 (retrato del dueno) NUNCA como tile de galeria: solo debe aparecer en el avatar
assert h_final.count('bk-9.jpg') == 1, f'bk-9.jpg deberia aparecer 1 vez (avatar), aparece {h_final.count("bk-9.jpg")}'

import os
os.makedirs('output/floridafreshcuts', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
