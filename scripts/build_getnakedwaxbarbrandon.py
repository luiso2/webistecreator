#!/usr/bin/env python3
"""Derivacion anclada: templates/light-v2/index.html -> output/getnakedwaxbarbrandon/index.html
Get Naked Wax Bar (dba Lush Aesthetics By Tatiana), Brandon FL. Solo waxing studio, owner
Tatiana Mclaughlin, 15+ years experience, inside Heads Up Barbershop #1. Palette: raspberry
magenta (hue-shift from the plum-pink original toward a vivid hot-pink/raspberry, matching the
business's real hot-pink brand graphics). 5.0 / 164 reviews on Booksy. 51 real services.
Severe photo desert (IG feed is mostly text-overlay promo graphics / owner selfies): only 3
usable real photos survived curation (real wall signage, owner with wax warmer, treatment room
interior) -> gallery intentionally kept small (2 tiles) rather than padded with unusable shots.
"""
import json
import os
import re

SRC = 'templates/light-v2/index.html'
DST = 'output/getnakedwaxbarbrandon/index.html'

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
# 1. PALETA: plum-pink -> raspberry magenta (no toca el badge dorado, sin colision)
# ============================================================
HEX_PAIRS = [
    ("#a04a72", "#b0175f"),   # accent-deep
    ("#c47a9c", "#e2569a"),   # accent-mid
    ("#f3e0ea", "#f8e3ec"),   # bg-2 / accent-soft
    ("#faf2f6", "#fdf7f4"),   # bg
    ("#33222c", "#241a1e"),   # ink
    ("#7d3457", "#7a0f45"),   # accent dark (btn-3d/step-num bottom stop)
    ("#5c2140", "#5c0d34"),   # btn shadow
    ("#f2d5e3", "#f7cfe1"),   # orb-a
    ("#d9a8c2", "#edb0cd"),   # orb-b
    ("#e5c1d4", "#f2c0da"),   # orb-c
    ("#c9789f", "#e478a8"),   # text-shine stop2
    ("#5f2c48", "#6b0f3f"),   # text-shine stop3
    ("#b25a85", "#c93670"),   # text-shine stop5
    ("#f0bed7", "#f9a8ce"),   # dark-band pink (stars/text-shine/ring)
    ("#f8dfeb", "#fcd9e8"),   # dark-band text-shine stop2
    ("#f2cfe0", "#f6bedd"),   # dark-band text-shine stop5
    ("#fbeff5", "#fdeaf3"),   # dark-band btn-3d stop1
    ("#efd0e0", "#f6c3dc"),   # dark-band btn-3d stop2
    ("#d3a2bc", "#dd8fb5"),   # dark-band btn-3d stop3
    ("#8a5573", "#8a2f5c"),   # dark-band btn shadow
    ("#dc9dbe", "#e58fb8"),   # scroll-progress stop3
    ("#2a1722", "#200a14"),   # CTA bg gradient stop1
    ("#1f0f18", "#150810"),   # CTA bg gradient stop2
    ("#1c0f16", "#170a10"),   # footer bg
    ("#f6f1ea", "#fdf7f4"),   # theme-color meta
]
for old, new in HEX_PAIRS:
    rep_all(old, new)

