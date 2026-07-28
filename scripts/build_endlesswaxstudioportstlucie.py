#!/usr/bin/env python3
"""Derivacion anclada: templates/light-v2/index.html -> output/endless-wax-studio-port-st-lucie/index.html
Endless Wax Studio & More, Port St. Lucie FL (2825 SW Brighton St #C, 34953). Full body waxing +
facials + lash/brow + permanent makeup studio owned by Iris Murray (25+ years, certified PMU
instructor). 4.9 rating / 376 reviews (labeled "Google rating" on the business's own zoca.com
booking microsite, self-verified live via the page HTML 2026-07-28). Booking: zoca.com (marketing
site with an embedded Acuity Scheduling widget). IG: @endlesswaxstudio. Public email found via
mailto: link on zoca.com: irisc.murray@gmail.com. Language: EN (site copy, reviews all English).
Palette: warm brass/champagne-gold hue-shift from light-v2's original plum-pink, matching the
studio's real sage-green walls + backlit gold circular logo sign seen in curated photos.
"""
import re
import os

SRC = 'templates/light-v2/index.html'
DST = 'output/endless-wax-studio-port-st-lucie/index.html'

h = open(SRC, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'ANCLA ROTA: ' + a[:160]
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    c = h.count(a)
    assert c > 0, 'ANCLA ROTA (0 matches): ' + a[:160]
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
# 2. PALETA: plum-pink original -> warm brass/champagne-gold
#    (hue-shift precomputado: delta +80 deg, saturacion x0.70, misma L,
#    calculado desde el rosa original del esqueleto light-v2)
# ============================================================
PALETTE = [
    ('a04a72', '938b57'),
    ('5c2140', '534b2a'),
    ('f0bed7', 'e8e3c6'),
    ('faf2f6', 'f9f8f3'),
    ('c47a9c', 'b9b285'),
    ('8a5573', '82795d'),
    ('f3e0ea', 'f0eee3'),
    ('d9a8c2', 'd2cbaf'),
    ('7d3457', '726b3f'),
    ('5f2c48', '575034'),
    ('33222c', '302d25'),
    ('fbf3f8', 'faf8f4'),
    ('fbeff5', 'f9f8f1'),
    ('f8dfeb', 'f4f2e3'),
    ('f6f1ea', 'ecf4ec'),
    ('f2d5e3', 'eeebd9'),
    ('f2cfe0', 'ede9d4'),
    ('efd0e0', 'eae6d5'),
    ('e5c1d4', 'e0dbc6'),
    ('dc9dbe', 'd3caa6'),
    ('d3a2bc', 'ccc5a9'),
    ('c9789f', 'bdb484'),
    ('b25a85', 'a59b67'),
    ('2a1722', '27241a'),
    ('1f0f18', '1d1a11'),
    ('1c0f16', '1a1811'),
]
for old, new in PALETTE:
    rep_all('#' + old, '#' + new)

RGBA_FAMILIES = [
    ((253, 246, 250), (252, 251, 247)),
    ((51, 34, 44), (48, 45, 37)),
    ((160, 74, 114), (147, 139, 87)),
    ((70, 25, 50), (63, 56, 32)),
    ((250, 242, 246), (249, 248, 243)),
    ((240, 190, 215), (232, 227, 198)),
    ((185, 138, 128), (156, 176, 137)),
    ((233, 205, 186), (202, 226, 193)),
    ((125, 52, 87), (114, 107, 63)),
    ((40, 16, 30), (36, 32, 20)),
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
# 3. GLOBALES: booking (zoca.com), Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
BK = 'https://endlesswaxportstlucie.zoca.com'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
IG = 'https://www.instagram.com/endlesswaxstudio/'
rep_all(OLD_IG_URL, IG)

rep_all('@_lashbloom', '@endlesswaxstudio')

print('OK: badge + paleta + globales (booking/IG)')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Endless Wax Studio &amp; More · Waxing, Facials &amp; PMU in Port St. Lucie, FL | 4.9 on Google</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Endless Wax Studio &amp; More, Port St. Lucie FL: Brazilian waxing, facials, lash extensions, brow shaping and permanent makeup with owner Iris Murray. 4.9 rating across 376 Google reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Endless Wax Studio &amp; More · Waxing, Facials &amp; PMU in Port St. Lucie, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Brazilian waxing, facials, lash extensions and permanent makeup. 4.9 on Google. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-storefront.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Endless Wax Studio & More",
    "description": "Full body waxing, facial and permanent makeup studio in Port St. Lucie, FL: Brazilian waxing for women and men, facials and skin treatments, lash extensions, brow shaping and permanent makeup.",
    "address": { "@type": "PostalAddress", "streetAddress": "2825 SW Brighton St, Suite C", "addressLocality": "Port St. Lucie", "addressRegion": "FL", "postalCode": "34953", "addressCountry": "US" },
    "telephone": "+17728772191",
    "email": "irisc.murray@gmail.com",
    "sameAs": ["https://endlesswaxportstlucie.zoca.com", "https://www.instagram.com/endlesswaxstudio/", "https://www.facebook.com/EndlessWaxStudioPSL"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "376", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Waxing, facial, lash/brow and PMU services", "itemListElement": [
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brazilian Waxing (Women's)" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brazilian Waxing (Men's)" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Signature Hydra Facial" } },
      { "@type": "Offer", "price": "119", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Eyelashes Extensions Classic Natural" } },
      { "@type": "Offer", "price": "400", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Permanent Make-Up Eyeliner or Eyebrows" } },
      { "@type": "Offer", "price": "89", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Custom Hydrafacial" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: head/JSON-LD')

# ============================================================
# 5. IDIOMA: el esqueleto light-v2 ya es EN default (negocio ingles) -> sin cambios
# ============================================================
assert "applyLang(lang === 'es' ? 'es' : 'en')" in h
assert '<html lang="en"' in h

# NOTA: la segmentacion por anclas de comentario se hace MAS ABAJO, despues de
# editar SERVICIOS in-place (los indices deben calcularse sobre el h ya mutado).

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">EW</span>
    <span class="pre-word">Endless Wax Studio</span>
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
        <img src="assets/logo.jpg" alt="Endless Wax Studio & More logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(147,139,87,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Endless <span class="text-[color:var(--accent-deep)]">Wax</span></span>
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

# ============================================================
# HERO
# ============================================================
NEW_HERO = f'''<!-- HERO -->
  <section id="top" class="relative min-h-screen flex items-center grain overflow-hidden pt-28 pb-16">
    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Port St. Lucie, FL · Estudio de Depilación" data-en="Port St. Lucie, FL · Waxing &amp; Skincare Studio">Port St. Lucie, FL · Waxing &amp; Skincare Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Con firmeza, siempre con delicadeza." data-en="Fearlessly gentle, every time.">Fearlessly gentle, every time.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Depilación, faciales y" data-en="Waxing, facials and">Waxing, facials and</span><br /><span data-es="PMU, hechos con " data-en="PMU, done ">PMU, done </span><span class="text-shine" data-es="delicadeza" data-en="gently">gently</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Endless Wax Studio & More es el estudio de depilación y cuidado de la piel de Iris Murray en Port St. Lucie: depilación brasileña para mujeres y hombres, faciales, extensión de pestañas, diseño de cejas y maquillaje permanente, con más de 25 años de experiencia en la industria de spa y belleza médica." data-en="Endless Wax Studio & More is Iris Murray's waxing and skincare studio in Port St. Lucie: Brazilian waxing for women and men, facials, lash extensions, brow shaping and permanent makeup, from an esthetician with over 25 years in the spa and medical beauty industry.">Endless Wax Studio &amp; More is Iris Murray's waxing and skincare studio in Port St. Lucie: Brazilian waxing for women and men, facials, lash extensions, brow shaping and permanent makeup, from an esthetician with over 25 years in the spa and medical beauty industry.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.9 · 376 reseñas en Google" data-en="4.9 · 376 reviews on Google">4.9 · 376 reviews on Google</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar cita" data-en="Book online">Book online</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @endlesswaxstudio
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/hero-storefront.jpg" alt="Endless Wax Studio & More storefront in Port St. Lucie, FL" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Brazilian Waxing</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$65 · 30 min" data-en="$65 · 30 min">$65 · 30 min</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="376">376</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Waxing <span class="text-shine">&amp;</span> Facials</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Pestañas · Cejas · PMU" data-en="Lash · Brow · PMU">Lash · Brow · PMU</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+25 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Esteticista con licencia" data-en="Licensed esthetician">Licensed esthetician</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Port St. Lucie</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2825 SW Brighton St</p></div>
    </div>
  </section>

  '''

print('OK: preloader + nav + hero + strip definidos')

# ============================================================
# MARQUEE (misma lista de palabras en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Brazilian Waxing</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Facials</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lash Extensions</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Shaping</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Permanent Makeup</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Port St. Lucie, FL</span><span class="marquee-star">✦</span>
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
          <img src="assets/experience-room.jpg" alt="Treatment room at Endless Wax Studio & More" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/experience-lounge.jpg" alt="Waiting lounge inside the studio in Port St. Lucie" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un solo estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="cuidado sin fin" data-en="endless care">endless care</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Endless Wax Studio & More es propiedad de Iris Murray, esteticista bilingüe con más de 25 años en la industria de spa y belleza médica, e instructora certificada de maquillaje permanente. Su equipo trabaja depilación brasileña, faciales, extensión de pestañas, diseño de cejas y maquillaje permanente en un estudio luminoso y privado en Port St. Lucie." data-en="Endless Wax Studio & More is owned by Iris Murray, a bilingual esthetician with more than 25 years in the spa and medical beauty industry and a certified permanent makeup instructor. Her team works Brazilian waxing, facials, lash extensions, brow shaping and permanent makeup inside a bright, private studio in Port St. Lucie.">Endless Wax Studio &amp; More is owned by Iris Murray, a bilingual esthetician with more than 25 years in the spa and medical beauty industry and a certified permanent makeup instructor. Her team works Brazilian waxing, facials, lash extensions, brow shaping and permanent makeup inside a bright, private studio in Port St. Lucie.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas repiten lo mismo una y otra vez: manos delicadas, un estudio impecable y un equipo que recuerda tu nombre. 4.9 de calificación en 376 reseñas de Google." data-en="Clients repeat the same thing over and over: gentle hands, a spotless studio and a team that remembers your name. A 4.9 rating across 376 reviews on Google.">Clients repeat the same thing over and over: gentle hands, a spotless studio and a team that remembers your name. A 4.9 rating across 376 reviews on Google.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="376">376</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">25+</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Años de experiencia" data-en="Years experience">Years experience</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/logo.jpg" alt="Endless Wax Studio & More" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(147,139,87,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Iris Murray · <span class="text-[color:var(--ink-40)]" data-es="Dueña y esteticista" data-en="Owner &amp; licensed esthetician">Owner &amp; licensed esthetician</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en zoca.com, desde una depilación brasileña hasta un facial completo, y confirmas tu cita en Port St. Lucie." data-en="Pick your service on zoca.com, from Brazilian waxing to a full facial, and confirm your appointment in Port St. Lucie.">Pick your service on zoca.com, from Brazilian waxing to a full facial, and confirm your appointment in Port St. Lucie.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Revisión de piel" data-en="Skin check">Skin check</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Iris o su equipo revisan tu piel y repasan qué esperar, sobre todo en una primera depilación o un nuevo facial o PMU." data-en="Iris or her team check your skin and go over what to expect, especially for a first wax or a new facial or PMU service.">Iris or her team check your skin and go over what to expect, especially for a first wax or a new facial or PMU service.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Tu servicio" data-en="Your service">Your service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Depilación, facial, set de pestañas o maquillaje permanente, con mano delicada en una sala privada e impecable." data-en="Waxing, facial, lash set or permanent makeup, done with a gentle hand in a private, spotless treatment room.">Waxing, facial, lash set or permanent makeup, done with a gentle hand in a private, spotless treatment room.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con recomendaciones de cuidado y tu próxima cita agendada, ya sea una brasileña de 3 semanas o un relleno de pestañas." data-en="You leave with aftercare tips and your next appointment already on the calendar, whether that is a 3 week Brazilian or a lash fill.">You leave with aftercare tips and your next appointment already on the calendar, whether that is a 3 week Brazilian or a lash fill.</p>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: metodo definido')

# ============================================================
# SERVICIOS: 4 highlight cards + menu completo agrupado por
# categoria (10 categorias reales del negocio, consolidadas en
# 6 bloques visibles con "y N mas" cuando aplica; nunca colapsable)
# ============================================================
NEW_SERVICIOS_ENCABEZADO_H2 = '''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span></h2>'''
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    NEW_SERVICIOS_ENCABEZADO_H2,
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Endless Wax Studio &amp; More. Reserva con confirmación en línea." data-en="Prices and durations as published by Endless Wax Studio &amp; More. Booking confirms online.">Prices and durations as published by Endless Wax Studio &amp; More. Booking confirms online.</p>',
)

grid_pattern = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m_grid = grid_pattern.search(h)
assert m_grid, 'grid destacados no encontrado'

def svc_row(name_es, name_en, price):
    if name_es == name_en:
        span = f'<span>{name_en}</span>'
    else:
        span = f'<span data-es="{name_es}" data-en="{name_en}">{name_en}</span>'
    return f'            <div class="flex items-center justify-between py-3">{span}<span class="font-display text-lg">{price}</span></div>\n'


NEW_HIGHLIGHTS = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Faciales" data-en="Facials">Facials</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Facial Hidratante de Firma" data-en="Signature Hydra Facial">Signature Hydra Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Facial de hidratación profunda con limpieza y extracción incluidas, una hora dedicada a tu piel." data-en="A deep hydrating facial with cleansing and extractions included, a full hour dedicated to your skin.">A deep hydrating facial with cleansing and extractions included, a full hour dedicated to your skin.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1 hour</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(147,139,87,0.4); box-shadow: 0 18px 50px rgba(48,45,37,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Depilación Brasileña" data-en="Brazilian Waxing">Brazilian Waxing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio más reservado del estudio: depilación brasileña completa con una técnica precisa y delicada. 30 minutos." data-en="The studio's most booked service: a full Brazilian wax with a precise, gentle technique. 30 minutes.">The studio's most booked service: a full Brazilian wax with a precise, gentle technique. 30 minutes.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30 min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pestañas y cejas" data-en="Lash &amp; brow">Lash &amp; brow</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Extensión de Pestañas Clásica" data-en="Eyelashes Extensions Classic Natural">Eyelashes Extensions Classic Natural</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una extensión por pestaña natural para un efecto limpio y elegante. Rellenos de 2 y 3 semanas disponibles." data-en="One extension per natural lash for a clean, elegant effect. 2 and 3 week fills available.">One extension per natural lash for a clean, elegant effect. 2 and 3 week fills available.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$119</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 40min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Maquillaje permanente" data-en="Permanent makeup">Permanent makeup</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cejas o Delineado Permanente" data-en="Permanent Make-Up Eyeliner or Eyebrows">Permanent Make-Up Eyeliner or Eyebrows</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Micropigmentación semipermanente de cejas o delineado, aplicada por una instructora certificada de PMU." data-en="Semi-permanent eyebrow or eyeliner cosmetic tattooing, applied by a certified PMU instructor.">Semi-permanent eyebrow or eyeliner cosmetic tattooing, applied by a certified PMU instructor.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$400</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2 hours</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>

      <!-- Menu completo por categoria: 10 categorias reales del negocio, agrupadas en 6 bloques -->
      <div class="grid lg:grid-cols-3 gap-5 mt-10">
        <div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-xl mb-5" data-es="Depilación para Mujeres" data-en="Women's Waxing">Women's Waxing</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
''' + \
    svc_row('Depilación Brasileña', 'Brazilian Waxing', '$65') + \
    svc_row('Bikini', 'Bikini Waxing', '$35') + \
    svc_row('Franja (Landing Strip)', 'Landing Strip Waxing', '$65') + \
    svc_row('Piernas, Pies y Dedos Completos', 'Full Legs, Feet &amp; Toes Waxing', '$70') + \
    svc_row('Piernas Superiores o Inferiores', 'Upper or Lower Legs Waxing', '$45') + \
    svc_row('Brazos Completos', 'Full Arms Waxing', '$40') + \
    svc_row('Axilas', 'Under Arms Waxing', '$20') + \
    svc_row('Rostro Completo', 'Full Face Waxing', '$35') + \
    svc_row('Labio, Mentón o Cejas', 'Lip, Chin or Brow Waxing', '$15') + \
    '''          </div>
          <p class="text-xs text-[color:var(--ink-40)] font-light mt-4" data-es="Y 8 servicios más: vientre, glúteos, entrepierna interna y más." data-en="Plus 8 more services: belly, buttock strip, inner thigh and more.">Plus 8 more services: belly, buttock strip, inner thigh and more.</p>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:90ms">
          <h3 class="font-display text-xl mb-5" data-es="Depilación para Hombres" data-en="Men's Waxing">Men's Waxing</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
''' + \
    svc_row('Depilación Brasileña (H)', 'Brazilian Waxing', '$85') + \
    svc_row('Pecho', 'Chest Waxing', '$65') + \
    svc_row('Espalda Completa', 'Full Back Waxing', '$65') + \
    svc_row('Media Espalda', 'Half Back Waxing', '$45') + \
    svc_row('Brazos Completos', 'Full Arms Waxing', '$50') + \
    svc_row('Piernas, Pies y Dedos Completos', 'Full Legs, Feet &amp; Toes Waxing', '$80') + \
    svc_row('Axilas', 'Under Arms Waxing', '$30') + \
    svc_row('Rostro Completo', 'Full Face Waxing', '$45') + \
    '''          </div>
          <p class="text-xs text-[color:var(--ink-40)] font-light mt-4" data-es="Y 3 servicios más: orejas, nariz y brasileña de mantenimiento." data-en="Plus 3 more services: ears, nose and ongoing Brazilian.">Plus 3 more services: ears, nose and ongoing Brazilian.</p>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:180ms">
          <h3 class="font-display text-xl mb-5" data-es="Pestañas y Cejas" data-en="Lash Extensions &amp; Brow Shaping">Lash Extensions &amp; Brow Shaping</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
''' + \
    svc_row('Extensión Clásica', 'Eyelashes Extensions Classic Natural', '$119') + \
    svc_row('Extensión Signature', 'Eyelashes Extensions Signature', '$129') + \
    svc_row('Extensión Mega/Diva', 'Eyelash Extension Mega/Diva', '$149') + \
    svc_row('Relleno Clásico/Signature 3 sem', 'Classic/Signature 3 Week Fill', '$75') + \
    svc_row('Laminado y Tinte de Cejas', 'Eyebrow Lamination Perm &amp; Tinting', '$75') + \
    svc_row('Laminado y Tinte de Pestañas', 'Eyelash Lamination Perm &amp; Tinting', '$85') + \
    svc_row('Depilación y Tinte de Cejas', 'Brow Waxing &amp; Tint', '$45') + \
    svc_row('Tinte de Pestañas o Cejas', 'Eyelash or Brow Tint', '$45') + \
    '''          </div>
          <p class="text-xs text-[color:var(--ink-40)] font-light mt-4" data-es="Y 3 servicios más: rellenos mega/diva de 2 y 3 semanas, remoción." data-en="Plus 3 more services: mega/diva 2 and 3 week fills, removal.">Plus 3 more services: mega/diva 2 and 3 week fills, removal.</p>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:270ms">
          <h3 class="font-display text-xl mb-5" data-es="Faciales" data-en="Facials Treatments">Facials Treatments</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
''' + \
    svc_row('Facial Hidratante de Firma', 'Signature Hydra Facial', '$75') + \
    svc_row('Microdermoabrasión', 'Microdermabrasion Treatment', '$95') + \
    svc_row('Peelings Químicos', 'Chemical Peels', '$150') + \
    svc_row('Dermaplaning', 'Derma-Planing', '$95') + \
    svc_row('Tratamiento Ultrasonido RF', 'Ultrasound RF Treatment', '$155') + \
    svc_row('Acné Adolescente/Adulto', 'Teen/Adult Acne', '$65') + \
    svc_row('Acné Adulto', 'Adult Acne', '$55') + \
    '''          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:360ms">
          <h3 class="font-display text-xl mb-5" data-es="Tratamientos de Piel" data-en="Skin Treatments">Skin Treatments</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
''' + \
    svc_row('Hydrafacial Personalizado', 'Custom Hydrafacial', '$89') + \
    svc_row('Iluminación Triple Berry', 'Triple Berry Brightening', '$110') + \
    svc_row('Peel Facial C-Peptide', 'C-Peptide Peel Facial', '$135') + \
    svc_row('Nano Infusión Regenerate', 'Regenerate Nano Infusion', '$149') + \
    svc_row('Microchanneling Procell', 'Procell Microchanneling', '$265') + \
    svc_row('Biorepeel Ci3', 'Biorepeel Ci3 One Treatment', '$245') + \
    svc_row('Jet Plasma', 'Jet Plasma', '$220') + \
    svc_row('Remoción de Verruga (1 Unidad)', 'Skin Tag Removal (1 Unit)', '$35') + \
    '''          </div>
          <p class="text-xs text-[color:var(--ink-40)] font-light mt-4" data-es="Y 5 servicios más: Oxigen Rx, Jet Plasma en paquete, The Swich y más." data-en="Plus 5 more services: Oxigen Rx, Jet Plasma package, The Swich and more.">Plus 5 more services: Oxigen Rx, Jet Plasma package, The Swich and more.</p>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:450ms">
          <h3 class="font-display text-xl mb-5" data-es="Maquillaje Permanente y Más" data-en="Permanent Makeup &amp; More">Permanent Makeup &amp; More</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
''' + \
    svc_row('Cejas o Delineado Permanente', 'PMU Eyeliner or Eyebrows', '$400') + \
    svc_row('Retoque de PMU', 'PMU Touch-Up', '$175') + \
    svc_row('Envoltura Corporal', 'Single Body Wrap', '$110') + \
    svc_row('Depilación de Glúteos', 'Buns &amp; In-Between Waxing', '$45') + \
    svc_row('Depilación con Velas (Oído)', 'Ear / Candling Waxing', '$15') + \
    svc_row('Brasileña Estudiante/Clienta', 'Student Brazilian / Pre-Existing Client', '$45') + \
    '''          </div>
        </div>
      </div>
      '''
h = h[:m_grid.start()] + NEW_HIGHLIGHTS + h[m_grid.end():]

nota_pattern = re.compile(r'<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>', flags=re.S)
m_nota = nota_pattern.search(h)
assert m_nota, 'nota de servicios no encontrada'
new_nota = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Más de 60 servicios entre depilación, faciales, pestañas, cejas y maquillaje permanente. Precios y duraciones publicados por Endless Wax Studio &amp; More; llama o reserva en línea para confirmar." data-en="60+ services across waxing, facials, lash, brow and permanent makeup. Prices and durations as published by Endless Wax Studio &amp; More; call or book online to confirm.">60+ services across waxing, facials, lash, brow and permanent makeup. Prices and durations as published by Endless Wax Studio &amp; More; call or book online to confirm.</span></p>'
h = h[:m_nota.start()] + new_nota + h[m_nota.end():]

print('OK: servicios (highlights + menu completo agrupado) definidos')

# ============================================================
# GALERIA (1 tile 16/9 + 3 tiles 3/4: 4 fotos reales curadas,
# distintas de hero/experiencia)
# ============================================================
NEW_GALERIA = f'''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Nuestro" data-en="Inside the">Inside the</span> <span class="text-shine" data-es="estudio" data-en="studio">studio</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @endlesswaxstudio
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Endless Wax Studio &amp; More" data-en="Endless Wax Studio &amp; More">Endless Wax Studio &amp; More</span><img src="assets/gallery-sign.jpg" alt="Endless Wax Studio & More logo sign inside the studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Interior del estudio" data-en="Inside the studio">Inside the studio</span><img src="assets/gallery-hallway.jpg" alt="Hallway inside Endless Wax Studio & More" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Recepción" data-en="Front desk">Front desk</span><img src="assets/gallery-reception.jpg" alt="Front desk at Endless Wax Studio & More" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Fachada en Port St. Lucie" data-en="Port St. Lucie storefront">Port St. Lucie storefront</span><img src="assets/gallery-storefront.jpg" alt="Endless Wax Studio & More storefront and parking lot" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

print('OK: galeria definida')

# ============================================================
# OPINIONES (3 resenas reales verbatim de Google via poyst.com,
# verificadas 2026-07-28, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="las clientas" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 376 reseñas en Google" data-en="4.9 out of 5 · 376 reviews on Google">4.9 out of 5 · 376 reviews on Google</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I've been coming to Iris for 9 years now and she is Always friendly! Always on time! Studio is beautiful and pristine!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Juliette Gardner</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I've been going to Llycsela for waxing services and she is seriously the best. Every appointment is professional, comfortable, and efficient."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karen Sanchez</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Had a wonderful facial with Carol! Felt like a million bucks. Came back on the weekend to talk to Iris about permanent makeup for brows, and she was so accommodating."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Barbara Irwin</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver más reseñas" data-en="Read more reviews">Read more reviews</a>
      </div>
    </div>
  </section>

  '''

print('OK: opiniones definidas')

# ============================================================
# UBICACION (Direccion, Reservas, Instagram; horarios omitidos
# por conflicto entre fuentes reales -> nota generica honesta)
# ============================================================
MAPQ = '2825+SW+Brighton+St,+Port+St.+Lucie,+FL+34953'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Port St. Lucie</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">2825 SW Brighton St, Suite C, Port St. Lucie, FL 34953</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(147,139,87,0.4)]" href="https://www.google.com/maps?q={MAPQ}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa, de lunes a sábado. Llama o escribe para confirmar la disponibilidad de hoy." data-en="By appointment, Monday through Saturday. Call or text to confirm today's availability.">By appointment, Monday through Saturday. Call or text to confirm today's availability.</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Reserva en línea eligiendo servicio, día y hora, o llama al (772) 877-2191." data-en="Book online by picking your service, day and time, or call (772) 877-2191.">Book online by picking your service, day and time, or call (772) 877-2191.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(147,139,87,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar cita" data-en="Book online">Book online</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira resultados reales de depilación, faciales y PMU, y escribe por DM cualquier duda antes de tu cita." data-en="See real waxing, facial and PMU results, and DM any questions before your appointment.">See real waxing, facial and PMU results, and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(147,139,87,0.4)]" href="{IG}" target="_blank" rel="noopener">@endlesswaxstudio</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Endless Wax Studio & More, 2825 SW Brighton St, Port St. Lucie FL"
          src="https://www.google.com/maps?q={MAPQ}&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

  '''

# ============================================================
# CTA FINAL
# ============================================================
NEW_CTA = f'''<!-- CTA FINAL -->
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #27241a 0%, #1d1a11 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Con firmeza, siempre con delicadeza." data-en="Fearlessly gentle, every time.">Fearlessly gentle, every time.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu depilación brasileña, tu facial, tu set de pestañas o esa sesión de maquillaje permanente que has estado planeando." data-en="Book online in seconds: your Brazilian wax, your facial, your lash set, or that permanent makeup session you have been planning.">Book online in seconds: your Brazilian wax, your facial, your lash set, or that permanent makeup session you have been planning.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar cita" data-en="Book online">Book online</a>
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
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#1a1811]">
    <span class="foot-mark" aria-hidden="true">Endless Wax</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/logo.jpg" alt="Endless Wax Studio & More" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,227,198,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Endless Wax Studio &amp; More</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de depilación, faciales y PMU en Port St. Lucie, FL. Atención con cita previa." data-en="Waxing, facial and PMU studio in Port St. Lucie, FL. By appointment only.">Waxing, facial and PMU studio in Port St. Lucie, FL. By appointment only.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>2825 SW Brighton St, Suite C, Port St. Lucie, FL 34953</p>
        <p><a href="tel:+17728772191" class="hover:text-[#e8e3c6]">(772) 877-2191</a></p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#e8e3c6]" data-es="Reservas online" data-en="Online booking">Online booking</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#e8e3c6]">Instagram · @endlesswaxstudio</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Endless Wax Studio &amp; More.</p>
        {badge_html}
      </div>
    </div>
  </footer>

  '''

# ============================================================
# BOTON FLOTANTE (mismo markup, solo booking url + aria-label EN)
# ============================================================
NEW_BOOKFLOAT = f'''<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f9f8f3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>

  '''

print('OK: footer + book-float definidos')

# ============================================================
# TAIL: cursorRing + back-top (aria-label ya en EN en el esqueleto)
# ============================================================
# ============================================================
# 6. SEGMENTACION POR ANCLAS DE COMENTARIO (AHORA, sobre el h ya
#    mutado: paleta + globales + head/JSON-LD + SERVICIOS in-place)
# ============================================================
def idx(marker, start=0):
    i = h.find(marker, start)
    assert i != -1, 'MARCADOR NO ENCONTRADO: ' + marker
    return i


i_preloader = idx('<!-- PRELOADER DE MARCA -->')
i_scroll = idx('<!-- BARRA DE PROGRESO DE SCROLL -->')
i_nav = idx('<!-- NAV -->')
i_servicios = idx('<!-- SERVICIOS -->')
i_galeria = idx('<!-- GALERIA -->')
i_cursorring = idx('<div id="cursorRing"')

seg_head = h[:i_preloader]
seg_scroll = h[i_scroll:i_nav]
seg_servicios = h[i_servicios:i_galeria]
seg_tail = h[i_cursorring:]

print('OK: segmentacion por anclas de comentario (post-servicios)')

new_seg_tail = seg_tail.replace('aria-label="Volver arriba"', 'aria-label="Back to top"')
assert new_seg_tail != seg_tail, 'no se pudo traducir aria-label de back-top'
seg_tail = new_seg_tail

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
    + seg_servicios
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
for word in ['Brazilian Waxing', 'Facials', 'Lash Extensions', 'Brow Shaping', 'Permanent Makeup', 'Port St. Lucie, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

# sanity: fotos prohibidas (leftovers del esqueleto o raw sin curar) nunca deben aparecer
for banned in ['bk-1.jpg', 'bk-2.jpg', 'bk-3.jpg', 'bk-6.jpg', 'bk-10.jpg', 'bk-12.jpg',
               'gallery-7.jpg', 'gallery-2.jpg', 'about-2.jpg', 'hero-1.jpg', 'assets/raw/']:
    assert banned not in h_final, f'foto/ruta prohibida usada: {banned}'

# sanity: leftovers del esqueleto/negocio anterior ausentes
for leftover in ['Lash Bloom', 'West Palm Beach', '519855', 'Cresthaven', '_lashbloom',
                 'Yesi', 'wispy', 'Wispy']:
    assert leftover not in h_final, f'LEFTOVER presente: {leftover}'

os.makedirs('output/endless-wax-studio-port-st-lucie', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
