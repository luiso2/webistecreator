#!/usr/bin/env python3
"""Deriva output/meris-beauty-studio-jacksonville/index.html desde templates/dark-v2/index.html
siguiendo la receta de templates/SKELETONS-V2.md (transformacion anclada, rep() con assert).
"""
import re

SLUG = 'meris-beauty-studio-jacksonville'
SRC = f'output/{SLUG}/index.html'  # ya copiado del esqueleto dark-v2

h = open(SRC, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    count = h.count(a)
    assert count >= n, f'NO ENCONTRADO (necesita {n}, hay {count}): {a[:90]!r}'
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    count = h.count(a)
    if expect is not None:
        assert count == expect, f'esperaba {expect} ocurrencias, hay {count}: {a[:90]!r}'
    else:
        assert count > 0, f'NO ENCONTRADO: {a[:90]!r}'
    h = h.replace(a, b)


# =====================================================================
# 1) PROTEGER EL BADGE MERKTOP (queda dorado siempre)
# =====================================================================
badge_re = re.compile(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", re.S)
m = badge_re.search(h)
assert m, 'no se encontro el bloque .merktop-badge'
badge_block = m.group(0)
h = h[:m.start()] + '@@BADGE@@' + h[m.end():]

# =====================================================================
# 2) PALETA: dusty orchid-plum sobre charcoal calido (real: linos morados +
#    guantes rosa magenta vistos en las fotos reales del estudio; el logo
#    negro+dorado se conserva solo en el badge Merktop, que queda protegido).
#    Generado por rotacion de matiz (colorsys) desde el dorado original del
#    esqueleto para mantener consistencia de brillo/rol entre todos los tonos.
# =====================================================================
HEX_PAIRS = [
    ('#0f0b07', '#0e090d'),  # bg
    ('#171207', '#160c12'),  # bg-2
    ('#f5efe3', '#e6dce2'),  # ink
    ('#d4a84b', '#c777a6'),  # accent-deep
    ('#b8934a', '#ad6d94'),  # accent-mid
    ('#241c0e', '#22151d'),  # accent-soft
    ('#f0dc9e', '#e2b2ca'),  # shimmer highlight
    ('#9a7431', '#91547a'),  # shimmer shadow / step-num end
    ('#e5c374', '#d795bb'),  # shimmer accent / step-num start
    ('#e8c476', '#da98be'),  # btn-3d gradient top
    ('#c9a04a', '#bd739f'),  # btn-3d gradient mid / book-float bottom
    ('#96742c', '#8d4f74'),  # btn-3d gradient bottom
    ('#1c1408', '#1a0f16'),  # btn-3d text / svg stroke (near black)
    ('#6b5222', '#653a54'),  # btn-3d shadow "suela"
    ('#e9c3ab', '#dbb7d7'),  # dark-band stars
    ('#e8cf96', '#daaac6'),  # dark-band text-shine start/accent
    ('#f8eed3', '#e9d4df'),  # dark-band text-shine highlight
    ('#bfa060', '#b47c9d'),  # dark-band text-shine mid
    ('#f0dcae', '#e2bbd1'),  # dark-band text-shine end
    ('#faf1dc', '#ebdae3'),  # dark-band btn-3d top
    ('#ecd9a8', '#deb6cc'),  # dark-band btn-3d mid
    ('#c9ab6b', '#bd86a6'),  # dark-band btn-3d bottom
    ('#8a744a', '#825c73'),  # dark-band btn-3d shadow
    ('#fbf6ea', '#ece2e8'),  # tile-cap text (near white)
    ('#191307', '#170d13'),  # cta-final bg gradient start
    ('#100c05', '#0f090d'),  # cta-final bg gradient end
    ('#0c0905', '#0b070a'),  # footer bg
]
for old, new in HEX_PAIRS:
    rep_all(old, new)
# #D4A84B uppercase variant used once outside the badge (theme irrelevant; already inside badge only)

RGB_PAIRS = [
    ('212,168,75', '199,119,166'),
    ('232,207,150', '218,170,198'),
    ('245,239,227', '230,220,226'),
    ('232,210,160', '218,176,200'),
    ('185,138,128', '171,141,174'),
    ('180,140,60', '169,99,141'),
    ('122,90,30', '115,61,94'),
    ('110,85,35', '103,60,86'),
    ('80,58,18', '75,39,62'),
    ('15,11,7', '14,9,13'),
]
for old, new in RGB_PAIRS:
    rep_all(f'rgba({old},', f'rgba({new},')

# restaurar el badge (dorado intacto)
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block)

# =====================================================================
# 3) GLOBALES: Booksy, Instagram, handle
# =====================================================================
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/1126607_meris-beauty-studio-massage-waxing-sugaring-facials_massage_15697_jacksonville'
rep_all(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/miss__meriss/'
rep_all(OLD_IG_URL, NEW_IG_URL)

rep_all('@pure.artistrysk', '@miss__meriss')

# =====================================================================
# 4) HEAD: title, meta, og, JSON-LD, theme-color
# =====================================================================
# nota: el hex de theme-color ya fue transformado por la paleta (paso 2) a #0e090d

rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    "<title>Meri's Beauty Studio · Waxing, Facials &amp; Massage in Jacksonville, FL | 5.0 on Booksy</title>")

rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Meri\'s Beauty Studio, Jacksonville FL: Brazilian and full body waxing, sugaring, facials and therapeutic massage. 5.0 with 50 reviews on Booksy. Book online." />')

rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Meri\'s Beauty Studio · Waxing &amp; Skincare in Jacksonville, FL" />')

rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Brazilian waxing, sugaring, facials and massage. 5.0 on Booksy. Book online." />')

# og:image y favicon quedan en assets/raw/bk-1.jpg y bk-2.jpg (mismos numeros, contenido nuevo)

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "Meri's Beauty Studio",
    "description": "Beauty studio in Jacksonville, FL: Brazilian and full body waxing, sugaring, facials and therapeutic massage.",
    "telephone": "+19046546396",
    "address": { "@type": "PostalAddress", "streetAddress": "9825 San Jose Blvd, Suite 32", "addressLocality": "Jacksonville", "addressRegion": "FL", "postalCode": "32257", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1126607_meris-beauty-studio-massage-waxing-sugaring-facials_massage_15697_jacksonville", "https://www.instagram.com/miss__meriss/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "50", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "15:30", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "12:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Beauty services", "itemListElement": [
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brazilian Wax" } },
      { "@type": "Offer", "price": "298", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Body Wax" } },
      { "@type": "Offer", "price": "111", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Signature Deep Cleansing & Hydrating Facial" } },
      { "@type": "Offer", "price": "94", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Body Massage" } }
    ] }
  }
  </script>'''
rep(OLD_JSONLD, NEW_JSONLD)

# =====================================================================
# 5) IDIOMA: negocio EN-primario (Jacksonville FL, reseñas en ingles).
#    El esqueleto dark-v2 ya es EN-default (html lang="en"); no se toca el
#    ternario de applyLang. Solo se llenan data-es/data-en reales abajo.
# =====================================================================

# =====================================================================
# 6) NAV
# =====================================================================
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(199,119,166,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Meri\'s Beauty Studio logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(199,119,166,0.35)]" />')

rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Meri\'s <span class="text-[color:var(--accent-deep)]">Beauty Studio</span></span>')

# =====================================================================
# 7) HERO
# =====================================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Jacksonville, FL · Estudio de Depilación y Skincare" data-en="Jacksonville, FL · Wax &amp; Skincare Studio">Jacksonville, FL · Wax &amp; Skincare Studio</p>')

rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Tu piel, tratada con cuidado." data-en="Your skin, treated with care.">Your skin, treated with care.</p>', n=1)

rep('''<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>''',
    '''<span data-es="Depilación brasileña," data-en="Brazilian waxing,">Brazilian waxing,</span><br /><span data-es="faciales y " data-en="facials and ">facials and </span><span class="text-shine" data-es="masajes" data-en="massage therapy">massage therapy</span>''')

rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Un estudio de belleza privado en Jacksonville, atendido por una esteticista y masajista con licencia: depilación de cuerpo completo, sugaring, faciales y masaje terapéutico, con 5.0 perfecto en 50 reseñas de Booksy." data-en="A private beauty studio in Jacksonville run by a licensed massage therapist and esthetician: full body waxing, sugaring, facials and therapeutic massage, with a perfect 5.0 across 50 reviews on Booksy.">A private beauty studio in Jacksonville run by a licensed massage therapist and esthetician: full body waxing, sugaring, facials and therapeutic massage, with a perfect 5.0 across 50 reviews on Booksy.</p>')

rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 50 reseñas en Booksy" data-en="5.0 · 50 reviews on Booksy">5.0 · 50 reviews on Booksy</span>')

rep('''<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />''',
    '''<img src="assets/raw/bk-1.jpg" alt="Meri, licensed esthetician, holding a wax pot and applicator at Meri's Beauty Studio in Jacksonville, FL" class="blur-up w-full h-full object-cover" />''')

rep('data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Silk Press</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Brazilian Wax</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $85 · 45min" data-en="From $85 · 45min">From $85 · 45min</p>')

# =====================================================================
# 8) STRIP DE CONFIANZA
# =====================================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="50">50</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>')

rep('''<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>''',
    '''<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Wax <span class="text-shine">&amp;</span> Sugaring</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Brasileña · Bikini · Cuerpo completo" data-en="Brazilian · Bikini · Full body">Brazilian · Bikini · Full body</p></div>''')

rep('''<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>''',
    '''<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Facials <span class="text-shine">&amp;</span> Massage</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Limpieza profunda · Piedras calientes" data-en="Deep cleansing · Hot stones">Deep cleansing · Hot stones</p></div>''')

rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Jacksonville</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">San Jose Blvd</p></div>')

# =====================================================================
# 9) MARQUEE (6 palabras x 4 apariciones cada una)
# =====================================================================
MARQUEE_WORDS = [
    ('Silk Press', 'Brazilian Wax'),
    ('Loc Retwist', 'Sugaring'),
    ('Knotless Braids', 'Facials'),
    ('K-Tip Extensions', 'Deep Tissue Massage'),
    ('Keratin', 'Hot Stones'),
    ('Orlando, FL', 'Jacksonville, FL'),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)

# =====================================================================
# 10) LA EXPERIENCIA
# =====================================================================
rep('''<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />''',
    '''<img src="assets/raw/bk-4.jpg" alt="Meri, licensed esthetician, with her skincare products at Meri's Beauty Studio" class="blur-up w-full h-full object-cover" loading="lazy" />''')

rep('''<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />''',
    '''<img src="assets/raw/bk-6.jpg" alt="Treatment room interior at Meri's Beauty Studio in Jacksonville, FL" class="blur-up w-full h-full object-cover" loading="lazy" />''')

rep('''<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>''',
    '''<span data-es="Una esteticista," data-en="One esthetician,">One esthetician,</span><br /><span class="text-shine" data-es="manos expertas" data-en="caring hands">caring hands</span>''')

rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Meri\'s Beauty Studio es el suite privado de Meri, masajista y esteticista con licencia, especializada en depilación de cuerpo completo, sugaring, faciales y skincare personalizado. Cada tratamiento es uno a uno, en un suite privado sobre San Jose Blvd." data-en="Meri\'s Beauty Studio is the private suite of Meri, a licensed massage therapist and esthetician specializing in full body waxing, sugaring, facials and personalized skincare. Every treatment is one-on-one, in a private suite on San Jose Blvd.">Meri\'s Beauty Studio is the private suite of Meri, a licensed massage therapist and esthetician specializing in full body waxing, sugaring, facials and personalized skincare. Every treatment is one-on-one, in a private suite on San Jose Blvd.</p>')

rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus reseñas lo dicen todo: cuidadosa, minuciosa y atenta a cada detalle, desde unas cejas rápidas hasta un tratamiento de cuerpo completo. 5.0 perfecto en 50 reseñas verificadas de Booksy." data-en="Her reviews say it best: gentle, thorough and detail oriented, from a quick brow wax to a full body treatment. A perfect 5.0 across 50 verified reviews on Booksy.">Her reviews say it best: gentle, thorough and detail oriented, from a quick brow wax to a full body treatment. A perfect 5.0 across 50 verified reviews on Booksy.</p>')

rep('<span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="50">50</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>')

rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(199,119,166,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
    '''<img src="assets/raw/bk-1.jpg" alt="Meri, esthetician" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(199,119,166,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Meri's Beauty Studio · <span class="text-[color:var(--ink-40)]" data-es="Esteticista y Masajista con Licencia" data-en="Licensed Esthetician &amp; Massage Therapist">Licensed Esthetician &amp; Massage Therapist</span></span>''')

# =====================================================================
# 11) EL METODO
# =====================================================================
rep('data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Elige tu servicio en Booksy con precio y duración claros: depilación, facial o masaje, y tu cita queda confirmada al instante." data-en="Pick your service on Booksy with clear price and duration: waxing, facial or massage, and your spot is confirmed instantly.">Pick your service on Booksy with clear price and duration: waxing, facial or massage, and your spot is confirmed instantly.</p>')

