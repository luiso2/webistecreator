#!/usr/bin/env python3
"""Derivacion anclada: templates/light-v2/index.html -> output/estnatouch-wesleychapel/index.html
Estnatouch, Wesley Chapel FL. Braids & locs studio, solo artist Esther Ansah.
Paleta violet-mauve/berry (hue-shift a ~300deg desde el rosa original del esqueleto light-v2
"Lash Bloom"), distinta de rust (~15deg), amber (~35deg), rose-copper (~5deg) y steel-blue (~205deg)
usados por otros agentes en paralelo.
5.0 / 19 reviews en Booksy. 12 servicios reales publicados en Booksy (knotless braids, box braids,
crochet braids, boho bob, bohemian/boho braids, sew in weave, faux locs, fulani/tribal braids,
french curls braids, twist).
"""
import re
import os
import colorsys

SRC = 'templates/light-v2/index.html'
DST = 'output/estnatouch-wesleychapel/index.html'

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
# 2. PALETA: rosa/mauve (Lash Bloom, ~336deg) -> violeta-mauve/berry (~300deg),
#    computado con colorsys desde los hex reales del esqueleto light-v2.
#    Distinto de rust (~15deg), amber (~35deg), rose-copper (~5deg), steel-blue (~205deg).
# ============================================================
_HEXES = ["#1c0f16", "#1f0f18", "#2a1722", "#33222c", "#5c2140", "#5f2c48", "#7d3457", "#8a5573",
          "#a04a72", "#b25a85", "#c47a9c", "#c9789f", "#d3a2bc", "#d9a8c2", "#dc9dbe", "#e5c1d4",
          "#efd0e0", "#f0bed7", "#f2cfe0", "#f2d5e3", "#f3e0ea", "#f6f1ea", "#f8dfeb",
          "#faf2f6", "#fbeff5", "#fbf3f8"]
_RGBAS = [(125, 52, 87), (160, 74, 114), (185, 138, 128), (233, 205, 186), (240, 190, 215),
          (250, 242, 246), (253, 246, 250), (70, 25, 50), (40, 16, 30), (51, 34, 44)]
# nota: (212,168,75), (244,238,226), (27,21,14), (36,28,20) y '#D4A84B' solo aparecen dentro del
# bloque .merktop-badge (protegido arriba).
TARGET_HUE = 300 / 360.0
SAT_MUL = 1.0


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

ACCENT_DEEP = _shift_hex('#a04a72')
ACCENT_MID = _shift_hex('#c47a9c')
print('ACCENT_DEEP', ACCENT_DEEP, 'ACCENT_MID', ACCENT_MID)

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
BK = 'https://booksy.com/en-us/1203888_estnatouch_braids-locs_15976_wesley-chapel'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
IG = 'https://www.instagram.com/estnatouch/'
rep_all(OLD_IG_URL, IG)

