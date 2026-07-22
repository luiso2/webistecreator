#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/vierostudiobarber/index.html
Viero Studio Barber (Booksy: "Casa_viero", real brand per signage/IG @vierostudiobarber),
Miami FL (Edgewater/downtown, 33132). Paleta steel/navy azul (#4b94d4 / #4a85b8).
Barber: Luis Rolon. 5.0 rating, 124 reviews on Booksy.
"""
import re
import os

SRC = 'templates/dark-v2/index.html'
DST = 'output/vierostudiobarber/index.html'

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
# 1. PROTEGER EL BADGE MERKTOP (dorado, no debe cambiar NUNCA)
#    - bloque CSS .merktop-badge {...} @keyframes mkPulse
#    - el <a href="https://merktop.com">...</a> del footer (contiene el
#      hex literal #f4eee2 que tambien esta en nuestra lista de paleta)
# ============================================================
m_css = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m_css, 'no se encontro el bloque merktop-badge/mkPulse'
badge_css = m_css.group(0)
h = h.replace(badge_css, '@@BADGE_CSS@@', 1)

m_html = re.search(r'<a href="https://merktop\.com".*?</a>', h, flags=re.S)
assert m_html, 'no se encontro el <a> merktop del footer'
badge_html = m_html.group(0)
h = h.replace(badge_html, '@@BADGE_HTML@@', 1)

# ============================================================
# 2. PALETA: dorado calido -> steel/navy azul (hue-shift precomputado, ~208deg)
# ============================================================
PALETTE = [
    ('#6b5222', '#22496b'),
    ('#d4a84b', '#4b94d4'),
    ('#e9c3ab', '#abcce9'),
    ('#8a744a', '#4a6c8a'),
    ('#1c1408', '#08131c'),
    ('#f5efe3', '#e3edf5'),
    ('#f0dc9e', '#9ecaf0'),
    ('#e8cf96', '#96c2e8'),
    ('#e8c476', '#76b3e8'),
    ('#e5c374', '#74b0e5'),
    ('#c9a04a', '#4a8ec9'),
    ('#9a7431', '#31699a'),
    ('#96742c', '#2c6596'),
    ('#0f0b07', '#070b0f'),
    ('#fbf6ea', '#eaf3fb'),
    ('#faf1dc', '#dcecfa'),
    ('#f8eed3', '#d3e7f8'),
    # ('#f4eee2', '#e2ecf4') se omite: su unica aparicion en el esqueleto es
    # el "Powered by Merktop" del footer, ya protegido via badge_html.
    ('#f0dcae', '#aed1f0'),
    ('#ecd9a8', '#a8ccec'),
    ('#c9ab6b', '#6b9dc9'),
    ('#bfa060', '#6093bf'),
    ('#b8934a', '#4a85b8'),
    ('#241c0e', '#0e1a24'),
    ('#191307', '#071119'),
    ('#171207', '#071017'),
    ('#100c05', '#050b10'),
    ('#0c0905', '#05090c'),
]
for old, new in PALETTE:
    rep_all(old, new)

# rgba() por familia de color (hue-shift equivalente en decimal; el badge
# ya esta protegido asi que estos son todos los usos "vivos" en el sitio)
RGBA_FAMILIES = [
    ((212, 168, 75), (75, 148, 212)),    # accent-deep
    ((232, 207, 150), (150, 194, 232)),  # dark-band accent claro
    ((245, 239, 227), (227, 237, 245)),  # --ink-60/--ink-40 base
    ((110, 85, 35), (35, 75, 110)),      # dark-band btn-3d inset shadow
    ((54, 42, 38), (38, 47, 54)),        # btn-ghost hover shadow neutro
    ((232, 210, 160), (160, 198, 232)),  # dark-band accent-ghost
    ((185, 138, 128), (128, 158, 185)),  # dark-band orb-b
    ((180, 140, 60), (60, 124, 180)),    # orb-c
    ((15, 11, 7), (7, 11, 15)),          # nav scrolled bg
    ((122, 90, 30), (30, 79, 122)),      # orb-b
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)
# nota: rgba(80,58,18,*) se deja SIN cambiar (no es un literal de la lista de
# paleta; asi quedo tambien en classabarberstudio, el ejemplo de referencia).

# restaurar los dos bloques del badge, intactos
assert '@@BADGE_CSS@@' in h
h = h.replace('@@BADGE_CSS@@', badge_css, 1)
assert '@@BADGE_HTML@@' in h
h = h.replace('@@BADGE_HTML@@', badge_html, 1)

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://booksy.com/en-us/317362_casa-viero_barber-shop_15889_miami'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
IG = 'https://www.instagram.com/vierostudiobarber/'
rep_all(OLD_IG_URL, IG)

rep_all('@pure.artistrysk', '@vierostudiobarber')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Viero Studio Barber · Barbershop in Miami, FL | Fades, Beard Steam &amp; Grooming | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Viero Studio Barber, Miami FL: precision fades, haircut and beard with steam, and grooming with barber Luis Rolon. 5.0 rating across 124 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Viero Studio Barber · Barbershop in Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Fades, beard steam and grooming with barber Luis Rolon. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-4.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-7.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Viero Studio Barber",
    "description": "Barbershop in Miami, FL: precision fades, haircut and beard with steam, grooming and hair system installs with barber Luis Rolon.",
    "address": { "@type": "PostalAddress", "streetAddress": "1442 NE Miami Pl, Suite 209", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33132", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.78909, "longitude": -80.19332 },
    "sameAs": ["https://booksy.com/en-us/317362_casa-viero_barber-shop_15889_miami", "https://www.instagram.com/vierostudiobarber/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "124", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday"], "opens": "13:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday"], "opens": "10:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday"], "opens": "10:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday", "Friday"], "opens": "09:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barber services", "itemListElement": [
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Men's haircut" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut and beard with steam" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Men's haircut and grooming" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Beard grooming" } }
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
seg_tail = h[i_cursorring:]

print('OK: segmentacion por anclas de comentario')

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">VS</span>
    <span class="pre-word">Viero Studio Barber</span>
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
        <img src="assets/raw/bk-6.jpg" alt="Viero Studio Barber logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,148,212,0.35)] bg-white" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Viero Studio <span class="text-[color:var(--accent-deep)]">Barber</span></span>
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

# ============================================================
# HERO
# ============================================================
NEW_HERO = f'''<!-- HERO -->
  <section id="top" class="relative min-h-screen flex items-center grain overflow-hidden pt-28 pb-16">
    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami, FL · Barbería" data-en="Miami, FL · Barbershop">Miami, FL · Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Fades nítidos. Barba al vapor. Siempre." data-en="Sharp fades. Steamed beards. Every time.">Sharp fades. Steamed beards. Every time.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, barba al vapor y" data-en="Fades, beard steam and">Fades, beard steam and</span><br /><span data-es="grooming hecho " data-en="grooming done ">grooming done </span><span class="text-shine" data-es="bien" data-en="right">right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Fades de precisión, barba terminada al vapor e instalación de hair systems con el barbero Luis Rolon, en el corazón de Edgewater. Una barbería de Miami con 124 reseñas y un 5.0 perfecto." data-en="Precision fades, steam-finished beard work and hair system installs with barber Luis Rolon, right in the heart of Edgewater. A Miami shop with 124 reviews and a perfect 5.0 rating.">Precision fades, steam-finished beard work and hair system installs with barber Luis Rolon, right in the heart of Edgewater. A Miami shop with 124 reviews and a perfect 5.0 rating.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 124 reseñas en Booksy" data-en="5.0 · 124 reviews on Booksy">5.0 · 124 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @vierostudiobarber
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-4.jpg" alt="Client with a sharp finished fade in dramatic side profile at Viero Studio Barber" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Haircut &amp; Beard with Steam</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $70 · 50min" data-en="From $70 · 50min">From $70 · 50min</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="124">124</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fade <span class="text-shine">&amp;</span> Steam</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cortes · Barbas · Grooming" data-en="Haircuts · Beards · Grooming">Haircuts · Beards · Grooming</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Edgewater</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Barbería del centro de Miami" data-en="Downtown Miami barbershop">Downtown Miami barbershop</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1442 NE Miami Pl</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Haircuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard + Steam</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Line-Ups</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hair Systems</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Grooming</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-2.jpg" alt="Client portrait, cap and beard, after a visit to Viero Studio Barber" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-5.jpg" alt="Barber tools and ring light setup inside Viero Studio Barber" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="resultados nítidos" data-en="sharp results">sharp results</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Viero Studio Barber es la barbería de Luis Rolon en Edgewater, Miami: fades de precisión, barba terminada al vapor e instalación de hair systems, todo en una sola silla y con atención personal." data-en="Viero Studio Barber is barber Luis Rolon's shop in Miami's Edgewater neighborhood: precision fades, beard work finished with hot steam, and hair system installs, all handled personally in one chair.">Viero Studio Barber is barber Luis Rolon's shop in Miami's Edgewater neighborhood: precision fades, beard work finished with hot steam, and hair system installs, all handled personally in one chair.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientes vuelven silla tras silla por lo mismo: un fade limpio y una visita sin apuros. Viero Studio Barber tiene un 5.0 perfecto en 124 reseñas de Booksy." data-en="Clients keep coming back chair after chair for the same reason: a clean fade and an unhurried visit. Viero Studio Barber holds a perfect 5.0 rating across 124 reviews on Booksy.">Clients keep coming back chair after chair for the same reason: a clean fade and an unhurried visit. Viero Studio Barber holds a perfect 5.0 rating across 124 reviews on Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="124">124</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-6.jpg" alt="Viero Studio Barber, close-up of a haircut in progress" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,133,184,0.3)] bg-white" loading="lazy" />
            <span class="text-sm font-light">Luis Rolon · <span class="text-[color:var(--ink-40)]" data-es="Barbero" data-en="Barber">Barber</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: corte, corte y barba, o barba con vapor, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: haircut, haircut and beard, or beard with steam, and confirm instantly.">Pick your service on Booksy with clear price and duration: haircut, haircut and beard, or beard with steam, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El largo, el desvanecido que buscas y el estilo de barba definen el plan antes de tocar la máquina." data-en="The length, the fade you want and your beard style set the plan before the clippers ever touch down.">The length, the fade you want and your beard style set the plan before the clippers ever touch down.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El fade y el vapor" data-en="The fade &amp; the steam">The fade &amp; the steam</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Luis trabaja el fade con precisión y termina la barba con toalla y vapor caliente para un afeitado más suave." data-en="Luis works the fade with precision and finishes the beard with a hot towel and steam for a smoother shave.">Luis works the fade with precision and finishes the beard with a hot towel and steam for a smoother shave.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un fade limpio, la barba en forma y consejos para mantenerlo fresco. Tu próxima cita queda agendada antes de irte." data-en="You leave with a clean fade, a shaped beard and tips to keep it fresh at home. Your next appointment gets booked before you go.">You leave with a clean fade, a shaped beard and tips to keep it fresh at home. Your next appointment gets booked before you go.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (4 cards, card 2 destacada)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="corte" data-en="cut">cut</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Viero Studio Barber en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Viero Studio Barber on Booksy. Booking confirms instantly.">Prices and durations as published by Viero Studio Barber on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte de caballero" data-en="Men's haircut">Men's haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El corte de caballero de siempre, nítido y bien fundido, listo en media hora." data-en="The classic men's haircut, sharp and clean-blended, done in half an hour.">The classic men's haircut, sharp and clean-blended, done in half an hour.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(75,148,212,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y barba con vapor" data-en="Haircut &amp; beard with steam">Haircut &amp; beard with steam</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio más reservado: fade completo y barba terminada con toalla caliente y vapor, para un acabado suave." data-en="The most booked service: a full fade paired with a beard finished with hot towel and steam for a smooth result.">The most booked service: a full fade paired with a beard finished with hot towel and steam for a smooth result.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">50min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Paquete completo" data-en="Full package">Full package</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y arreglo de barba" data-en="Haircut &amp; grooming">Haircut &amp; grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte completo más arreglo de barba en una sola visita: la rutina de grooming completa, bien hecha." data-en="A full haircut plus a beard grooming session in one visit: the complete grooming routine, done right.">A full haircut plus a beard grooming session in one visit: the complete grooming routine, done right.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Solo barba" data-en="Beard only">Beard only</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Arreglo de barba" data-en="Beard grooming">Beard grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseño y arreglo de barba solamente, para mantener la línea nítida entre cortes." data-en="Beard shaping and grooming on its own, to keep the line sharp between haircuts.">Beard shaping and grooming on its own, to keep the line sharp between haircuts.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: hair system desde $100 (2h 30min), highlights desde $55 y trim desde $15. Menú completo en Booksy." data-en="Also: hair system from $100 (2h 30min), highlights from $55 and a trim from $15. Full menu on Booksy.">Also: hair system from $100 (2h 30min), highlights from $55 and a trim from $15. Full menu on Booksy.</span></p>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 5 tiles 3/4; solo bk-2..bk-9, nunca bk-1,10,11,12,13)
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
          @vierostudiobarber
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Estilizando en el momento" data-en="Styling in progress">Styling in progress</span><img src="assets/raw/bk-7.jpg" alt="Barber styling a client's hair in side profile at Viero Studio Barber" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Fade fresco, acabado limpio" data-en="Fresh fade, finished clean">Fresh fade, finished clean</span><img src="assets/raw/bk-3.jpg" alt="Finished fade in side profile at Viero Studio Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalle del fade, de cerca" data-en="Fade detail, up close">Fade detail, up close</span><img src="assets/raw/bk-8.jpg" alt="Close-up detail of a fade haircut at Viero Studio Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Máquina en acción" data-en="Clippers at work">Clippers at work</span><img src="assets/raw/bk-9.jpg" alt="Barber using clippers on a client wearing a cape at Viero Studio Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Perfil nítido" data-en="Sharp side profile">Sharp side profile</span><img src="assets/raw/bk-4.jpg" alt="Client with a sharp finished fade in dramatic side profile" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Retrato de cliente" data-en="Client portrait">Client portrait</span><img src="assets/raw/bk-2.jpg" alt="Client portrait, cap and beard, after a visit to Viero Studio Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 reseñas reales verbatim, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="los clientes" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 124 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 124 verified reviews on Booksy">5.0 out of 5 · 124 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing, if you are looking for a new look: this is your guy! Thanks again"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jayden G…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"First time needing a new barber in over 10 years and Luis was exceptional"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Victor C…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente servicio! Encantado"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Alexander T…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 124 reseñas en Booksy" data-en="Read all 124 reviews on Booksy">Read all 124 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

# ============================================================
# UBICACION (Direccion, Horario, Reservas, Instagram)
# ============================================================
MAPS_Q = '25.78909,-80.19332'
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
              <p class="text-sm text-[color:var(--ink-60)] font-light">1442 NE Miami Pl, Suite 209, Miami, FL 33132</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,148,212,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lun 1pm–8pm · Mar 10am–6pm · Mié 10am–8pm · Jue–Vie 9am–8pm · Sáb 9am–7pm · Dom cerrado" data-en="Mon 1pm–8pm · Tue 10am–6pm · Wed 10am–8pm · Thu–Fri 9am–8pm · Sat 9am–7pm · Sun closed">Mon 1pm–8pm · Tue 10am–6pm · Wed 10am–8pm · Thu–Fri 9am–8pm · Sat 9am–7pm · Sun closed</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,148,212,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and DM any questions before your appointment.">See the latest cuts and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,148,212,0.4)]" href="{IG}" target="_blank" rel="noopener">@vierostudiobarber</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Viero Studio Barber, 1442 NE Miami Pl, Miami FL"
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
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #071119 0%, #050b10 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Fade fresco, cada vez." data-en="Fresh fade, every time.">Fresh fade, every time.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo fade" data-en="Your next fade">Your next fade</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu fade, tu barba con vapor, o ese hair system que has estado planeando." data-en="Book online in seconds: your fade, your steamed beard, or that hair system install you have been planning.">Book online in seconds: your fade, your steamed beard, or that hair system install you have been planning.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>
      </div>
    </div>
  </section>

  '''

print('OK: ubicacion + cta final definidos')

# ============================================================
# FOOTER (el merktop-badge original se mantiene intacto: badge_html)
# ============================================================
NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#05090c]">
    <span class="foot-mark" aria-hidden="true">Viero Studio Barber</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-6.jpg" alt="Viero Studio Barber logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(128,158,185,0.35)] bg-white" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Viero Studio Barber</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería en Edgewater, Miami, FL. Con cita previa vía Booksy." data-en="Barbershop in Edgewater, Miami, FL. By appointment via Booksy.">Barbershop in Edgewater, Miami, FL. By appointment via Booksy.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>1442 NE Miami Pl, Suite 209, Miami, FL 33132</p>
        <p class="text-xs text-[color:var(--ink-40)]" data-es="Lun 1-8p · Mar 10-6p · Mié 10-8p · Jue-Vie 9-8p · Sáb 9-7p · Dom cerrado" data-en="Mon 1-8p · Tue 10-6p · Wed 10-8p · Thu-Fri 9-8p · Sat 9-7p · Sun closed">Mon 1-8p · Tue 10-6p · Wed 10-8p · Thu-Fri 9-8p · Sat 9-7p · Sun closed</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#96c2e8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#96c2e8]">Instagram · @vierostudiobarber</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Viero Studio Barber.</p>
        {badge_html}
      </div>
    </div>
  </footer>

  '''

# ============================================================
# BOTON FLOTANTE (mismo markup, solo booksy url + aria-label EN)
# ============================================================
NEW_BOOKFLOAT = f'''<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#08131c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
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
for word in ['Haircuts', 'Beard + Steam', 'Line-Ups', 'Hair Systems', 'Beard Grooming', 'Miami, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (logo, artefactos, selfies) nunca deben aparecer
for banned in ['bk-1.jpg', 'bk-10.jpg', 'bk-11.jpg', 'bk-12.jpg', 'bk-13.jpg']:
    assert banned not in h_final, f'foto prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk',
                 'silk press', 'Silk Press', 'NBA', 'MLB']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/vierostudiobarber', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