RGBA_PAIRS = [
    ((51, 34, 44), (36, 26, 30)),        # ink
    ((160, 74, 114), (176, 23, 95)),     # accent-deep
    ((240, 190, 215), (249, 168, 206)),  # dark-band pink family
    ((185, 138, 128), (200, 110, 150)),  # dark-band orb-b
    ((233, 205, 186), (238, 150, 195)),  # dark-band accent-ghost
    ((70, 25, 50), (74, 12, 42)),        # btn-3d inset shadow (light)
    ((125, 52, 87), (138, 30, 80)),      # btn-3d inset shadow (dark-band)
    ((250, 242, 246), (253, 247, 244)),  # bg in rgb form
    ((253, 246, 250), (255, 249, 251)),  # surface in rgb form
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_PAIRS:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

print('OK: paleta')

# ============================================================
# 2. GLOBALES: Booksy, Instagram
# ============================================================
BK = 'https://booksy.com/en-us/785108_get-naked-wax-bar_hair-removal_15746_brandon'
IG = 'https://www.instagram.com/getnakedwaxbar/'
FB = 'https://www.facebook.com/Getnakedwaxbar/'
PHONE_DISPLAY = '(910) 373-8228'
PHONE_TEL = '+19103738228'

OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
rep_all(OLD_IG_URL, IG)

rep_all('@_lashbloom', '@getnakedwaxbar')

print('OK: globales')

# ============================================================
# 3. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Get Naked Wax Bar · Waxing Studio in Brandon, FL | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Get Naked Wax Bar, Brandon FL: Brazilian, bikini, brow and full body waxing with owner Tatiana Mclaughlin. 5.0 rating across 164 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Get Naked Wax Bar · Waxing Studio in Brandon, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Brazilian, brow and full body waxing with Tatiana Mclaughlin. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/sign-wide.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
)

jsonld = {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Get Naked Wax Bar",
    "description": "Waxing studio in Brandon, FL inside Heads Up Barbershop #1: Brazilian, bikini, brow and full body waxing with owner and aesthetician Tatiana Mclaughlin, 15+ years of experience.",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "106 E Bloomingdale Ave (inside Heads Up Barbershop #1)",
        "addressLocality": "Brandon",
        "addressRegion": "FL",
        "postalCode": "33511",
        "addressCountry": "US",
    },
    "telephone": PHONE_TEL,
    "sameAs": [BK, IG, FB],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "164", "bestRating": "5"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Thursday"], "opens": "09:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday"], "opens": "09:00", "closes": "18:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:00", "closes": "16:00"},
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Waxing services",
        "itemListElement": [
            {"@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Bikini Wax"}},
            {"@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Brazilian Wax"}},
            {"@type": "Offer", "price": "165", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "The Naked Experience"}},
            {"@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Manzilian Wax"}},
        ],
    },
}
NEW_JSONLD = '<script type="application/ld+json">\n  ' + json.dumps(jsonld, indent=2) + '\n  </script>'
m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: head + JSON-LD')

# ============================================================
# 4. IDIOMA: light-v2 ya es EN default (negocio ingles) -> sin cambios
# ============================================================
assert "applyLang(lang === 'es' ? 'es' : 'en')" in h
assert '<html lang="en"' in h

# ============================================================
# 5. SEGMENTACION POR ANCLAS DE COMENTARIO
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

print('OK: segmentacion')

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = """<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">GN</span>
    <span class="pre-word">Get Naked Wax Bar</span>
    <span class="pre-line"></span>
  </div>

  """

# ============================================================
# NAV
# ============================================================
NEW_NAV = f"""<!-- NAV -->
  <header id="nav" class="fixed top-0 inset-x-0 z-50">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 h-[72px] flex items-center justify-between">
      <a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/logo.jpg" alt="Get Naked Wax Bar" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(176,23,95,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Get Naked <span class="text-[color:var(--accent-deep)]">Wax Bar</span></span>
      </a>
      <nav class="hidden md:flex items-center gap-7 text-sm font-light">
        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>
        <a class="nav-link" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>
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
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>
      </nav>
    </div>
  </header>

  """

# ============================================================
# HERO
# ============================================================
NEW_HERO = f"""<!-- HERO -->
  <section id="top" class="relative min-h-screen flex items-center grain overflow-hidden pt-28 pb-16">
    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Brandon, FL · Estudio de Depilación" data-en="Brandon, FL · Waxing Studio">Brandon, FL · Waxing Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Piel suave, con calma de verdad." data-en="Smooth skin, real care.">Smooth skin, real care.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Depilación brasileña, de cejas" data-en="Brazilian, brow and body">Brazilian, brow and body</span><br /><span data-es="y de cuerpo, hecha con " data-en="waxing, done with ">waxing, done with </span><span class="text-shine" data-es="calma real" data-en="real care">real care</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Tatiana Mclaughlin lleva más de 15 años depilando y atiende cada cita ella misma dentro de Heads Up Barbershop en Brandon: brasileña, bikini, cejas y cuerpo completo con cera dura. 5.0 perfecto en 164 reseñas de Booksy." data-en="Tatiana Mclaughlin has been waxing for over 15 years and runs every appointment herself inside Heads Up Barbershop in Brandon: Brazilian, bikini, brow and full body waxing with hard wax. A perfect 5.0 across 164 reviews on Booksy.">Tatiana Mclaughlin has been waxing for over 15 years and runs every appointment herself inside Heads Up Barbershop in Brandon: Brazilian, bikini, brow and full body waxing with hard wax. A perfect 5.0 across 164 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 164 reseñas en Booksy" data-en="5.0 · 164 reviews on Booksy">5.0 · 164 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @getnakedwaxbar
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/studio-room.jpg" alt="Treatment room at Get Naked Wax Bar, Brandon FL, with pink neon sign" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Brazilian Wax</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$75 · 30min" data-en="$75 · 30min">$75 · 30min</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  """

