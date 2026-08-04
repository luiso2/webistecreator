#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/jhongthebarber-wesleychapel/index.html
Jhon G The Barber, Wesley Chapel FL (27658 Cashford Circle Ste 102, 33544). Barbershop de Jhon
Garcia Montoya. Paleta acero/slate azul (hue-shift ~205deg desde el dorado original del
esqueleto, distinto de rust ~15deg, caramelo/amber ~35deg, rosa-cobre ~5deg, violeta ~300deg
usados en sites hermanos). 5.0 / 272 reviews en Booksy. 10 servicios reales publicados en
Booksy (VIP King Full Service, combos de corte+barba+cejas, cortes infantiles, shape up, etc).
Sin telefono ni email publico tras busqueda profunda: CTA siempre a Booksy/Instagram.
Idioma principal del negocio: ESPANOL (resenas y clientela mayormente hispanos) -> este site
es ES POR DEFECTO (html lang="es", applyLang default "es"), con EN como toggle.
"""
import re
import os
import colorsys

SRC = 'templates/dark-v2/index.html'
DST = 'output/jhongthebarber-wesleychapel/index.html'

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
# 2. PALETA: dorado -> acero/slate azul (hue-shift a ~205deg, sat x0.9, computado con
#    colorsys desde los hex reales del esqueleto). Distinto de rust (~15deg), caramelo
#    (~30deg), coral fairy (~345deg), esmeralda (~152deg), teal (~180deg), violeta (~262deg),
#    rosa-cobre (~5deg) y del dorado original (~42deg) usados en sites hermanos hoy.
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(110, 85, 35), (122, 90, 30), (15, 11, 7), (180, 140, 60), (185, 138, 128), (212, 168, 75),
          (232, 207, 150), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]
# nota: (27,21,14) y (36,28,20) solo aparecen dentro del bloque .merktop-badge (protegido arriba).
TARGET_HUE = 205 / 360.0
SAT_MUL = 0.9


def _shift_hex(hx):
    hx = hx.lstrip('#')
    r, g, b = int(hx[0:2], 16) / 255, int(hx[2:4], 16) / 255, int(hx[4:6], 16) / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return '#%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def _shift_rgb(rgb):
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return (round(r2 * 255), round(g2 * 255), round(b2 * 255))


PALETTE = [(hx, _shift_hex(hx)) for hx in _HEXES]
for old, new in PALETTE:
    rep_all(old, new)
# nota: '#D4A84B' (uppercase) y 'rgba(244,238,226,' son unicas del merktop-badge, protegido arriba.

RGBA_FAMILIES = [(rgb, _shift_rgb(rgb)) for rgb in _RGBAS]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

# restaurar los dos bloques del badge, intactos
assert '@@BADGE_CSS@@' in h
h = h.replace('@@BADGE_CSS@@', badge_css, 1)
assert '@@BADGE_HTML@@' in h
h = h.replace('@@BADGE_HTML@@', badge_html, 1)

ACCENT_DEEP = _shift_hex('#d4a84b')
ACCENT_MID = _shift_hex('#b8934a')
ACCENT_GHOST_RGB = _shift_rgb((212, 168, 75))
HOVER_DARKBAND_RGB = _shift_rgb((232, 207, 150))
print('ACCENT_DEEP', ACCENT_DEEP, 'ACCENT_MID', ACCENT_MID, 'GHOST', ACCENT_GHOST_RGB, 'HOVER', HOVER_DARKBAND_RGB)

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://booksy.com/en-us/771244_jhon-g-the-barber_barber-shop_15751_lutz'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
IG = 'https://www.instagram.com/Jhong1706/'
rep_all(OLD_IG_URL, IG)

rep_all('@pure.artistrysk', '@Jhong1706')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Jhon G The Barber · Barbería en Wesley Chapel, FL | Fades y Diseños de Precisión</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Jhon G The Barber, Wesley Chapel FL: fades, diseños, barba y el VIP King Full Service con Jhon García Montoya. 5.0 perfecto en 272 reseñas de Booksy. Reserva en línea." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Jhon G The Barber · Barbería en Wesley Chapel, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Fades, diseños y barba de precisión. 5.0 en Booksy. Reserva en línea." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Jhon G The Barber",
    "description": "Barbershop in Wesley Chapel, FL: precision fades, hair designs, beard grooming, kids haircuts and the VIP King Full Service with barber Jhon Garcia Montoya.",
    "address": { "@type": "PostalAddress", "streetAddress": "27658 Cashford Circle Ste 102", "addressLocality": "Wesley Chapel", "addressRegion": "FL", "postalCode": "33544", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.20159, "longitude": -82.36459 },
    "sameAs": ["https://booksy.com/en-us/771244_jhon-g-the-barber_barber-shop_15751_lutz", "https://www.instagram.com/Jhong1706/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "272", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "17:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barber services", "itemListElement": [
      { "@type": "Offer", "price": "56", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "VIP King Full Service" } },
      { "@type": "Offer", "price": "44", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut, Beard & Eyebrows" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut & Beard" } },
      { "@type": "Offer", "price": "24", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Kid's Haircut" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Shape Up" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: badge + paleta + globales + head/JSON-LD')

# ============================================================
# 5. IDIOMA: negocio ES -> el esqueleto queda ES POR DEFECTO
# ============================================================
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep(
    "applyLang(lang === 'es' ? 'es' : 'en');",
    "applyLang(lang === 'en' ? 'en' : 'es');",
)
# aria-labels del esqueleto (langToggle, menuBtn, back-top, book-float) ya estan en
# espanol de fabrica: al quedar ES por defecto no requieren traduccion.

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
    <span class="pre-mono">JG</span>
    <span class="pre-word">Jhon G The Barber</span>
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
        <img src="assets/raw/bk-1.jpg" alt="Jhon G The Barber" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba({ACCENT_GHOST_RGB[0]},{ACCENT_GHOST_RGB[1]},{ACCENT_GHOST_RGB[2]},0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Jhon G <span class="text-[color:var(--accent-deep)]">The Barber</span></span>
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
        <button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Cambiar idioma">EN</button>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>
        <button id="menuBtn" class="md:hidden w-10 h-10 flex flex-col items-center justify-center gap-[5px]" aria-label="Abrir menú">
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Wesley Chapel, FL · Barbería" data-en="Wesley Chapel, FL · Barbershop">Wesley Chapel, FL · Barbería</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cada corte, hecho con precisión." data-en="Every cut, made with precision.">Cada corte, hecho con precisión.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, diseños y" data-en="Fades, designs and">Fades, diseños y</span><br /><span data-es="barba con " data-en="beard work, ">barba con </span><span class="text-shine" data-es="precisión real" data-en="done right">precisión real</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Jhon García Montoya corta fades, diseños y barba en Wesley Chapel: cada cita es trabajo hecho a mano, con la misma atención sea un adulto o el primer corte de un niño. 5.0 perfecto en 272 reseñas de Booksy." data-en="Jhon Garcia Montoya cuts fades, designs and beards in Wesley Chapel: every appointment gets hand-finished work, with the same care whether it is an adult or a kid's first haircut. A perfect 5.0 across 272 reviews on Booksy.">Jhon García Montoya corta fades, diseños y barba en Wesley Chapel: cada cita es trabajo hecho a mano, con la misma atención sea un adulto o el primer corte de un niño. 5.0 perfecto en 272 reseñas de Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 272 reseñas en Booksy" data-en="5.0 · 272 reviews on Booksy">5.0 · 272 reseñas en Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @Jhong1706
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-1.jpg" alt="Jhon García Montoya, barbero, frente a Jhon G The Barber con sus herramientas" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">VIP King Full Service</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$56 · 1h" data-en="$56 · 1h">$56 · 1h</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="272">272</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Diseños</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Barba · Shape Up · VIP" data-en="Beard · Shape Up · VIP">Barba · Shape Up · VIP</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Se habla español" data-en="Spanish spoken">Se habla español</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Niños y adultos" data-en="Kids and adults">Niños y adultos</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Wesley Chapel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Cashford Circle</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Diseños</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Barba</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Shape Up</span><span class="marquee-star">✦</span>
        <span class="marquee-word">VIP King</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Wesley Chapel, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-5.jpg" alt="Fade y barba recién terminados en Jhon G The Barber" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-11.jpg" alt="Detalle del fade en proceso, línea perfilada con máquina" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">Un barbero,</span><br /><span class="text-shine" data-es="atención de verdad" data-en="real attention">atención de verdad</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Jhon G The Barber es la barbería de Jhon García Montoya en Wesley Chapel: fades, diseños de cabello, barba y el VIP King Full Service, todo hecho a mano, cliente por cliente." data-en="Jhon G The Barber is Jhon Garcia Montoya's shop in Wesley Chapel: fades, hair designs, beard work and the VIP King Full Service, all done by hand, one client at a time.">Jhon G The Barber es la barbería de Jhon García Montoya en Wesley Chapel: fades, diseños de cabello, barba y el VIP King Full Service, todo hecho a mano, cliente por cliente.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus reseñas lo repiten una y otra vez: trato profesional, cariñoso y un resultado que se nota semanas después del corte. 5.0 perfecto en 272 reseñas verificadas de Booksy." data-en="His reviews say it again and again: professional, warm treatment and a cut that still looks sharp weeks later. A perfect 5.0 across 272 verified Booksy reviews.">Sus reseñas lo repiten una y otra vez: trato profesional, cariñoso y un resultado que se nota semanas después del corte. 5.0 perfecto en 272 reseñas verificadas de Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="272">272</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-1.jpg" alt="Jhon García Montoya, barbero" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(ACCENT_RGB,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Jhon García Montoya · <span class="text-[color:var(--ink-40)]" data-es="Dueño y Barbero" data-en="Owner &amp; Barber">Dueño y Barbero</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''
NEW_EXPERIENCIA = NEW_EXPERIENCIA.replace(
    'rgba(ACCENT_RGB,0.3)',
    f'rgba({ACCENT_GHOST_RGB[0]},{ACCENT_GHOST_RGB[1]},{ACCENT_GHOST_RGB[2]},0.3)',
)

print('OK: marquee x2 + experiencia definidos')

# ============================================================
# EL METODO
# ============================================================
NEW_METODO = '''<!-- EL METODO -->
  <section id="metodo" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">02</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">Así se trabaja</span> <span class="text-shine" data-es="aquí" data-en="here">aquí</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy, desde un shape up hasta el VIP King Full Service, y confirmas al instante." data-en="Pick your service on Booksy, from a shape up to the VIP King Full Service, and confirm instantly.">Eliges tu servicio en Booksy, desde un shape up hasta el VIP King Full Service, y confirmas al instante.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Consulta rápida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El fade, el diseño o el estilo de barba que buscas se conversan antes de tocar la máquina." data-en="The fade, design or beard style you want gets talked through before the clippers start.">El fade, el diseño o el estilo de barba que buscas se conversan antes de tocar la máquina.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El corte" data-en="The cut">El corte</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Jhon trabaja cada línea y cada fade con precisión, del degradado al diseño terminado." data-en="Jhon works every line and fade with precision, from the blend to the finished design.">Jhon trabaja cada línea y cada fade con precisión, del degradado al diseño terminado.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">El toque final</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un corte nítido y la barba en forma. Tu próxima cita queda lista antes de irte." data-en="You leave with a sharp cut and a shaped beard. Your next appointment is set before you go.">Sales con un corte nítido y la barba en forma. Tu próxima cita queda lista antes de irte.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (4 cards destacadas + bloque con los 6 servicios restantes visibles,
# los 10 servicios reales de Booksy, nombres EXACTOS, PROHIBIDO acordeon/details)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="corte" data-en="cut">corte</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Jhon G The Barber en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Jhon G The Barber on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Jhon G The Barber en Booksy. Reserva con confirmación inmediata.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico" data-en="Classic">Clásico</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Haircut &amp; Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo de siempre: corte preciso y barba bien definida en la misma cita." data-en="The classic combo: a precise haircut and a well-defined beard in one visit.">El combo de siempre: corte preciso y barba bien definida en la misma cita.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">50min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba({ACCENT_GHOST_RGB[0]},{ACCENT_GHOST_RGB[1]},{ACCENT_GHOST_RGB[2]},0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">Firma de la casa</p>
          <h3 class="font-display text-2xl leading-snug mb-3">VIP King Full Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio completo: corte, barba, cejas y el trato VIP de principio a fin." data-en="The full service: haircut, beard, eyebrows and the VIP treatment start to finish.">El servicio completo: corte, barba, cejas y el trato VIP de principio a fin.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$56</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Look completo" data-en="Full look">Look completo</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Haircut, Beard &amp; Eyebrows</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte, barba y cejas perfiladas: el look completo en una sola cita." data-en="Haircut, beard and shaped eyebrows: the complete look in one visit.">Corte, barba y cejas perfiladas: el look completo en una sola cita.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$44</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">50min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para los más chicos" data-en="For the little ones">Para los más chicos</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Kid's Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Su primer fade o el de siempre, con la misma paciencia y el mismo cuidado." data-en="Their first fade or their usual one, with the same patience and care.">Su primer fade o el de siempre, con la misma paciencia y el mismo cuidado.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$24</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      <div class="reveal glass rounded-3xl p-7 sm:p-9 mt-8" style="transition-delay:120ms">
        <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="También en la barbería" data-en="Also at the shop">También en la barbería</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-3 text-sm">
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light">Haircut</span><span class="font-display text-[color:var(--accent-deep)]">$28</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light">Haircut and Eyebrows</span><span class="font-display text-[color:var(--accent-deep)]">$32 <span class="text-[color:var(--ink-40)] text-xs">· 40min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light">Beard and Shaved Head</span><span class="font-display text-[color:var(--accent-deep)]">$28</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light">Hot Towel Shave</span><span class="font-display text-[color:var(--accent-deep)]">$24</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light">Beard</span><span class="font-display text-[color:var(--accent-deep)]">$16 <span class="text-[color:var(--ink-40)] text-xs">· 20min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light">Shape Up</span><span class="font-display text-[color:var(--accent-deep)]">$25 <span class="text-[color:var(--ink-40)] text-xs">· 25min</span></span></div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 10 servicios y su disponibilidad completa están en Booksy. Reserva en línea." data-en="All 10 services and full availability are on Booksy. Book online.">Los 10 servicios y su disponibilidad completa están en Booksy. Reserva en línea.</span></p>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 4 tiles 3/4: 5 fotos reales curadas, sin selfies ni watermark)
# ============================================================
NEW_GALERIA = f'''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Cortes" data-en="Real">Cortes</span> <span class="text-shine" data-es="reales" data-en="cuts">reales</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @Jhong1706
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Listo para su cita" data-en="Ready for his appointment">Listo para su cita</span><img src="assets/raw/bk-16.jpg" alt="Niño en la silla con capa roja, listo para su corte en Jhon G The Barber" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Fade con textura" data-en="Textured fade">Fade con textura</span><img src="assets/raw/bk-6.jpg" alt="Fade en cabello rizado, detalle de la línea" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Line up limpio" data-en="Clean line up">Line up limpio</span><img src="assets/raw/bk-7.jpg" alt="Fade terminado dentro de la barbería" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Fade infantil" data-en="Kids fade">Fade infantil</span><img src="assets/raw/bk-10.jpg" alt="Niño sonriendo con su fade recién hecho, afuera de la barbería" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Otro cliente, la misma dedicación" data-en="Another client, same care">Otro cliente, la misma dedicación</span><img src="assets/raw/bk-15.jpg" alt="Niño en la silla de barbero con capa roja durante su corte" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 reseñas reales verbatim de Booksy, idioma original, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">Lo que dicen</span> <span class="text-shine" data-es="los clientes" data-en="say">los clientes</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 272 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 272 verified reviews on Booksy">5.0 de 5 · 272 reseñas verificadas en Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Pues que puedo decir todo fue bien VIP, ya casi a un mes de haberme recortado y sigo recibiendo piropos por el recorte. Estoy seguro que me ofrecio algo de agua pa beber que nunca llego pero se la cobro para la proxima. Super buena gente, profesional y cariñoso. Pal que habla english pues highly recommended."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Christian B…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"100% recomendado excelente trabajo"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carlos E…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"great cut"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Bimwa M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las reseñas en Booksy" data-en="Read reviews on Booksy">Leer las reseñas en Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

# ============================================================
# UBICACION (Direccion, Horario, Reservas, Instagram; sin telefono, no hay uno publico)
# ============================================================
MAPS_Q = '28.20159,-82.36459'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visítanos</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Wesley Chapel</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">27658 Cashford Circle Ste 102, Wesley Chapel, FL 33544</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba({ACCENT_GHOST_RGB[0]},{ACCENT_GHOST_RGB[1]},{ACCENT_GHOST_RGB[2]},0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes a viernes 10:00 am – 5:30 pm · Sábado 10:00 am – 6:00 pm · Domingo y lunes cerrado" data-en="Tuesday-Friday 10:00 AM - 5:30 PM · Saturday 10:00 AM - 6:00 PM · Closed Sunday and Monday">Martes a viernes 10:00 am – 5:30 pm · Sábado 10:00 am – 6:00 pm · Domingo y lunes cerrado</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba({ACCENT_GHOST_RGB[0]},{ACCENT_GHOST_RGB[1]},{ACCENT_GHOST_RGB[2]},0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and DM any questions before your appointment.">Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba({ACCENT_GHOST_RGB[0]},{ACCENT_GHOST_RGB[1]},{ACCENT_GHOST_RGB[2]},0.4)]" href="{IG}" target="_blank" rel="noopener">@Jhong1706</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Jhon G The Barber, 27658 Cashford Circle, Wesley Chapel FL"
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
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #191307 0%, #100c05 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cada corte, hecho con precisión." data-en="Every cut, made with precision.">Cada corte, hecho con precisión.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo fade" data-en="Your next fade">Tu próximo fade</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">empieza aquí</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu fade, tu barba o el VIP King Full Service que has estado esperando." data-en="Book online in seconds: your fade, your beard, or the VIP King Full Service you have been waiting for.">Reserva en línea en segundos: tu fade, tu barba o el VIP King Full Service que has estado esperando.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>
      </div>
    </div>
  </section>

  '''

print('OK: ubicacion + cta final definidos')

# ============================================================
# FOOTER (el merktop-badge original se mantiene intacto: badge_html)
# ============================================================
NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#0c0905]">
    <span class="foot-mark" aria-hidden="true">Jhon G Barber</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-1.jpg" alt="Jhon G The Barber" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba({HOVER_DARKBAND_RGB[0]},{HOVER_DARKBAND_RGB[1]},{HOVER_DARKBAND_RGB[2]},0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Jhon G The Barber</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería en Wesley Chapel, FL. Atención con cita previa." data-en="Barbershop in Wesley Chapel, FL. By appointment only.">Barbería en Wesley Chapel, FL. Atención con cita previa.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>27658 Cashford Circle Ste 102, Wesley Chapel, FL 33544</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#{ACCENT_MID.lstrip('#')}]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#{ACCENT_MID.lstrip('#')}]">Instagram · @Jhong1706</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Jhon G The Barber.</p>
        {badge_html}
      </div>
    </div>
  </footer>

  '''

# ============================================================
# BOTON FLOTANTE (aria-label ya en espanol de fabrica, sin traducir: ES por defecto)
# ============================================================
NEW_BOOKFLOAT = f'''<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>

  '''

# ============================================================
# TAIL: cursorRing + back-top + script. El esqueleto ya tiene aria-label
# "Volver arriba" en espanol -> ES por defecto no requiere traduccion.
# ============================================================
print('OK: footer + book-float + tail (sin cambios, ya en espanol)')

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

# sanity: las 6 marquee-word deben aparecer exactamente 4 veces cada una
for word in ['Fades', 'Diseños', 'Barba', 'Shape Up', 'VIP King', 'Wesley Chapel, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas en galeria (leftovers, selfies, watermark PhotoRoom) nunca deben aparecer
for banned in ['bk-2.jpg', 'bk-3.jpg', 'bk-4.jpg', 'bk-8.jpg', 'bk-9.jpg', 'bk-12.jpg', 'bk-13.jpg', 'bk-14.jpg']:
    assert f'assets/raw/{banned}' not in h_final, f'ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk',
                 'Silk Press', 'K-Tip', 'knotless', 'Knotless', 'hair studio']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/jhongthebarber-wesleychapel', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
