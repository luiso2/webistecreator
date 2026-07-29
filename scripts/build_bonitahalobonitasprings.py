#!/usr/bin/env python3
"""Deriva output/bonita-halo-bonita-springs/index.html desde templates/dark-v2/index.html
(esqueleto Pure Artistry) via transformacion anclada (assert-then-replace).
"""
import re

SLUG = 'bonita-halo-bonita-springs'
PATH = f'output/{SLUG}/index.html'

h = open(PATH, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert h.count(a) >= n, f'NO ENCONTRADO (esperaba >= {n}): {a[:90]!r}'
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    c = h.count(a)
    if expect is not None:
        assert c == expect, f'count={c} esperado={expect} para {a[:90]!r}'
    else:
        assert c > 0, f'NO ENCONTRADO: {a[:90]!r}'
    h = h.replace(a, b)


# ============================================================
# 1. PROTEGER EL BADGE MERKTOP (queda dorado SIEMPRE)
# ============================================================
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque merktop-badge'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ============================================================
# 2. PALETA: gold dark original -> "ember copper" (terracota/cobre oscuro)
#    Distinta de: coral fairy #c04e62, caramelo #a86a2e, esmeralda #2f7d5a,
#    teal acero #4fb8b8, violeta dark #b18ae8, rosa dark, gold dark original.
# ============================================================
PALETTE = [
    # rgba principal accent-deep (212,168,75) -> nuevo accent-deep (181,86,47)
    ('212,168,75', '181,86,47'),
    # rgba variante clara dark-band (232,207,150) y (232,210,160) -> tinte claro cobre
    ('232,207,150', '226,162,120'),
    ('232,210,160', '226,162,120'),
    # orb-b oscuro (122,90,30) -> cobre oscuro profundo
    ('122,90,30', '100,48,26'),
    # orb-c medio (180,140,60) -> cobre medio
    ('180,140,60', '199,110,66'),
    # btn-3d inset shadow marron (80,58,18) -> sombra cobre oscura
    ('80,58,18', '74,40,20'),
    # dark-band btn-3d shadow (110,85,35) -> variante clara
    ('110,85,35', '96,58,32'),
    # dark-band orb-b dusty (185,138,128) -> dusty terracota
    ('185,138,128', '198,138,112'),
    # hex solidos: accent-deep / accent-mid
    ('#d4a84b', '#b5562f'),
    ('#b8934a', '#cf7a4a'),
    # btn-3d gradiente (claro, medio, oscuro) + sombra "suela"
    ('#e8c476', '#e2926a'),
    ('#c9a04a', '#c46a3e'),
    ('#96742c', '#7a3f22'),
    ('#6b5222', '#5c2f18'),
    # text-shine base: oscuro / claro-medio / clarisimo
    ('#9a7431', '#7a3f22'),
    ('#e5c374', '#e2926a'),
    ('#f0dc9e', '#f0c9a8'),
    # accent-soft
    ('#241c0e', '#2a190f'),
    # bg / bg-2 (tinte calido levemente distinto)
    ('#0f0b07', '#100c09'),
    ('#171207', '#181310'),
    # cta-final gradient stops + footer bg
    ('#191307', '#1c130c'),
    ('#100c05', '#120d09'),
    ('#0c0905', '#0e0b08'),
    # dark-band text-shine stops
    ('#e8cf96', '#eab68c'),
    ('#f8eed3', '#f6ddc8'),
    ('#bfa060', '#b8724a'),
    # dark-band btn-3d gradient + shadow sole
    ('#faf1dc', '#f5ddc8'),
    ('#ecd9a8', '#e8b590'),
    ('#c9ab6b', '#c98a5e'),
    ('#8a744a', '#8a5a3a'),
    # dark-band stars / hover link accent
    ('#e9c3ab', '#e6b092'),
]
for old, new in PALETTE:
    c = h.count(old)
    assert c > 0, f'paleta: no encontrado {old!r}'
    h = h.replace(old, new)

# restaurar badge (siempre dorado)
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

# ============================================================
# 3. GLOBALES: URL de GlossGenius, IG, handle, tema
# ============================================================
rep_all('https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando',
        'https://bonitahalo.glossgenius.com/')
rep_all('https://www.instagram.com/pure.artistrysk/', 'https://www.instagram.com/bonitahaloheadspa/')
rep_all('@pure.artistrysk', '@bonitahaloheadspa')
# theme-color ya quedo en #100c09 por el replace global de paleta (bg)

# ============================================================
# 4. HEAD: title, meta, og, JSON-LD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Bonita Halo Head Spa · Head Spa in Bonita Springs, FL | Scalp Rituals &amp; Red Light Therapy | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Bonita Halo Head Spa, Bonita Springs FL: scalp rituals, exfoliation, steam, hydration masks and red light therapy. 5.0 with 22 reviews on Google. Book on GlossGenius." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Bonita Halo Head Spa · Head Spa in Bonita Springs, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Scalp rituals, steam, hydration masks and red light therapy. 5.0 on Google. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-scalp-massage.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-scalp-massage.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "Bonita Halo Head Spa",
    "description": "Head spa studio in Bonita Springs, FL: scalp assessments, exfoliation, detox shampoo, steam, hydration masks, red light therapy and high-frequency scalp stimulation.",
    "address": { "@type": "PostalAddress", "streetAddress": "11338 Bonita Beach Rd SE, Suite 105", "addressLocality": "Bonita Springs", "addressRegion": "FL", "postalCode": "34135", "addressCountry": "US" },
    "telephone": "+12393667240",
    "sameAs": ["https://bonitahalo.glossgenius.com/", "https://www.instagram.com/bonitahaloheadspa/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "22", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "10:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Head spa services", "itemListElement": [
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Refresh Ritual" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Halo Glow Experience" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Blissful Crown Journey" } },
      { "@type": "Offer", "price": "249", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Luxe Rejuvenation Escape" } },
      { "@type": "Offer", "price": "114", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Gentleman's Reset" } }
    ] }
  }
  </script>'''
assert old_jsonld in h
h = h.replace(old_jsonld, new_jsonld, 1)

# ============================================================
# 5. IDIOMA: negocio en ingles, el esqueleto YA es EN default. Sin cambios en applyLang/html lang.
# ============================================================

# ============================================================
# 5b. PRELOADER DE MARCA
# ============================================================
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">BH</span>\n    <span class="pre-word">Bonita Halo</span>')

# ============================================================
# 6. NAV: monograma texto (sin foto real de logo), nombre del negocio
# ============================================================
rep('<a href="#top" class="flex items-center gap-3">\n        <img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,86,47,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>\n      </a>',
    '<a href="#top" class="flex items-center gap-3">\n        <span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(181,86,47,0.35)]" style="background:linear-gradient(135deg, rgba(181,86,47,0.22), rgba(181,86,47,0.06)); color:var(--accent-deep);">BH</span>\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Bonita <span class="text-[color:var(--accent-deep)]">Halo</span></span>\n      </a>')

for old, new in [
    ('data-es="La Experiencia" data-en="The Experience">La Experiencia</a>', 'data-es="The Experience" data-en="The Experience">The Experience</a>'),
    ('data-es="El Método" data-en="The Method">El Método</a>', 'data-es="The Ritual" data-en="The Ritual">The Ritual</a>'),
    ('data-es="Servicios" data-en="Services">Servicios</a>', 'data-es="Services" data-en="Services">Services</a>'),
    ('data-es="Galería" data-en="Gallery">Galería</a>', 'data-es="Gallery" data-en="Gallery">Gallery</a>'),
    ('data-es="Opiniones" data-en="Reviews">Opiniones</a>', 'data-es="Reviews" data-en="Reviews">Reviews</a>'),
    ('data-es="Ubicación" data-en="Location">Ubicación</a>', 'data-es="Location" data-en="Location">Location</a>'),
]:
    rep_all(old, new, expect=2)  # aparece en nav desktop + mobileMenu

rep_all('data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
        'data-es="Book now" data-en="Book now">Book now</span>')
rep_all('data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
        'data-es="Book now" data-en="Book now">Book now</a>')

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Bonita Springs, FL · Head Spa" data-en="Bonita Springs, FL · Head Spa">Bonita Springs, FL · Head Spa</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Scalp care, done right." data-en="Scalp care, done right.">Scalp care, done right.</p>', n=1)
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Head spa rituals that turn" data-en="Head spa rituals that turn">Head spa rituals that turn</span><br /><span data-es="your scalp into " data-en="your scalp into ">your scalp into </span><span class="text-shine" data-es="pure calm" data-en="pure calm">pure calm</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="The Refresh Ritual, the Halo Glow Experience, the Blissful Crown Journey and the signature Luxe Rejuvenation Escape: scalp assessments, exfoliation, steam and red light therapy in a private Bonita Springs studio. 5.0 stars across 22 Google reviews." data-en="The Refresh Ritual, the Halo Glow Experience, the Blissful Crown Journey and the signature Luxe Rejuvenation Escape: scalp assessments, exfoliation, steam and red light therapy in a private Bonita Springs studio. 5.0 stars across 22 Google reviews.">The Refresh Ritual, the Halo Glow Experience, the Blissful Crown Journey and the signature Luxe Rejuvenation Escape: scalp assessments, exfoliation, steam and red light therapy in a private Bonita Springs studio. 5.0 stars across 22 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 22 reviews on Google" data-en="5.0 · 22 reviews on Google">5.0 · 22 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</span>', n=1)
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-scalp-massage.jpg" alt="Client receiving a relaxing scalp massage by candlelight at Bonita Halo Head Spa" class="blur-up w-full h-full object-cover" />')
rep('data-es="Reserva online" data-en="Book online">Reserva online</p>',
    'data-es="Book online" data-en="Book online">Book online</p>', n=1)
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">Luxe Rejuvenation Escape</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="From $249 · 120 min" data-en="From $249 · 120 min">From $249 · 120 min</p>')

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="22">22</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Scalp <span class="text-shine">&amp;</span> Hair</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Exfoliation · Steam · Massage" data-en="Exfoliation · Steam · Massage">Exfoliation · Steam · Massage</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Red Light <span class="text-shine">&amp;</span> Freq.</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Luxe Rejuvenation Escape" data-en="Luxe Rejuvenation Escape">Luxe Rejuvenation Escape</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Bonita Springs</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Bonita Beach Rd</p></div>')

# ============================================================
# 9. MARQUEE (x2 franjas, 4 ocurrencias por palabra)
# ============================================================
marquee_pairs = [
    ('Silk Press', 'The Refresh Ritual'),
    ('Loc Retwist', 'Halo Glow Experience'),
    ('Knotless Braids', 'Blissful Crown Journey'),
    ('K-Tip Extensions', 'Luxe Rejuvenation Escape'),
    ('Keratin', 'Red Light Therapy'),
    ('Orlando, FL', 'Bonita Springs, FL'),
]
for old, new in marquee_pairs:
    old_tag = f'<span class="marquee-word">{old}</span>'
    new_tag = f'<span class="marquee-word">{new}</span>'
    rep_all(old_tag, new_tag, expect=4)

# ============================================================
# 10. LA EXPERIENCIA
# ============================================================
exp_grid_old = re.search(
    r'<div class="grid grid-cols-2 gap-5">\s*<div class="frame zoomable aspect-\[3/4\] img-reveal">\s*'
    r'<img src="assets/raw/bk-2\.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry"[^>]*/>\s*</div>\s*'
    r'<div class="frame zoomable aspect-\[3/4\] mt-10 img-reveal" style="transition-delay:140ms">\s*'
    r'<img src="assets/raw/bk-6\.jpg" alt="Twists recien terminados en Pure Artistry"[^>]*/>\s*</div>\s*</div>', h)
assert exp_grid_old, 'no se encontro el grid de 2 imagenes de experiencia'
# El esqueleto trae 2 imagenes en Experiencia; solo hay 1 foto real distinta disponible para esta
# seccion (la otra ya se reutiliza en Galeria), asi que se reduce a 1 sola imagen en vez de repetir.
exp_grid_new = (
    '<div class="grid grid-cols-1 max-w-sm mx-auto lg:mx-0">'
    '<div class="frame zoomable aspect-[3/4] img-reveal">'
    '<img src="assets/about-scalp-massage-detail.jpg" alt="Close detail of a scalp massage in progress at Bonita Halo Head Spa" class="blur-up w-full h-full object-cover" loading="lazy" />'
    '</div></div>'
)
h = h[:exp_grid_old.start()] + exp_grid_new + h[exp_grid_old.end():]
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="The experience" data-en="The experience">The experience</p>')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="One studio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="one scalp at a time" data-en="one scalp at a time">one scalp at a time</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Bonita Halo Head Spa is Marcela Montalvo\'s private studio in Bonita Springs: a cosmetologist with a background in trichology who built her practice around scalp health, not just hair styling. Every visit starts with a scalp assessment before any product touches your hair." data-en="Bonita Halo Head Spa is Marcela Montalvo\'s private studio in Bonita Springs: a cosmetologist with a background in trichology who built her practice around scalp health, not just hair styling. Every visit starts with a scalp assessment before any product touches your hair.">Bonita Halo Head Spa is Marcela Montalvo\'s private studio in Bonita Springs: a cosmetologist with a background in trichology who built her practice around scalp health, not just hair styling. Every visit starts with a scalp assessment before any product touches your hair.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Clients come back for the full ritual: exfoliation, a detox shampoo, a steaming hydration mask and, for signature visits, red light therapy with high-frequency scalp stimulation. 5.0 stars across 22 Google reviews." data-en="Clients come back for the full ritual: exfoliation, a detox shampoo, a steaming hydration mask and, for signature visits, red light therapy with high-frequency scalp stimulation. 5.0 stars across 22 Google reviews.">Clients come back for the full ritual: exfoliation, a detox shampoo, a steaming hydration mask and, for signature visits, red light therapy with high-frequency scalp stimulation. 5.0 stars across 22 Google reviews.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="22">22</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reviews" data-en="Reviews">Reviews</p></div>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,86,47,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-xs ring-1 ring-[rgba(181,86,47,0.3)]" style="background:rgba(181,86,47,0.14); color:var(--accent-deep);">BH</span>\n            <span class="text-sm font-light">Bonita Halo Head Spa · <span class="text-[color:var(--ink-40)]" data-es="Trichology-based care" data-en="Trichology-based care">Trichology-based care</span></span>')

# ============================================================
# 11. EL METODO -> "The Ritual"
# ============================================================
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Your visit, step by step" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="here" data-en="here">here</span>')
rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Book online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Pick your ritual on GlossGenius with clear price and duration: Refresh Ritual, Halo Glow, Blissful Crown or the signature Luxe Rejuvenation Escape." data-en="Pick your ritual on GlossGenius with clear price and duration: Refresh Ritual, Halo Glow, Blissful Crown or the signature Luxe Rejuvenation Escape.">Pick your ritual on GlossGenius with clear price and duration: Refresh Ritual, Halo Glow, Blissful Crown or the signature Luxe Rejuvenation Escape.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Scalp assessment" data-en="Scalp assessment">Scalp assessment</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Marcela\'s trichology background means every visit opens with a scalp read before any product or steam touches your hair." data-en="Marcela\'s trichology background means every visit opens with a scalp read before any product or steam touches your hair.">Marcela\'s trichology background means every visit opens with a scalp read before any product or steam touches your hair.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="The ritual" data-en="The ritual">The ritual</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Exfoliation, a detox shampoo and a steaming hydration mask, with red light therapy and high-frequency stimulation added on signature visits." data-en="Exfoliation, a detox shampoo and a steaming hydration mask, with red light therapy and high-frequency stimulation added on signature visits.">Exfoliation, a detox shampoo and a steaming hydration mask, with red light therapy and high-frequency stimulation added on signature visits.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="The finish" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A finishing blow dry and at-home guidance to keep your scalp healthy between visits." data-en="A finishing blow dry and at-home guidance to keep your scalp healthy between visits.">A finishing blow dry and at-home guidance to keep your scalp healthy between visits.</p>')

# ============================================================
# 12. SERVICIOS (4 cards reales + nota con el resto del menu)
# ============================================================
rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Services" data-en="Services">Services</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Choose your" data-en="Choose your">Choose your</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Prices and durations as published by Bonita Halo Head Spa on GlossGenius. Booking confirms instantly." data-en="Prices and durations as published by Bonita Halo Head Spa on GlossGenius. Booking confirms instantly.">Prices and durations as published by Bonita Halo Head Spa on GlossGenius. Booking confirms instantly.</p>')

services_old = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert services_old, 'no se encontro el grid de servicios'
services_new = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(181,86,47,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="House signature" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">The Luxe Rejuvenation Escape</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A two-hour escape with red light therapy, high-frequency scalp stimulation and an extended massage covering neck, shoulders, arms and decollete." data-en="A two-hour escape with red light therapy, high-frequency scalp stimulation and an extended massage covering neck, shoulders, arms and decollete.">A two-hour escape with red light therapy, high-frequency scalp stimulation and an extended massage covering neck, shoulders, arms and decollete.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$249</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">120 min</p></div>
            <a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Head spa" data-en="Head spa">Head spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="The Halo Glow Experience" data-en="The Halo Glow Experience">The Halo Glow Experience</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Scalp assessment, exfoliation, detox shampoo and hydration mask, plus a soothing scalp steam." data-en="Scalp assessment, exfoliation, detox shampoo and hydration mask, plus a soothing scalp steam.">Scalp assessment, exfoliation, detox shampoo and hydration mask, plus a soothing scalp steam.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">10+ min</p></div>
            <a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Head spa" data-en="Head spa">Head spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="The Blissful Crown Journey" data-en="The Blissful Crown Journey">The Blissful Crown Journey</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="The full ritual plus a shoulder massage. A shared version for two, with a waterfall halo ritual, aromatherapy and hot stone shoulder and neck massage, runs $359 for 90 minutes." data-en="The full ritual plus a shoulder massage. A shared version for two, with a waterfall halo ritual, aromatherapy and hot stone shoulder and neck massage, runs $359 for 90 minutes.">The full ritual plus a shoulder massage. A shared version for two, with a waterfall halo ritual, aromatherapy and hot stone shoulder and neck massage, runs $359 for 90 minutes.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">10+ min</p></div>
            <a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="For him" data-en="For him">For him</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="The Gentleman's Reset" data-en="The Gentleman's Reset">The Gentleman's Reset</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Scalp assessment, in-house detox shampoo, warm steam, hydration mask, red light and high-frequency therapy." data-en="Scalp assessment, in-house detox shampoo, warm steam, hydration mask, red light and high-frequency therapy.">Scalp assessment, in-house detox shampoo, warm steam, hydration mask, red light and high-frequency therapy.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$114</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">60 min</p></div>
            <a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_old.start()] + services_new + h[services_old.end():]

nota_old = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert nota_old
nota_new = nota_old.group(1) + '<span data-es="Also: The Refresh Ritual from $25 (10+ min), The Halo Hair Extensions Cleanse from $119 (60+ min) and a finishing Blow Dry for $65 (30 min). Full menu and booking on GlossGenius." data-en="Also: The Refresh Ritual from $25 (10+ min), The Halo Hair Extensions Cleanse from $119 (60+ min) and a finishing Blow Dry for $65 (30 min). Full menu and booking on GlossGenius.">Also: The Refresh Ritual from $25 (10+ min), The Halo Hair Extensions Cleanse from $119 (60+ min) and a finishing Blow Dry for $65 (30 min). Full menu and booking on GlossGenius.</span>' + nota_old.group(2)
h = h[:nota_old.start()] + nota_new + h[nota_old.end():]

# ============================================================
# 13. GALERIA
# ============================================================
rep('data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    'data-es="Gallery" data-en="Gallery">Gallery</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="visit" data-en="visit">visit</span></h2>')

gallery_old = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert gallery_old, 'no se encontro el grid de galeria'
gallery_new = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Scalp analysis" data-en="Scalp analysis">Scalp analysis</span><img src="assets/gallery-scalp-scanner.jpg" alt="Scalp analysis device with red light used at Bonita Halo Head Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="The studio" data-en="The studio">The studio</span><img src="assets/gallery-storefront.jpg" alt="Bonita Halo Head Spa storefront in Bonita Springs, FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Inside" data-en="Inside">Inside</span><img src="assets/gallery-interior-tile.jpg" alt="Interior tile detail inside the Bonita Halo Head Spa studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_old.start()] + gallery_new + h[gallery_old.end():]

# ============================================================
# 14. OPINIONES (solo 2 reviews reales verbatim disponibles; sin nombre de autor
#     disponible en la fuente -> NO se inventa un nombre, se atribuye honestamente)
# ============================================================
rep('data-es="Opiniones" data-en="Reviews">Opiniones</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    'data-es="Reviews" data-en="Reviews">Reviews</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="What her" data-en="What her">What her</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 22 reviews on Google" data-en="5.0 out of 5 · 22 reviews on Google">5.0 out of 5 · 22 reviews on Google</span></p>')

reviews_old = re.search(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)', h, flags=re.S)
assert reviews_old, 'no se encontro el grid de opiniones'
reviews_new = '''<div class="grid sm:grid-cols-2 gap-5 items-stretch max-w-3xl mx-auto">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"It was amazing! The hair spa was so relaxing. I can't wait to be back. Highly recommended."</blockquote>
          <figcaption class="text-sm"><span class="font-medium" data-es="Real client" data-en="Real client">Real client</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"My scalp is susceptible. The technician knew exactly what to do and what products to use. My treatment was perfect."</blockquote>
          <figcaption class="text-sm"><span class="font-medium" data-es="Real client" data-en="Real client">Real client</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_old.start()] + reviews_new + h[reviews_old.end():]