# ============================================================
# STRIP DE CONFIANZA
# ============================================================
NEW_STRIP = """<!-- STRIP DE CONFIANZA -->
  <section class="relative border-y border-[color:var(--accent-ghost)] bg-[color:var(--bg-2)]">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="164">164</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Brazilian <span class="text-shine">&amp;</span> Body</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cera · Cejas" data-en="Wax · Brows">Wax · Brows</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">15+ <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="De experiencia" data-en="Of experience">Of experience</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Brandon</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">E Bloomingdale Ave</p></div>
    </div>
  </section>

  """

print('OK: preloader + nav + hero + strip')

# ============================================================
# MARQUEE (misma lista en los dos marquees)
# ============================================================
MARQUEE_SEQ = """      <div class="marquee-seq">
        <span class="marquee-word">Brazilian Wax</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Bikini Wax</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Manzilian Wax</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Full Body Wax</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brandon, FL</span><span class="marquee-star">✦</span>
      </div>
"""
NEW_MARQUEE1 = """<!-- MARQUEE -->
  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
""" + MARQUEE_SEQ + MARQUEE_SEQ + """    </div>
  </div>

  """
NEW_MARQUEE2 = """<!-- MARQUEE -->
  <div class="marquee marquee-reverse" aria-hidden="true">
    <div class="marquee-track">
""" + MARQUEE_SEQ + MARQUEE_SEQ + """    </div>
  </div>

  """

# ============================================================
# LA EXPERIENCIA
# ============================================================
NEW_EXPERIENCIA = """<!-- LA EXPERIENCIA -->
  <section id="experiencia" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">01</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-14 items-center">
      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/owner-wax.jpg" alt="Tatiana Mclaughlin with a wax warmer at Get Naked Wax Bar" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/studio-decor.jpg" alt="Studio corner at Get Naked Wax Bar with pink neon sign and plant" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Solo Tatiana," data-en="Just Tatiana,">Just Tatiana,</span><br /><span class="text-shine" data-es="de principio a fin" data-en="start to finish">start to finish</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Get Naked Wax Bar es el estudio de una sola profesional, Tatiana Mclaughlin, dentro de Heads Up Barbershop en Brandon. Lleva más de 15 años depilando y atiende cada cita ella misma, desde un diseño rápido de cejas hasta un cuerpo completo." data-en="Get Naked Wax Bar is the solo studio of Tatiana Mclaughlin, inside Heads Up Barbershop in Brandon. She has been waxing for over 15 years and handles every single appointment herself, from a quick brow shape to a full body wax.">Get Naked Wax Bar is the solo studio of Tatiana Mclaughlin, inside Heads Up Barbershop in Brandon. She has been waxing for over 15 years and handles every single appointment herself, from a quick brow shape to a full body wax.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Le encanta educar a sus clientas mientras trabaja: repasa tipo de piel, medicamentos y cuidado posterior para que nada sea sorpresa. El resultado: 5.0 perfecto en 164 reseñas verificadas de Booksy." data-en="She loves educating her clients while she works, walking through skin type, medications and aftercare so nothing about the process is a surprise. The result: a perfect 5.0 across 164 verified reviews on Booksy.">She loves educating her clients while she works, walking through skin type, medications and aftercare so nothing about the process is a surprise. The result: a perfect 5.0 across 164 verified reviews on Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="164">164</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Get Naked Wax Bar" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(176,23,95,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Tatiana Mclaughlin · <span class="text-[color:var(--ink-40)]" data-es="Dueña y especialista en depilación" data-en="Owner &amp; wax specialist">Owner &amp; wax specialist</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  """