rep('data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    'data-es="Consulta de piel" data-en="Skin check-in">Skin check-in</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Una charla breve sobre tu piel, el vello y lo que buscas, antes de cada depilación, sugaring o facial." data-en="A quick conversation about your skin, hair growth and what you want, before every wax, sugaring or facial.">A quick conversation about your skin, hair growth and what you want, before every wax, sugaring or facial.</p>')

rep('data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    'data-es="El tratamiento" data-en="The treatment">The treatment</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde una cejas de 15 minutos hasta una sesión de cuerpo completo de 2 horas: cada tratamiento recibe su tiempo completo, sin apuros." data-en="From a 15-minute brow wax to a 2-hour full body session: every treatment gets its full, unhurried time.">From a 15-minute brow wax to a 2-hour full body session: every treatment gets its full, unhurried time.</p>')

rep('data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    'data-es="Cuidado final" data-en="Aftercare">Aftercare</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con resultados suaves y consejos simples de cuidado para mantener tu piel tranquila, con tu próxima cita ya en mente." data-en="You leave with smooth results and simple aftercare tips to keep your skin calm, with your next appointment already in mind.">You leave with smooth results and simple aftercare tips to keep your skin calm, with your next appointment already in mind.</p>')

print('OK hasta EL METODO')

# =====================================================================
# 12) SERVICIOS: eyebrow / H2 / subtitulo
# =====================================================================
rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">treatment</span></h2>')

rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Meri\'s Beauty Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Meri\'s Beauty Studio on Booksy. Booking confirms instantly.">Prices and durations as published by Meri\'s Beauty Studio on Booksy. Booking confirms instantly.</p>')

# =====================================================================
# 13) SERVICIOS: grid de 4 cards destacadas (regex, bloque completo)
# =====================================================================
SERVICES_GRID_RE = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    re.S)
m = SERVICES_GRID_RE.search(h)
assert m, 'no se encontro el grid de servicios'

BOOKSY = NEW_BOOKSY


def service_card(featured, label_es, label_en, title, desc_es, desc_en, price, dur, delay=None):
    border = ' style="border-color: rgba(199,119,166,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);"' if featured else (f' style="transition-delay:{delay}ms"' if delay else '')
    btn_cls = 'btn-3d' if featured else 'btn-ghost'
    return f'''<div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal"{border}>
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="{label_es}" data-en="{label_en}">{label_en}</p>
          <h3 class="font-display text-2xl leading-snug mb-3">{title}</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="{desc_es}" data-en="{desc_en}">{desc_en}</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">{price}</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">{dur}</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="{btn_cls} rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>'''


cards = [
    service_card(True, 'Firma de la casa', 'House signature', 'Brazilian Wax',
                 'El tratamiento más reservado en Meri’s: preciso, rápido y cuidadoso. Incluye toda la zona del bikini.',
                 'The most booked treatment at Meri’s: precise, quick and gentle. Includes the full bikini area.',
                 '$85+', '45min'),
    service_card(False, 'Depilación', 'Waxing', 'Full Body Wax',
                 'Axilas, brazos, bikini y piernas juntos desde $298 (2h), o por zona: desde $21 axilas hasta $180 brazos y piernas completos.',
                 'Underarms, arms, bikini and legs together from $298 (2h), or by area: from $21 underarms to $180 full arms and legs.',
                 '$21+', '15min+', delay=110),
    service_card(False, 'Faciales', 'Facials', 'Deep Cleansing Facial',
                 'Un facial hidratante que limpia, exfolia y nutre, terminado con una mascarilla calmante. Desde $111.',
                 'A hydrating facial that cleanses, exfoliates and nourishes, finished with a calming mask. From $111.',
                 '$111', 'Facial', delay=220),
    service_card(False, 'Masaje', 'Massage', 'Full Body Massage',
                 '60 o 90 minutos de masaje terapéutico, o la versión de lujo con piedras calientes. Desde $94.',
                 '60 or 90 minutes of therapeutic massage, or the luxury version with hot stones. From $94.',
                 '$94+', '1h+', delay=330),
]
NEW_GRID = '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">\n        ' + '\n        '.join(cards) + '\n      </div>\n      '

h = h[:m.start()] + NEW_GRID + h[m.end():]
print('OK grid servicios')

# =====================================================================
# 14) MENU COMPLETO (37 servicios, agrupado por categoria, TODO VISIBLE,
#     sin acordeon -- requisito de la puerta de calidad para menus 20+).
#     Se inserta despues del grid de 4 cards, antes de la nota final.
# =====================================================================
def row(name, price, dur=None):
    right = f'${price} · {dur}' if dur else f'${price}'
    return f'''<div class="flex items-center justify-between gap-4 py-2.5 border-b border-[color:var(--accent-ghost)] last:border-0">
              <span class="text-sm font-light text-[color:var(--ink-60)]">{name}</span>
              <span class="text-sm font-medium whitespace-nowrap">{right}</span>
            </div>'''


CATEGORIES = [
    ('Body Waxing', 'Depilación de Cuerpo', [
        ('Full Arms & Full Legs Wax', 180, '1h'),
        ('Full Legs Wax', 84, '1h 30min'),
        ('Half Legs Wax', 55, None),
        ('Full Arms Wax', 47, '35min'),
        ('Half Arms Wax', 38, '30min'),
        ('Underarm Wax', 21, None),
        ('Bikini Line', 55, None),
        ('Bikini Sugaring', 66, None),
        ('Manzilian Wax (Men’s Brazilian)', 95, '1h'),
        ('Chest Wax', 30, None),
        ('Back Wax', 55, None),
        ('Stomach Wax', 33, '30min'),
    ]),
    ('Face Waxing', 'Depilación Facial', [
        ('Full Face Wax', 55, None),
        ('Chin Wax', 13, '25min'),
        ('Eyebrow Wax', 21, None),
        ('Upper Lip Wax', 17, None),
        ('Nose Wax', 17, None),
    ]),
    ('Massage', 'Masaje', [
        ('Full Body Massage (90min)', 160, '1h 30min'),
        ('Luxury Full Body Massage + Hot Stones', 135, '1h'),
        ('Mobile Massage (IN-HOME)', 170, '2h'),
        ('Targeted Body Massage (Back & Legs)', 75, '45min'),
        ('Lower Body Massage (Legs Focus)', 66, None),
        ('Express Legs Massage', 65, '30min'),
        ('Express Back Massage', 65, '30min'),
        ('Neck & Shoulders Massage', 65, '30min'),
        ('Face Massage', 55, None),
    ]),
    ('Facials & Extras', 'Faciales y Extras', [
        ('Luxury Intimate Post-Wax Treatment', 26, '20min'),
        ('Hot Stones', 25, '15min'),
        ('Jelly Mask (Face)', 30, None),
        ('Extra 15 Minutes Massage', 25, '15min'),
        ('Aromatherapy', 10, '15min'),
        ('Paraffin Hands', 17, None),
        ('Paraffin Feet', 17, None),
    ]),
]

cat_cards = []
for title_en, title_es, items in CATEGORIES:
    rows_html = '\n            '.join(row(n, p, d) for n, p, d in items)
    cat_cards.append(f'''<div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-xl mb-4" data-es="{title_es}" data-en="{title_en}">{title_en}</h3>
          <div>
            {rows_html}
          </div>
        </div>''')

FULL_MENU = f'''<div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Menú completo" data-en="Full menu">Full menu</p>
        <h3 class="reveal text-center font-display text-2xl sm:text-3xl mb-10" data-es="Cada servicio, con su precio real" data-en="Every service, at its real price">Every service, at its real price</h3>
        <div class="grid sm:grid-cols-2 gap-5">
          {"".join(c + chr(10) + "          " for c in cat_cards)}
        </div>
      </div>
      '''

NOTE_ANCHOR = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8">'
assert NOTE_ANCHOR in h
h = h.replace(NOTE_ANCHOR, FULL_MENU + NOTE_ANCHOR, 1)

rep('<span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span>',
    '<span data-es="Precios publicados por Meri\'s Beauty Studio en Booksy. Disponibilidad y reserva en línea." data-en="Prices as published by Meri\'s Beauty Studio on Booksy. Availability and online booking through Booksy.">Prices as published by Meri\'s Beauty Studio on Booksy. Availability and online booking through Booksy.</span>')

print('OK menu completo')

# =====================================================================
# 15) PRELOADER
# =====================================================================
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">MB</span>\n    <span class="pre-word">Meri\'s Beauty Studio</span>')

# =====================================================================
# 16) GALERIA
# =====================================================================
rep('data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    'data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')

GALLERY_RE = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    re.S)
gm = GALLERY_RE.search(h)
assert gm, 'no se encontro el grid de galeria'


def tile(cls, delay, file, cap_es, cap_en, alt):
    style = f' style="transition-delay:{delay}ms"' if delay else ''
    return (f'<div class="frame zoomable {cls} img-reveal"{style}>'
            f'<span class="tile-cap" data-es="{cap_es}" data-en="{cap_en}">{cap_en}</span>'
            f'<img src="assets/raw/{file}" alt="{alt}" class="blur-up w-full h-full object-cover" loading="lazy" /></div>')


tiles = [
    tile('col-span-2 aspect-[16/9]', None, 'bk-13.jpg', 'Suite de depilación', 'Waxing suite',
         "Meri applying a leg wax to a client inside her private studio in Jacksonville, FL"),
    tile('aspect-[3/4]', 90, 'bk-12.jpg', 'Piel lista', 'Smooth results',
         "Applying a wax strip during a leg waxing treatment at Meri's Beauty Studio"),
    tile('aspect-[3/4]', 150, 'bk-7.jpg', 'Depilación precisa', 'Precision waxing',
         "Esthetician applying wax with pink gloves during a leg treatment"),
    tile('aspect-[3/4] lg:mt-10', 120, 'bk-3.jpg', 'Tratamiento en el estudio', 'In-studio treatment',
         "In-studio treatment session at Meri's Beauty Studio, Jacksonville FL"),
    tile('aspect-[3/4]', 210, 'bk-10.jpg', 'Cera fresca, siempre', 'Fresh wax, every time',
         "Dipping a wooden applicator into warm wax before a treatment"),
    tile('aspect-[3/4] lg:mt-10', 300, 'bk-5.jpg', 'Hecho con cariño', 'Made with care',
         "A heart made of wax beads, a small signature touch at Meri's Beauty Studio"),
]
NEW_GALLERY = ('<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">\n        '
               + '\n        '.join(tiles) + '\n      </div>\n    </div>\n  </section>')
h = h[:gm.start()] + NEW_GALLERY + h[gm.end():]
print('OK galeria')

# =====================================================================
# 17) OPINIONES (3 reseñas verbatim reales de Booksy)
# =====================================================================
rep('data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    'data-es="5.0 de 5 · 50 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 50 verified reviews on Booksy">5.0 out of 5 · 50 verified reviews on Booksy</span>')

rep('''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mariya is the best in Jacksonville"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Wayon C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''')

rep('''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Quick, professional and so sweet! Will definitely be back."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Brioni L.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''')

rep('''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"My skin feels like a newborn's😊. Thank you Maria! I will definitely come again!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Cliente de Booksy</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''')

rep('data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Leer las 50 reseñas en Booksy" data-en="Read all 50 reviews on Booksy">Read all 50 reviews on Booksy</a>')

# =====================================================================
# 18) UBICACION
# =====================================================================
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Jacksonville</span>')

rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(199,119,166,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">9825 San Jose Blvd, Suite 32, Jacksonville, FL 32257</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(199,119,166,0.4)]" href="https://www.google.com/maps?q=9825+San+Jose+Blvd,+Suite+32,+Jacksonville,+FL+32257" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>')

rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
    'data-es="Con cita previa vía Booksy. Lunes a viernes 3:30pm-7pm, sábado y domingo 12pm-7pm." data-en="By appointment via Booksy. Monday-Friday 3:30pm-7pm, Saturday-Sunday 12pm-7pm.">By appointment via Booksy. Monday-Friday 3:30pm-7pm, Saturday-Sunday 12pm-7pm.</p>')

rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira el trabajo más reciente y escribe por DM cualquier duda antes de tu cita." data-en="See recent work and DM any questions before your appointment.">See recent work and DM any questions before your appointment.</p>')

rep('<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Mapa: Meri\'s Beauty Studio, 9825 San Jose Blvd, Jacksonville FL"\n          src="https://www.google.com/maps?q=9825+San+Jose+Blvd,+Suite+32,+Jacksonville,+FL+32257&output=embed"')

# =====================================================================
# 19) CTA FINAL
# =====================================================================
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Tu piel, tratada con cuidado." data-en="Your skin, treated with care.">Your skin, treated with care.</p>', n=1)

rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu lugar" data-en="Your spot">Your spot</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')

rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: tu depilación, tu facial o ese masaje que llevas planeando." data-en="Book online in seconds: your wax, your facial, or that massage you have been meaning to schedule.">Book online in seconds: your wax, your facial, or that massage you have been meaning to schedule.</p>')

# =====================================================================
# 20) FOOTER
# =====================================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Meri\'s Beauty Studio</span>')

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(218,170,198,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/raw/bk-2.jpg" alt="Meri\'s Beauty Studio logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(218,170,198,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Meri\'s Beauty Studio</span>')

rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Estudio de belleza en Jacksonville, FL, especializado en depilación, masaje y skincare. Atención con cita previa." data-en="Beauty studio in Jacksonville, FL specializing in waxing, massage and skincare. By appointment only.">Beauty studio in Jacksonville, FL specializing in waxing, massage and skincare. By appointment only.</p>')

rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p>9825 San Jose Blvd, Suite 32, Jacksonville, FL 32257</p>')

rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Meri\'s Beauty Studio.</p>')

# =====================================================================
# 21) Verificacion final de leftovers obvios antes de escribir
# =====================================================================
for leftover in ['Pure Artistry', 'pure.artistrysk', '121705_pure-artistry', 'Orlando',
                  'Silk Press', 'silk press', 'K-Tip', 'knotless', 'Locs', '234']:
    assert leftover not in h, f'LEFTOVER SIN LIMPIAR: {leftover!r}'

open(SRC, 'w', encoding='utf-8').write(h)
print('OK: index.html completo escrito en', SRC)
