#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2/index.html -> output/copper-penny-hair-studio-lakeland/index.html
Copper Penny Hair Studio, Lakeland FL. Paleta cobre/copper profundo (#e0893f / #c27a40), sobre el
mismo fondo warm-black del esqueleto (ya calza con el ladrillo visto en las fotos reales).
Sin Booksy verificado: CTA real = llamar al (863) 940-2161 + Instagram.
"""
import re

SRC = 'templates/dark-v2/index.html'
DST = 'output/copper-penny-hair-studio-lakeland/index.html'

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
# 1. PROTEGER EL BADGE MERKTOP (dorado, no debe cambiar)
# ============================================================
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque merktop-badge/mkPulse'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ============================================================
# 2. PALETA: gold -> copper (bg se mantiene, ya es warm-black y calza con
#    el ladrillo visto en las fotos reales del salon)
# ============================================================
rep_all(
    'linear-gradient(90deg, #96742c 0%, #d4a84b 45%, #f0dc9e 100%)',
    'linear-gradient(90deg, #a05c22 0%, #e0893f 45%, #f7cb97 100%)',
)

PALETTE = [
    ('#d4a84b', '#e0893f'),
    ('#b8934a', '#c27a40'),
    ('#e8c476', '#f2ab6c'),
    ('#c9a04a', '#d4843f'),
    ('#96742c', '#a05c22'),
    ('#6b5222', '#72411b'),
    ('#f0dc9e', '#f7cb97'),
    ('#9a7431', '#a35c28'),
    ('#e5c374', '#efaa6a'),
    ('#e8cf96', '#efbd8f'),
    ('#f8eed3', '#fbe6d0'),
    ('#bfa060', '#c88b57'),
    ('#f0dcae', '#f6cda8'),
    ('#faf1dc', '#fdead9'),
    ('#ecd9a8', '#f2caa2'),
    ('#c9ab6b', '#d19663'),
    ('#8a744a', '#906544'),
    ('#e9c3ab', '#efb2a5'),
    ('#241c0e', '#26170c'),
]
for old, new in PALETTE:
    rep_all(old, new)

RGBA_FAMILIES = [
    ((212, 168, 75), (224, 137, 63)),
    ((232, 207, 150), (239, 189, 143)),
    ((232, 210, 160), (238, 194, 154)),
    ((122, 90, 30), (130, 69, 22)),
    ((180, 140, 60), (191, 113, 49)),
    ((185, 138, 128), (190, 123, 126)),
    ((110, 85, 35), (117, 68, 28)),
    ((80, 58, 18), (86, 44, 12)),
]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

# restaurar el badge dorado intacto
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

# ============================================================
# 3. GLOBALES: quitar Booksy (no verificado), Instagram real
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_TEL = 'tel:+18639402161'
n_booksy = h.count(OLD_BOOKSY)
assert n_booksy > 0
h = h.replace(OLD_BOOKSY, NEW_TEL)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/copperpennyhairstudiollc/'
rep_all(OLD_IG_URL, NEW_IG_URL)

rep_all('@pure.artistrysk', '@copperpennyhairstudiollc')

print('OK paso 1-3')

# ============================================================
# 4. HEAD: title, meta, JSON-LD, favicon, theme-color (bg no cambia)
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Copper Penny Hair Studio · Hair Salon in Lakeland, FL | Balayage, Color &amp; Cuts | 4.9 on Google</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Copper Penny Hair Studio, Lakeland FL: balayage, color melts, highlights, cuts and treatments near S Florida Ave. 4.9 with 124 Google reviews. Call to book." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Copper Penny Hair Studio · Hair Salon in Lakeland, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Balayage, color and cuts near Lake Morton. 4.9 on Google. Call to book." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-8.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-12.jpg" />',
)

OLD_LD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Pure Artistry",
    "description": "Hair studio in Orlando, FL: silk press, loc retwists and interlocks, knotless braids, K-Tip and microlink extensions, keratin treatments.",
    "address": { "@type": "PostalAddress", "streetAddress": "80 W Grant St, Suite 111, Studio 156", "addressLocality": "Orlando", "addressRegion": "FL", "postalCode": "32806", "addressCountry": "US" },
    "sameAs": ["tel:+18639402161", "https://www.instagram.com/copperpennyhairstudiollc/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "234", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Silk Press" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full-head Loc Retwist" } },
      { "@type": "Offer", "price": "400", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Small Knotless Braids" } },
      { "@type": "Offer", "price": "750", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "K-Tip Extensions" } }
    ] }
  }
  </script>'''
NEW_LD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Copper Penny Hair Studio",
    "description": "Hair salon in Lakeland, FL: balayage, color melts, highlights, precision cuts and styling near the South Lake Morton Historic District.",
    "address": { "@type": "PostalAddress", "streetAddress": "1003 S Florida Ave", "addressLocality": "Lakeland", "addressRegion": "FL", "postalCode": "33803", "addressCountry": "US" },
    "telephone": "+18639402161",
    "sameAs": ["https://www.instagram.com/copperpennyhairstudiollc/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "124", "bestRating": "5" },
    "openingHoursSpecification": { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "10:00", "closes": "19:00" }
  }
  </script>'''
rep(OLD_LD, NEW_LD)

print('OK paso 4 (head)')

# ============================================================
# 5. NAV
# ============================================================
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(224,137,63,0.35)]" />',
    '<img src="assets/raw/bk-12.jpg" alt="Copper Penny Hair Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(224,137,63,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Copper <span class="text-[color:var(--accent-deep)]">Penny</span></span>',
)
rep(
    '<a href="tel:+18639402161" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n'
    '          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n'
    '        </a>',
    '<a href="tel:+18639402161" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n'
    '          <span data-es="Llamar para reservar" data-en="Call to book">Call to book</span>\n'
    '        </a>',
)
rep(
    '<a href="tel:+18639402161" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    '<a href="tel:+18639402161" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar para reservar" data-en="Call to book">Call to book</a>',
)

print('OK paso 5 (nav)')

# ============================================================
# 6. HERO
# ============================================================
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Lakeland, FL · Hair Studio" data-en="Lakeland, FL · Hair Studio">Lakeland, FL · Hair Studio</p>',
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Donde el color se convierte en arte." data-en="Where color meets craft.">Where color meets craft.</p>',
)
rep(
    '<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">\n'
    '          <span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>\n'
    '        </h1>',
    '<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">\n'
    '          <span data-es="Balayage, color y" data-en="Balayage, color and">Balayage, color and</span><br /><span data-es="cortes pulidos a un " data-en="cuts polished to a ">cuts polished to a </span><span class="text-shine" data-es="brillo cobrizo" data-en="copper shine">copper shine</span>\n'
    '        </h1>',
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="De balayage envolvente a color melts y cortes de precisión, Copper Penny Hair Studio es un referente en S Florida Ave desde hace años, con 4.9 de calificación en 124 reseñas de Google." data-en="From dimensional balayage to color melts and precision cuts, Copper Penny Hair Studio has been a go-to on S Florida Ave for years, with a 4.9 rating across 124 Google reviews.">From dimensional balayage to color melts and precision cuts, Copper Penny Hair Studio has been a go-to on S Florida Ave for years, with a 4.9 rating across 124 Google reviews.</p>',
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="4.9 · 124 reseñas en Google" data-en="4.9 · 124 reviews on Google">4.9 · 124 reviews on Google</span>',
)
rep(
    '<a href="tel:+18639402161" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>\n'
    '            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>\n'
    '          </a>',
    '<a href="tel:+18639402161" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <span data-es="Llamar para reservar" data-en="Call to book">Call to book</span>\n'
    '            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>\n'
    '          </a>',
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-8.jpg" alt="Copper peekaboo highlights finished at Copper Penny Hair Studio, Lakeland" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>\n'
    '            <p class="font-display text-lg">Silk Press</p>\n'
    '            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Con cita previa" data-en="By appointment">By appointment</p>\n'
    '            <p class="font-display text-lg">Balayage</p>\n'
    '            <p class="text-sm text-[color:var(--ink-60)]" data-es="Llama para precios" data-en="Call for pricing">Call for pricing</p>',
)

print('OK paso 6 (hero)')

# ============================================================
# 7. STRIP DE CONFIANZA
# ============================================================
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="124">124</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Balayage <span class="text-shine">&amp;</span> Color</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Reflejos · Color Melt · Gloss" data-en="Highlights · Color Melt · Gloss">Highlights · Color Melt · Gloss</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Cuts <span class="text-shine">&amp;</span> Styling</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cortes de precisión · Blowouts" data-en="Precision cuts · Blowouts">Precision cuts · Blowouts</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Lakeland</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">S Florida Ave</p></div>',
)

# ============================================================
# 8. MARQUEE (x2 marquees, cada palabra aparece 4 veces en total)
# ============================================================
MARQUEE_WORDS = [
    ('Silk Press', 'Balayage'),
    ('Loc Retwist', 'Color Melt'),
    ('Knotless Braids', 'Highlights'),
    ('K-Tip Extensions', 'Precision Cuts'),
    ('Keratin', 'Gloss Treatment'),
    ('Orlando, FL', 'Lakeland, FL'),
]
for old_w, new_w in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old_w}</span>', f'<span class="marquee-word">{new_w}</span>', expect=4)

print('OK paso 7-8 (strip + marquee)')

# ============================================================
# 9. LA EXPERIENCIA
# ============================================================
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Dimensional blonde balayage finished at Copper Penny Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Caramel money-piece highlights finished at Copper Penny Hair Studio" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un equipo," data-en="A team,">A team,</span><br /><span class="text-shine" data-es="de confianza en Lakeland" data-en="Lakeland trusts">Lakeland trusts</span></h2>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Copper Penny Hair Studio colorea y corta cabello desde un estudio de ladrillo a la vista sobre S Florida Ave, en el área de South Lake Morton en Lakeland. Estilistas como Lisa, Kapi, Tina y Ashley trabajan de forma personalizada con cada clienta, desde la consulta de color hasta el blowout final." data-en="Copper Penny Hair Studio colors and cuts hair from a cozy exposed-brick studio on S Florida Ave, in the South Lake Morton area of Lakeland. Stylists like Lisa, Kapi, Tina and Ashley work one-on-one with every client, from the first color consult to the finished blowout.">Copper Penny Hair Studio colors and cuts hair from a cozy exposed-brick studio on S Florida Ave, in the South Lake Morton area of Lakeland. Stylists like Lisa, Kapi, Tina and Ashley work one-on-one with every client, from the first color consult to the finished blowout.</p>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman: reseñas que hablan de un salón donde te sientes como en familia y de colores que se ven exquisitos. 4.9 de calificación en 124 reseñas de Google." data-en="Their clients confirm it: reviews that describe a salon where you feel like family and color work they call exquisite. A 4.9 rating across 124 Google reviews.">Their clients confirm it: reviews that describe a salon where you feel like family and color work they call exquisite. A 4.9 rating across 124 Google reviews.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>\n'
    '          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n'
    '          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>\n'
    '          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="124">124</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n'
    '          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">S. FL Ave</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Lakeland, FL" data-en="Lakeland, FL">Lakeland, FL</p></div>',
)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(224,137,63,0.3)]" loading="lazy" />\n'
    '            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/raw/bk-12.jpg" alt="Copper Penny Hair Studio, color team" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(224,137,63,0.3)]" loading="lazy" />\n'
    '            <span class="text-sm font-light">Copper Penny · <span class="text-[color:var(--ink-40)]" data-es="Especialistas en color" data-en="Color specialists">Color specialists</span></span>',
)

print('OK paso 9 (experiencia)')

# ============================================================
# 10. EL METODO
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Llama para reservar" data-en="Call to book">Call to book</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama al (863) 940-2161 para asegurar tu cita con la estilista que prefieras. Martes a sábado, de 10am a 7pm." data-en="Call (863) 940-2161 to lock in your spot with the stylist you want. Tuesday through Saturday, 10am to 7pm.">Call (863) 940-2161 to lock in your spot with the stylist you want. Tuesday through Saturday, 10am to 7pm.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de color" data-en="Color consult">Color consult</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cada servicio de color comienza con una consulta rápida: el historial de tu cabello, el tono que buscas y la técnica más segura para llegar ahí." data-en="Every color service starts with a quick consult: your hair history, the tone you want and the technique that gets you there safely.">Every color service starts with a quick consult: your hair history, the tone you want and the technique that gets you there safely.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un balayage completo a un corte rápido, cada cita recibe el tiempo que necesita, sin citas dobles ni apuros con tu color." data-en="From a full balayage to a quick trim, every appointment gets the time it needs, no double booking, no rushing through your color.">From a full balayage to a quick trim, every appointment gets the time it needs, no double booking, no rushing through your color.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n'
    '          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un blowout pulido y los productos y consejos para mantener tu color fresco hasta la próxima visita." data-en="You leave with a polished blowout and the products and tips to keep your color looking fresh until your next visit.">You leave with a polished blowout and the products and tips to keep your color looking fresh until your next visit.</p>',
)

print('OK paso 10 (metodo)')

# ============================================================
# 11. SERVICIOS: heading + nota + grid completo (regex, sin precios
#     fabricados: no hay lista de precios publicada -> "Call for pricing")
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n'
    '        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine">service</span></h2>\n'
    '        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Copper Penny no publica una lista de precios fija: cada color depende del largo y la técnica. Llama y te cotizan al instante." data-en="Copper Penny does not publish a fixed price list: every color depends on length and technique. Call and get a quote right away.">Copper Penny does not publish a fixed price list: every color depends on length and technique. Call and get a quote right away.</p>',
)

grid_pat = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    flags=re.S,
)
assert grid_pat.search(h), 'no se encontro el grid de servicios'
NEW_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(224,137,63,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Balayage y Reflejos" data-en="Balayage &amp; Highlights">Balayage &amp; Highlights</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Balayage pintado a mano, foilyage y reflejos dimensionales, terminados con gloss para un brillo que dura. El servicio que más se ve en su Instagram." data-en="Hand-painted balayage, foilyage and dimensional highlights, finished with a gloss for shine that lasts. The service you will see all over their Instagram.">Hand-painted balayage, foilyage and dimensional highlights, finished with a gloss for shine that lasts. The service you will see all over their Instagram.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Llamar" data-en="Call">Call</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="para precios" data-en="for pricing">for pricing</p></div>
            <a href="tel:+18639402161" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cortes" data-en="Cuts">Cuts</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cortes y Peinados" data-en="Cuts &amp; Styling">Cuts &amp; Styling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cortes de precisión, blowouts y peinados para todo tipo de cabello, desde un despunte rápido hasta una transformación completa." data-en="Precision cuts, blowouts and styling for every hair type, from a quick trim to a full transformation.">Precision cuts, blowouts and styling for every hair type, from a quick trim to a full transformation.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Llamar" data-en="Call">Call</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="para precios" data-en="for pricing">for pricing</p></div>
            <a href="tel:+18639402161" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Color" data-en="Color">Color</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Color y Correcciones" data-en="Color &amp; Corrections">Color &amp; Corrections</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Color completo, retoque de raíz, color melts y corrección de color, con estilistas a quienes las clientas confían la misma cita año tras año." data-en="Full color, root touch-ups, color melts and color correction from stylists clients trust with the same appointment year after year.">Full color, root touch-ups, color melts and color correction from stylists clients trust with the same appointment year after year.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Llamar" data-en="Call">Call</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="para precios" data-en="for pricing">for pricing</p></div>
            <a href="tel:+18639402161" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamientos" data-en="Treatments">Treatments</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tratamientos y Textura" data-en="Treatments &amp; Texture">Treatments &amp; Texture</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tratamientos de keratina, gloss, hidratación profunda y perms para mantener saludable el cabello con color entre visitas." data-en="Keratin treatments, glosses, deep conditioning and perms to keep color-treated hair healthy between visits.">Keratin treatments, glosses, deep conditioning and perms to keep color-treated hair healthy between visits.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Llamar" data-en="Call">Call</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="para precios" data-en="for pricing">for pricing</p></div>
            <a href="tel:+18639402161" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = grid_pat.sub(NEW_GRID, h, count=1)

note_pat = re.compile(
    r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)',
    flags=re.S,
)
assert note_pat.search(h), 'no se encontro la nota de servicios'
NEW_NOTE = (
    r'\1<span data-es="También: gel nails y servicios de cejas por cita. Menú completo y precios vigentes al llamar al (863) 940-2161." '
    r'data-en="Also: gel nails and brow services by appointment. Full menu and current pricing by calling (863) 940-2161.">'
    r'Also: gel nails and brow services by appointment. Full menu and current pricing by calling (863) 940-2161.</span>\2'
)
h = note_pat.sub(NEW_NOTE, h, count=1)

print('OK paso 11 (servicios)')

# ============================================================
# 12. GALERIA: heading + IG link + grid completo (regex)
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajos" data-en="Recent">Recent</span> <span class="text-shine" data-es="recientes de color" data-en="color work">color work</span></h2>',
)

gal_pat = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    flags=re.S,
)
assert gal_pat.search(h), 'no se encontro el grid de galeria'
NEW_GAL = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Ombré cobrizo" data-en="Copper ombre">Copper ombre</span><img src="assets/raw/bk-3.jpg" alt="Auburn-to-copper color melt finished at Copper Penny Hair Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Castaño con brillo" data-en="Glossy brunette">Glossy brunette</span><img src="assets/raw/bk-9.jpg" alt="Rich glossy brunette finish" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Balayage con raíz" data-en="Rooted balayage">Rooted balayage</span><img src="assets/raw/bk-7.jpg" alt="Blonde balayage with a soft shadow root" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Rubio dorado" data-en="Golden blonde">Golden blonde</span><img src="assets/raw/bk-11.jpg" alt="Golden blonde balayage finish" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Rubio ceniza" data-en="Cool blonde">Cool blonde</span><img src="assets/raw/bk-5.jpg" alt="Cool-toned ashy blonde balayage" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Rubio dimensional" data-en="Dimensional blonde">Dimensional blonde</span><img src="assets/raw/bk-10.jpg" alt="Dimensional blonde color with a soft money-piece" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = gal_pat.sub(NEW_GAL, h, count=1)

print('OK paso 12 (galeria)')

# ============================================================
# 13. OPINIONES
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>\n'
    '        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="las clientas" data-en="are saying">are saying</span></h2>\n'
    '        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 124 reseñas en Google" data-en="4.9 out of 5 · 124 reviews on Google">4.9 out of 5 · 124 reviews on Google</span></p>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n'
    '          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Lisa is so awesome! She is patient with my kids and does an amazing job!"</blockquote>\n'
    '          <figcaption class="text-sm"><span class="font-medium">Niki Gilbertsen</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n'
    '          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Exquisite exquisite hair designs by the staff. The ambiance exudes relaxation."</blockquote>\n'
    '          <figcaption class="text-sm"><span class="font-medium">Louella Taylor</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n'
    '          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Feel like a new person after every visit for a very reasonable price."</blockquote>\n'
    '          <figcaption class="text-sm"><span class="font-medium">Michelle McPherson</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>',
)
rep(
    '<a href="tel:+18639402161" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=Copper+Penny+Hair+Studio+Lakeland+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 124 reseñas en Google" data-en="Read all 124 reviews on Google">Read all 124 reviews on Google</a>',
)

print('OK paso 13 (opiniones)')

# ============================================================
# 14. UBICACION
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Lakeland</span></h2>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(224,137,63,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1003 S Florida Ave, Lakeland, FL 33803</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(224,137,63,0.4)]" href="https://www.google.com/maps?q=1003+S+Florida+Ave,+Lakeland,+FL+33803" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>',
)
rep(
    '<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(224,137,63,0.4)]" href="tel:+18639402161" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<p class="font-medium mb-1" data-es="Citas" data-en="Appointments">Appointments</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa: llama o pasa por el estudio. Martes a sábado, de 10am a 7pm." data-en="By appointment: call or stop by the studio. Tuesday through Saturday, 10am to 7pm.">By appointment: call or stop by the studio. Tuesday through Saturday, 10am to 7pm.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(224,137,63,0.4)]" href="tel:+18639402161" data-es="Llamar al (863) 940-2161" data-en="Call (863) 940-2161">Call (863) 940-2161</a>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos de color más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest color work and DM any questions before your appointment.">See the latest color work and DM any questions before your appointment.</p>',
)
rep(
    '<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n'
    '          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Map: Copper Penny Hair Studio, 1003 S Florida Ave, Lakeland FL"\n'
    '          src="https://www.google.com/maps?q=1003+S+Florida+Ave,+Lakeland,+FL+33803&output=embed"',
)

print('OK paso 14 (ubicacion)')

# ============================================================
# 15. CTA FINAL
# ============================================================
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Donde el color se convierte en arte." data-en="Where color meets craft.">Where color meets craft.</p>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Llama y asegura el color que llevas planeando con la estilista de tu confianza, o con la próxima colorista disponible." data-en="Call to grab the color you have been planning with the stylist you trust, or the next open colorist on the schedule.">Call to grab the color you have been planning with the stylist you trust, or the next open colorist on the schedule.</p>',
)
rep(
    '<a href="tel:+18639402161" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="tel:+18639402161" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar para reservar" data-en="Call to book">Call to book</a>',
)

print('OK paso 15 (cta final)')

# ============================================================
# 16. FOOTER
# ============================================================
rep(
    '<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Copper Penny</span>',
)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(239,189,143,0.35)]" loading="lazy" />\n'
    '          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/raw/bk-12.jpg" alt="Copper Penny Hair Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(239,189,143,0.35)]" loading="lazy" />\n'
    '          <span class="font-display text-lg tracking-[0.1em] uppercase">Copper Penny Hair Studio</span>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Salón de belleza en Lakeland, FL. Atención con cita previa." data-en="Hair salon in Lakeland, FL. By appointment only.">Hair salon in Lakeland, FL. By appointment only.</p>',
)
rep(
    '<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n'
    '        <p><a href="tel:+18639402161" target="_blank" rel="noopener" class="hover:text-[#efb2a5]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p>1003 S Florida Ave, Lakeland, FL 33803</p>\n'
    '        <p><a href="tel:+18639402161" class="hover:text-[#efb2a5]" data-es="Llamar · (863) 940-2161" data-en="Call · (863) 940-2161">Call · (863) 940-2161</a></p>',
)
rep(
    '<p><a href="https://www.instagram.com/copperpennyhairstudiollc/" target="_blank" rel="noopener" class="hover:text-[#efb2a5]">Instagram · @copperpennyhairstudiollc</a></p>',
    '<p><a href="https://www.instagram.com/copperpennyhairstudiollc/" target="_blank" rel="noopener" class="hover:text-[#efb2a5]">Instagram · @copperpennyhairstudiollc</a></p>',
)
rep(
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Copper Penny Hair Studio.</p>',
)

print('OK paso 16 (footer)')

# ============================================================
# 17. PRELOADER + BOTON FLOTANTE
# ============================================================
rep(
    '<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">CP</span>\n    <span class="pre-word">Copper Penny</span>',
)
rep(
    '<a href="tel:+18639402161" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n'
    '    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n'
    '  </a>',
    '<a href="tel:+18639402161" class="book-float" aria-label="Call to book an appointment">\n'
    '    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n'
    '  </a>',
)

print('OK paso 17 (preloader + book-float)')
h_out = h
open(DST, 'w', encoding='utf-8').write(h_out)
print('BUILD COMPLETO:', DST)
