#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/cocoa-cowrie-beauty-largo/index.html
Cocoa Cowrie Beauty, Largo FL. Hair salon: braids, locs, sew-ins, silk press and color.
Stylists Kylah Faye and Phoebe D. 4.9 / 353 reviews on Booksy. 65 real services with published
prices/durations. Paleta rose-copper (hue-shift a ~5deg desde el dorado original del esqueleto,
distinto de rust ~15deg, amber ~35deg, violeta ~300deg, steel-blue ~205deg usados hoy).
"""
import re
import os
import json
import colorsys

SRC = 'templates/dark-v2/index.html'
DST = 'output/cocoa-cowrie-beauty-largo/index.html'
DATA = json.load(open('output/cocoa-cowrie-beauty-largo/data.json', encoding='utf-8'))

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
# 2. PALETA: dorado -> rose-copper (hue-shift a ~5deg, sat x0.95, computado con
#    colorsys desde los hex reales del esqueleto). Distinto de rust (#a86a2e-ish ~15deg,
#    tomado hoy por un precedente), amber ~35deg, violeta ~300deg y steel-blue ~205deg
#    (tomados hoy por agentes hermanos), y del dorado original (~42deg).
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(110, 85, 35), (122, 90, 30), (15, 11, 7), (180, 140, 60), (185, 138, 128), (212, 168, 75),
          (232, 207, 150), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]
# nota: (27,21,14) y (36,28,20) solo aparecen dentro del bloque .merktop-badge (protegido arriba).
TARGET_HUE = 5 / 360.0
SAT_MUL = 0.95


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

ACCENT_DEEP = _shift_hex('#d4a84b')
ACCENT_MID = _shift_hex('#b8934a')
print('ACCENT_DEEP', ACCENT_DEEP, 'ACCENT_MID', ACCENT_MID)

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://booksy.com/en-us/545915_cocoa-cowrie-beauty_hair-salon_15985_largo'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
IG = 'https://www.instagram.com/cocoacowrie/'
rep_all(OLD_IG_URL, IG)

rep_all('@pure.artistrysk', '@cocoacowrie')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Cocoa Cowrie Beauty · Hair Salon in Largo, FL | Braids, Locs &amp; Color | 4.9 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Cocoa Cowrie Beauty, Largo FL: individual crochet, goddess box braids, sew-ins, silk press, locs and color by Kylah Faye and Phoebe D. 4.9 with 353 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Cocoa Cowrie Beauty · Hair Salon in Largo, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Braids, locs, sew-ins, silk press and color. 4.9 across 353 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-26.jpg" />',
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
    "name": "Cocoa Cowrie Beauty",
    "description": "Hair salon in Largo, FL: individual crochet, goddess box braids, feed-ins, sew-ins, silk press, locs and color, styled by Kylah Faye and Phoebe D.",
    "address": { "@type": "PostalAddress", "streetAddress": "11100 66th Street, Suite 21", "addressLocality": "Largo", "addressRegion": "FL", "postalCode": "33773", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.873522031869086, "longitude": -82.73045085271316 },
    "telephone": "+1-727-458-3585",
    "email": "cocoacowrie@gmail.com",
    "sameAs": ["https://booksy.com/en-us/545915_cocoa-cowrie-beauty_hair-salon_15985_largo", "https://www.instagram.com/cocoacowrie/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "353", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Friday"], "opens": "09:00", "closes": "18:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday"], "opens": "09:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday"], "opens": "09:00", "closes": "17:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "15:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "155", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Individual Crochet" } },
      { "@type": "Offer", "price": "185", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Goddess box braids" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Silk Press" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Kid's Braids natural hair" } }
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
    <span class="pre-mono">CC</span>
    <span class="pre-word">Cocoa Cowrie</span>
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
        <img src="assets/raw/bk-2.jpg" alt="Cocoa Cowrie Beauty logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,101,75,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Cocoa <span class="text-[color:var(--accent-deep)]">Cowrie</span></span>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Largo, FL · Salón de Belleza" data-en="Largo, FL · Hair Salon">Largo, FL · Hair Salon</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu cabello, tratado con cuidado." data-en="Your crown, handled with care.">Your crown, handled with care.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Trenzas, locs y color," data-en="Braids, locs and color,">Braids, locs and color,</span><br /><span data-es="hechos a mano, " data-en="crafted by hand, ">crafted by hand, </span><span class="text-shine" data-es="con corazón" data-en="with heart">with heart</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Cocoa Cowrie Beauty es el estudio de Kylah Faye y Phoebe D en Largo: crochet individual, goddess box braids, sew-ins, silk press y color, además de un menú completo de estilos protectores para niñas y adultas. Calificación de 4.9 en 353 reseñas de Booksy." data-en="Cocoa Cowrie Beauty is Kylah Faye and Phoebe D's hair studio in Largo: individual crochet, goddess box braids, sew-ins, silk press and color, plus a full menu of protective styles for kids and adults. A 4.9 rating across 353 reviews on Booksy.">Cocoa Cowrie Beauty is Kylah Faye and Phoebe D's hair studio in Largo: individual crochet, goddess box braids, sew-ins, silk press and color, plus a full menu of protective styles for kids and adults. A 4.9 rating across 353 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.9 · 353 reseñas en Booksy" data-en="4.9 · 353 reviews on Booksy">4.9 · 353 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @cocoacowrie
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-26.jpg" alt="Side profile of finished feed-in braids with burgundy color at Cocoa Cowrie Beauty" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Individual Crochet</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 4h" data-en="$155 · 4h">$155 · 4h</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="353">353</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Braids <span class="text-shine">&amp;</span> Locs</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Feed-Ins · Sew-Ins · Color" data-en="Feed-Ins · Sew-Ins · Color">Feed-Ins · Sew-Ins · Color</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Dos Estilistas" data-en="Two Stylists">Two Stylists</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Kylah Faye &amp; Phoebe D</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Largo</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">66th Street</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Individual Crochet</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Goddess Box Braids</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Sew-Ins</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Silk Press</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Locs</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Largo, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-23.jpg" alt="Finished box braids with burgundy ombre curls at Cocoa Cowrie Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-27.jpg" alt="Client smiling with a finished loc updo styled with gold cuffs at Cocoa Cowrie Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Dos estilistas," data-en="Two stylists,">Two stylists,</span><br /><span class="text-shine" data-es="un mismo cuidado" data-en="one standard of care">one standard of care</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Cocoa Cowrie Beauty es el estudio de Kylah Faye y Phoebe D en 11100 66th Street, Largo: trenzas, locs, sew-ins, silk press y color, hechos a mano para cada tipo de cabello." data-en="Cocoa Cowrie Beauty is Kylah Faye and Phoebe D's studio at 11100 66th Street in Largo: braids, locs, sew-ins, silk press and color, done by hand for every hair type.">Cocoa Cowrie Beauty is Kylah Faye and Phoebe D's studio at 11100 66th Street in Largo: braids, locs, sew-ins, silk press and color, done by hand for every hair type.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Las clientas describen a Kylah como de mano ligera y trato cercano, y a Phoebe como fácil de trabajar desde el primer momento. Una calificación de 4.9 en 353 reseñas lo respalda." data-en="Clients describe Kylah as light handed and light hearted, and Phoebe as easy to work with from the moment you walk in. A 4.9 rating across 353 reviews backs it up.">Clients describe Kylah as light handed and light hearted, and Phoebe as easy to work with from the moment you walk in. A 4.9 rating across 353 reviews backs it up.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="353">353</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Estilistas" data-en="Stylists">Stylists</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Cocoa Cowrie Beauty logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,101,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Cocoa Cowrie Beauty · <span class="text-[color:var(--ink-40)]" data-es="Kylah Faye &amp; Phoebe D" data-en="Kylah Faye &amp; Phoebe D">Kylah Faye &amp; Phoebe D</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu estilo en Booksy, de crochet individual a un simple corte, con precio y duración claros desde el inicio." data-en="Pick your style on Booksy, from individual crochet to a quick trim, with price and duration up front.">Pick your style on Booksy, from individual crochet to a quick trim, with price and duration up front.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta de estilo" data-en="Style consult">Style consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El largo, la densidad de tu cabello y el look que buscas definen la partición, el tamaño y la tensión antes de empezar." data-en="Your hair's length, density and the look you want shape the parting, size and tension before a single braid starts.">Your hair's length, density and the look you want shape the parting, size and tension before a single braid starts.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un trim de 45 minutos a las kinky twists de 6 horas: cada estilo recibe el tiempo completo que realmente necesita." data-en="From a 45 minute trim to 6 hour kinky twists, each style gets the full time it actually needs.">From a 45 minute trim to 6 hour kinky twists, each style gets the full time it actually needs.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con indicaciones de cuidado para tu nuevo estilo y tu próximo retoque ya en mente." data-en="You leave with care instructions for your new style and your next retouch already in mind.">You leave with care instructions for your new style and your next retouch already in mind.</p>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: metodo definido')

# ============================================================
# SERVICIOS (65 servicios reales de Booksy: 4 cards destacadas + 9 bloques por categoria)
# ============================================================
SVC = {s['name']: s for s in DATA['services']}


def price_row(name, es_name=None):
    s = SVC.pop(name)
    p = f"${int(s['price'])}"
    dur = f'<span class="text-[color:var(--ink-40)] text-xs">&middot; {s["duration"]}</span>' if s['duration'] else ''
    label = es_name or name
    return (f'<div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2">'
            f'<span class="font-light">{label}</span>'
            f'<span class="font-display text-[color:var(--accent-deep)]">{p} {dur}</span></div>')


CATEGORIES = [
    ('Trenzas y Estilos Protectores', 'Braids &amp; Protective Styles', [
        'Miracle knots', 'Individual Crochet', 'Goddess box braids', '2 Jumbo Feed In Braids',
        'Bantu Knots', 'Braid down', 'Ghana Braids', 'Box Braids', 'Crochet Braids',
        'poetic justice plaits', 'Tree Braids', '2 French Braids with natural hair',
        'Cornrows with Extentions', 'Goddess Braids', 'Kinky Twists', "Men's Cornrow Braids",
        'Additional Extension Add-On',
    ]),
    ('Niños', 'Kids', [
        "Kid's Braids natural hair", 'Kids Cornrows With Extentions', 'Kids Crochet',
    ]),
    ('Sew-Ins y Extensiones', 'Sew-Ins &amp; Extensions', [
        'Wig Install Sew-In', 'Lace Closure Sew In', 'Micro Ring Extensions',
        'Microlinks Extensions', 'Netting', 'No Braid Sew-In', 'Sew-in maintenance',
        'Partial Sew In', 'Tracking / Single Track Sew-In', 'sew in', 'Quick weave',
        'Glue in Extensions full head', 'Versatile Sew In',
    ]),
    ('Peinado y Acabado', 'Styling &amp; Finish', [
        'Styling', 'Flat Iron', 'Silk Wrap', 'Wand / Barrel Curls', 'Silk Press',
        'Style take down/shampoo and conditioner',
    ]),
    ('Tratamientos Capilares', 'Hair Treatments', [
        'Growth stimulating treatment', 'Shampoo, conditioner and style', 'Shampoo and conditioner',
        'Takedown', 'Deep Conditioning Treatment', 'Hot Oil Treatment', 'Protein Treatment',
        'Olaplex Treatment', 'Stimulating scalp treatment',
    ]),
    ('Color', 'Color', [
        'Root Touch Up', 'Double Process Color', 'Semi Color', 'All Over Color',
    ]),
    ('Cortes', 'Cuts', [
        'Transitioning Cut', "Men's Cut", 'Trim', "Women's  Style Cut",
    ]),
    ('Cabello Natural y Alisado', 'Natural Hair &amp; Relaxers', [
        'Natural hair Perm Rods', 'Smooth Transformation', 'Relaxer Retouch', 'Virgin Relaxer',
    ]),
    ('Locs', 'Locs', [
        'Micro Locs retight', 'Loc Coils', 'Traditional Loc retight', 'Starter traditional locs',
    ]),
]

CATEGORY_BLOCKS = []
for es_label, en_label, names in CATEGORIES:
    rows = '\n          '.join(price_row(n) for n in names)
    block = f'''      <div class="reveal glass rounded-3xl p-7 sm:p-9 mt-8">
        <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="{es_label}" data-en="{en_label}">{en_label}</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-3 text-sm">
          {rows}
        </div>
      </div>
'''
    CATEGORY_BLOCKS.append(block)

# Travel Fee se referencia en la nota final, no como categoria propia (item de logistica, no de estilo)
SVC.pop('Travel Fee')
assert not SVC, f'servicios sin categorizar: {list(SVC.keys())}'

NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="estilo" data-en="style">style</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Cocoa Cowrie Beauty en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Cocoa Cowrie Beauty on Booksy. Booking confirms instantly.">Prices and durations as published by Cocoa Cowrie Beauty on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,101,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Individual Crochet</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Crochet individual hecho a mano, hebra por hebra, para un resultado protector con textura y volumen natural." data-en="Hand-done individual crochet, strand by strand, for a protective look with natural texture and volume.">Hand-done individual crochet, strand by strand, for a protective look with natural texture and volume.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$155</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">4h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Trenzas" data-en="Braids">Braids</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Goddess Box Braids" data-en="Goddess Box Braids">Goddess Box Braids</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Box braids estilo goddess, limpias y sin tensión, la protectora favorita de las clientas de Cocoa Cowrie." data-en="Goddess-style box braids, clean and tension-free, a favorite protective style at Cocoa Cowrie.">Goddess-style box braids, clean and tension-free, a favorite protective style at Cocoa Cowrie.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$185</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Liso" data-en="Sleek">Sleek</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Silk Press</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Silk press con acabado liso y brillante, cuidando la salud del cabello natural en cada pasada." data-en="A smooth, shiny silk press finish that keeps natural hair health in mind with every pass.">A smooth, shiny silk press finish that keeps natural hair health in mind with every pass.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Niños" data-en="Kids">Kids</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Trenzas para Niños" data-en="Kid's Braids">Kid's Braids</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trenzas sobre cabello natural para niñas, con paciencia y un ambiente cómodo durante toda la cita." data-en="Braids on natural hair for kids, with patience and a comfortable environment through the whole visit.">Braids on natural hair for kids, with patience and a comfortable environment through the whole visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 15min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
{''.join(CATEGORY_BLOCKS)}      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 65 servicios y su disponibilidad completa están en Booksy, incluyendo el travel fee de $40 (2h) para citas a domicilio. Reserva en línea o escribe/llama al (727) 458-3585." data-en="All 65 services and full availability are on Booksy, including a $40 travel fee (2h) for on-location bookings. Book online or call/text (727) 458-3585.">All 65 services and full availability are on Booksy, including a $40 travel fee (2h) for on-location bookings. Book online or call/text (727) 458-3585.</span></p>
    </div>
  </section>

  '''

print('OK: servicios definidos (4 destacados + 9 categorias)')

# ============================================================
# GALERIA (1 tile 16/9 + 2 tiles 3/4: 3 fotos reales curadas)
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
          @cocoacowrie
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Trenzas con puntas doradas" data-en="Feed-ins, golden ends">Feed-ins, golden ends</span><img src="assets/raw/bk-28.jpg" alt="Side profile of feed-in braids with golden blonde ends at Cocoa Cowrie Beauty" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Patrón de trenza corona" data-en="Crown braid pattern">Crown braid pattern</span><img src="assets/raw/bk-21.jpg" alt="Overhead view of a spiral crown braid pattern at Cocoa Cowrie Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalle de color" data-en="Color detail">Color detail</span><img src="assets/raw/bk-22.jpg" alt="Close-up detail of braided extensions with color highlights at Cocoa Cowrie Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

print('OK: galeria definida')

# ============================================================
# OPINIONES (3 reseñas reales verbatim de Booksy, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="las clientas" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 353 reseñas verificadas en Booksy" data-en="4.9 out of 5 · 353 verified reviews on Booksy">4.9 out of 5 · 353 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She's light handed, light hearted, and the best at what she does! My braids look exceptional!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Andrea M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Phoebe was great! I needed a chop to get rid of damage while also wanting cute short effortless style. I love it! It's exactly what I wanted. Phoebe is very easy to work with and I was comfortable the moment I walked in. I will be back for future trims. 💕"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Patricia R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"great"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jewlana S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 353 reseñas en Booksy" data-en="Read all 353 reviews on Booksy">Read all 353 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: opiniones definidas')

# ============================================================
# UBICACION (Direccion, Horario, Reservas, Contacto, Instagram)
# ============================================================
MAPS_Q = '11100+66th+Street,+Largo,+FL+33773'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Largo</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">11100 66th Street, Suite 21, Largo, FL 33773</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,101,75,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes y viernes 9:00 am – 6:30 pm · Miércoles 9:00 am – 6:00 pm · Jueves 9:00 am – 5:30 pm · Sábado 9:00 am – 3:00 pm · Domingo y lunes cerrado" data-en="Tuesday &amp; Friday 9:00 AM - 6:30 PM · Wednesday 9:00 AM - 6:00 PM · Thursday 9:00 AM - 5:30 PM · Saturday 9:00 AM - 3:00 PM · Closed Sunday &amp; Monday">Tuesday &amp; Friday 9:00 AM - 6:30 PM · Wednesday 9:00 AM - 6:00 PM · Thursday 9:00 AM - 5:30 PM · Saturday 9:00 AM - 3:00 PM · Closed Sunday &amp; Monday</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,101,75,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Contacto" data-en="Contact">Contact</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light"><a class="text-[color:var(--accent-deep)]" href="tel:+17274583585">(727) 458-3585</a></p>
              <p class="text-sm text-[color:var(--ink-60)] font-light"><a class="text-[color:var(--accent-deep)]" href="mailto:cocoacowrie@gmail.com">cocoacowrie@gmail.com</a></p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:300ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira el trabajo más reciente y escribe por DM cualquier duda antes de tu cita." data-en="See the latest work and DM any questions before your appointment.">See the latest work and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,101,75,0.4)]" href="{IG}" target="_blank" rel="noopener">@cocoacowrie</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Cocoa Cowrie Beauty, 11100 66th Street, Largo FL"
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
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado con cuidado." data-en="Your crown, handled with care.">Your crown, handled with care.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo estilo" data-en="Your next style">Your next style</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: crochet individual, goddess braids, un retwist de locs o el silk press que llevas planeando." data-en="Book online in seconds: individual crochet, goddess braids, a loc retwist or the silk press you have been planning.">Book online in seconds: individual crochet, goddess braids, a loc retwist or the silk press you have been planning.</p>
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
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#0c0905]">
    <span class="foot-mark" aria-hidden="true">Cocoa Cowrie</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Cocoa Cowrie Beauty logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,167,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Cocoa Cowrie</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Salón de belleza en Largo, FL. Atención con cita previa." data-en="Hair salon in Largo, FL. By appointment only.">Hair salon in Largo, FL. By appointment only.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>11100 66th Street, Suite 21, Largo, FL 33773</p>
        <p><a href="tel:+17274583585" class="hover:text-[#e9c3ab]">(727) 458-3585</a></p>
        <p><a href="mailto:cocoacowrie@gmail.com" class="hover:text-[#e9c3ab]">cocoacowrie@gmail.com</a></p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · @cocoacowrie</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Cocoa Cowrie Beauty.</p>
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
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
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
for word in ['Individual Crochet', 'Goddess Box Braids', 'Sew-Ins', 'Silk Press', 'Locs', 'Largo, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (leftovers no curados, thumbnails 100x100, texto/selfies/blur) nunca deben aparecer
BANNED_PHOTOS = [f'bk-{n}.jpg' for n in range(1, 21)] + ['bk-24.jpg', 'bk-25.jpg']
USED_PHOTOS = ['bk-2.jpg', 'bk-21.jpg', 'bk-22.jpg', 'bk-23.jpg', 'bk-26.jpg', 'bk-27.jpg', 'bk-28.jpg']
for banned in BANNED_PHOTOS:
    if banned in USED_PHOTOS:
        continue
    assert f'assets/raw/{banned}' not in h_final, f'ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk',
                  'K-Tip', 'K-Tips', 'knotless', 'Knotless', 'celebrity']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/cocoa-cowrie-beauty-largo', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
