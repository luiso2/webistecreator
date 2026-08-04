#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/labenditabarbershop/index.html
La Bendita Barbershop, owner Valeria "La Bendita" Perez, Miami Beach FL (1125 5th St).
High-end barbershop specializing in fades, beard design and cuts for every hair texture
including Afro-textured hair (grounded: Atly listing description + Men Hair Straightening
and Perm/Curls/Waves services + curl-texture photo). Paleta sapphire/navy blue (hue-shift +
desaturado desde el dorado original del esqueleto), el badge Merktop se queda dorado.
5.0 / 36 reviews on Booksy (self-verified via JSON-LD dossier, 2026-08-04). 13 servicios con
precios reales publicados en Booksy.
"""
import re
import os
import colorsys

SRC = 'templates/dark-v2/index.html'
DST = 'output/labenditabarbershop/index.html'

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
# 2. PALETA: dorado -> sapphire / navy blue (hue-shift a ~210deg + saturacion x0.92,
#    computado con colorsys desde los hex reales del esqueleto)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(110, 85, 35), (122, 90, 30), (15, 11, 7), (180, 140, 60), (185, 138, 128), (212, 168, 75),
          (232, 207, 150), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]
# nota: #f4eee2 y (27,21,14)/(36,28,20) solo aparecen dentro del bloque .merktop-badge (protegido).
TARGET_HUE = 210 / 360.0
SAT_MUL = 0.92


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

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://booksy.com/en-us/1318137_la-bendita-barbershop_barber-shop_15890_miami-beach'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
IG = 'https://www.instagram.com/labenditav/'
rep_all(OLD_IG_URL, IG)

rep_all('@pure.artistrysk', '@labenditav')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>La Bendita Barbershop · Miami Beach, FL | Fades, Beards &amp; Afro Cuts | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="La Bendita Barbershop, Miami Beach FL: fades, beard design, hair color and cuts for every texture, including Afro-textured hair. 5.0 with 36 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="La Bendita Barbershop · Miami Beach, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Fades, beard design and cuts for every texture. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/fade-profile.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/fade-profile.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Barbershop",
    "name": "La Bendita Barbershop",
    "description": "High-end barbershop in Miami Beach, FL run by Valeria \\"La Bendita\\" Perez: fades, beard design, hair color, straightening and curl/perm work for every hair texture, including Afro-textured hair.",
    "address": { "@type": "PostalAddress", "streetAddress": "1125 5th St", "addressLocality": "Miami Beach", "addressRegion": "FL", "postalCode": "33139", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.77457, "longitude": -80.14014 },
    "sameAs": ["https://booksy.com/en-us/1318137_la-bendita-barbershop_barber-shop_15890_miami-beach", "https://www.instagram.com/labenditav/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "36", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:30", "closes": "21:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "12:00", "closes": "17:30" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barber services", "itemListElement": [
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Male Haircut" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut + Beard" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "VIP Haircut+Beard (full service)" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut + Beard + Eyebrows" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Shape up" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Shape up + Beard" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Beard only" } },
      { "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Eyebrows" } },
      { "@type": "Offer", "price": "260", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Men Hair Color" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Men Hair Straightening" } },
      { "@type": "Offer", "price": "250", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Perm/Curls/Waves" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Female Haircut" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut + eyebrows" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: badge + paleta + globales + head/JSON-LD')

# ============================================================
# 5. IDIOMA: negocio EN default (reviews mayormente en ingles, sin mayoria clara en espanol)
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
    <span class="pre-mono">LB</span>
    <span class="pre-word">La Bendita</span>
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
        <span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(75,141,212,0.35)] bg-[rgba(75,141,212,0.1)] text-[color:var(--accent-deep)]">LB</span>
        <span class="font-display text-xl tracking-[0.1em] uppercase">La <span class="text-[color:var(--accent-deep)]">Bendita</span></span>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami Beach, FL · Barbería" data-en="Miami Beach, FL · Barbershop">Miami Beach, FL · Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Precisión en cada corte, para cada textura." data-en="Precision in every cut, for every texture.">Precision in every cut, for every texture.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, barba y" data-en="Fades, beards and">Fades, beards and</span><br /><span data-es="cada textura, " data-en="every texture, ">every texture, </span><span class="text-shine" data-es="bien hecho" data-en="done right">done right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Valeria &quot;La Bendita&quot; Pérez dirige esta barbería de alta gama a pasos de la calle 5 de Miami Beach: fades de precisión, diseño de barba y cortes para todo tipo de textura, incluido el cabello afro. Un 5.0 perfecto en 36 reseñas de Booksy." data-en="Valeria &quot;La Bendita&quot; Perez runs this high-end barbershop just off Miami Beach's 5th Street: precision fades, beard design and cuts for every hair texture, including Afro-textured hair. A perfect 5.0 across 36 reviews on Booksy.">Valeria "La Bendita" Perez runs this high-end barbershop just off Miami Beach's 5th Street: precision fades, beard design and cuts for every hair texture, including Afro-textured hair. A perfect 5.0 across 36 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 36 reseñas en Booksy" data-en="5.0 · 36 reviews on Booksy">5.0 · 36 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @labenditav
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/fade-profile.jpg" alt="Close-up side profile of a sharp fade haircut at La Bendita Barbershop, Miami Beach" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg" data-es="VIP Corte + Barba" data-en="VIP Haircut + Beard">VIP Haircut + Beard</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$100 · 1h 30min" data-en="$100 · 1h 30min">$100 · 1h 30min</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="36">36</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Afro Cuts</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Barba · Color · Textura" data-en="Beards · Color · Texture">Beards · Color · Texture</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Una artista" data-en="One artist">One artist</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Valeria &quot;La Bendita&quot;</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">5th Street</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Design</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Afro Cuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hair Color</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Perms &amp; Waves</span><span class="marquee-star">✦</span>
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
          <img src="assets/curl-texture.jpg" alt="Close-up of finished curl and coil texture work at La Bendita Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/crown-part.jpg" alt="Precision part and fade detail from the crown, La Bendita Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="cada textura" data-en="every texture">every texture</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="La Bendita Barbershop es la barbería de alta gama de Valeria &quot;La Bendita&quot; Pérez en la calle 5 de Miami Beach: fades, diseño de barba, color, alisado y trabajo de rizos para todo tipo de cabello, incluido el afro." data-en="La Bendita Barbershop is Valeria &quot;La Bendita&quot; Perez's high-end barbershop on Miami Beach's 5th Street: fades, beard design, color, straightening and curl work for every hair type, including Afro-textured hair.">La Bendita Barbershop is Valeria "La Bendita" Perez's high-end barbershop on Miami Beach's 5th Street: fades, beard design, color, straightening and curl work for every hair type, including Afro-textured hair.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus reseñas lo repiten una y otra vez: atención al detalle y un ambiente al que la gente vuelve. Un 5.0 perfecto en 36 reseñas de Booksy." data-en="Her reviews say it again and again: sharp attention to detail and a shop people keep coming back to. A perfect 5.0 across 36 reviews on Booksy.">Her reviews say it again and again: sharp attention to detail and a shop people keep coming back to. A perfect 5.0 across 36 reviews on Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="36">36</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/owner.jpg" alt="Valeria Perez, owner and barber at La Bendita Barbershop" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,141,212,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Valeria &quot;La Bendita&quot; Pérez · <span class="text-[color:var(--ink-40)]" data-es="Dueña y barbera" data-en="Owner &amp; Barber">Owner &amp; Barber</span></span>
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
NEW_METODO = f'''<!-- EL METODO -->
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio claro, de un shape up a un tratamiento completo de rizos, y confirmas al instante." data-en="Pick your service on Booksy with clear pricing, from a Shape Up to a full Perm/Curls/Waves treatment, and confirm instantly.">Pick your service on Booksy with clear pricing, from a Shape Up to a full Perm/Curls/Waves treatment, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu textura de cabello, el fade que buscas y la forma de tu barba se conversan antes de tocar la máquina." data-en="Your hair texture, the fade you want and your beard shape get talked through before the clippers start.">Your hair texture, the fade you want and your beard shape get talked through before the clippers start.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El corte" data-en="The cut">The cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Valeria trabaja con precisión, un cliente a la vez, desde el line-up hasta el acabado de textura." data-en="Valeria works with precision, one client at a time, from the line-up to the finished texture work.">Valeria works with precision, one client at a time, from the line-up to the finished texture work.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un look nítido y listo para cámara. Tu próxima cita queda agendada antes de irte." data-en="You leave with a sharp, camera-ready look. Your next appointment gets booked before you go.">You leave with a sharp, camera-ready look. Your next appointment gets booked before you go.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (13 servicios reales de Booksy: 4 cards destacadas + precios completos)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="corte" data-en="cut">cut</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por La Bendita Barbershop en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by La Bendita Barbershop on Booksy. Booking confirms instantly.">Prices and durations as published by La Bendita Barbershop on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y barba" data-en="Haircut &amp; Beard">Haircut &amp; Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo de siempre: corte completo y diseño de barba, terminado con precisión." data-en="The everyday combo: a full haircut paired with beard design, finished with precision.">The everyday combo: a full haircut paired with beard design, finished with precision.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(75,141,212,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="VIP Corte + Barba" data-en="VIP Haircut + Beard">VIP Haircut + Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio completo: corte, barba y el tiempo dedicado para que todo salga perfecto." data-en="The full service: haircut, beard and the dedicated time to get every detail right.">The full service: haircut, beard and the dedicated time to get every detail right.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Afro y textura" data-en="Afro &amp; Texture">Afro &amp; Texture</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Alisado para hombre" data-en="Men Hair Straightening">Men Hair Straightening</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Alisado profesional pensado para cabello afro y de textura densa, con acabado limpio y natural." data-en="Professional straightening built for Afro and dense-textured hair, finished clean and natural.">Professional straightening built for Afro and dense-textured hair, finished clean and natural.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Trabajo de rizos" data-en="Texture work">Texture work</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Perm/Curls/Waves</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Permanente, definición de rizos u ondas: trabajo de textura completo, de principio a fin." data-en="Perm, curl definition or waves: full texture work, start to finish.">Perm, curl definition or waves: full texture work, start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$250</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="reveal glass rounded-3xl p-7 sm:p-9 mt-8" style="transition-delay:120ms">
        <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Precios completos" data-en="Full price list">Full price list</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-3 text-sm">
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Corte de caballero" data-en="Male Haircut">Male Haircut</span><span class="font-display text-[color:var(--accent-deep)]">$50</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Corte + Barba + Cejas" data-en="Haircut + Beard + Eyebrows">Haircut + Beard + Eyebrows</span><span class="font-display text-[color:var(--accent-deep)]">$70 <span class="text-[color:var(--ink-40)] text-xs">· 1h 10min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Shape up" data-en="Shape up">Shape up</span><span class="font-display text-[color:var(--accent-deep)]">$25 <span class="text-[color:var(--ink-40)] text-xs">· 15min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Shape up + Barba" data-en="Shape up + Beard">Shape up + Beard</span><span class="font-display text-[color:var(--accent-deep)]">$35 <span class="text-[color:var(--ink-40)] text-xs">· 35min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Solo barba" data-en="Beard only">Beard only</span><span class="font-display text-[color:var(--accent-deep)]">$30 <span class="text-[color:var(--ink-40)] text-xs">· 20min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Cejas" data-en="Eyebrows">Eyebrows</span><span class="font-display text-[color:var(--accent-deep)]">$15 <span class="text-[color:var(--ink-40)] text-xs">· 5min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Color para hombre" data-en="Men Hair Color">Men Hair Color</span><span class="font-display text-[color:var(--accent-deep)]">$260 <span class="text-[color:var(--ink-40)] text-xs">· 3h</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Corte de dama" data-en="Female Haircut">Female Haircut</span><span class="font-display text-[color:var(--accent-deep)]">$75 <span class="text-[color:var(--ink-40)] text-xs">· 1h 15min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Corte + Cejas" data-en="Haircut + eyebrows">Haircut + eyebrows</span><span class="font-display text-[color:var(--accent-deep)]">$55 <span class="text-[color:var(--ink-40)] text-xs">· 50min</span></span></div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 13 servicios y su disponibilidad completa están en Booksy. Reserva en línea cuando quieras." data-en="All 13 services and full availability are on Booksy. Book online any time.">All 13 services and full availability are on Booksy. Book online any time.</span></p>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 4 tiles 3/4: 5 fotos reales curadas)
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
          @labenditav
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Acabado fresco" data-en="Fresh finish">Fresh finish</span><img src="assets/wavy-finish.jpg" alt="Finished wavy haircut result at La Bendita Barbershop, Miami Beach" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Fade nítido" data-en="Sharp fade">Sharp fade</span><img src="assets/fade-profile.jpg" alt="Close-up side profile of a sharp fade haircut at La Bendita Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Raya limpia" data-en="Clean part">Clean part</span><img src="assets/crown-part.jpg" alt="Precision hair part detail from the crown at La Bendita Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Side part pulido" data-en="Slick side part">Slick side part</span><img src="assets/side-part.jpg" alt="Slick side part haircut, back angle, at La Bendita Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Trabajo de textura" data-en="Texture work">Texture work</span><img src="assets/curl-texture.jpg" alt="Close-up of finished curl and coil texture work at La Bendita Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 reseñas reales verbatim de Booksy, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="los clientes" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 36 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 36 verified reviews on Booksy">5.0 out of 5 · 36 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Everywhere I go people are asking me who cuts my hair!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jovanny M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great cut, attention to detail was on point, and the service was top-notch. Highly recommend."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Christian S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent. High skin fade faded into the beard and cleaned up the lines. Perfect. Scheduling my next appointment now 👍🏼"</blockquote>
          <figcaption class="text-sm"><span class="font-medium" data-es="Cliente de Booksy" data-en="Booksy Client">Booksy Client</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las reseñas en Booksy" data-en="Read reviews on Booksy">Read reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

# ============================================================
# UBICACION (Direccion, Horario, Reservas, Instagram)
# ============================================================
MAPS_Q = '1125+5th+St,+Miami+Beach,+FL+33139'
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
              <p class="text-sm text-[color:var(--ink-60)] font-light">1125 5th St, Miami Beach, FL 33139</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,141,212,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sábado 9:30 am – 9:00 pm · Domingo 12:00 pm – 5:30 pm" data-en="Monday-Saturday 9:30 AM - 9:00 PM · Sunday 12:00 PM - 5:30 PM">Monday-Saturday 9:30 AM - 9:00 PM · Sunday 12:00 PM - 5:30 PM</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,141,212,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and DM any questions before your appointment.">See the latest cuts and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,141,212,0.4)]" href="{IG}" target="_blank" rel="noopener">@labenditav</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: La Bendita Barbershop, 1125 5th St, Miami Beach FL"
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
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #0a1420 0%, #050d16 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Precisión en cada corte, para cada textura." data-en="Precision in every cut, for every texture.">Precision in every cut, for every texture.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo corte" data-en="Your next cut">Your next cut</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu fade, tu barba o ese cambio de textura que has estado planeando." data-en="Book online in seconds: your fade, your beard, or that texture change you have been planning.">Book online in seconds: your fade, your beard, or that texture change you have been planning.</p>
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
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#050d16]">
    <span class="foot-mark" aria-hidden="true">La Bendita</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/owner.jpg" alt="La Bendita Barbershop" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(166,193,216,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">La Bendita Barbershop</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería de alta gama en Miami Beach, FL. Con cita previa vía Booksy." data-en="High-end barbershop in Miami Beach, FL. By appointment via Booksy.">High-end barbershop in Miami Beach, FL. By appointment via Booksy.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>1125 5th St, Miami Beach, FL 33139</p>
        <p class="text-xs text-[color:var(--ink-40)]" data-es="Lun-Sáb 9:30am-9pm · Dom 12-5:30pm" data-en="Mon-Sat 9:30am-9pm · Sun 12-5:30pm">Mon-Sat 9:30am-9pm · Sun 12-5:30pm</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#a6c1d8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#a6c1d8]">Instagram · @labenditav</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 La Bendita Barbershop.</p>
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
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#050c07" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
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
for word in ['Fades', 'Beard Design', 'Afro Cuts', 'Hair Color', 'Perms &amp; Waves', 'Miami Beach, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (leftovers del esqueleto o raw sin curar) nunca deben aparecer
for banned in ['assets/raw/']:
    assert banned not in h_final, f'ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk',
                  'silk press', 'Silk Press', 'K-Tip', 'knotless', '234 review']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/labenditabarbershop', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
