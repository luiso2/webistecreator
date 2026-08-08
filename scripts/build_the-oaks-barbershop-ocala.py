#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/the-oaks-barbershop-ocala/index.html
The Oaks Barbershop, Marion Oaks / Ocala FL (289 Marion Oaks Ln, 34473). Boutique barbershop run
by barber Jonathan "Bravo" Fuentes (barber since 2008). Palette sampled directly from the
business's own real logo (theoaksbarbershop.com): navy #2C3F60 / gold #BAA65D / cream #EDE9E0.
4.7 / 68 (Birdeye/Google aggregate). Booksy booking id 98370 (booked under the barber's own
Booksy profile 'Bravo.theoaksbarbershop', same address). has_own_site: True but the real site
(theoaksbarbershop.com, Square Online) is a bare logo + Book button with no content -- redesign
angle for outreach, but the demo build itself is unchanged in structure.
"""
import re

SRC = 'templates/dark-v2/index.html'
DST = 'output/the-oaks-barbershop-ocala/index.html'

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
# 1. PROTEGER EL BADGE MERKTOP (dorado fijo, no cambia nunca)
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
# 2. PALETA: gold-on-brown (pureartistry) -> navy/gold real de The Oaks
#    (muestreado del logo real: bg navy #2C3F60, gold #BAA65D, cream #EDE9E0)
# ============================================================
PALETTE = [
    ('#0c0905', '#0b0e14'),
    ('#0f0b07', '#12161d'),
    ('#100c05', '#0d1017'),
    ('#171207', '#1a212c'),
    ('#191307', '#1b2330'),
    ('#241c0e', '#171f2b'),
    ('#1c1408', '#1c2636'),
    ('#6b5222', '#5c4c28'),
    ('#8a744a', '#7a6d48'),
    ('#96742c', '#8f7a3a'),
    ('#9a7431', '#93803f'),
    ('#b8934a', '#baa65d'),
    ('#bfa060', '#b8a465'),
    ('#c9a04a', '#c2ab6c'),
    ('#c9ab6b', '#c7b87e'),
    ('#d4a84b', '#d9b976'),
    ('#e5c374', '#e0cf95'),
    ('#e8c476', '#e3cf94'),
    ('#e8cf96', '#e3d6ae'),
    ('#e9c3ab', '#ded0a0'),
    ('#ecd9a8', '#e8dcb4'),
    ('#f0dc9e', '#eddcac'),
    ('#f0dcae', '#ecdfc0'),
    ('#f5efe3', '#ede9e0'),
    ('#f8eed3', '#f0e9d2'),
    ('#faf1dc', '#f3ecd8'),
    ('#fbf6ea', '#f6f1e4'),
    # ('#f4eee2', ...) se omite: unica aparicion es "Powered by Merktop", protegido via badge_html.
    # (uppercase 'D4A84B') se omite: unica aparicion es .merktop-dot, protegido via badge_css.
]
for old, new in PALETTE:
    rep_all(old, new)

RGBA_FAMILIES = [
    ((212, 168, 75), (217, 185, 118)),
    ((232, 207, 150), (227, 214, 174)),
    ((232, 210, 160), (224, 213, 178)),
    ((245, 239, 227), (237, 233, 224)),
    ((110, 85, 35), (95, 78, 40)),
    ((122, 90, 30), (70, 85, 115)),
    ((180, 140, 60), (186, 166, 93)),
    ((185, 138, 128), (150, 140, 175)),
    ((54, 42, 38), (10, 14, 20)),
    ((15, 11, 7), (10, 12, 17)),
    ((80, 58, 18), (64, 50, 24)),
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

assert '@@BADGE_CSS@@' in h
h = h.replace('@@BADGE_CSS@@', badge_css, 1)
assert '@@BADGE_HTML@@' in h
h = h.replace('@@BADGE_HTML@@', badge_html, 1)

print('OK: badge protegido + paleta navy/gold aplicada')

# ============================================================
# 3. GLOBALES: Booksy, Instagram
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
BK = 'https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala'
rep_all(OLD_BOOKSY, BK)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
IG = 'https://www.instagram.com/bravo.hairhustler787/'
rep_all(OLD_IG_URL, IG)

rep_all('@pure.artistrysk', '@bravo.hairhustler787')

print('OK: globales Booksy/Instagram')

# ============================================================
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>The Oaks Barbershop · Barbershop in Ocala, FL | Fades, Beard Trims &amp; Hot Towel Shaves</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="The Oaks Barbershop, a boutique barbershop in Marion Oaks, Ocala FL. Skin fades, beard trims, hot towel shaves and kids cuts with barber Jonathan Bravo Fuentes. 4.7 stars across 68 reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="The Oaks Barbershop · Barbershop in Ocala, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Skin fades, beard trims and hot towel shaves in Marion Oaks. 4.7 stars, 68 reviews. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/shop-batman-fade.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo-full.jpg" />',
)

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Barbershop",
    "name": "The Oaks Barbershop",
    "description": "Boutique barbershop in Marion Oaks, Ocala, FL. Skin fades, beard trims, hot towel shaves and kids cuts.",
    "address": { "@type": "PostalAddress", "streetAddress": "289 Marion Oaks Ln", "addressLocality": "Ocala", "addressRegion": "FL", "postalCode": "34473", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.98029, "longitude": -82.16747 },
    "telephone": "+13526934118",
    "sameAs": ["https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala", "https://www.instagram.com/bravo.hairhustler787/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "68", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "09:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday"], "opens": "09:00", "closes": "21:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barbershop services", "itemListElement": [
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Haircut" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Haircut & Beard" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Haircut Hot Shave" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Kids Cut (12 & under)" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: head + JSON-LD')

# ============================================================
# 5. IDIOMA: dark-v2 ya es EN default (negocio en ingles) -> sin cambios
# ============================================================
assert "applyLang(lang === 'es' ? 'es' : 'en')" in h
assert '<html lang="en"' in h

# ============================================================
# 6. PRELOADER
# ============================================================
rep(
    '''<span class="pre-mono">PA</span>
    <span class="pre-word">Pure Artistry</span>''',
    '''<span class="pre-mono">OB</span>
    <span class="pre-word">The Oaks Barbershop</span>''',
)

# ============================================================
# 7. NAV (logo = monograma CSS "OB", el logo real es una banda ancha
#    que se distorsiona en un circulo pequeno; se usa como favicon/about)
# ============================================================
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(217,185,118,0.35)]" />',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(217,185,118,0.35)]" style="background:rgba(217,185,118,0.1); color:var(--accent-deep);">OB</span>',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">The Oaks <span class="text-[color:var(--accent-deep)]">Barbershop</span></span>',
)
NAV_ITEMS = [
    ('experiencia', 'La Experiencia', 'The Experience', 'Nosotros', 'About'),
    ('metodo', 'El Método', 'The Method', 'El Proceso', 'The Process'),
    ('servicios', 'Servicios', 'Services', 'Servicios', 'Services'),
    ('galeria', 'Galería', 'Gallery', 'Galería', 'Gallery'),
    ('opiniones', 'Opiniones', 'Reviews', 'Opiniones', 'Reviews'),
    ('ubicacion', 'Ubicación', 'Location', 'Ubicación', 'Location'),
]
for anchor, old_es, old_en, new_es, new_en in NAV_ITEMS:
    # el texto visible baked en este esqueleto = valor data-es (verificado con grep)
    old = f'href="#{anchor}" data-es="{old_es}" data-en="{old_en}">{old_es}</a>'
    new = f'href="#{anchor}" data-es="{new_es}" data-en="{new_en}">{new_en}</a>'
    rep_all(old, new, expect=2)  # nav desktop + menu movil

rep(
    'aria-label="Cambiar idioma">EN</button>',
    'aria-label="Change language">EN</button>',
)
rep_all(
    '<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>',
)
rep(
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>',
)
rep('aria-label="Abrir menú">', 'aria-label="Open menu">')

print('OK: preloader + nav')

# ============================================================
# 8. HERO
# ============================================================
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Marion Oaks · Ocala, FL · Barbería" data-en="Marion Oaks · Ocala, FL · Barbershop">Marion Oaks · Ocala, FL · Barbershop</p>',
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cada corte, afilado a propósito." data-en="Every cut, sharp on purpose.">Every cut, sharp on purpose.</p>',
)
rep(
    '''        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>
        </h1>''',
    '''        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, líneas limpias y" data-en="Skin fades, clean lineups">Skin fades, clean lineups</span><br /><span data-es="afeitados en toalla caliente," data-en="and hot towel shaves,">and hot towel shaves,</span> <span class="text-shine" data-es="hechos bien" data-en="done right">done right</span>
        </h1>''',
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Barbería boutique en Marion Oaks, Ocala. Fades, arreglo de barba y afeitados en toalla caliente de Jonathan &quot;Bravo&quot; Fuentes, barbero desde 2008 con 4.7 estrellas en 68 reseñas y clientas que han volado desde otro estado solo por su silla." data-en="Boutique barbershop in Marion Oaks, Ocala. Skin fades, beard trims and hot towel shaves from Jonathan &quot;Bravo&quot; Fuentes, a barber since 2008 with a 4.7 rating across 68 reviews and clients who have flown in just for his chair.">Boutique barbershop in Marion Oaks, Ocala. Skin fades, beard trims and hot towel shaves from Jonathan &quot;Bravo&quot; Fuentes, a barber since 2008 with a 4.7 rating across 68 reviews and clients who have flown in just for his chair.</p>',
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="4.7 · 68 reseñas" data-en="4.7 · 68 reviews">4.7 · 68 reviews</span>',
)
rep(
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>\n            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>\n          </a>\n          <a href="https://www.instagram.com/bravo.hairhustler787/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">',
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>\n            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>\n          </a>\n          <a href="https://www.instagram.com/bravo.hairhustler787/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">',
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/shop-batman-fade.jpg" alt="Kid\'s fade with a freehand Batman design, shot inside The Oaks Barbershop" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Silk Press</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Más pedido" data-en="Most requested">Most requested</p>\n            <p class="font-display text-lg">The Haircut &amp; Beard</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$50 · 40min" data-en="$50 · 40min">$50 · 40min</p>',
)

print('OK: hero')

# ============================================================
# 9. STRIP DE CONFIANZA
# ============================================================
rep(
    '''      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>''',
    '''      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="68">68</span> <span data-es="reseñas" data-en="reviews">reviews</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Beards</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Fade · Barba · Toalla caliente" data-en="Fade · Beard · Hot towel">Fade · Beard · Hot towel</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">$40</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="The Haircut · 40min" data-en="The Haircut · 40min">The Haircut · 40min</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Marion Oaks</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">289 Marion Oaks Ln</p></div>''',
)

print('OK: strip de confianza')

# ============================================================
# 10. MARQUEE (2 apariciones, 4 palabras cada una x2 filas = 8 por bloque)
# ============================================================
MARQUEE_OLD = '''        <span class="marquee-word">Silk Press</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Loc Retwist</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Knotless Braids</span><span class="marquee-star">✦</span>
        <span class="marquee-word">K-Tip Extensions</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Keratin</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Orlando, FL</span><span class="marquee-star">✦</span>'''
MARQUEE_NEW = '''        <span class="marquee-word">Skin Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Trims</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hot Towel Shaves</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Clean Lineups</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Kids Cuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Ocala, FL</span><span class="marquee-star">✦</span>'''
rep_all(MARQUEE_OLD, MARQUEE_NEW, expect=4)

print('OK: marquee x4')

# ============================================================
# 11. LA EXPERIENCIA (About)
# ============================================================
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/storefront-entrance.jpg" alt="The Oaks Barbershop storefront entrance in Marion Oaks, Ocala" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/shop-interior-cut.jpg" alt="Barber cutting a client\'s hair inside The Oaks Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Nosotros" data-en="About us">About us</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="clientas que vuelan por él" data-en="clients who fly in for him">clients who fly in for him</span></h2>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="The Oaks Barbershop es una barbería boutique en Marion Oaks, a cargo del barbero Jonathan &quot;Bravo&quot; Fuentes, cortando cabello desde 2008. Fades, arreglo de barba, afeitados en toalla caliente y cortes de niño, con la misma atención cada vez." data-en="The Oaks Barbershop is a boutique barbershop in Marion Oaks, run by barber Jonathan &quot;Bravo&quot; Fuentes, cutting hair since 2008. Skin fades, beard trims, hot towel shaves and kids cuts, all with the same attention every time.">The Oaks Barbershop is a boutique barbershop in Marion Oaks, run by barber Jonathan &quot;Bravo&quot; Fuentes, cutting hair since 2008. Skin fades, beard trims, hot towel shaves and kids cuts, all with the same attention every time.</p>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Las reseñas lo dicen mejor que nadie: 4.7 estrellas en 68 reseñas, y al menos una clienta que dice que volaría desde Rhode Island solo para volver a sentarse en su silla." data-en="The reviews say it best: a 4.7 rating across 68 reviews, and at least one client who says she would fly in from Rhode Island just to sit in his chair again.">The reviews say it best: a 4.7 rating across 68 reviews, and at least one client who says she would fly in from Rhode Island just to sit in his chair again.</p>',
)
rep(
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Calificación" data-en="Rating">Rating</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="68">68</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="18">18</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Años cortando" data-en="Years cutting hair">Years cutting hair</p></div>''',
)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(217,185,118,0.3)]" loading="lazy" />',
    '<img src="assets/raw/barber-portrait.jpg" alt="Jonathan &quot;Bravo&quot; Fuentes, barber at The Oaks Barbershop" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(217,185,118,0.3)]" loading="lazy" />',
)
rep(
    '<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Jonathan &quot;Bravo&quot; Fuentes · <span class="text-[color:var(--ink-40)]" data-es="Barbero" data-en="Barber">Barber</span></span>',
)

print('OK: la experiencia / about')

# ============================================================
# 12. EL METODO (The Process)
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu corte, paso a paso" data-en="Your cut, step by step">Your cut, step by step</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="en The Oaks" data-en="at The Oaks">at The Oaks</span></h2>',
)
rep(
    '''        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>
        </div>''',
    '''        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu corte, arreglo de barba o afeitado en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your haircut, beard trim or shave on Booksy with a clear price and time, and confirm instantly.">Pick your haircut, beard trim or shave on Booksy with a clear price and time, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Cuéntale el estilo" data-en="Tell him the look">Tell him the look</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Fade a piel, taper, corte clásico o afeitado en toalla caliente: hablan los detalles antes de que empiece la máquina." data-en="Skin fade, taper, classic cut or a hot towel shave: you talk through the details before the clippers start.">Skin fade, taper, classic cut or a hot towel shave: you talk through the details before the clippers start.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El corte" data-en="The cut">The cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="40 minutos dedicados a tu fade o afeitado, con el mismo cuidado sea tu primera visita o la número cincuenta." data-en="40 minutes dedicated to your fade or shave, with the same care whether it is your first visit or your fiftieth.">40 minutes dedicated to your fade or shave, with the same care whether it is your first visit or your fiftieth.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Acabado afilado" data-en="Sharp finish">Sharp finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con líneas limpias, la barba perfilada y la confianza que le ganó a Jonathan su 4.7 en reseñas." data-en="You leave with a clean lineup, a shaped beard and the confidence that earned Jonathan his 4.7 rating.">You leave with a clean lineup, a shaped beard and the confidence that earned Jonathan his 4.7 rating.</p>
        </div>''',
)

print('OK: el metodo')

# ============================================================
# 13. SERVICIOS (regex, grid completo)
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="corte" data-en="cut">cut</span></h2>',
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por The Oaks Barbershop en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by The Oaks Barbershop on Booksy. Booking confirms instantly.">Prices and durations as published by The Oaks Barbershop on Booksy. Booking confirms instantly.</p>',
)

m = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert m, 'no se encontro el grid de servicios'
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(217,185,118,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3">The Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Fade a piel, taper o corte clásico, con una línea limpia y afilada." data-en="Skin fade, taper or classic cut, with a clean, sharp lineup.">Skin fade, taper or classic cut, with a clean, sharp lineup.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Combo" data-en="Combo">Combo</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y Barba" data-en="The Haircut &amp; Beard">The Haircut &amp; Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tu corte más el arreglo completo de barba y perfilado, en la misma visita." data-en="Your haircut plus a full beard trim and shape-up, in the same visit.">Your haircut plus a full beard trim and shape-up, in the same visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Servicio completo" data-en="Full service">Full service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y Afeitado" data-en="The Haircut Hot Shave">The Haircut Hot Shave</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tu corte terminado con un afeitado tradicional en toalla caliente y navaja." data-en="Your haircut finished with a traditional hot towel straight razor shave.">Your haircut finished with a traditional hot towel straight razor shave.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para los más chicos" data-en="For the little ones">For the little ones</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte de niño (12 y menos)" data-en="Kids Cut (12 &amp; under)">Kids Cut (12 &amp; under)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Paciencia y buena mano con los más pequeños, del primer corte al fade que ya piden solos." data-en="Patient, steady haircuts for kids, from first cuts to the fades they ask for themselves.">Patient, steady haircuts for kids, from first cuts to the fades they ask for themselves.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES + h[m.end():]

m2 = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert m2, 'no se encontro la nota de servicios'
NEW_NOTE = m2.group(1) + '<span data-es="También hacemos afeitados de barba y diseños de líneas. Menú completo y disponibilidad en Booksy." data-en="We also do beard shaves and line-up designs. Full menu and availability on Booksy.">We also do beard shaves and line-up designs. Full menu and availability on Booksy.</span>' + m2.group(2)
h = h[:m2.start()] + NEW_NOTE + h[m2.end():]

print('OK: servicios (regex)')

# ============================================================
# 14. GALERIA (regex, grid completo)
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Cortes" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="cuts">cuts</span></h2>',
)

m = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert m, 'no se encontro el grid de galeria'
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Dentro de la barbería" data-en="Inside the shop">Inside the shop</span><img src="assets/raw/shop-interior-cut.jpg" alt="Barber cutting a client's hair inside The Oaks Barbershop, ring light and shop interior visible" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Toda la atención" data-en="Full attention">Full attention</span><img src="assets/raw/shop-interior-detail.jpg" alt="Barber giving a client full attention inside The Oaks Barbershop" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Fade limpio" data-en="Clean skin fade">Clean skin fade</span><img src="assets/raw/clean-fade-lineup.jpg" alt="Clean skin fade with a sharp lineup, finished cut at The Oaks Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Fade fresco" data-en="Fresh fade">Fresh fade</span><img src="assets/raw/kids-mullet-fade.jpg" alt="Kid's mullet fade combo, finished cut, outdoor natural light" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Fade con rizos" data-en="Curly fade">Curly fade</span><img src="assets/raw/curly-fade-result.jpg" alt="Curly-top fade, finished cut at The Oaks Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Más allá del fade" data-en="Beyond fades">Beyond fades</span><img src="assets/raw/twists-updo-result.jpg" alt="Twists styled into an updo, finished result at The Oaks Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:m.start()] + NEW_GALLERY + h[m.end():]

print('OK: galeria (regex)')

# ============================================================
# 15. OPINIONES (reviews reales, verbatim)
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What his">What his</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span></h2>',
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★☆</span> &nbsp;<span data-es="4.7 de 5 · 68 reseñas" data-en="4.7 out of 5 · 68 reviews">4.7 out of 5 · 68 reviews</span></p>',
)
rep(
    '''        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Jonathan Bravo at Oaks Barbershop is hands down the best barber I've ever been to. From the moment I sat in his chair, he was incredibly gentle, professional, and had such a calm, balanced energy... Honestly, he's so good that I'd take a plane from Rhode Island just to have him cut my hair again."</blockquote>
          <figcaption class="text-sm"><span class="font-medium" data-es="Cliente verificada" data-en="Verified client">Verified client</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent service. Very professional and thorough with his haircuts! No need to look for a new barber, you found the guy."</blockquote>
          <figcaption class="text-sm"><span class="font-medium" data-es="Cliente verificado" data-en="Verified client">Verified client</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Awesome experience!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Andres M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
)
rep(
    '<a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver el perfil en Booksy" data-en="See the Booksy profile">See the Booksy profile</a>',
)

print('OK: opiniones')

# ============================================================
# 16. UBICACION
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Marion Oaks</span></h2>',
)
rep(
    '''            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,185,118,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">289 Marion Oaks Ln, Ocala, FL 34473</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,185,118,0.4)]" href="https://www.google.com/maps?q=289+Marion+Oaks+Ln,+Ocala,+FL+34473" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>''',
)
rep(
    '''            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,185,118,0.4)]" href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Hasta las 9pm en viernes y sábado. Reserva en Booksy: eliges servicio, día y hora, confirmación inmediata." data-en="Open until 9pm on Fridays and Saturdays. Book on Booksy: pick the service, day and time, confirmation is instant.">Open until 9pm on Fridays and Saturdays. Book on Booksy: pick the service, day and time, confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,185,118,0.4)]" href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>''',
)
rep(
    '''            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,185,118,0.4)]" href="https://www.instagram.com/bravo.hairhustler787/" target="_blank" rel="noopener">@bravo.hairhustler787</a>
            </div>''',
    '''            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a jueves 9am a 7pm. Viernes y sábado 9am a 9pm. Domingo cerrado." data-en="Monday to Thursday 9am to 7pm. Friday and Saturday 9am to 9pm. Sunday closed.">Monday to Thursday 9am to 7pm. Friday and Saturday 9am to 9pm. Sunday closed.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,185,118,0.4)]" href="https://www.instagram.com/bravo.hairhustler787/" target="_blank" rel="noopener">@bravo.hairhustler787</a>
            </div>''',
)
rep(
    '<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Map: The Oaks Barbershop, 289 Marion Oaks Ln, Ocala FL"\n          src="https://www.google.com/maps?q=289+Marion+Oaks+Ln,+Ocala,+FL+34473&output=embed"',
)

print('OK: ubicacion')

# ============================================================
# 17. CTA FINAL
# ============================================================
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cada corte, afilado a propósito." data-en="Every cut, sharp on purpose.">Every cut, sharp on purpose.</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo fade" data-en="Your next fade">Your next fade</span> <span class="text-shine" data-es="a un toque de distancia" data-en="is one tap away">is one tap away</span></h2>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu fade, tu arreglo de barba o ese afeitado en toalla caliente que llevas posponiendo." data-en="Book online in seconds: your fade, your beard trim, or that hot towel shave you have been putting off.">Book online in seconds: your fade, your beard trim, or that hot towel shave you have been putting off.</p>',
)
rep(
    '<a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>',
)
rep(
    '<a href="https://www.instagram.com/bravo.hairhustler787/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="https://www.instagram.com/bravo.hairhustler787/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>',
)

print('OK: cta final')

# ============================================================
# 18. FOOTER + book-float
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">The Oaks</span>')
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(227,214,174,0.35)]" loading="lazy" />',
    '<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-xs ring-1 ring-[rgba(227,214,174,0.35)]" style="background:rgba(227,214,174,0.1); color:#ded0a0;">OB</span>',
)
rep(
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">The Oaks Barbershop</span>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería boutique en Marion Oaks, Ocala FL. Fades, barba y afeitados en toalla caliente." data-en="Boutique barbershop in Marion Oaks, Ocala FL. Skin fades, beards and hot towel shaves.">Boutique barbershop in Marion Oaks, Ocala FL. Skin fades, beards and hot towel shaves.</p>',
)
rep(
    '<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n        <p><a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="hover:text-[#ded0a0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p>289 Marion Oaks Ln, Ocala, FL 34473</p>\n        <p><a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="hover:text-[#ded0a0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>',
)
assert '<p><a href="https://www.instagram.com/bravo.hairhustler787/" target="_blank" rel="noopener" class="hover:text-[#ded0a0]">Instagram · @bravo.hairhustler787</a></p>' in h, 'footer IG link ancla rota'
rep(
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 The Oaks Barbershop.</p>',
)
rep(
    '<a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://booksy.com/en-us/98370_bravo-theoaksbarbershop_barber-shop_15870_ocala" target="_blank" rel="noopener" class="book-float" aria-label="Book online">',
)
rep('<button id="backTop" class="back-top glass" type="button" aria-label="Volver arriba">',
    '<button id="backTop" class="back-top glass" type="button" aria-label="Back to top">')

print('OK: footer + book-float')

open(DST, 'w', encoding='utf-8').write(h)
print('OK: paso 6 (ubicacion + cta + footer) escrito en', DST)