print('OK: marquee x2 + experiencia')

# ============================================================
# EL METODO
# ============================================================
NEW_METODO = f"""<!-- EL METODO -->
  <section id="metodo" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">02</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How a visit">How a visit</span> <span class="text-shine" data-es="aquí" data-en="goes">goes</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio claro, o llamas o escribes al {PHONE_DISPLAY} para confirmar." data-en="Pick your service on Booksy with clear pricing, or call or text {PHONE_DISPLAY} to confirm.">Pick your service on Booksy with clear pricing, or call or text {PHONE_DISPLAY} to confirm.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tatiana repasa tipo de piel, medicamentos y lo que buscas antes de tocar la cera." data-en="Tatiana checks in on skin type, medications and what you want before she ever touches the wax pot.">Tatiana checks in on skin type, medications and what you want before she ever touches the wax pot.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="La cera" data-en="The wax">The wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cera dura, aplicada rápido y retirada limpia, dentro de Heads Up Barbershop en Brandon." data-en="Hard wax, applied fast and pulled clean, right inside Heads Up Barbershop in Brandon.">Hard wax, applied fast and pulled clean, right inside Heads Up Barbershop in Brandon.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con indicaciones reales de cuidado posterior y tu próxima cita ya agendada." data-en="You leave with real aftercare guidance and your next appointment already on the books.">You leave with real aftercare guidance and your next appointment already on the books.</p>
        </div>
      </div>
    </div>
  </section>

  """

print('OK: metodo')

# ============================================================
# SERVICIOS (4 cards destacadas + menu completo de 47 servicios, agrupado por categoria)
# ============================================================
FEATURED_CARDS = f"""      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Todos los días" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Bikini Wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Contorno de bikini limpio y rápido con cera dura, ideal para mantenimiento entre citas grandes." data-en="Clean, quick bikini-line shaping with hard wax, ideal upkeep between the bigger appointments.">Clean, quick bikini-line shaping with hard wax, ideal upkeep between the bigger appointments.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(176,23,95,0.4); box-shadow: 0 18px 50px rgba(36,26,30,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Brazilian Wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio más reservado de Get Naked: brasileña completa con cera dura, rápida y casi sin dolor." data-en="Get Naked's most booked service: a full Brazilian with hard wax, done fast and about as painless as it gets.">Get Naked's most booked service: a full Brazilian with hard wax, done fast and about as painless as it gets.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Ritual completo" data-en="Full ritual">Full ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="La Experiencia Naked" data-en="The Naked Experience">The Naked Experience</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo firma de Tatiana: vapor, cera brasileña y mascarilla hidrojelly para máxima comodidad." data-en="Tatiana's signature combo: steam, a Brazilian wax and a hydrojelly mask finish for maximum comfort.">Tatiana's signature combo: steam, a Brazilian wax and a hydrojelly mask finish for maximum comfort.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$165</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para él" data-en="For him">For him</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manzilian Wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Depilación brasileña para hombre, con el mismo cuidado y precisión que cualquier otro servicio." data-en="Men's Brazilian wax, handled with the same care and precision as every other service here.">Men's Brazilian wax, handled with the same care and precision as every other service here.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
"""

