#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/mim-the-barber-lakeland/index.html
MIM The Barber (aka MIM'S Fade Room, same operator Michael Melendez), Lakeland FL. Boutique
solo-barber shop. Paleta verde bosque / jade (hue-shift + desaturado desde el dorado original
del esqueleto), grounded en los capes/fundas verdes reales visibles en las fotos del taller.
5.0 / 290 reviews en Booksy (self-verified live via JSON-LD, 2026-07-31). 8 servicios con
precios reales publicados en Booksy.
"""
import re
import os
import colorsys

SRC = 'templates/dark-v2/index.html'
DST = 'output/mim-the-barber-lakeland/index.html'

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
# 2. PALETA: dorado -> verde bosque / jade (hue-shift a ~152deg + saturacion x0.62,
#    computado con colorsys desde los hex reales del esqueleto)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(110, 85, 35), (122, 90, 30), (15, 11, 7), (180, 140, 60), (185, 138, 128), (212, 168, 75),
          (232, 207, 150), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]
# nota: (27,21,14) y (36,28,20) solo aparecen dentro del bloque .merktop-badge (protegido arriba).
TARGET_HUE = 152 / 360.0
SAT_MUL = 0.62


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

ACCENT_DEEP = _shift_hex('#d4a84b')   # '#65ba92'
ACCENT_MID = _shift_hex('#b8934a')    # '#5fa383'

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://booksy.com/en-us/388628_mim-the-barber_barber-shop_16013_lakeland'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
IG = 'https://www.instagram.com/mim_the_barber/'
rep_all(OLD_IG_URL, IG)

rep_all('@pure.artistrysk', '@mim_the_barber')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>MIM The Barber · Barbershop in Lakeland, FL | Fades, Beards &amp; Line-Ups | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="MIM The Barber, Lakeland FL: haircuts, fades, beard line-ups and facials with barber Michael Melendez. 5.0 rating across 290 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="MIM The Barber · Barbershop in Lakeland, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Haircuts, fades, beard line-ups and facials. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/shop-interior.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/owner.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Barbershop",
    "name": "MIM The Barber",
    "description": "Boutique barbershop in Lakeland, FL: haircuts, fades, beard line-ups and facials with barber Michael Melendez.",
    "address": { "@type": "PostalAddress", "streetAddress": "6950 Appaloosa Dr, Suite 27", "addressLocality": "Lakeland", "addressRegion": "FL", "postalCode": "33811", "addressCountry": "US" },
    "telephone": "+18636601188",
    "sameAs": ["https://booksy.com/en-us/388628_mim-the-barber_barber-shop_16013_lakeland", "https://www.instagram.com/mim_the_barber/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "290", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:30", "closes": "13:20" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "14:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barber services", "itemListElement": [
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut & Beard" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hair and Beard Line-up" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Facial" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Kids haircut 10 and under" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Senior citizen haircut 65+" } },
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Beard Only Line-up" } },
      { "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Ladies Neck Undercut" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: badge + paleta + globales + head/JSON-LD')

# ============================================================
# 5. IDIOMA: el esqueleto dark-v2 ya es EN default (negocio ingles) -> sin cambios
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
    <span class="pre-mono">MB</span>
    <span class="pre-word">MIM The Barber</span>
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
        <span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(101,186,146,0.35)] bg-[rgba(101,186,146,0.1)] text-[color:var(--accent-deep)]">MB</span>
        <span class="font-display text-xl tracking-[0.1em] uppercase">MIM <span class="text-[color:var(--accent-deep)]">Barber</span></span>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Lakeland, FL · Barbería" data-en="Lakeland, FL · Barbershop">Lakeland, FL · Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Un fade limpio, cada vez." data-en="A clean fade, every time.">A clean fade, every time.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, barba y" data-en="Fades, beards and">Fades, beards and</span><br /><span data-es="line-ups a " data-en="line-ups, done ">line-ups, done </span><span class="text-shine" data-es="mano de barbero" data-en="right">right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Michael Melendez atiende cada cita de uno en uno en su barbería boutique de Lakeland: cortes, fades, diseño de barba y faciales. 5.0 perfecto en 290 reseñas de Booksy." data-en="Michael Melendez runs every appointment one on one at his boutique Lakeland barbershop: haircuts, fades, beard line-ups and facials. A perfect 5.0 across 290 reviews on Booksy.">Michael Melendez runs every appointment one on one at his boutique Lakeland barbershop: haircuts, fades, beard line-ups and facials. A perfect 5.0 across 290 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 290 reseñas en Booksy" data-en="5.0 · 290 reviews on Booksy">5.0 · 290 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="tel:+18636601188" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span data-es="(863) 660-1188" data-en="(863) 660-1188">(863) 660-1188</span>
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/shop-interior.jpg" alt="Client seated in the chair at MIM The Barber wearing a shop branded t-shirt, Lakeland FL" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Haircut &amp; Beard</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$40 · 50min" data-en="$40 · 50min">$40 · 50min</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="290">290</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fade <span class="text-shine">&amp;</span> Line-Up</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Barba · Faciales" data-en="Beards · Facials">Beards · Facials</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Uno a uno" data-en="One on one">One on one</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Con Michael Melendez" data-en="With Michael Melendez">With Michael Melendez</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Lakeland</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Appaloosa Dr</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Haircuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Line-Ups</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Facials</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Booksy Online</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lakeland, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/fade-profile.jpg" alt="Close-up side profile of a fresh fade haircut at MIM The Barber" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/fade-result.jpg" alt="Finished fade result, back angle, at MIM The Barber" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="atención total" data-en="full attention">full attention</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="MIM The Barber es la barbería boutique de Michael Melendez en Lakeland: cortes, fades, diseño de barba y faciales, cita por cita, sin prisa y sin filas." data-en="MIM The Barber is Michael Melendez's boutique barbershop in Lakeland: haircuts, fades, beard design and facials, one appointment at a time, no rush and no crowding.">MIM The Barber is Michael Melendez's boutique barbershop in Lakeland: haircuts, fades, beard design and facials, one appointment at a time, no rush and no crowding.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus reseñas lo repiten cita tras cita: atención al detalle y un trato profesional. 5.0 perfecto en 290 reseñas de Booksy." data-en="His reviews say it appointment after appointment: attention to detail and a professional touch. A perfect 5.0 across 290 reviews on Booksy.">His reviews say it appointment after appointment: attention to detail and a professional touch. A perfect 5.0 across 290 reviews on Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="290">290</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/owner.jpg" alt="Michael Melendez, owner and barber at MIM The Barber" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(101,186,146,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Michael Melendez · <span class="text-[color:var(--ink-40)]" data-es="Dueño y barbero" data-en="Owner &amp; Barber">Owner &amp; Barber</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, o llamas al (863) 660-1188 y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, or call (863) 660-1188 and confirm instantly.">Pick your service on Booksy with clear price and duration, or call (863) 660-1188 and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El fade que buscas, el largo y la forma de la barba se conversan antes de tocar la máquina." data-en="The fade you want, the length and your beard shape get talked through before the clippers ever touch down.">The fade you want, the length and your beard shape get talked through before the clippers ever touch down.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El corte" data-en="The cut">The cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Michael trabaja el fade con precisión, uno a uno, desde el line-up hasta el acabado final." data-en="Michael works the fade with precision, one on one, from the line-up to the finished look.">Michael works the fade with precision, one on one, from the line-up to the finished look.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un corte nítido y la barba en forma. Tu próxima cita queda agendada antes de irte." data-en="You leave with a sharp cut and a shaped beard. Your next appointment gets booked before you go.">You leave with a sharp cut and a shaped beard. Your next appointment gets booked before you go.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (8 servicios reales de Booksy: 4 cards destacadas + bloque de precios completo)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="corte" data-en="cut">cut</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios publicados por MIM The Barber en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by MIM The Barber on Booksy. Booking confirms instantly.">Prices as published by MIM The Barber on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El corte de caballero de siempre, listo y bien fundido, con opción de recorte de ceja, nariz y oreja." data-en="The classic men's haircut, sharp and clean-blended, with an optional ear, nose and eyebrow trim.">The classic men's haircut, sharp and clean-blended, with an optional ear, nose and eyebrow trim.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(101,186,146,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y barba" data-en="Haircut &amp; Beard">Haircut &amp; Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio más reservado: corte completo más diseño de barba, terminado con precisión." data-en="The most booked service: a full haircut paired with beard design, finished with precision.">The most booked service: a full haircut paired with beard design, finished with precision.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">50min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Barba" data-en="Beard">Beard</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Línea de cabello y barba" data-en="Hair and Beard Line-up">Hair and Beard Line-up</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Line-up nítido de cabello y barba para mantener tu look entre cortes completos." data-en="A crisp hair and beard line-up to keep your look sharp between full haircuts.">A crisp hair and beard line-up to keep your look sharp between full haircuts.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cuidado facial" data-en="Skin care">Skin care</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Facial completo" data-en="Full Facial">Full Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Facial completo para complementar tu corte, de manos de Michael Melendez." data-en="A full facial to round out your visit, done by Michael Melendez.">A full facial to round out your visit, done by Michael Melendez.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="reveal glass rounded-3xl p-7 sm:p-9 mt-8" style="transition-delay:120ms">
        <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Precios completos" data-en="Full price list">Full price list</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-3 text-sm">
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Corte para niños (10 años o menos)" data-en="Kids haircut 10 and under">Kids haircut 10 and under</span><span class="font-display text-[color:var(--accent-deep)]">$25 <span class="text-[color:var(--ink-40)] text-xs">· 30min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Corte para adultos mayores (65+)" data-en="Senior citizen haircut 65+">Senior citizen haircut 65+</span><span class="font-display text-[color:var(--accent-deep)]">$25 <span class="text-[color:var(--ink-40)] text-xs">· 30min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Corte de nuca para dama" data-en="Ladies Neck Undercut">Ladies Neck Undercut</span><span class="font-display text-[color:var(--accent-deep)]">$15 <span class="text-[color:var(--ink-40)] text-xs">· 20min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Línea de barba solamente" data-en="Beard Only Line-up">Beard Only Line-up</span><span class="font-display text-[color:var(--accent-deep)]">$20 <span class="text-[color:var(--ink-40)] text-xs">· 20min</span></span></div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 8 servicios y su disponibilidad completa están en Booksy. Reserva en línea o llama al (863) 660-1188." data-en="All 8 services and full availability are on Booksy. Book online or call (863) 660-1188.">All 8 services and full availability are on Booksy. Book online or call (863) 660-1188.</span></p>
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
          @mim_the_barber
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Interior de la barbería" data-en="Shop interior">Shop interior</span><img src="assets/shop-interior.jpg" alt="Client seated in the chair at MIM The Barber wearing a shop branded t-shirt, Lakeland FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Fade fresco" data-en="Fresh fade">Fresh fade</span><img src="assets/fade-profile.jpg" alt="Close-up side profile of a fresh fade haircut at MIM The Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Acabado limpio" data-en="Clean finish">Clean finish</span><img src="assets/fade-result.jpg" alt="Finished fade result, back angle, at MIM The Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Otro angulo" data-en="Another angle">Another angle</span><img src="assets/fade-result-2.jpg" alt="Another finished fade, back of the head, at MIM The Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Transformación" data-en="Transformation">Transformation</span><img src="assets/mega-transformation.jpg" alt="Finished fade close-up, back of the head, in the shop at MIM The Barber" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
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
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 290 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 290 verified reviews on Booksy">5.0 out of 5 · 290 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I had a great experience at this barbershop. The haircut met all of my expectations, and I absolutely love how it turned out. The barber was professional, attentive, and made sure I got exactly what I wanted. I really appreciate the great service and attention to detail. I highly recommend this shop to anyone looking for a quality haircut. Thank you for the excellent experience!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yaritza R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dunier C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"El mejor sin duda alguna."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rafael F.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
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
MAPS_Q = '6950+Appaloosa+Dr+Suite+27,+Lakeland,+FL+33811'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Lakeland</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">6950 Appaloosa Dr, Suite 27, Lakeland, FL 33811</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(101,186,146,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes 9:30 am – 1:20 pm y 2:00 pm – 6:00 pm · Fin de semana cerrado" data-en="Monday-Friday 9:30 AM - 1:20 PM and 2:00 PM - 6:00 PM · Closed weekends">Monday-Friday 9:30 AM - 1:20 PM and 2:00 PM - 6:00 PM · Closed weekends</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy, o llama al (863) 660-1188 para reservar." data-en="By appointment via Booksy, or call (863) 660-1188 to book.">By appointment via Booksy, or call (863) 660-1188 to book.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(101,186,146,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and DM any questions before your appointment.">See the latest cuts and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(101,186,146,0.4)]" href="{IG}" target="_blank" rel="noopener">@mim_the_barber</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: MIM The Barber, 6950 Appaloosa Dr Suite 27, Lakeland FL"
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
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #0a1610 0%, #051009 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Un fade limpio, cada vez." data-en="A clean fade, every time.">A clean fade, every time.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo fade" data-en="Your next fade">Your next fade</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu corte, tu barba o ese facial que has estado planeando." data-en="Book online in seconds: your fade, your beard, or that facial you have been planning.">Book online in seconds: your fade, your beard, or that facial you have been planning.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="tel:+18636601188" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Llamar: (863) 660-1188" data-en="Call: (863) 660-1188">Call: (863) 660-1188</a>
      </div>
    </div>
  </section>

  '''

print('OK: ubicacion + cta final definidos')

# ============================================================
# FOOTER (el merktop-badge original se mantiene intacto: badge_html)
# ============================================================
NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#051009]">
    <span class="foot-mark" aria-hidden="true">MIM Barber</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/owner.jpg" alt="MIM The Barber" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(166,216,193,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">MIM The Barber</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería boutique en Lakeland, FL. Con cita previa vía Booksy o por teléfono." data-en="Boutique barbershop in Lakeland, FL. By appointment via Booksy or by phone.">Boutique barbershop in Lakeland, FL. By appointment via Booksy or by phone.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>6950 Appaloosa Dr, Suite 27, Lakeland, FL 33811</p>
        <p class="text-xs text-[color:var(--ink-40)]" data-es="Lun-Vie 9:30am-1:20pm y 2-6pm · Fin de semana cerrado" data-en="Mon-Fri 9:30am-1:20pm and 2-6pm · Weekends closed">Mon-Fri 9:30am-1:20pm and 2-6pm · Weekends closed</p>
        <p><a href="tel:+18636601188" class="hover:text-[#a6d8c1]">(863) 660-1188</a></p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#a6d8c1]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#a6d8c1]">Instagram · @mim_the_barber</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 MIM The Barber.</p>
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
for word in ['Haircuts', 'Fades', 'Beard Line-Ups', 'Facials', 'Booksy Online', 'Lakeland, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (leftovers del esqueleto o raw sin curar) nunca deben aparecer
for banned in ['assets/raw/']:
    assert banned not in h_final, f'ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk',
                 'silk press', 'Silk Press', 'K-Tip', 'knotless']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/mim-the-barber-lakeland', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
