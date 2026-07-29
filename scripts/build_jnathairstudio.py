#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/j-nat-hair-studio/index.html
J.Nat Hair Studio, Coral Gables/Miami FL. Paleta esmeralda/jade profundo (#1f6f5c / #3a8f74).
"""
import re

SRC = 'templates/dark-v2/index.html'
DST = 'output/j-nat-hair-studio/index.html'

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
# 2. PALETA: gold -> esmeralda/jade profundo
# ============================================================
# gradiente compuesto: reemplazar ANTES de tocar los hex individuales que lo forman
rep_all(
    'linear-gradient(90deg, #96742c 0%, #d4a84b 45%, #f0dc9e 100%)',
    'linear-gradient(90deg, #12463a 0%, #1f6f5c 45%, #7fcbb0 100%)',
)

PALETTE = [
    # accent principal
    ('#d4a84b', '#1f6f5c'),
    ('#b8934a', '#3a8f74'),
    # bg
    ('#0f0b07', '#0a1210'),
    ('#171207', '#10201c'),
    ('#241c0e', '#16302a'),
    # btn-3d gradient (claro->oscuro) + sombras
    ('#e8c476', '#7fcbb0'),
    ('#c9a04a', '#3a8f74'),
    ('#96742c', '#12463a'),
    ('#6b5222', '#1a3a30'),
    ('#1c1408', '#08150f'),
    # shimmer
    ('#f0dc9e', '#7fcbb0'),
    ('#9a7431', '#0d3830'),
    ('#e5c374', '#5cb896'),
    # dark-band shimmer/orb/btn
    ('#e8cf96', '#8ed6bd'),
    ('#f8eed3', '#d7f3e8'),
    ('#bfa060', '#2a6b58'),
    ('#f0dcae', '#a8e6cf'),
    ('#faf1dc', '#d7f3e8'),
    ('#ecd9a8', '#8ed6bd'),
    ('#c9ab6b', '#34806a'),
    ('#8a744a', '#173d33'),
    ('#e9c3ab', '#8ed6bd'),
    # nav scrolled bg
    ('rgba(15,11,7,0.85)', 'rgba(10,18,16,0.85)'),
    # cta band + footer bg
    ('linear-gradient(180deg, #191307 0%, #100c05 100%)',
     'linear-gradient(180deg, #12241f 0%, #0a1712 100%)'),
    ('#0c0905', '#0a1712'),
]
for old, new in PALETTE:
    rep_all(old, new)

# 2b. rgba() por familia de color: swap de hue via regex (cubre TODAS las
# variantes de alpha sin enumerarlas una a una; el badge ya esta protegido).
RGBA_FAMILIES = [
    ((212, 168, 75), (31, 111, 92)),     # accent-deep dorado -> esmeralda profundo
    ((232, 207, 150), (140, 214, 190)),  # dark-band accent claro -> jade claro
    ((232, 210, 160), (140, 214, 190)),  # dark-band accent-ghost
    ((122, 90, 30), (18, 70, 56)),       # orb-b
    ((180, 140, 60), (58, 143, 116)),    # orb-c
    ((185, 138, 128), (58, 120, 100)),   # dark-band orb-b
    ((110, 85, 35), (20, 80, 64)),       # dark-band btn-3d inset shadow
    ((80, 58, 18), (10, 50, 40)),        # btn-3d inset shadow (principal)
    ((54, 42, 38), (10, 30, 24)),        # btn-ghost hover shadow neutro
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

# restaurar el badge dorado intacto
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

# theme-color meta (mismo hex que --bg, ya cubierto arriba via PALETTE)

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/307551_j-nat-hair-studio_hair-salon_15889_miami'
rep_all(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/Jnathairstudio/'
rep_all(OLD_IG_URL, NEW_IG_URL)

rep_all('@pure.artistrysk', '@Jnathairstudio')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>J.Nat Hair Studio · Hair Salon in Coral Gables, FL | Cuts, Color &amp; Balayage | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="J.Nat Hair Studio, Coral Gables FL: men\'s and women\'s haircuts, full color, balayage and hair painting, highlights and Brazilian blowouts with stylist Nathaniel. 5.0 rating across 484 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="J.Nat Hair Studio · Hair Salon in Coral Gables, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Cuts, color, balayage and treatments with stylist Nathaniel. 5.0 rating across 484 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-4.jpg" />',
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
    "name": "J.Nat Hair Studio",
    "description": "Hair salon in Coral Gables, FL: men's and women's haircuts, full color, balayage and hair painting, highlights, Brazilian blowouts and scalp treatments with stylist Nathaniel.",
    "address": { "@type": "PostalAddress", "streetAddress": "1340 S. Dixie Highway, Suite 150, #202", "addressLocality": "Coral Gables", "addressRegion": "FL", "postalCode": "33146", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.7128299999999, "longitude": -80.27863 },
    "sameAs": ["https://booksy.com/en-us/307551_j-nat-hair-studio_hair-salon_15889_miami", "https://www.instagram.com/Jnathairstudio/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "484", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "66", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Men's Haircut & Beard" } },
      { "@type": "Offer", "price": "420", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Balayage & Hair Painting" } },
      { "@type": "Offer", "price": "135", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Color" } },
      { "@type": "Offer", "price": "305", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brazilian Blowout" } }
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
seg_tail_start = i_cursorring
seg_bookfloat = h[i_bookfloat:i_cursorring]
seg_tail = h[i_cursorring:]

print('OK: segmentacion por anclas de comentario')

BK = 'https://booksy.com/en-us/307551_j-nat-hair-studio_hair-salon_15889_miami'
IG = 'https://www.instagram.com/Jnathairstudio/'

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">JN</span>
    <span class="pre-word">J.Nat Hair Studio</span>
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
        <img src="assets/raw/bk-2.jpg" alt="J.Nat Hair Studio logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,111,92,0.35)] bg-white" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">J.Nat <span class="text-[color:var(--accent-deep)]">Hair Studio</span></span>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Coral Gables, FL · Hair Studio" data-en="Coral Gables, FL · Hair Studio">Coral Gables, FL · Hair Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cada corte, un nuevo comienzo." data-en="Every cut, a fresh start.">Every cut, a fresh start.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Cortes, color y" data-en="Haircuts, color and">Haircuts, color and</span><br /><span data-es="balayage hechos " data-en="balayage done ">balayage done </span><span class="text-shine" data-es="bien" data-en="right">right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Cortes para hombre, mujer y niños, color completo, balayage y hair painting, mechas y Brazilian Blowout con el estilista Nathaniel. Un estudio full-service en Coral Gables con un 5.0 perfecto en 484 reseñas de Booksy." data-en="Men's, women's and kids' haircuts, full color, balayage and hair painting, highlights and Brazilian Blowout with stylist Nathaniel. A full-service studio in Coral Gables with a perfect 5.0 across 484 reviews on Booksy.">Men's, women's and kids' haircuts, full color, balayage and hair painting, highlights and Brazilian Blowout with stylist Nathaniel. A full-service studio in Coral Gables with a perfect 5.0 across 484 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 484 reseñas en Booksy" data-en="5.0 · 484 reviews on Booksy">5.0 · 484 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @Jnathairstudio
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-4.jpg" alt="Copper balayage result at J.Nat Hair Studio, Coral Gables" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Balayage &amp; Hair Painting</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$420 · 4h" data-en="$420 · 4h">$420 · 4h</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="484">484</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Cuts <span class="text-shine">&amp;</span> Color</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Hombre · Mujer · Niños" data-en="Men's · Women's · Kids">Men's · Women's · Kids</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Balayage" data-en="Balayage">Balayage</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Estilo full-service" data-en="Full-service styling">Full-service styling</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Coral Gables</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1340 S. Dixie Hwy</p></div>
    </div>
  </section>

  '''

print('OK: hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Haircuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Balayage</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Full Color</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Highlights</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brazilian Blowout</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Coral Gables, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-9.jpg" alt="Close-up of a precision fade haircut at J.Nat Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-8.jpg" alt="Side view of a textured men's haircut finished at J.Nat Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="cuidado full-service" data-en="full-service care">full-service care</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="J.Nat Hair Studio es el estudio de Nathaniel en Coral Gables: cortes de precisión para hombre, mujer y niños, color completo, balayage y hair painting, todo con la misma atención de cerca, cita tras cita." data-en="J.Nat Hair Studio is Nathaniel's studio in Coral Gables: precision haircuts for men, women and kids, full color, balayage and hair painting, all done chair-side with the same close attention every time.">J.Nat Hair Studio is Nathaniel's studio in Coral Gables: precision haircuts for men, women and kids, full color, balayage and hair painting, all done chair-side with the same close attention every time.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientes vuelven por una razón: escucha primero, y luego entrega exactamente lo que pediste, hasta la última capa. Un 5.0 perfecto en 484 reseñas verificadas de Booksy." data-en="His clients keep coming back for one reason: he listens first, then delivers exactly what you asked for, down to the last layer. A perfect 5.0 across 484 verified Booksy reviews.">His clients keep coming back for one reason: he listens first, then delivers exactly what you asked for, down to the last layer. A perfect 5.0 across 484 verified Booksy reviews.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="484">484</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-1.jpg" alt="Nathaniel, stylist and owner of J.Nat Hair Studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,111,92,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Nathaniel · <span class="text-[color:var(--ink-40)]" data-es="Dueño y estilista" data-en="Owner &amp; Stylist">Owner &amp; Stylist</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elige tu servicio en Booksy con precio y duración claros: corte, color, balayage o tratamiento, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: haircut, color, balayage or treatment, and confirm instantly.">Pick your service on Booksy with clear price and duration: haircut, color, balayage or treatment, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, tus metas y el estilo que buscas definen el plan, ya sea un corte de precisión o una transformación completa de color." data-en="Your hair type, goals and the look you want shape the plan, whether it is a precise haircut or a full color transformation.">Your hair type, goals and the look you want shape the plan, whether it is a precise haircut or a full color transformation.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde un corte de hombre de 35 minutos hasta un balayage de 4 horas: cada servicio recibe su tiempo completo, sin apuros." data-en="From a 35-minute men's haircut to a 4-hour balayage: every service gets its full time, chair-side, done right.">From a 35-minute men's haircut to a 4-hour balayage: every service gets its full time, chair-side, done right.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un corte o color fresco y consejos para mantenerlo en casa. Tu próxima cita queda agendada antes de irte." data-en="You leave with a fresh cut or color and tips to keep it looking great at home. Your next visit gets booked before you go.">You leave with a fresh cut or color and tips to keep it looking great at home. Your next visit gets booked before you go.</p>
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
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por J.Nat Hair Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by J.Nat Hair Studio on Booksy. Booking confirms instantly.">Prices and durations as published by J.Nat Hair Studio on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más reservado" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Men&#8217;s Haircut &amp; Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un corte completo de hombre junto con un diseño de barba de precisión, terminado limpio en una sola visita." data-en="A full men's haircut paired with a precision beard shape, finished clean in one visit.">A full men's haircut paired with a precision beard shape, finished clean in one visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$66</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(31,111,92,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Balayage &amp; Hair Painting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Color y dimensión pintados a mano, personalizados para tu cabello, para un resultado suave y luminoso." data-en="Hand-painted color and dimension, customized to your hair for a soft, sun-kissed result.">Hand-painted color and dimension, customized to your hair for a soft, sun-kissed result.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$420</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">4h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Color completo" data-en="Color specialist">Color specialist</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Color</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Color de raíz a puntas para una cobertura total y una base fresca y vibrante." data-en="All-over color for full coverage and a fresh, vibrant base, from root to end.">All-over color for full coverage and a fresh, vibrant base, from root to end.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$135</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 20min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamiento alisador" data-en="Smoothing treatment">Smoothing treatment</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Brazilian Blowout</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un tratamiento alisador que reduce el frizz y el tiempo de secado, dejando el cabello sedoso por meses." data-en="A smoothing treatment that cuts frizz and blow-dry time, leaving hair silky for months.">A smoothing treatment that cuts frizz and blow-dry time, leaving hair silky for months.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$305</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo: 21 servicios, desde $25 hasta $500. Todo se reserva igual, en Booksy." data-en="Full menu: 21 services, from $25 to $500. Everything below books the same way, on Booksy.">Full menu: 21 services, from $25 to $500. Everything below books the same way, on Booksy.</span></p>
      <div class="reveal grid sm:grid-cols-3 gap-5 mt-10" style="transition-delay:120ms">
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Cortes" data-en="Haircuts">Haircuts</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Men&#8217;s Haircut <span class="text-[color:var(--ink-40)] text-xs">· 35min</span></span><span class="text-[color:var(--ink)]">$50</span></li>
            <li class="flex justify-between gap-3"><span>Men&#8217;s Layered Haircut</span><span class="text-[color:var(--ink)]">$66</span></li>
            <li class="flex justify-between gap-3"><span>Boys Haircut, 3 to 12 <span class="text-[color:var(--ink-40)] text-xs">· 30min</span></span><span class="text-[color:var(--ink)]">$45</span></li>
            <li class="flex justify-between gap-3"><span>Girls 12 &amp; Under Wash-Cut-Blowdry</span><span class="text-[color:var(--ink)]">$90</span></li>
            <li class="flex justify-between gap-3"><span>Pixie Haircut, short hair <span class="text-[color:var(--ink-40)] text-xs">· 50min</span></span><span class="text-[color:var(--ink)]">$88</span></li>
            <li class="flex justify-between gap-3"><span>Long Curly Haircut, no blowdry <span class="text-[color:var(--ink-40)] text-xs">· 50min</span></span><span class="text-[color:var(--ink)]">$95</span></li>
            <li class="flex justify-between gap-3"><span>Women&#8217;s Wash-Cut-Style, from <span class="text-[color:var(--ink-40)] text-xs">· 1h 5min</span></span><span class="text-[color:var(--ink)]">$105</span></li>
          </ul>
        </div>
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Color" data-en="Color">Color</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Express Color Touch Up</span><span class="text-[color:var(--ink)]">$85</span></li>
            <li class="flex justify-between gap-3"><span>Color Gloss / Toner</span><span class="text-[color:var(--ink)]">$90</span></li>
            <li class="flex justify-between gap-3"><span>Partial Highlights w/ Toner <span class="text-[color:var(--ink-40)] text-xs">· 2h 15min</span></span><span class="text-[color:var(--ink)]">$245</span></li>
            <li class="flex justify-between gap-3"><span>Full Highlights w/ Toner</span><span class="text-[color:var(--ink)]">$305</span></li>
            <li class="flex justify-between gap-3"><span>Bleachout Touch Up, 8 weeks</span><span class="text-[color:var(--ink)]">$305</span></li>
            <li class="flex justify-between gap-3"><span>Full Head Bleach Out <span class="text-[color:var(--ink-40)] text-xs">· 4h 20min</span></span><span class="text-[color:var(--ink)]">$500</span></li>
          </ul>
        </div>
        <div class="glass rounded-2xl p-6">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Estilo y tratamientos" data-en="Styling &amp; treatments">Styling &amp; treatments</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Wash &amp; Blowdry Style</span><span class="text-[color:var(--ink)]">$66</span></li>
            <li class="flex justify-between gap-3"><span>Glam Waves Addition</span><span class="text-[color:var(--ink)]">$25</span></li>
            <li class="flex justify-between gap-3"><span>Hair &amp; Scalp Detox Treatment</span><span class="text-[color:var(--ink)]">$85</span></li>
            <li class="flex justify-between gap-3"><span>Deep Hydrating Treatment</span><span class="text-[color:var(--ink)]">$25</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 4 tiles 3/4: solo 5 fotos reales distintas
# en el pool de fotos, sin repetir la misma imagen dos veces dentro
# de la galeria; grid a 2 columnas para no dejar huecos)
# ============================================================
NEW_GALERIA = f'''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Cortes y color" data-en="Real cuts">Real cuts</span> <span class="text-shine" data-es="reales" data-en="and color">and color</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @Jnathairstudio
        </a>
      </div>
      <div class="grid grid-cols-2 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Dentro del estudio" data-en="Inside the studio">Inside the studio</span><img src="assets/raw/bk-3.jpg" alt="Nathaniel at the entrance of J.Nat Hair Studio, Coral Gables" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Fade de precisión" data-en="Precision fade">Precision fade</span><img src="assets/raw/bk-9.jpg" alt="Close-up of a precision fade haircut at J.Nat Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Corte con textura" data-en="Textured cut">Textured cut</span><img src="assets/raw/bk-8.jpg" alt="Side view of a textured men's haircut finished at J.Nat Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Balayage cobrizo" data-en="Copper balayage">Copper balayage</span><img src="assets/raw/bk-6.jpg" alt="Copper balayage result with soft waves at J.Nat Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Nathaniel, dueño y estilista" data-en="Nathaniel, owner &amp; stylist">Nathaniel, owner &amp; stylist</span><img src="assets/raw/bk-1.jpg" alt="Nathaniel, stylist and owner of J.Nat Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (4 reseñas reales verbatim, grid 2x2)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="los clientes" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 484 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 484 verified reviews on Booksy">5.0 out of 5 · 484 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-2 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"100% recommend Nathanial! He will listen to you and you will walk out with exactly with what you came in asking for. You will not regret going to him :)"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Beatriz M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"He's excellent!!! I'm very happy!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jeanette M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Loved the experience, really attentive, really helpful"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yordan F…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:330ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"For the first time, I have met a barber who can cut my hair using scissors and understands layering better than anyone I've gone too."</blockquote>
          <figcaption class="text-sm"><span class="font-medium" data-es="Cliente de Booksy" data-en="Booksy Client">Booksy Client</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 484 reseñas en Booksy" data-en="Read all 484 reviews on Booksy">Read all 484 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

# ============================================================
# UBICACION
# ============================================================
MAPS_Q = '1340+S+Dixie+Highway,+Coral+Gables,+FL+33146'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Coral Gables</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">1340 S. Dixie Highway, Suite 150, #202, Coral Gables, FL 33146</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,111,92,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: miércoles y sábado de 9am a 4pm, jueves y viernes de 11am a 6pm." data-en="By appointment via Booksy: Wednesday &amp; Saturday 9am-4pm, Thursday &amp; Friday 11am-6pm.">By appointment via Booksy: Wednesday &amp; Saturday 9am-4pm, Thursday &amp; Friday 11am-6pm.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,111,92,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los cortes y colores más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and color and DM any questions before your appointment.">See the latest cuts and color and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,111,92,0.4)]" href="{IG}" target="_blank" rel="noopener">@Jnathairstudio</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: J.Nat Hair Studio, 1340 S. Dixie Highway, Coral Gables FL"
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
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #12241f 0%, #0a1712 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cortes, color, cuidado." data-en="Cuts, color, care.">Cuts, color, care.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo look" data-en="Your next look">Your next look</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu corte, tu color, o ese balayage que has estado planeando." data-en="Book online in seconds: your haircut, your color, or that balayage you have been planning.">Book online in seconds: your haircut, your color, or that balayage you have been planning.</p>
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
seg_footer_orig = h[i_footer:i_bookfloat]
m_badge_footer = re.search(r'<a href="https://merktop\.com".*?</a>', seg_footer_orig, flags=re.S)
assert m_badge_footer, 'no se encontro merktop-badge en footer original'
MERKTOP_BADGE_HTML = m_badge_footer.group(0)

NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#0a1712]">
    <span class="foot-mark" aria-hidden="true">J.Nat Hair Studio</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="J.Nat Hair Studio logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(140,214,190,0.35)] bg-white" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">J.Nat Hair Studio</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en Coral Gables, FL. Con cita previa vía Booksy." data-en="Hair studio in Coral Gables, FL. By appointment via Booksy.">Hair studio in Coral Gables, FL. By appointment via Booksy.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>1340 S. Dixie Highway, Suite 150, #202, Coral Gables, FL 33146</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#8ed6bd]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#8ed6bd]">Instagram · @Jnathairstudio</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 J.Nat Hair Studio.</p>
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
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#08150f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
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
for word in ['Haircuts', 'Balayage', 'Full Color', 'Highlights', 'Brazilian Blowout', 'Coral Gables, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

import os
os.makedirs('output/j-nat-hair-studio', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