rep_all('@_lashbloom', '@estnatouch')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Estnatouch · Braids &amp; Locs Studio en Wesley Chapel, FL | Knotless, Boho &amp; Locs</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Estnatouch, Wesley Chapel FL: knotless braids, box braids, crochet braids, boho bob and faux locs by Esther Ansah. A perfect 5.0 across 19 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Estnatouch · Braids &amp; Locs Studio in Wesley Chapel, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Knotless braids, box braids, crochet braids, boho bob and faux locs. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-15.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-13.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Estnatouch",
    "description": "Braids and locs studio in Wesley Chapel, FL: knotless braids, box braids, crochet braids, boho bob, bohemian/boho braids, faux locs, tribal braids and twists by Esther Ansah.",
    "address": { "@type": "PostalAddress", "streetAddress": "27642 Cashford Circle, Suite 114", "addressLocality": "Wesley Chapel", "addressRegion": "FL", "postalCode": "33544", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.20229893642983, "longitude": -82.36448823789695 },
    "sameAs": ["https://booksy.com/en-us/1203888_estnatouch_braids-locs_15976_wesley-chapel", "https://www.instagram.com/estnatouch/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "19", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "15:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday"], "opens": "16:00", "closes": "21:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Braids and locs services", "itemListElement": [
      { "@type": "Offer", "price": "180", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Knotless Braids (synthetic hair included)" } },
      { "@type": "Offer", "price": "245", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Box Braids (braiding hair included, free part)" } },
      { "@type": "Offer", "price": "170", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Crochet Braids" } },
      { "@type": "Offer", "price": "400", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Boho Bob (100% virgin human hair curls included)" } },
      { "@type": "Offer", "price": "260", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Boho Bob (bring your own curly hair)" } },
      { "@type": "Offer", "price": "550", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Bohemian/Boho Braids (human hair curls included)" } },
      { "@type": "Offer", "price": "350", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Bohemian/Boho Braids (bring your own curly hair)" } },
      { "@type": "Offer", "price": "200", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Sew In Weave" } },
      { "@type": "Offer", "price": "250", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Individual Faux Locs" } },
      { "@type": "Offer", "price": "250", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Fulani/Tribal Braids" } },
      { "@type": "Offer", "price": "300", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "French Curls Braids" } },
      { "@type": "Offer", "price": "200", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Twist (with your natural hair)" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: badge + paleta + globales + head/JSON-LD')

# ============================================================
# 5. IDIOMA: el esqueleto light-v2 ya es EN default (fallback en/es en applyLang
#    y <html lang="en">) -> sin cambios, coincide con el negocio (language: en)
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
    <span class="pre-mono">ET</span>
    <span class="pre-word">Estnatouch</span>
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
        <img src="assets/raw/bk-13.jpg" alt="Estnatouch" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba({_shift_rgb((160,74,114))[0]},{_shift_rgb((160,74,114))[1]},{_shift_rgb((160,74,114))[2]},0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Estna<span class="text-[color:var(--accent-deep)]">touch</span></span>
      </a>
      <nav class="hidden md:flex items-center gap-7 text-sm font-light">
        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">The Experience</a>
        <a class="nav-link" href="#metodo" data-es="El Proceso" data-en="The Process">The Process</a>
        <a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>
        <a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Location</a>
      </nav>
      <div class="flex items-center gap-3">
        <button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Change language">ES</button>
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
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Proceso" data-en="The Process">The Process</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Location</a>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Book now</a>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Wesley Chapel, FL · Estudio de Trenzas y Locs" data-en="Wesley Chapel, FL · Braids &amp; Locs Studio">Wesley Chapel, FL · Braids &amp; Locs Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cada trenza, tejida a mano con propósito." data-en="Every braid, hand woven with purpose.">Every braid, hand woven with purpose.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Knotless, box braids y" data-en="Knotless, box braids and">Knotless, box braids and</span><br /><span data-es="locs, tejidos para " data-en="locs, styled to ">locs, styled to </span><span class="text-shine" data-es="durar" data-en="last">last</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Esther Ansah teje cada estilo a mano en Estnatouch: knotless, box braids, crochet, boho bob, faux locs y trenzas tribales, con cabello real incluido en la mayoría de sets. 5.0 perfecto en 19 reseñas de Booksy." data-en="Esther Ansah hand braids every style at Estnatouch: knotless, box braids, crochet, boho bob, faux locs and tribal braids, with real hair included in most sets. A perfect 5.0 across 19 reviews on Booksy.">Esther Ansah hand braids every style at Estnatouch: knotless, box braids, crochet, boho bob, faux locs and tribal braids, with real hair included in most sets. A perfect 5.0 across 19 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 19 reseñas en Booksy" data-en="5.0 · 19 reviews on Booksy">5.0 · 19 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @estnatouch
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-15.jpg" alt="Overhead view of a geometric box braid parting pattern at Estnatouch" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Knotless Braids</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$180 · 3h" data-en="$180 · 3h">$180 · 3h</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="19">19</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Braids <span class="text-shine">&amp;</span> Locs</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Knotless · Box · Crochet · Boho" data-en="Knotless · Box · Crochet · Boho">Knotless · Box · Crochet · Boho</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Cabello real" data-en="Real hair">Real hair</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Incluido en la mayoría de sets" data-en="Included in most sets">Included in most sets</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Wesley Chapel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Cashford Circle</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Knotless Braids</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Box Braids</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Crochet Braids</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Boho Bob</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Faux Locs</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-9.jpg" alt="Esther Ansah, owner and braider at Estnatouch" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-14.jpg" alt="Close-up of caramel-toned box braids styled at Estnatouch" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="cada trenza a mano" data-en="every braid by hand">every braid by hand</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Estnatouch es el estudio de Esther Ansah en Wesley Chapel: knotless braids, box braids, crochet, boho bob, bohemian braids, faux locs y trenzas tribales, tejidas a mano cliente por cliente." data-en="Estnatouch is Esther Ansah's studio in Wesley Chapel: knotless braids, box braids, crochet, boho bob, bohemian braids, faux locs and tribal braids, hand woven one client at a time.">Estnatouch is Esther Ansah's studio in Wesley Chapel: knotless braids, box braids, crochet, boho bob, bohemian braids, faux locs and tribal braids, hand woven one client at a time.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus reseñas lo repiten una y otra vez: trato cálido, mucho detalle en cada partición y un resultado que se siente cómodo desde el primer día. 5.0 perfecto en 19 reseñas de Booksy." data-en="Her reviews say it again and again: warm, patient, detailed parting work and a result that feels comfortable from day one. A perfect 5.0 across 19 reviews on Booksy.">Her reviews say it again and again: warm, patient, detailed parting work and a result that feels comfortable from day one. A perfect 5.0 across 19 reviews on Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="19">19</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-9.jpg" alt="Esther Ansah" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(RGB1,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Esther Ansah · <span class="text-[color:var(--ink-40)]" data-es="Dueña y estilista" data-en="Owner &amp; Braider">Owner &amp; Braider</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''
NEW_EXPERIENCIA = NEW_EXPERIENCIA.replace('RGB1', f'{_shift_rgb((160,74,114))[0]},{_shift_rgb((160,74,114))[1]},{_shift_rgb((160,74,114))[2]}')

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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu estilo en Booksy con precio y duración claros, o escribes a @estnatouch por Instagram para resolver dudas antes." data-en="Pick your style on Booksy with clear price and duration, or message @estnatouch on Instagram to ask questions first.">Pick your style on Booksy with clear price and duration, or message @estnatouch on Instagram to ask questions first.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta y parte" data-en="Consult &amp; part">Consult &amp; part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El grosor, el largo deseado y el patrón de partición se definen contigo antes de empezar a tejer." data-en="Braid size, desired length and the parting pattern get mapped out with you before a single braid starts.">Braid size, desired length and the parting pattern get mapped out with you before a single braid starts.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El tejido" data-en="The braiding">The braiding</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Esther teje cada sección a mano, con el tiempo completo que cada estilo realmente necesita, de 3 a 6 horas." data-en="Esther hand braids every section, with the full time each style actually needs, from 3 to 6 hours.">Esther hand braids every section, with the full time each style actually needs, from 3 to 6 hours.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con instrucciones claras de cuidado para que tus trenzas o locs se vean frescos por semanas." data-en="You leave with clear care instructions so your braids or locs stay looking fresh for weeks.">You leave with clear care instructions so your braids or locs stay looking fresh for weeks.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (12 servicios reales de Booksy: 4 cards destacadas + bloque completo)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="estilo" data-en="style">style</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Estnatouch en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Estnatouch on Booksy. Booking confirms instantly.">Prices and durations as published by Estnatouch on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito de siempre" data-en="Studio classic">Studio classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Knotless Braids</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trenzas sin nudo con cabello sintético incluido, para un inicio suave y sin tensión en el cuero cabelludo." data-en="Knotless braids with synthetic braiding hair included, for a soft start with less tension on the scalp.">Knotless braids with synthetic braiding hair included, for a soft start with less tension on the scalp.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$180</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba({_shift_rgb((160,74,114))[0]},{_shift_rgb((160,74,114))[1]},{_shift_rgb((160,74,114))[2]},0.4); box-shadow: 0 18px 50px rgba({_shift_rgb((51,34,44))[0]},{_shift_rgb((51,34,44))[1]},{_shift_rgb((51,34,44))[2]},0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Box Braids</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Box braids clásicas con cabello incluido y parte libre, el estilo más versátil del menú." data-en="Classic box braids with braiding hair included and free part, the most versatile style on the menu.">Classic box braids with braiding hair included and free part, the most versatile style on the menu.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$245</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">4h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Textura rizada" data-en="Curly texture">Curly texture</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Crochet Braids</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trenzas de crochet para un cambio rápido de textura, con acabado lleno y natural." data-en="Crochet braids for a quick texture change, with a full, natural finish.">Crochet braids for a quick texture change, with a full, natural finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$170</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h 30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cabello humano" data-en="Human hair">Human hair</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Boho Bob</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Bob bohemio con rizos de cabello 100% humano incluidos, para un acabado corto y con mucho movimiento." data-en="Bohemian bob with 100% virgin human hair curls included, for a short style with real movement.">Bohemian bob with 100% virgin human hair curls included, for a short style with real movement.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$400</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">5h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="reveal glass rounded-3xl p-7 sm:p-9 mt-8" style="transition-delay:120ms">
        <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="También en el estudio" data-en="Also at the studio">Also at the studio</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-3 text-sm">
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Boho Bob (trae tu propio cabello rizado)" data-en="Boho Bob (bring your own curly hair)">Boho Bob (bring your own curly hair)</span><span class="font-display text-[color:var(--accent-deep)]">$260 <span class="text-[color:var(--ink-40)] text-xs">· 5h</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Bohemian/Boho Braids (cabello humano incluido)" data-en="Bohemian/Boho Braids (human hair included)">Bohemian/Boho Braids (human hair included)</span><span class="font-display text-[color:var(--accent-deep)]">$550 <span class="text-[color:var(--ink-40)] text-xs">· 6h</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Bohemian/Boho Braids (trae tu propio cabello)" data-en="Bohemian/Boho Braids (bring your own hair)">Bohemian/Boho Braids (bring your own hair)</span><span class="font-display text-[color:var(--accent-deep)]">$350</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Sew In Weave" data-en="Sew In Weave">Sew In Weave</span><span class="font-display text-[color:var(--accent-deep)]">$200</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Faux Locs individuales" data-en="Individual Faux Locs">Individual Faux Locs</span><span class="font-display text-[color:var(--accent-deep)]">$250</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Trenzas Fulani / Tribales" data-en="Fulani / Tribal Braids">Fulani / Tribal Braids</span><span class="font-display text-[color:var(--accent-deep)]">$250</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="French Curls Braids" data-en="French Curls Braids">French Curls Braids</span><span class="font-display text-[color:var(--accent-deep)]">$300</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Twist con tu cabello natural" data-en="Twist (with your natural hair)">Twist (with your natural hair)</span><span class="font-display text-[color:var(--accent-deep)]">$200</span></div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 12 servicios y su disponibilidad completa están en Booksy. Reserva en línea o escribe a @estnatouch." data-en="All 12 services and full availability are on Booksy. Book online or message @estnatouch.">All 12 services and full availability are on Booksy. Book online or message @estnatouch.</span></p>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 7 tiles 3/4: 8 fotos reales curadas)
# ============================================================
NEW_GALERIA = f'''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="work">work</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @estnatouch
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Trenzas knotless recién hechas" data-en="Fresh knotless braids">Fresh knotless braids</span><img src="assets/raw/bk-1.jpg" alt="Close-up of freshly finished knotless braids with a geometric part" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Diseño de parte geométrico" data-en="Geometric parting design">Geometric parting design</span><img src="assets/raw/bk-3.jpg" alt="Overhead view of a geometric box braid parting pattern" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Locs en color borgoña" data-en="Burgundy loc color">Burgundy loc color</span><img src="assets/raw/bk-5.jpg" alt="Client smiling with finished burgundy-toned faux locs" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Locs bohemios terminados" data-en="Finished boho locs">Finished boho locs</span><img src="assets/raw/bk-10.jpg" alt="Client outdoors showing long finished boho locs from the back" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Trenzas clásicas de cerca" data-en="Classic braids close-up">Classic braids close-up</span><img src="assets/raw/bk-11.jpg" alt="Side profile close-up of classic box braids" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Volumen y largo" data-en="Volume and length">Volume and length</span><img src="assets/raw/bk-12.jpg" alt="Client holding up long ombre box braids to show volume and length" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:240ms"><span class="tile-cap" data-es="Twists con resorte" data-en="Springy twists">Springy twists</span><img src="assets/raw/bk-13.jpg" alt="Overhead view of springy natural hair twists with a chevron part" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:180ms"><span class="tile-cap" data-es="Parte de precisión" data-en="Precision parting">Precision parting</span><img src="assets/raw/bk-16.jpg" alt="Close-up of precise braid parting at the crown" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 resenas reales verbatim de Booksy, con nombre, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="las clientas" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 19 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 19 verified reviews on Booksy">5.0 out of 5 · 19 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely love getting my hair braided here. 5 stars all around!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ysna</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely wonderful. My son loved his experience at Estnatouch. They went above and beyond expectations and he will definitely be back! Thank you!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">KJ C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I loved my hair and my color. Ester did a great job!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karonica B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
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
MAPS_Q = '27642+Cashford+Circle,+Suite+114,+Wesley+Chapel,+FL+33544'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visítanos</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Wesley Chapel</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">27642 Cashford Circle, Suite 114, Wesley Chapel, FL 33544</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba({_shift_rgb((160,74,114))[0]},{_shift_rgb((160,74,114))[1]},{_shift_rgb((160,74,114))[2]},0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sábado 8:00 am – 3:00 pm · Lunes y martes también 4:00 – 9:00 pm" data-en="Monday-Saturday 8:00 AM - 3:00 PM · Monday &amp; Tuesday also 4:00 - 9:00 PM">Monday-Saturday 8:00 AM - 3:00 PM · Monday &amp; Tuesday also 4:00 - 9:00 PM</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba({_shift_rgb((160,74,114))[0]},{_shift_rgb((160,74,114))[1]},{_shift_rgb((160,74,114))[2]},0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes de Esther y escribe por DM cualquier duda antes de tu cita." data-en="See Esther's latest styles and DM any questions before your appointment.">See Esther's latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba({_shift_rgb((160,74,114))[0]},{_shift_rgb((160,74,114))[1]},{_shift_rgb((160,74,114))[2]},0.4)]" href="{IG}" target="_blank" rel="noopener">@estnatouch</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Estnatouch, 27642 Cashford Circle, Wesley Chapel FL"
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
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, {_shift_hex("#2a1722")} 0%, {_shift_hex("#1f0f18")} 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cada trenza, tejida a mano con propósito." data-en="Every braid, hand woven with purpose.">Every braid, hand woven with purpose.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo estilo" data-en="Your next style">Your next style</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: knotless, box braids, crochet, boho bob o el estilo que ya tienes en mente." data-en="Book knotless, box braids, crochet, boho bob or the style you already have in mind online in seconds.">Book knotless, box braids, crochet, boho bob or the style you already have in mind online in seconds.</p>
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
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[{_shift_hex("#1c0f16")}]">
    <span class="foot-mark" aria-hidden="true">Estnatouch</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-13.jpg" alt="Estnatouch" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba({_shift_rgb((240,190,215))[0]},{_shift_rgb((240,190,215))[1]},{_shift_rgb((240,190,215))[2]},0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Estnatouch</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de trenzas y locs en Wesley Chapel, FL. Atención con cita previa." data-en="Braids and locs studio in Wesley Chapel, FL. By appointment only.">Braids and locs studio in Wesley Chapel, FL. By appointment only.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>27642 Cashford Circle, Suite 114, Wesley Chapel, FL 33544</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[{_shift_hex("#f0bed7")}]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[{_shift_hex("#f0bed7")}]">Instagram · @estnatouch</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Estnatouch.</p>
        {badge_html}
      </div>
    </div>
  </footer>

  '''

# ============================================================
# BOTON FLOTANTE (mismo markup, solo booksy url)
# ============================================================
NEW_BOOKFLOAT = f'''<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{_shift_hex("#faf2f6")}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
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
for word in ['Knotless Braids', 'Box Braids', 'Crochet Braids', 'Boho Bob', 'Faux Locs', 'Wesley Chapel, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (leftovers no curados: charts y selfie) nunca deben aparecer
for banned in ['bk-2.jpg', 'bk-4.jpg', 'bk-6.jpg', 'bk-7.jpg', 'bk-8.jpg', 'logo.jpg',
               'hero-1.jpg', 'about-2.jpg', 'gallery-7.jpg', 'gallery-2.jpg']:
    assert f'assets/raw/{banned}' not in h_final, f'ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Lash Bloom', 'Yesi', 'West Palm', 'Cresthaven', '519855', 'lash', 'Lash']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/estnatouch-wesleychapel', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
