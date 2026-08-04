#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/crowned-locs-largo/index.html
Crowned Locs, Largo FL. Loc/dreadlock studio, solo loctician Briana "Bri" Drayton. Paleta
warm amber/bronze (hue-shift a ~35deg desde el dorado original del esqueleto, distinto del
rust ~15deg, caramelo ~30deg, coral ~345deg, violeta ~262deg y del dorado original ~42deg).
5.0 / 41 reviews en Booksy. 11 servicios reales publicados en Booksy (retwist, Instant Locs,
Crochet/Wicks product-free maintenance, Loc Mastery workshop). Sin Instagram publico
verificado: el canal secundario en todo el site es telefono (call/text), no redes.
"""
import re
import os
import colorsys

SRC = 'templates/dark-v2/index.html'
DST = 'output/crowned-locs-largo/index.html'

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
# 2. PALETA: dorado -> amber/bronze (hue-shift a ~35deg, sat x0.95, computado con
#    colorsys desde los hex reales del esqueleto). Distinto de rust (#..., ~15deg),
#    caramelo (~30deg), coral fairy (~345deg), esmeralda (~152deg), violeta (~262deg)
#    y del dorado original (~42deg).
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(110, 85, 35), (122, 90, 30), (15, 11, 7), (180, 140, 60), (185, 138, 128), (212, 168, 75),
          (232, 207, 150), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]
# nota: (27,21,14) y (36,28,20) solo aparecen dentro del bloque .merktop-badge (protegido arriba).
TARGET_HUE = 35 / 360.0
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
print('ACCENT_DEEP', ACCENT_DEEP, 'ACCENT_MID', ACCENT_MID)

# ============================================================
# 3. GLOBALES: Booksy (no hay Instagram publico verificado: se usa telefono como
#    canal secundario en todo el sitio en su lugar)
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://booksy.com/en-us/1194438_crowned-locs_braids-locs_15985_largo'
rep_all(OLD_BOOKSY, BK)

TEL = 'tel:+17275588547'
PHONE_DISPLAY = '727-558-8547'

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Crowned Locs · Loc &amp; Dreadlock Studio in Largo, FL | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Crowned Locs, Largo FL: routine retwists, Instant Locs, Crochet and Wicks maintenance and the Loc Mastery workshop with Briana Drayton. 5.0 rating across 41 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Crowned Locs · Loc &amp; Dreadlock Studio in Largo, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Routine retwists, Instant Locs and loc maintenance with Briana Drayton. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-8.jpg" />',
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
    "name": "Crowned Locs",
    "description": "Loc and dreadlock studio in Largo, FL: routine retwists, Instant Locs installs, Crochet and Wicks maintenance, and the Loc Mastery: Parent &amp; Me workshop with Briana Drayton.",
    "address": { "@type": "PostalAddress", "streetAddress": "990 Missouri Ave N", "addressLocality": "Largo", "addressRegion": "FL", "postalCode": "33770", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.92640561002141, "longitude": -82.78601713478565 },
    "telephone": "+1-727-558-8547",
    "sameAs": ["https://booksy.com/en-us/1194438_crowned-locs_braids-locs_15985_largo"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "41", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Friday"], "opens": "09:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday"], "opens": "09:00", "closes": "15:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Loc care services", "itemListElement": [
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Routine Retwist" } },
      { "@type": "Offer", "price": "350", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Instant Locs (Up to 40 locs)" } },
      { "@type": "Offer", "price": "125", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Loc Mastery: Parent and Me Loc Care Workshop" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "In-Person Consultation" } }
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
    <span class="pre-mono">CL</span>
    <span class="pre-word">Crowned Locs</span>
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
        <img src="assets/raw/bk-2.jpg" alt="Crowned Locs" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Crowned <span class="text-[color:var(--accent-deep)]">Locs</span></span>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Largo, FL · Estudio de Locs" data-en="Largo, FL · Loc Studio">Largo, FL · Loc Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Locs saludables, cuidados a mano." data-en="Healthy locs, cared for by hand.">Healthy locs, cared for by hand.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Retwists, Instant Locs y" data-en="Routine retwists, Instant Locs and">Routine retwists, Instant Locs and</span><br /><span data-es="cuidado de locs, " data-en="loc care, ">loc care, </span><span class="text-shine" data-es="hecho bien" data-en="done right">done right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Briana &quot;Bri&quot; Drayton retuerce, mantiene e instala locs en Crowned Locs, en Largo: retwists de rutina, instalaciones de Instant Locs, mantenimiento Crochet y Wicks sin producto, y hasta un taller Loc Mastery para padres e hijos. 5.0 perfecto en 41 reseñas de Booksy." data-en="Briana &quot;Bri&quot; Drayton retwists, maintains and installs locs at Crowned Locs in Largo: routine retwists, Instant Locs installs, product-free Crochet and Wicks maintenance, and a hands-on Loc Mastery workshop for parents and kids. A perfect 5.0 across 41 reviews on Booksy.">Briana &quot;Bri&quot; Drayton retwists, maintains and installs locs at Crowned Locs in Largo: routine retwists, Instant Locs installs, product-free Crochet and Wicks maintenance, and a hands-on Loc Mastery workshop for parents and kids. A perfect 5.0 across 41 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 41 reseñas en Booksy" data-en="5.0 · 41 reviews on Booksy">5.0 · 41 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{TEL}" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span data-es="Llamar o enviar mensaje" data-en="Call or text">Call or text</span>
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-8.jpg" alt="Finished wrapped loc style with faded sides at Crowned Locs, Largo" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg" data-es="Retwist de Rutina" data-en="Routine Retwist">Routine Retwist</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$100 · 2h 30min" data-en="$100 · 2h 30min">$100 · 2h 30min</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="41">41</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Retwists</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Rutina · Instant Locs · Crochet" data-en="Routine · Instant Locs · Crochet">Routine · Instant Locs · Crochet</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Loc Mastery" data-en="Loc Mastery">Loc Mastery</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Taller para padres e hijos" data-en="Parent &amp; Me workshop">Parent &amp; Me workshop</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Largo</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Missouri Ave N</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Routine Retwist</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Instant Locs</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Loc Maintenance</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Wicks</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Loc Mastery</span><span class="marquee-star">✦</span>
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
          <img src="assets/raw/bk-13.jpg" alt="Long retwisted locs with a clean grid parting pattern" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-12.jpg" alt="Close-up of a precise grid retwist pattern at Crowned Locs" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una loctician," data-en="One loctician,">One loctician,</span><br /><span class="text-shine" data-es="cuidado que se nota" data-en="care that shows">care that shows</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Crowned Locs es el estudio de locs de Briana &quot;Bri&quot; Drayton en Largo: retwists de rutina, instalaciones de Instant Locs, mantenimiento Crochet y Wicks sin producto, y el taller Loc Mastery para padres e hijos, todo hecho a mano, cliente por cliente." data-en="Crowned Locs is Briana &quot;Bri&quot; Drayton&#39;s loc studio in Largo: routine retwists, Instant Locs installs, product-free Crochet and Wicks maintenance, and the Loc Mastery workshop for parents and kids, all done by hand, one client at a time.">Crowned Locs is Briana &quot;Bri&quot; Drayton&#39;s loc studio in Largo: routine retwists, Instant Locs installs, product-free Crochet and Wicks maintenance, and the Loc Mastery workshop for parents and kids, all done by hand, one client at a time.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus reseñas lo repiten una y otra vez: manos gentiles incluso para cueros cabelludos muy sensibles, y un ambiente limpio y profesional en cada cita. 5.0 perfecto en 41 reseñas de Booksy." data-en="Her reviews say it again and again: gentle hands even for scalps that are severely tender headed, and a clean, professional atmosphere every visit. A perfect 5.0 across 41 reviews on Booksy.">Her reviews say it again and again: gentle hands even for scalps that are severely tender headed, and a clean, professional atmosphere every visit. A perfect 5.0 across 41 reviews on Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="41">41</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Crowned Locs logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Briana &quot;Bri&quot; Drayton · <span class="text-[color:var(--ink-40)]" data-es="Dueña y Loctician" data-en="Owner &amp; Loctician">Owner &amp; Loctician</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu retwist de rutina, una instalación de Instant Locs o el taller Loc Mastery en Booksy con precio claro, o llamas o envías mensaje al 727-558-8547." data-en="Pick a routine retwist, an Instant Locs install or the Loc Mastery workshop on Booksy with clear pricing, or call or text 727-558-8547 first.">Pick a routine retwist, an Instant Locs install or the Loc Mastery workshop on Booksy with clear pricing, or call or text 727-558-8547 first.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consultation">Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Bri revisa el estado de tus locs, tu cuero cabelludo y tus metas antes de cualquier retwist o instalación nueva." data-en="Bri checks your loc journey, scalp and goals before any retwist or new install begins.">Bri checks your loc journey, scalp and goals before any retwist or new install begins.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El trabajo" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cada cita recibe su tiempo completo, desde un retwist de 2h 30min hasta una instalación de Instant Locs de todo el día." data-en="Every appointment gets its full time, from a 2h 30min retwist to a full-day Instant Locs install.">Every appointment gets its full time, from a 2h 30min retwist to a full-day Instant Locs install.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con indicaciones claras de cuidado y tu próxima cita de mantenimiento de 8-12 semanas ya planeada." data-en="You leave with clear care guidance and your next 8-12 week maintenance appointment already planned.">You leave with clear care guidance and your next 8-12 week maintenance appointment already planned.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (11 servicios reales de Booksy: 4 cards destacadas + bloque de precios completo)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios publicados por Crowned Locs en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by Crowned Locs on Booksy. Booking confirms instantly.">Prices as published by Crowned Locs on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Retwist de Rutina" data-en="Routine Retwist">Routine Retwist</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El mantenimiento base de tus locs, con manos gentiles que sus reseñas describen una y otra vez." data-en="Your locs&#39; base maintenance, with the gentle hands her reviews describe again and again.">Your locs&#39; base maintenance, with the gentle hands her reviews describe again and again.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Instalación" data-en="Install">Install</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Instant Locs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Instalación de Instant Locs hasta 40 locs; hasta 85 locs disponible desde $550, 8h 30min." data-en="Instant Locs install up to 40 locs; up to 85 locs available from $550, 8h 30min.">Instant Locs install up to 40 locs; up to 85 locs available from $550, 8h 30min.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$350+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">7h 30min+</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Taller" data-en="Workshop">Workshop</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Loc Mastery: Padres e Hijos" data-en="Loc Mastery: Parent &amp; Me">Loc Mastery: Parent &amp; Me</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Taller práctico de cuidado de locs para que aprendas a partir y retwistear los locs de tu hijo en casa." data-en="A hands-on loc care workshop so you learn to part and retwist your child&#39;s locs at home.">A hands-on loc care workshop so you learn to part and retwist your child&#39;s locs at home.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$125</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Primer paso" data-en="First step">First step</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Consulta en Persona" data-en="In-Person Consultation">In-Person Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Revisamos el estado de tus locs y trazamos el plan correcto antes de tu primera cita." data-en="A review of your locs and the right plan mapped out before your first appointment.">A review of your locs and the right plan mapped out before your first appointment.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="reveal glass rounded-3xl p-7 sm:p-9 mt-8" style="transition-delay:120ms">
        <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="También en el estudio" data-en="Also at the studio">Also at the studio</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-3 text-sm">
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Mantenimiento de Locs (8-12 sem.)" data-en="8-12 Weeks Loc Maintenance">8-12 Weeks Loc Maintenance</span><span class="font-display text-[color:var(--accent-deep)]">$125</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Retwist Crochet sin producto (8-12 sem.)" data-en="8-12 Weeks Crochet Retwist (Product-Free)">8-12 Weeks Crochet Retwist (Product-Free)</span><span class="font-display text-[color:var(--accent-deep)]">$150</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Mantenimiento de Rutina Wicks sin producto" data-en="Wicks Routine Maintenance (Product-Free)">Wicks Routine Maintenance (Product-Free)</span><span class="font-display text-[color:var(--accent-deep)]">$150</span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Mantenimiento de Locs Extra Care" data-en="Extra Care Loc Maintenance">Extra Care Loc Maintenance</span><span class="font-display text-[color:var(--accent-deep)]">$160 <span class="text-[color:var(--ink-40)] text-xs">· 4h 30min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Mantenimiento Crochet Extra Care" data-en="Extra Care Crochet Maintenance">Extra Care Crochet Maintenance</span><span class="font-display text-[color:var(--accent-deep)]">$175 <span class="text-[color:var(--ink-40)] text-xs">· 5h 30min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2"><span class="font-light" data-es="Instant Locs (hasta 85 locs)" data-en="Instant Locs (Up to 85 locs)">Instant Locs (Up to 85 locs)</span><span class="font-display text-[color:var(--accent-deep)]">$550 <span class="text-[color:var(--ink-40)] text-xs">· 8h 30min</span></span></div>
          <div class="flex items-baseline justify-between border-b border-[color:var(--accent-ghost)] pb-2 sm:border-b-0"><span class="font-light" data-es="Depósito Loc Mastery" data-en="Loc Mastery Deposit">Loc Mastery Deposit</span><span class="font-display text-[color:var(--accent-deep)]">$250 <span class="text-[color:var(--ink-40)] text-xs">· 6h</span></span></div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 11 servicios y su disponibilidad completa están en Booksy. Reserva en línea o llama/escribe al 727-558-8547." data-en="All 11 services and full availability are on Booksy. Book online or call/text 727-558-8547.">All 11 services and full availability are on Booksy. Book online or call/text 727-558-8547.</span></p>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 4 tiles 3/4: 5 fotos reales curadas, sin graficos/banners)
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
        <a href="{BK}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Más en Booksy" data-en="More on Booksy">More on Booksy</span>
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Retwist recién hecho" data-en="Fresh retwist">Fresh retwist</span><img src="assets/raw/bk-14.jpg" alt="Freshly retwisted locs with a clean grid parting pattern at Crowned Locs" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Detalle de la partición" data-en="Parting detail">Parting detail</span><img src="assets/raw/bk-3.jpg" alt="Close-up top-down view of a grid retwist parting pattern" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Estilo envuelto" data-en="Wrapped style">Wrapped style</span><img src="assets/raw/bk-8.jpg" alt="Finished wrapped loc style with faded sides" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Partición de precisión" data-en="Precision parting">Precision parting</span><img src="assets/raw/bk-12.jpg" alt="Close-up of a precise grid retwist pattern" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Locs largos, retwisteados" data-en="Long locs, retwisted">Long locs, retwisted</span><img src="assets/raw/bk-13.jpg" alt="Long retwisted locs with a clean grid parting pattern" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
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
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="las clientas" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 41 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 41 verified reviews on Booksy">5.0 out of 5 · 41 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I am so pleased with Bri's work. I have received many compliments. My hair &amp; scalp feels wonderful, as I am severely tender headed."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jamila B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"If I could give Bee 10 stars I definitely would! She REALLY made me experience an enjoyable one! She answered all my questions, she made me feel at ease. TY LOVE GURL"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Raine</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She does beautiful work, efficient and very professional. Glad I found her ⭐️⭐️⭐️⭐️"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Stephanye F.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
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
# UBICACION (Direccion, Horario, Reservas, Llamar/Texto)
# ============================================================
MAPS_Q = '990+Missouri+Ave+N,+Largo,+FL+33770'
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
              <p class="text-sm text-[color:var(--ink-60)] font-light">990 Missouri Ave N, Largo, FL 33770</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lun, Mar, Mié, Vie 9:00 am – 5:00 pm · Jue 9:00 am – 3:00 pm · Sáb 8:00 am – 5:00 pm · Dom cerrado" data-en="Mon, Tue, Wed, Fri 9:00 AM - 5:00 PM · Thu 9:00 AM - 3:00 PM · Sat 8:00 AM - 5:00 PM · Closed Sundays">Mon, Tue, Wed, Fri 9:00 AM - 5:00 PM · Thu 9:00 AM - 3:00 PM · Sat 8:00 AM - 5:00 PM · Closed Sundays</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Llama o escribe" data-en="Call or text">Call or text</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Para dudas rápidas o para agendar directamente con Bri." data-en="For quick questions or to book straight with Bri.">For quick questions or to book straight with Bri.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="{TEL}">{PHONE_DISPLAY}</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Crowned Locs, 990 Missouri Ave N, Largo FL"
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
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Locs saludables, cuidados a mano." data-en="Healthy locs, cared for by hand.">Healthy locs, cared for by hand.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo retwist" data-en="Your next retwist">Your next retwist</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: un retwist de rutina, una instalación de Instant Locs o el taller Loc Mastery." data-en="Book a routine retwist, an Instant Locs install or the Loc Mastery workshop online in seconds.">Book a routine retwist, an Instant Locs install or the Loc Mastery workshop online in seconds.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="{TEL}" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Llamar a Crowned Locs" data-en="Call Crowned Locs">Call Crowned Locs</a>
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
    <span class="foot-mark" aria-hidden="true">Crowned Locs</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Crowned Locs" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Crowned Locs</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de locs y dreadlocks en Largo, FL. Atención con cita previa." data-en="Loc and dreadlock studio in Largo, FL. By appointment only.">Loc and dreadlock studio in Largo, FL. By appointment only.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>990 Missouri Ave N, Largo, FL 33770</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</p>
        <p><a href="{TEL}" class="hover:text-[#e9c3ab]">{PHONE_DISPLAY}</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Crowned Locs.</p>
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
for word in ['Routine Retwist', 'Instant Locs', 'Loc Maintenance', 'Wicks', 'Loc Mastery', 'Largo, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (graficos/banners/overlays, no curados) nunca deben aparecer
for banned in ['bk-1.jpg', 'bk-4.jpg', 'bk-5.jpg', 'bk-6.jpg', 'bk-7.jpg', 'bk-9.jpg',
               'bk-10.jpg', 'bk-11.jpg', 'bk-15.jpg', 'bk-16.jpg']:
    assert f'assets/raw/{banned}' not in h_final, f'ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk',
                  'Silk Press', 'K-Tip', 'knotless', 'Knotless']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/crowned-locs-largo', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