rep('data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Read reviews on Google" data-en="Read reviews on Google">Read reviews on Google</a>')
rep('href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read reviews on Google"',
    'href="https://www.google.com/search?q=Bonita+Halo+Head+Spa+Bonita+Springs+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read reviews on Google"')

# ============================================================
# 15. UBICACION
# ============================================================
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    'data-es="Visit us" data-en="Visit us">Visit us</p>')
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Bonita Springs</span>')
rep('data-es="Dirección" data-en="Address">Dirección</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,86,47,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    'data-es="Address" data-en="Address">Address</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light">11338 Bonita Beach Rd SE, Suite 105, Bonita Springs, FL 34135</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,86,47,0.4)]" href="https://www.google.com/maps?q=11338+Bonita+Beach+Rd+SE,+Bonita+Springs,+FL+34135" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>')
rep('data-es="Reservas" data-en="Bookings">Reservas</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,86,47,0.4)]" href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    'data-es="Bookings" data-en="Bookings">Bookings</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="By appointment via GlossGenius: pick the ritual, day and time, and the confirmation is instant." data-en="By appointment via GlossGenius: pick the ritual, day and time, and the confirmation is instant.">By appointment via GlossGenius: pick the ritual, day and time, and the confirmation is instant.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,86,47,0.4)]" href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="See recent scalp rituals and DM any questions before your appointment." data-en="See recent scalp rituals and DM any questions before your appointment.">See recent scalp rituals and DM any questions before your appointment.</p>')
rep('<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Map: Bonita Halo Head Spa, 11338 Bonita Beach Rd SE, Bonita Springs FL"\n          src="https://www.google.com/maps?q=11338+Bonita+Beach+Rd+SE,+Bonita+Springs,+FL+34135&output=embed"')

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Scalp care, done right." data-en="Scalp care, done right.">Scalp care, done right.</p>')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Your scalp deserves" data-en="Your scalp deserves">Your scalp deserves</span> <span class="text-shine" data-es="this ritual" data-en="this ritual">this ritual</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Book online in seconds: the Halo Glow Experience, the Blissful Crown Journey, or the signature Luxe Rejuvenation Escape." data-en="Book online in seconds: the Halo Glow Experience, the Blissful Crown Journey, or the signature Luxe Rejuvenation Escape.">Book online in seconds: the Halo Glow Experience, the Blissful Crown Journey, or the signature Luxe Rejuvenation Escape.</p>')
rep('<a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Bonita Halo</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(226,162,120,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-xs ring-1 ring-[rgba(226,162,120,0.35)]" style="background:rgba(226,162,120,0.14); color:#f2ece0;">BH</span>\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Bonita Halo</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Head spa studio in Bonita Springs, FL. By appointment via GlossGenius." data-en="Head spa studio in Bonita Springs, FL. By appointment via GlossGenius.">Head spa studio in Bonita Springs, FL. By appointment via GlossGenius.</p>')
rep('data-es="Contacto" data-en="Contact">Contacto</p>\n        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n        <p><a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="hover:text-[#e6b092]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    'data-es="Contact" data-en="Contact">Contact</p>\n        <p>11338 Bonita Beach Rd SE, Suite 105, Bonita Springs, FL 34135</p>\n        <p><a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="hover:text-[#e6b092]" data-es="Online booking · GlossGenius" data-en="Online booking · GlossGenius">Online booking · GlossGenius</a></p>')
rep('data-es="Síguenos" data-en="Follow">Síguenos</p>\n        <p><a href="https://www.instagram.com/bonitahaloheadspa/" target="_blank" rel="noopener" class="hover:text-[#e6b092]">Instagram · @bonitahaloheadspa</a></p>',
    'data-es="Follow" data-en="Follow">Follow</p>\n        <p><a href="https://www.instagram.com/bonitahaloheadspa/" target="_blank" rel="noopener" class="hover:text-[#e6b092]">Instagram · @bonitahaloheadspa</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Bonita Halo Head Spa.</p>')
rep('<a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://bonitahalo.glossgenius.com/" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')

open(PATH, 'w', encoding='utf-8').write(h)
print('OK escrito:', PATH, len(h), 'bytes')
