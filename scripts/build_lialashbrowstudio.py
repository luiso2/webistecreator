#!/usr/bin/env python3
"""Derivacion anclada: templates/light-v2/index.html -> output/lialashbrowstudio/index.html
Metodo: SKELETONS-V2.md. Palette terracota. Idioma ES default. Booksy CTA (sin telefono).
"""
import re

SRC = 'templates/light-v2/index.html'
DST = 'output/lialashbrowstudio/index.html'

lines = open(SRC, encoding='utf-8').read().split('\n')

def sl(a, b):
    """1-indexed inclusive line slice -> exact original text block."""
    return '\n'.join(lines[a - 1:b])

h = open(SRC, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    assert h.count(a) >= n, 'NO MATCH (count=%d need %d): %s' % (h.count(a), n, a[:120])
    h = h.replace(a, b, n)

def repall(a, b):
    global h
    assert a in h, 'NO MATCH: ' + a[:120]
    h = h.replace(a, b)

OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1784538_lia-lash-brow-studio_brows-lashes_15889_miami'
OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/lia_lashandbrowstudio/'
OLD_IG_HANDLE = '@_lashbloom'
NEW_IG_HANDLE = '@lia_lashandbrowstudio'

# ---------------------------------------------------------------------------
# 1) GLOBALES: booksy url, instagram url, handle
# ---------------------------------------------------------------------------
assert h.count(OLD_BOOKSY) == 13, h.count(OLD_BOOKSY)
repall(OLD_BOOKSY, NEW_BOOKSY)
assert h.count(OLD_IG_URL) == 10, h.count(OLD_IG_URL)
repall(OLD_IG_URL, NEW_IG_URL)
assert h.count(OLD_IG_HANDLE) == 2, h.count(OLD_IG_HANDLE)
repall(OLD_IG_HANDLE, NEW_IG_HANDLE)

# ---------------------------------------------------------------------------
# 2) HEAD: lang, title/meta/og/icon, JSON-LD
# ---------------------------------------------------------------------------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

old_head = sl(7, 13)
new_head = '''  <title>Lía Lash &amp; Brow Studio · Lash &amp; Brow Studio en Miami Springs, FL | 5.0 en Booksy</title>
  <meta name="description" content="Lía Lash &amp; Brow Studio, Miami Springs FL: pestañas clásicas, híbridas y de volumen, lash lift, laminado de cejas y depilación con cera. 5.0 en 13 reseñas de Booksy. Reserva online." />
  <meta property="og:title" content="Lía Lash &amp; Brow Studio · Lash &amp; Brow Studio en Miami Springs, FL" />
  <meta property="og:description" content="Pestañas, cejas y depilación con cera. 5.0 en Booksy. Reserva online." />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="assets/og-image.jpg" />
  <link rel="icon" type="image/jpeg" href="assets/logo.jpg" />'''
rep(old_head, new_head)

old_jsonld = sl(14, 30)
new_jsonld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "L\\u00eda Lash & Brow Studio",
    "description": "Lash and brow studio in Miami Springs, FL: classic, hybrid and volume lash extensions, brow lamination, lash lift and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "5399 NW 36th St", "addressLocality": "Miami Springs", "addressRegion": "FL", "postalCode": "33166", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.80807, "longitude": -80.28485 },
    "sameAs": ["https://booksy.com/en-us/1784538_lia-lash-brow-studio_brows-lashes_15889_miami", "https://www.instagram.com/lia_lashandbrowstudio/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "13", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "10:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash & brow services", "itemListElement": [
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Classic full set" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Hybrid full set" } },
      { "@type": "Offer", "price": "110", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Volumen Full Set" } },
      { "@type": "Offer", "price": "120", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Combo Lash lift + Brows Lami" } }
    ] }
  }
  </script>'''
rep(old_jsonld, new_jsonld)

# ---------------------------------------------------------------------------
# 3) PRELOADER
# ---------------------------------------------------------------------------
old_pre = sl(218, 222)
new_pre = '''  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">LB</span>
    <span class="pre-word">L\\u00eda Lash &amp; Brow</span>
    <span class="pre-line"></span>
  </div>'''.replace('\\u00eda', 'ía')
rep(old_pre, new_pre)

# ---------------------------------------------------------------------------
# 4) NAV brand block (logo + name)
# ---------------------------------------------------------------------------
old_nav_brand = sl(230, 233)
new_nav_brand = '''      <a href="#top" class="flex items-center gap-3">
        <img src="assets/logo.jpg" alt="Lía Lash &amp; Brow Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(193,112,74,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Lía <span class="text-[color:var(--accent-deep)]">Lash &amp; Brow</span></span>
      </a>'''
rep(old_nav_brand, new_nav_brand)

# also update the mobile-menu CTA + nav CTA "Reservar cita" -> keep text but href already replaced globally.
# (nav-link anchors and mobile menu are generic bilingual copy: no change needed)

# ---------------------------------------------------------------------------
# 5) HERO
# ---------------------------------------------------------------------------
old_eyebrow = sl(273, 273)
new_eyebrow = ('        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" '
               'data-es="Miami Springs, FL · Lash &amp; Brow Studio" data-en="Miami Springs, FL · Lash &amp; Brow Studio">'
               'Miami Springs, FL · Lash &amp; Brow Studio</p>')
rep(old_eyebrow, new_eyebrow)

old_script = sl(274, 274)
new_script = ('        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" '
              'data-es="Miradas que enamoran, cejas que enmarcan." data-en="Eyes that enchant, brows that frame.">'
              'Miradas que enamoran, cejas que enmarcan.</p>')
rep(old_script, new_script)

old_h1 = sl(275, 277)
new_h1 = '''        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas y cejas hechas" data-en="Lashes and brows made">Pestañas y cejas hechas</span><br /><span data-es="para resaltar " data-en="to enhance ">para resaltar </span><span class="text-shine" data-es="tu mirada" data-en="your look">tu mirada</span>
        </h1>'''
rep(old_h1, new_h1)

old_sub = sl(278, 278)
new_sub = ('        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" '
           'data-es="Sets completos clásicos, híbridos y de volumen, laminado de cejas, lash lift y depilación con cera, todo en un estudio íntimo en Miami Springs. Lianys, la artista detrás de Lía Lash &amp; Brow Studio, cuida cada detalle desde el diseño hasta el resultado final." '
           'data-en="Full classic, hybrid and volume lash sets, brow lamination, lash lift and waxing, all in an intimate studio in Miami Springs. Lianys, the artist behind Lía Lash &amp; Brow Studio, cares for every detail from design to final result.">'
           'Sets completos clásicos, híbridos y de volumen, laminado de cejas, lash lift y depilación con cera, todo en un estudio íntimo en Miami Springs. Lianys, la artista detrás de Lía Lash &amp; Brow Studio, cuida cada detalle desde el diseño hasta el resultado final.</p>')
rep(old_sub, new_sub)

old_rating = sl(279, 282)
new_rating = '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 13 reseñas en Booksy" data-en="5.0 · 13 reviews on Booksy">5.0 · 13 reseñas en Booksy</span>
        </div>'''
rep(old_rating, new_rating)

old_img_price = sl(294, 305)
new_img_price = '''    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
''' # placeholder, replaced below precisely (kept for readability, not used)
rep_removed = True

print('base rewrites in progress...')
open(DST, 'w', encoding='utf-8').write(h)