# (name_en, name_es, price, duration_or_None)
CATEGORIES = [
    ("Brazilian &amp; Bikini", "Brasileña y Bikini", [
        ("Bikini Full Wax", "Cera de Bikini Completo", 55, None),
        ("Inner Cheek Strip", "Franja Interna", 25, None),
        ("Inner Thigh", "Muslo Interno", 20, None),
        ("Manzilian W/ Steam", "Manzilian con Vapor", 100, None),
        ("Manzilian W/ Steam &amp; Mask", "Manzilian con Vapor y Mascarilla", 135, "1h 20min"),
    ]),
    ("Brows &amp; Face", "Cejas y Rostro", [
        ("Eyebrow Wax", "Cera de Cejas", 18, "15min"),
        ("Eyebrow Tint", "Tinte de Cejas", 40, None),
        ("Eyebrow Lamination", "Laminado de Cejas", 55, None),
        ("Brow Pampering", "Cuidado de Cejas", 40, None),
        ("Brow Deluxe Pampering - Lamination", "Cuidado Deluxe - Laminado", 120, "45min"),
        ("Brow Deluxe Pampering - Lamination &amp; Dye", "Cuidado Deluxe - Laminado y Tinte", 145, "1h"),
        ("Brow Correction", "Corrección de Cejas", 395, "2h 30min"),
        ("Powder Brows", "Cejas en Polvo", 350, "2h 30min"),
        ("4-8 Week Touch Up", "Retoque de 4-8 Semanas", 100, None),
        ("Touch Up", "Retoque (consulta precio en estudio)", 275, "2h 30min"),
        ("Full Face Wax", "Cera de Rostro Completo", 65, None),
        ("Lip Wax", "Cera de Labio", 15, "15min"),
        ("Chin Wax", "Cera de Mentón", 15, "15min"),
        ("Side Burns", "Patillas", 18, "15min"),
        ("Nose Wax", "Cera de Nariz", 15, "15min"),
        ("Ear Wax", "Cera de Oídos", 15, "15min"),
    ]),
    ("Body Waxing", "Depilación Corporal", [
        ("Chest Wax", "Cera de Pecho", 65, None),
        ("Beard Wax", "Cera de Barba", 30, None),
        ("Underarm Wax", "Cera de Axilas", 25, None),
        ("Back Wax", "Cera de Espalda", 65, None),
        ("Lower Back", "Espalda Baja", 35, None),
        ("Leg Wax - Half", "Cera de Piernas - Media", 65, None),
        ("Leg Wax - Full", "Cera de Piernas - Completa", 85, None),
        ("Junior Full Legs", "Piernas Completas Junior", 65, None),
        ("Arm Wax - Half", "Cera de Brazos - Media", 35, None),
        ("Arm Wax - Full", "Cera de Brazos - Completa", 55, None),
        ("Neck", "Cuello", 20, None),
        ("Stomach Wax", "Cera de Abdomen", 45, "30min"),
        ("Glutes", "Glúteos", 40, None),
        ("Toes", "Dedos de los Pies", 20, None),
        ("Head Wax", "Cera de Cabeza", 45, "30min"),
    ]),
    ("Full Body &amp; Rituals", "Cuerpo Completo y Rituales", [
        ("Men's Full Body Wax", "Cuerpo Completo para Hombre", 300, "3h 30min"),
        ("Women's Full Body", "Cuerpo Completo para Mujer", 220, "2h"),
        ("Hydrojelly Mask", "Mascarilla Hidrojelly", 25, None),
        ("Steam", "Vapor", 35, None),
        ("Steam W/ Brazilian", "Vapor con Brasileña", 90, "35min"),
        ("Steam W/ Brazilian &amp; Hydrojelly Mask", "Vapor con Brasileña y Mascarilla", 110, "1h"),
        ("Consultation", "Consulta", 25, None),
        ("Extractions", "Extracciones (consulta detalles)", 30, None),
        ("Body Extractions", "Extracciones Corporales", 40, None),
        ("Ingrown Hair Extraction", "Extracción de Vello Encarnado", 25, None),
    ]),
    ("Training", "Entrenamiento", [
        ("One-on-One Hard Wax Training", "Entrenamiento Individual de Cera Dura", 575, "5h"),
    ]),
]

cat_blocks = []
for title_en, title_es, items in CATEGORIES:
    rows = []
    for name_en, name_es, price, dur in items:
        dur_html = f' <span class="text-[color:var(--ink-40)] text-xs">· {dur}</span>' if dur else ''
        rows.append(
            f'          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2">'
            f'<span class="font-light" data-es="{name_es}" data-en="{name_en}">{name_en}</span>'
            f'<span class="font-display text-[color:var(--accent-deep)]">${price}{dur_html}</span></div>'
        )
    cat_blocks.append(
        f'        <div>\n          <p class="text-xs tracking-[0.2em] uppercase text-[color:var(--ink-40)] mb-3 mt-2" data-es="{title_es}" data-en="{title_en}">{title_en}</p>\n'
        + '\n'.join(rows) + '\n        </div>'
    )

