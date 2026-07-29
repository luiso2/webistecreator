#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/scalp-bar-naples/index.html
Scalp Bar, Naples FL (2950 Immokalee Road, Suite 3, Naples, FL 34110). Head spa / scalp spa
boutique owned by Monica Luciano (licensed cosmetologist, certified hair loss practitioner,
trichologist-in-training). Signature: microscopic scalp analysis (trichoscope), detox/exfoliation,
Halo Water Sensory Experience. 4.9 / 133 reviews on Google (self-verified live via Birdeye's
Google-sourced aggregateRating JSON-LD, 2026-07-28). Booking via GlossGenius (scalpbar.glossgenius.com;
their own vanity domain scalpbarnaples.com 301-redirects there, so no site propio). Paleta copper
(hue-shift -16deg desde el dorado original del esqueleto, hacia un cobre/bronce calido que combina
con las lamparas de laton y el dispositivo "halo" real de las fotos).
"""
import re
import os

SRC = 'templates/dark-v2/index.html'
DST = 'output/scalp-bar-naples/index.html'

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
# 2. PALETA: dorado -> cobre/bronce (hue-shift -16deg)
# ============================================================
PALETTE = [
    ('#0c0905', '#0c0705'),
    ('#0f0b07', '#0f0907'),
    ('#100c05', '#100905'),
    ('#171207', '#170e07'),
    ('#191307', '#190e07'),
    ('#1c1408', '#1c0f08'),
    ('#241c0e', '#24160e'),
    ('#6b5222', '#6b3f22'),
    ('#8a744a', '#8a634a'),
    ('#96742c', '#96582c'),
    ('#9a7431', '#9a5831'),
    ('#b8934a', '#b8764a'),
    ('#bfa060', '#bf8760'),
    ('#c9a04a', '#c97e4a'),
    ('#c9ab6b', '#c9926b'),
    ('#d4a84b', '#d4834b'),
    ('#e5c374', '#e5a574'),
    ('#e8c476', '#e8a676'),
    ('#e8cf96', '#e8b996'),
    ('#e9c3ab', '#e9b2ab'),
    ('#ecd9a8', '#ecc7a8'),
    ('#f0dc9e', '#f0c69e'),
    ('#f0dcae', '#f0caae'),
    ('#f5efe3', '#f5eae3'),
    ('#f8eed3', '#f8e4d3'),
    ('#faf1dc', '#fae9dc'),
    ('#fbf6ea', '#fbf1ea'),
    # ('#f4eee2', ...) se omite: unica aparicion es "Powered by Merktop", protegido via badge_html.
    # (uppercase 'D4A84B') se omite: unica aparicion es .merktop-dot, protegido via badge_css.
]
for old, new in PALETTE:
    rep_all(old, new)

RGBA_FAMILIES = [
    ((212, 168, 75), (212, 131, 75)),
    ((232, 207, 150), (232, 185, 150)),
    ((245, 239, 227), (245, 234, 227)),
    ((80, 58, 18), (80, 41, 18)),
    ((110, 85, 35), (110, 65, 35)),
    ((122, 90, 30), (122, 65, 30)),
    ((180, 140, 60), (180, 108, 60)),
    ((54, 42, 38), (54, 38, 38)),
    ((15, 11, 7), (15, 9, 7)),
    ((232, 210, 160), (232, 191, 160)),
    ((185, 138, 128), (185, 128, 133)),
]
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
# 3. GLOBALES: Booksy->GlossGenius, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://scalpbar.glossgenius.com'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
IG = 'https://www.instagram.com/scalp.bar/'
rep_all(OLD_IG_URL, IG)

rep_all('@pure.artistrysk', '@scalp.bar')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Scalp Bar · Head Spa in Naples, FL | Scalp Spa, Trichology &amp; Halo Water Ritual | 4.9 on Google</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Scalp Bar, Naples FL: scalp spa, microscopic scalp analysis, trichology-based treatments and the Halo Water Sensory Experience. 4.9 rating across 133 Google reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Scalp Bar · Head Spa in Naples, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Scalp spa, trichology and the Halo Water Sensory Experience. 4.9 on Google. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />',
)
# theme-color ya quedo actualizado por el replace global de paleta (#0f0b07 -> #0f0907)
assert '<meta name="theme-color" content="#0f0907" />' in h

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "Scalp Bar",
    "description": "Head spa and scalp spa in Naples, FL: microscopic scalp analysis, detox and exfoliation, and the signature Halo Water Sensory Experience, led by licensed cosmetologist and certified hair loss practitioner Monica Luciano.",
    "address": { "@type": "PostalAddress", "streetAddress": "2950 Immokalee Road, Suite 3", "addressLocality": "Naples", "addressRegion": "FL", "postalCode": "34110", "addressCountry": "US" },
    "telephone": "+19413631806",
    "email": "scalpbarnaples@gmail.com",
    "sameAs": ["https://scalpbar.glossgenius.com", "https://www.instagram.com/scalp.bar/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "133", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Friday"], "opens": "09:00", "closes": "17:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday"], "opens": "10:00", "closes": "17:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "16:30" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Scalp spa services", "itemListElement": [
      { "@type": "Offer", "price": "250", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Ultimate Scalp Spa" } },
      { "@type": "Offer", "price": "199", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "LUXE Scalp Spa" } },
      { "@type": "Offer", "price": "135", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Bliss Scalp Spa" } },
      { "@type": "Offer", "price": "99", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gentleman's Scalp Spa" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: badge + paleta + globales + head/JSON-LD')

# ============================================================
# 5. IDIOMA: esqueleto dark-v2 ya es EN default (negocio ingles, Naples FL) -> sin cambios
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
    <span class="pre-mono">SB</span>
    <span class="pre-word">Scalp Bar</span>
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
        <img src="assets/logo.jpg" alt="Scalp Bar" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,131,75,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Scalp <span class="text-[color:var(--accent-deep)]">Bar</span></span>
      </a>
      <nav class="hidden md:flex items-center gap-7 text-sm font-light">
        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">The Experience</a>
        <a class="nav-link" href="#metodo" data-es="El Ritual" data-en="The Ritual">The Ritual</a>
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
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Ritual" data-en="The Ritual">The Ritual</a>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Naples, FL · Head Spa" data-en="Naples, FL · Head Spa">Naples, FL · Head Spa</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cabello sano, saludable y hermoso, empieza en el cuero cabelludo." data-en="Healthy, beautiful hair starts with a healthy scalp.">Healthy, beautiful hair starts with a healthy scalp.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Cuidado capilar," data-en="Scalp health,">Scalp health,</span><br /><span data-es="respaldado por " data-en="backed by ">backed by </span><span class="text-shine" data-es="ciencia real" data-en="real science">real science</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Análisis microscópico del cuero cabelludo, desintoxicación, exfoliación y la firma Halo Water Sensory Experience. Scalp Bar es el head spa de Naples liderado por Monica Luciano, cosmetóloga licenciada y practicante certificada en pérdida de cabello, con 4.9 en 133 reseñas de Google." data-en="Microscopic scalp analysis, detox and exfoliation, and the signature Halo Water Sensory Experience. Scalp Bar is Naples' head spa, led by licensed cosmetologist and certified hair loss practitioner Monica Luciano, with a 4.9 rating across 133 Google reviews.">Microscopic scalp analysis, detox and exfoliation, and the signature Halo Water Sensory Experience. Scalp Bar is Naples' head spa, led by licensed cosmetologist and certified hair loss practitioner Monica Luciano, with a 4.9 rating across 133 Google reviews.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.9 · 133 reseñas en Google" data-en="4.9 · 133 reviews on Google">4.9 · 133 reviews on Google</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="tel:+19413631806" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span data-es="(941) 363-1806" data-en="(941) 363-1806">(941) 363-1806</span>
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/hero.jpg" alt="Client relaxing during a scalp spa treatment at Scalp Bar, Naples, with an eye mask and the halo water ritual device" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Ultimate Scalp Spa</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$250 · 2h" data-en="$250 · 2h">$250 · 2h</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="133">133</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Scalp <span class="text-shine">&amp;</span> Trichology</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Análisis · Detox · Halo Ritual" data-en="Analysis · Detox · Halo Ritual">Analysis · Detox · Halo Ritual</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Halo Water Ritual" data-en="Halo Water Ritual">Halo Water Ritual</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Firma de la casa" data-en="Signature finish">Signature finish</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Naples</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2950 Immokalee Rd</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Scalp Spa</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Head Spa</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Trichology</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Halo Water Ritual</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hair Restoration</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Naples, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/experience-1.jpg" alt="Scalp Bar specialist performing the halo water ritual on a client, Naples FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/experience-2.jpg" alt="Finishing blowdry detail on freshly treated hair at Scalp Bar" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un solo head spa," data-en="One head spa,">One head spa,</span><br /><span class="text-shine" data-es="respaldado por ciencia" data-en="backed by science">backed by science</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Scalp Bar es el head spa de Naples fundado por Monica Luciano, cosmetóloga licenciada, practicante certificada en pérdida de cabello y en formación como tricóloga. Cada cita empieza con un análisis microscópico del cuero cabelludo para que veas su estado real antes de cualquier tratamiento." data-en="Scalp Bar is the Naples head spa founded by Monica Luciano, a licensed cosmetologist, certified hair loss practitioner and trichologist-in-training. Every visit starts with a microscopic scalp analysis so you see the real state of your scalp before any treatment begins.">Scalp Bar is the Naples head spa founded by Monica Luciano, a licensed cosmetologist, certified hair loss practitioner and trichologist-in-training. Every visit starts with a microscopic scalp analysis so you see the real state of your scalp before any treatment begins.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="De la desintoxicación y exfoliación a la firma Halo Water Sensory Experience, el ritual combina terapia de calor, frío y vapor con tricología real. 4.9 en 133 reseñas de Google lo confirman." data-en="From detox and exfoliation to the signature Halo Water Sensory Experience, the ritual blends hot, cold and steam therapy with real trichology. A 4.9 rating across 133 Google reviews backs it up.">From detox and exfoliation to the signature Halo Water Sensory Experience, the ritual blends hot, cold and steam therapy with real trichology. A 4.9 rating across 133 Google reviews backs it up.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="133">133</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Halo" data-en="Halo">Halo</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Water Ritual" data-en="Water Ritual">Water Ritual</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/logo.jpg" alt="Scalp Bar" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,131,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Monica Luciano · <span class="text-[color:var(--ink-40)]" data-es="Fundadora y especialista en cuero cabelludo" data-en="Founder &amp; Scalp Specialist">Founder &amp; Scalp Specialist</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: marquee x2 + experiencia definidos')

# ============================================================
# EL METODO (El Ritual, 4 pasos reales del servicio Bliss Scalp Spa)
# ============================================================
NEW_METODO = '''<!-- EL METODO -->
  <section id="metodo" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">02</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="El ritual" data-en="The ritual">The ritual</span> <span class="text-shine" data-es="Scalp Bar" data-en="at Scalp Bar">at Scalp Bar</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Análisis del cuero cabelludo" data-en="Scalp analysis">Scalp analysis</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Un análisis microscópico bajo aumento muestra el estado real de tu cuero cabelludo antes de empezar cualquier tratamiento." data-en="A microscopic scalp analysis under magnification shows the true, follicle-level state of your scalp before any treatment begins.">A microscopic scalp analysis under magnification shows the true, follicle-level state of your scalp before any treatment begins.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Detox y vapor" data-en="Detox &amp; steam">Detox &amp; steam</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Mascarilla de ojos tibia, aromaterapia, aceites nutritivos y un tratamiento detox a medida, con exfoliación y terapia de calor, frío y vapor." data-en="A warm eye mask, aromatherapy, nourishing oils and a customized detox treatment, with exfoliation and hot, cold and steam therapy.">A warm eye mask, aromatherapy, nourishing oils and a customized detox treatment, with exfoliation and hot, cold and steam therapy.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Halo Water Ritual" data-en="Halo Water Ritual">Halo Water Ritual</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="La firma Halo Water Sensory Experience: una cascada refrescante y varias técnicas de masaje que liberan tensión y estimulan la circulación." data-en="The signature Halo Water Sensory Experience: a refreshing cascade and multiple massage techniques that release tension and stimulate circulation.">The signature Halo Water Sensory Experience: a refreshing cascade and multiple massage techniques that release tension and stimulate circulation.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Nutrición y plan" data-en="Nourish &amp; plan">Nourish &amp; plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Mascarilla capilar personalizada, tratamiento leave-in y un secado final, con un plan de cuidado en casa antes de tu próxima cita." data-en="A customized hair mask, leave-in conditioning treatment and a finishing dry, with an at-home care plan before your next visit.">A customized hair mask, leave-in conditioning treatment and a finishing dry, with an at-home care plan before your next visit.</p>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: metodo definido')

# ============================================================
# SERVICIOS (4 cards destacadas + menu completo agrupado, sin acordeon)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="ritual" data-en="ritual">ritual</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Scalp Bar en GlossGenius. Reserva con confirmación inmediata." data-en="Prices and durations as published by Scalp Bar on GlossGenius. Booking confirms instantly.">Prices and durations as published by Scalp Bar on GlossGenius. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,131,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Ultimate Scalp Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Análisis microscópico bajo aumento, tratamiento de alta frecuencia y una mini facial con Circadia: el ritual más completo del menú." data-en="Microscopic scalp analysis under magnification, a high-frequency treatment and a Circadia mini facial layered into the most complete ritual on the menu.">Microscopic scalp analysis under magnification, a high-frequency treatment and a Circadia mini facial layered into the most complete ritual on the menu.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$250</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">120 min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Ritual completo" data-en="Full ritual">Full ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3">LUXE Scalp Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Mini facial con Circadia y enzima de cacao, mascarilla a medida y mascarilla de ojos tibia, combinada con el ritual completo de scalp spa." data-en="A Circadia mini facial with cocoa enzyme exfoliation, a custom mask and warm eye mask, paired with the full scalp spa ritual.">A Circadia mini facial with cocoa enzyme exfoliation, a custom mask and warm eye mask, paired with the full scalp spa ritual.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$199</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">90 min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="La mas reservada" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Bliss Scalp Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Aromaterapia, un tratamiento detox a medida, exfoliación y la Halo Water Sensory Experience, terminado con mascarilla hidratante." data-en="Aromatherapy, a customized detox treatment, exfoliation and the Halo Water Sensory Experience, finished with a hydrating mask and rough dry.">Aromatherapy, a customized detox treatment, exfoliation and the Halo Water Sensory Experience, finished with a hydrating mask and rough dry.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$135</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">60 min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para caballeros" data-en="For gentlemen">For gentlemen</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gentleman's Scalp Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Mascarilla de ojos herbal tibia, exfoliación suave, terapia de halo water, vapor aromático y masaje terminado con terapia fría." data-en="A warm herbal eye mask, gentle exfoliation, halo water therapy, aromatic steam and a massage finished with cold therapy.">A warm herbal eye mask, gentle exfoliation, halo water therapy, aromatic steam and a massage finished with cold therapy.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$99</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40 min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>

      <div class="reveal mt-14 grid md:grid-cols-3 gap-5" style="transition-delay:120ms">
        <div class="glass rounded-3xl p-7">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Mas Scalp Spa" data-en="More Scalp Spa">More Scalp Spa</p>
          <div class="space-y-3 text-sm">
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Summer Refresh Special" data-en="Summer Refresh Special">Summer Refresh Special</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$165 · 90 min</span></div>
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Extension Removal &amp; Scalp Spa" data-en="Extension Removal &amp; Scalp Spa">Extension Removal &amp; Scalp Spa</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$165 · 90 min</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Servicios adicionales" data-en="Add-on services">Add-on services</p>
          <div class="space-y-3 text-sm">
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Análisis microscópico del cuero cabelludo" data-en="Microscopic Scalp Analysis">Microscopic Scalp Analysis</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$50</span></div>
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Blowdry (cabello corto)" data-en="Blowdry (short hair)">Blowdry (short hair)</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$30</span></div>
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Blowdry (cabello largo)" data-en="Blowdry (long hair)">Blowdry (long hair)</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$35</span></div>
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Mascarilla K18 Molecular Repair" data-en="K18 Molecular Repair Mask">K18 Molecular Repair Mask</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$15</span></div>
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Dream Coat XL Treatment" data-en="Dream Coat XL Treatment">Dream Coat XL Treatment</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$25</span></div>
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Dream Coat Curl Treatment" data-en="Dream Coat Curl Treatment">Dream Coat Curl Treatment</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$25</span></div>
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Dream Filter Treatment" data-en="Dream Filter Treatment">Dream Filter Treatment</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$20</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Keratina y membresías" data-en="Keratin &amp; memberships">Keratin &amp; memberships</p>
          <div class="space-y-3 text-sm">
            <div class="flex items-baseline justify-between gap-3"><span class="font-light" data-es="Keratin Natural Smoothing Treatment" data-en="Keratin Natural Smoothing Treatment">Keratin Natural Smoothing Treatment</span><span class="text-[color:var(--ink-40)] whitespace-nowrap" data-es="Desde $350" data-en="From $350">From $350</span></div>
          </div>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mt-4" data-es="Membresías Silver, Gold y Platinum con precio preferencial de Scalp Spa. Pregunta al reservar en GlossGenius." data-en="Silver, Gold and Platinum memberships with preferred Scalp Spa pricing. Ask when booking on GlossGenius.">Silver, Gold and Platinum memberships with preferred Scalp Spa pricing. Ask when booking on GlossGenius.</p>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo y disponibilidad en GlossGenius. Debes tener 16 años o más para reservar." data-en="Full menu and availability on GlossGenius. Guests must be 16 or older to book.">Full menu and availability on GlossGenius. Guests must be 16 or older to book.</span></p>
    </div>
  </section>

  '''

print('OK: servicios definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 4 tiles 3/4: 5 fotos reales curadas)
# ============================================================
NEW_GALERIA = f'''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="El ritual," data-en="The ritual,">The ritual,</span> <span class="text-shine" data-es="en vivo" data-en="in real life">in real life</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @scalp.bar
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Suite boutique de scalp spa" data-en="Boutique scalp spa suite">Boutique scalp spa suite</span><img src="assets/gallery-interior.jpg" alt="Interior of the Scalp Bar boutique suite in Naples, FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Gentleman's Scalp Spa" data-en="Gentleman's Scalp Spa">Gentleman's Scalp Spa</span><img src="assets/gallery-gentleman.jpg" alt="Male client receiving the Gentleman's Scalp Spa treatment with the halo water ritual device" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalle del masaje" data-en="Massage detail">Massage detail</span><img src="assets/gallery-massage.jpg" alt="Close-up detail of a scalp massage during a Scalp Bar treatment" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Halo Water Ritual" data-en="Halo Water Ritual">Halo Water Ritual</span><img src="assets/gallery-specialist.jpg" alt="Scalp Bar specialist performing the halo water ritual on a client" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Vapor y desintoxicación" data-en="Steam &amp; detox">Steam &amp; detox</span><img src="assets/gallery-steam.jpg" alt="Steam detox treatment in progress at Scalp Bar, Naples" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

print('OK: galeria definida')

# ============================================================
# OPINIONES (3 reseñas reales verbatim de Google, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="los clientes" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 133 reseñas verificadas en Google" data-en="4.9 out of 5 · 133 verified reviews on Google">4.9 out of 5 · 133 verified reviews on Google</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I had the 'ultimate' scalp service with Monica. She's incredibly knowledgeable and so very nice. I learned a lot and really loved the treatment. Besides my hair, I received a very relaxing facial. I highly recommend."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Judy E</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Scalp Bar Head Spa is absolutely amazing! I booked an appointment with Bailey, and she is truly the sweetest and most knowledgeable person I have ever met. She took the time to explain everything detail by detail. I left feeling relaxed and completely educated on how to care for my scalp."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Stephanie Marie Narvaez</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Not very often do you experience something so informative as well as so deeply relaxing. Bailey did an amazing job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ethan Klein</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las reseñas en Google" data-en="Read reviews on Google">Read reviews on Google</a>
      </div>
    </div>
  </section>

  '''

print('OK: opiniones definidas')

# ============================================================
# UBICACION (Direccion, Horario, Reservas, Instagram)
# ============================================================
MAPS_Q = '2950+Immokalee+Rd,+Naples,+FL+34110'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Naples</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">2950 Immokalee Road, Suite 3, Naples, FL 34110</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,131,75,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mar-Vie 9:00am-5:30pm (Jue desde 10am) · Sáb 10:00am-4:30pm · Lun y Dom cerrado" data-en="Tue-Fri 9:00am-5:30pm (Thu from 10am) · Sat 10:00am-4:30pm · Closed Mon &amp; Sun">Tue-Fri 9:00am-5:30pm (Thu from 10am) · Sat 10:00am-4:30pm · Closed Mon &amp; Sun</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía GlossGenius, o llama al (941) 363-1806." data-en="By appointment via GlossGenius, or call (941) 363-1806.">By appointment via GlossGenius, or call (941) 363-1806.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,131,75,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira el ritual más reciente y escribe por DM cualquier duda antes de tu cita." data-en="See the latest rituals and DM any questions before your appointment.">See the latest rituals and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,131,75,0.4)]" href="{IG}" target="_blank" rel="noopener">@scalp.bar</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Scalp Bar, 2950 Immokalee Road, Naples FL"
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
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #190e07 0%, #100905 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cabello sano, saludable y hermoso, empieza en el cuero cabelludo." data-en="Healthy, beautiful hair starts with a healthy scalp.">Healthy, beautiful hair starts with a healthy scalp.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu ritual" data-en="Your ritual">Your ritual</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu análisis de cuero cabelludo, tu Halo Water Ritual o el scalp spa que llevas planeando." data-en="Book online in seconds: your scalp analysis, your Halo Water Ritual, or that scalp spa you have been planning.">Book online in seconds: your scalp analysis, your Halo Water Ritual, or that scalp spa you have been planning.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>
        <a href="tel:+19413631806" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Llamar: (941) 363-1806" data-en="Call: (941) 363-1806">Call: (941) 363-1806</a>
      </div>
    </div>
  </section>

  '''

print('OK: ubicacion + cta final definidos')

# ============================================================
# FOOTER (el merktop-badge original se mantiene intacto: badge_html)
# ============================================================
NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#0c0705]">
    <span class="foot-mark" aria-hidden="true">Scalp Bar</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/logo.jpg" alt="Scalp Bar logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,185,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Scalp Bar</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Head spa en Naples, FL. Atención con cita previa vía GlossGenius o por teléfono." data-en="Head spa in Naples, FL. By appointment via GlossGenius or by phone.">Head spa in Naples, FL. By appointment via GlossGenius or by phone.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>2950 Immokalee Road, Suite 3, Naples, FL 34110</p>
        <p class="text-xs text-[color:var(--ink-40)]" data-es="Mar-Vie 9am-5:30pm · Sáb 10am-4:30pm" data-en="Tue-Fri 9am-5:30pm · Sat 10am-4:30pm">Tue-Fri 9am-5:30pm · Sat 10am-4:30pm</p>
        <p><a href="tel:+19413631806" class="hover:text-[#e9b2ab]">(941) 363-1806</a></p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#e9b2ab]" data-es="Reservas online · GlossGenius" data-en="Online booking · GlossGenius">Online booking · GlossGenius</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#e9b2ab]">Instagram · @scalp.bar</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Scalp Bar.</p>
        {badge_html}
      </div>
    </div>
  </footer>

  '''

# ============================================================
# BOTON FLOTANTE (mismo markup, solo GlossGenius url + aria-label EN)
# ============================================================
NEW_BOOKFLOAT = f'''<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c0f08" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
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
for word in ['Scalp Spa', 'Head Spa', 'Trichology', 'Halo Water Ritual', 'Hair Restoration', 'Naples, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (leftovers del esqueleto o raw sin curar) nunca deben aparecer
for banned in ['assets/raw/', 'bk-1.jpg', 'bk-2.jpg', 'bk-3.jpg', 'bk-4.jpg', 'bk-5.jpg',
               'bk-6.jpg', 'bk-7.jpg', 'bk-8.jpg', 'bk-9.jpg', 'bk-10.jpg', 'bk-11.jpg', 'bk-12.jpg']:
    assert banned not in h_final, f'foto/ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Pure Artistry', 'Orlando', '121705', 'Grant St', 'pure.artistrysk',
                 'silk press', 'Silk Press', 'NBA', 'MLB', 'Booksy']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/scalp-bar-naples', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)

print('OK: escrito', DST)