FULL_MENU = f"""      <div class="reveal glass rounded-3xl p-7 sm:p-9 mt-8" style="transition-delay:120ms">
        <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Menú completo · 51 servicios" data-en="Full menu · 51 services">Full menu · 51 services</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-6 text-sm">
{chr(10).join(cat_blocks)}
        </div>
      </div>
"""

NEW_SERVICIOS = f"""<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios publicados por Get Naked Wax Bar en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by Get Naked Wax Bar on Booksy. Booking confirms instantly.">Prices as published by Get Naked Wax Bar on Booksy. Booking confirms instantly.</p>
      </div>
{FEATURED_CARDS}{FULL_MENU}      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 51 servicios y su disponibilidad completa están en Booksy. Reserva en línea o llama o escribe al {PHONE_DISPLAY}." data-en="All 51 services and full availability are on Booksy. Book online or call or text {PHONE_DISPLAY}.">All 51 services and full availability are on Booksy. Book online or call or text {PHONE_DISPLAY}.</span></p>
    </div>
  </section>

  """

print('OK: servicios (4 cards + 47 en menu completo)')

# ============================================================
# GALERIA (2 fotos reales curadas: firma en la pared + sala de tratamiento)
# ============================================================
NEW_GALERIA = f"""<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Dentro del" data-en="Inside the">Inside the</span> <span class="text-shine" data-es="estudio" data-en="studio">studio</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @getnakedwaxbar
        </a>
      </div>
      <div class="grid grid-cols-1 gap-4 sm:gap-5">
        <div class="frame zoomable aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Get Naked Wax Bar, en Brandon" data-en="Get Naked Wax Bar, Brandon">Get Naked Wax Bar, Brandon</span><img src="assets/raw/sign-wide.jpg" alt="Get Naked Wax Bar logo signage on the studio wall, Brandon FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal max-w-xs sm:max-w-sm mx-auto" style="transition-delay:90ms"><span class="tile-cap" data-es="La sala de tratamiento" data-en="The treatment room">The treatment room</span><img src="assets/raw/studio-room.jpg" alt="Treatment room at Get Naked Wax Bar with pink neon sign and vanity" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  """

# ============================================================
# OPINIONES (3 reseñas reales verbatim de Booksy, sin em-dash)
# ============================================================
NEW_OPINIONES = f"""<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="las clientas" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 164 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 164 verified reviews on Booksy">5.0 out of 5 · 164 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very professional and great customer service! If you want an excellent waxing service provider, book her ASAP!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ladricka G.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She was very kind, knowledgeable fast. It was almost painless and this being my first time I was extremely comfortable and 100% satisfied with the outcome. I recommend it and I am now a permanent customer."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Donald T.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I had an appointment to get my eyebrows and ears waxed. I added a nose wax in person. Tatiana was professional and personable. She makes one feel very comfortable almost immediately."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">John P.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 164 reseñas en Booksy" data-en="Read all 164 reviews on Booksy">Read all 164 reviews on Booksy</a>
      </div>
    </div>
  </section>

  """

print('OK: galeria + opiniones')

# ============================================================
# UBICACION (Direccion, Horario, Reservas, Instagram)
# ============================================================
MAPS_Q = '106+E+Bloomingdale+Ave,+Brandon,+FL+33511'
NEW_UBICACION = f"""<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Brandon</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">106 E Bloomingdale Ave (inside Heads Up Barbershop #1), Brandon, FL 33511</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(176,23,95,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Miércoles y jueves 9am-6pm · Viernes 9am-6:30pm · Sábado 8am-4pm · Domingo a martes cerrado" data-en="Wed-Thu 9am-6pm · Fri 9am-6:30pm · Sat 8am-4pm · Closed Sun-Tue">Wed-Thu 9am-6pm · Fri 9am-6:30pm · Sat 8am-4pm · Closed Sun-Tue</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy, o llama o escribe al {PHONE_DISPLAY}." data-en="By appointment via Booksy, or call or text {PHONE_DISPLAY}.">By appointment via Booksy, or call or text {PHONE_DISPLAY}.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(176,23,95,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos más recientes de Tatiana y escribe por DM cualquier duda antes de tu cita." data-en="See Tatiana's latest work and DM any questions before your appointment.">See Tatiana's latest work and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(176,23,95,0.4)]" href="{IG}" target="_blank" rel="noopener">@getnakedwaxbar</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Get Naked Wax Bar, 106 E Bloomingdale Ave, Brandon FL"
          src="https://www.google.com/maps?q={MAPS_Q}&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

  """

# ============================================================
# CTA FINAL
# ============================================================
NEW_CTA = f"""<!-- CTA FINAL -->
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #200a14 0%, #150810 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Piel suave, con calma de verdad." data-en="Smooth skin, real care.">Smooth skin, real care.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="está a un clic" data-en="is one tap away">is one tap away</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu brasileña, un retoque de cejas o ese cuerpo completo que has estado posponiendo." data-en="Book online in seconds: your Brazilian, a brow touch-up, or that full body wax you have been putting off.">Book online in seconds: your Brazilian, a brow touch-up, or that full body wax you have been putting off.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>
      </div>
    </div>
  </section>

  """

print('OK: ubicacion + cta final')

# ============================================================
# FOOTER
# ============================================================
NEW_FOOTER = f"""<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#170a10]">
    <span class="foot-mark" aria-hidden="true">Get Naked</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/logo.jpg" alt="Get Naked Wax Bar" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(249,168,206,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Get Naked Wax Bar</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de depilación en Brandon, FL, dentro de Heads Up Barbershop #1. Atención con cita previa." data-en="Waxing studio in Brandon, FL, inside Heads Up Barbershop #1. By appointment only.">Waxing studio in Brandon, FL, inside Heads Up Barbershop #1. By appointment only.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>106 E Bloomingdale Ave, Brandon, FL 33511</p>
        <p class="text-xs text-[color:var(--ink-40)]" data-es="Mié-Jue 9am-6pm · Vie 9am-6:30pm · Sáb 8am-4pm" data-en="Wed-Thu 9am-6pm · Fri 9am-6:30pm · Sat 8am-4pm">Wed-Thu 9am-6pm · Fri 9am-6:30pm · Sat 8am-4pm</p>
        <p><a href="tel:{PHONE_TEL}" class="hover:text-[#f9a8ce]">{PHONE_DISPLAY}</a></p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#f9a8ce]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#f9a8ce]">Instagram · @getnakedwaxbar</a></p>
        <p><a href="{FB}" target="_blank" rel="noopener" class="hover:text-[#f9a8ce]" data-es="Facebook · Lush Aesthetics By Tatiana" data-en="Facebook · Lush Aesthetics By Tatiana">Facebook · Lush Aesthetics By Tatiana</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Get Naked Wax Bar.</p>
        <a href="https://merktop.com" target="_blank" rel="noopener" class="merktop-badge">
          <span class="merktop-dot"></span>
          <span class="text-xs text-[#f4eee2]">Powered by <span class="font-semibold">Merktop</span></span>
        </a>
      </div>
    </div>
  </footer>

  """

# ============================================================
# BOTON FLOTANTE
# ============================================================
NEW_BOOKFLOAT = f"""<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fdf7f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>

  """

print('OK: footer + book-float')

# ============================================================
# ENSAMBLADO FINAL
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
for word in ['Brazilian Wax', 'Bikini Wax', 'Brow Lamination', 'Manzilian Wax', 'Full Body Wax', 'Brandon, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'
assert '<details' not in h_final.lower(), 'hay <details> (acordeon prohibido)'

for leftover in ['Lash Bloom', 'West Palm Beach', '519855', 'Cresthaven', '_lashbloom',
                 'lash', 'Lash', 'Yesi']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/getnakedwaxbarbrandon', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
