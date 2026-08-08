#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2 (Pure Artistry) -> Vogue Nail Spa, Pompano Beach FL.
Metodo: templates/SKELETONS-V2.md. Datos reales: output/vogue-nail-spa-pompano-beach/data.json
(Booksy dossier, listado actualmente como 'Hidden Gem Nail Boutique' en Booksy pero el mismo
negocio: misma direccion 1 N Ocean Blvd Suite 101, mismo IG @vogue.nail.spa, misma dueña Marcela).
"""
import re

PATH = 'output/vogue-nail-spa-pompano-beach/index.html'
h = open(PATH).read()


def rep(a, b, n=1):
    global h
    assert a in h, 'ANCLA ROTA: ' + a[:120]
    if n == -1:
        h = h.replace(a, b)
    else:
        cnt = h.count(a)
        assert cnt == n, f'esperaba {n} occurrencias, hay {cnt}: ' + a[:120]
        h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop (dorado SIEMPRE, pase lo que pase con la paleta)
# ---------------------------------------------------------------------------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque .merktop-badge'
BADGE_TOKEN = '@@MERKTOP_BADGE_BLOCK@@\n'
badge_block = m.group(0)
h = h[:m.start()] + BADGE_TOKEN + h[m.end():]

# ---------------------------------------------------------------------------
# 2. Paleta: gold editorial (#d4a84b) -> rose-gold "Vogue" sobre negro
# ---------------------------------------------------------------------------
PALETTE = [
    ('#d4a84b', '#c68f76'),
    ('#b8934a', '#a5735c'),
    ('#241c0e', '#241512'),
    ('rgba(212,168,75,', 'rgba(198,143,118,'),
    ('#e8c476', '#dba98d'),
    ('#c9a04a', '#b97e63'),
    ('#96742c', '#7a4f3c'),
    ('#6b5222', '#5c3b2e'),
    ('#f0dc9e', '#eac9b5'),
    ('#9a7431', '#8a5c47'),
    ('#e5c374', '#d9a688'),
    ('rgba(122,90,30,0.28)', 'rgba(150,95,70,0.28)'),
    ('rgba(180,140,60,0.18)', 'rgba(190,120,95,0.18)'),
    ('#1c1408', '#2a1712'),
    ('#e8cf96', '#e8c3ab'),
    ('#f8eed3', '#f7e6da'),
    ('#bfa060', '#b98a72'),
    ('#f0dcae', '#edd2bd'),
    ('rgba(232,210,160,', 'rgba(232,199,181,'),
    ('rgba(232,207,150,', 'rgba(232,195,171,'),
    ('#faf1dc', '#f8e6da'),
    ('#ecd9a8', '#e8c9b3'),
    ('#c9ab6b', '#c08b6e'),
    ('#8a744a', '#8a5d47'),
    ('#0f0b07', '#110c0c'),
    ('#171207', '#1a1112'),
    ('#191307', '#1c1113'),
    ('#100c05', '#120c0d'),
    ('#0c0905', '#0e0a0a'),
]
for old, new in PALETTE:
    assert old in h, 'PALETA ANCLA ROTA: ' + old
    h = h.replace(old, new)

# Restaurar el badge dorado intacto
assert BADGE_TOKEN in h
h = h.replace(BADGE_TOKEN, badge_block, 1)

# ---------------------------------------------------------------------------
# 3. Globales: URL de Booksy, URL de IG, @handle
# ---------------------------------------------------------------------------
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/736882_vogue-nail-spa_nail-salon_15649_pompano-beach'
assert h.count(OLD_BOOKSY) == 13, h.count(OLD_BOOKSY)
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/vogue.nail.spa/'
assert h.count(OLD_IG_URL) == 6, h.count(OLD_IG_URL)
h = h.replace(OLD_IG_URL, NEW_IG_URL)

assert h.count('@pure.artistrysk') == 4, h.count('@pure.artistrysk')
h = h.replace('@pure.artistrysk', '@vogue.nail.spa')

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Vogue Nail Spa · Nail Salon in Pompano Beach, FL | Gel Manicures, Dip Powder &amp; Gel X | 5.0 on Booksy</title>'
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Vogue Nail Spa, Pompano Beach FL: gel manicures, dip powder, Gel X and spa pedicures by nail artist Marcela. 5.0 with 66 reviews on Booksy. Book online." />'
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Vogue Nail Spa · Nail Salon in Pompano Beach, FL" />'
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel manicures, dip powder, Gel X and spa pedicures. 5.0 on Booksy. Book online." />'
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-17.jpg" />'
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-4.jpg" />'
)

JSONLD_NEW = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Vogue Nail Spa",
    "description": "Private nail studio in Pompano Beach, FL: gel manicures, dip powder, Gel X and spa pedicures by nail artist Marcela.",
    "address": { "@type": "PostalAddress", "streetAddress": "1 N Ocean Blvd, Suite 101", "addressLocality": "Pompano Beach", "addressRegion": "FL", "postalCode": "33062", "addressCountry": "US" },
    "telephone": "+19544643812",
    "sameAs": ["https://booksy.com/en-us/736882_vogue-nail-spa_nail-salon_15649_pompano-beach", "https://www.instagram.com/vogue.nail.spa/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "66", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "10:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday"], "opens": "09:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure" } },
      { "@type": "Offer", "price": "58", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Dip Powder" } },
      { "@type": "Offer", "price": "62", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Gel" } },
      { "@type": "Offer", "price": "68", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Dip Powder with Tips" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel X" } },
      { "@type": "Offer", "price": "57", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Dr. Teal Express Gel Pedicure" } },
      { "@type": "Offer", "price": "64", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "VOESH Spa Gel Pedicure" } },
      { "@type": "Offer", "price": "74", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Be Natural Athletic Gel Pedicure" } },
      { "@type": "Offer", "price": "82", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Farmhouse Fresh Luxury Gel Pedicure" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Boujee Butter Gel Pedicure" } }
    ] }
  }
  </script>'''
h = re.sub(r'<script type="application/ld\+json">.*?</script>', JSONLD_NEW, h, count=1, flags=re.S)

# ---------------------------------------------------------------------------
# 5. Preloader + nav
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">VN</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Vogue Nail Spa</span>')

rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(198,143,118,0.35)]" />',
    '<img src="assets/raw/bk-4.jpg" alt="Vogue Nail Spa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(198,143,118,0.35)]" />'
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Vogue <span class="text-[color:var(--accent-deep)]">Nail Spa</span></span>'
)

# ---------------------------------------------------------------------------
# 6. HERO
# ---------------------------------------------------------------------------
rep(
    'data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Pompano Beach, FL · Salón de Uñas" data-en="Pompano Beach, FL · Nail Salon">Pompano Beach, FL · Nail Salon</p>'
)
rep(
    'data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Arte en tus uñas, una clienta a la vez." data-en="Nail artistry, one client at a time.">Nail artistry, one client at a time.</p>',
    n=2,
)
rep(
    '<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Nail art personalizado," data-en="Custom nail art,">Custom nail art,</span><br /><span data-es="geles y pedicures spa en un " data-en="gel sets and spa pedicures at a ">gel sets and spa pedicures at a </span><span class="text-shine" data-es="estudio privado" data-en="private studio">private studio</span>'
)
rep(
    'data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Vogue Nail Spa es el estudio privado de la artista de uñas Marcela en Ocean Blvd, Pompano Beach: manicure en gel, dip powder, Gel X y pedicures spa, con un 5.0 perfecto en 66 reseñas de Booksy." data-en="Vogue Nail Spa is the private studio of nail artist Marcela on Ocean Blvd in Pompano Beach: gel manicures, dip powder, Gel X and spa pedicures, with a perfect 5.0 across 66 reviews on Booksy.">Vogue Nail Spa is the private studio of nail artist Marcela on Ocean Blvd in Pompano Beach: gel manicures, dip powder, Gel X and spa pedicures, with a perfect 5.0 across 66 reviews on Booksy.</p>'
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 66 reseñas en Booksy" data-en="5.0 · 66 reviews on Booksy">5.0 · 66 reviews on Booksy</span>'
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-17.jpg" alt="Fresh nude manicure by Vogue Nail Spa, shot on Pompano Beach" class="blur-up w-full h-full object-cover" />'
)
rep(
    '<p class="font-display text-lg">Silk Press</p>',
    '<p class="font-display text-lg">Gel Manicure</p>'
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $40 · 1h" data-en="From $40 · 1h">From $40 · 1h</p>'
)

# ---------------------------------------------------------------------------
# 7. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Dip</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel Manicure · Dip Powder · Gel X" data-en="Gel Manicure · Dip Powder · Gel X">Gel Manicure · Dip Powder · Gel X</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Spa <span class="text-shine">&amp;</span> Pedis</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Pedicures de lujo" data-en="Luxury pedicures">Luxury pedicures</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Pompano Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1 N Ocean Blvd</p></div>'
)

# ---------------------------------------------------------------------------
# 8. MARQUEE (4 ocurrencias por palabra: 2 secuencias x 2 marquees)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ('Silk Press', 'Gel Manicure'),
    ('Loc Retwist', 'Dip Powder'),
    ('Knotless Braids', 'Gel X'),
    ('K-Tip Extensions', 'Spa Pedicure'),
    ('Keratin', 'Nail Art'),
    ('Orlando, FL', 'Pompano Beach, FL'),
]
for old, new in MARQUEE_WORDS:
    old_tag = f'<span class="marquee-word">{old}</span>'
    new_tag = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(old_tag)
    assert cnt == 4, f'{old_tag} -> {cnt} occurrencias'
    h = h.replace(old_tag, new_tag)

# ---------------------------------------------------------------------------
# 9. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-18.jpg" alt="Bright hot pink gel manicure by Vogue Nail Spa" class="blur-up w-full h-full object-cover" loading="lazy" />'
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-19.jpg" alt="Minimalist burgundy gel set by Vogue Nail Spa" class="blur-up w-full h-full object-cover" loading="lazy" />'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="detalle obsesivo" data-en="obsessive detail">obsessive detail</span></h2>'
)
rep(
    'data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Vogue Nail Spa es el estudio privado de la artista de uñas Marcela en 1 N Ocean Blvd, Pompano Beach: una silla, una clienta, atención completa desde un manicure en gel clásico hasta nail art pintado a mano." data-en="Vogue Nail Spa is the private studio of nail artist Marcela at 1 N Ocean Blvd in Pompano Beach: one chair, one client, full attention from a classic gel manicure to hand-painted nail art.">Vogue Nail Spa is the private studio of nail artist Marcela at 1 N Ocean Blvd in Pompano Beach: one chair, one client, full attention from a classic gel manicure to hand-painted nail art.</p>'
)
rep(
    'data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus reseñas lo dicen todo: un 5.0 perfecto en 66 reseñas verificadas de Booksy, con clientas que vuelven a la misma silla cada vez." data-en="Her reviews say it best: a perfect 5.0 across 66 verified reviews on Booksy, with clients who return for the exact same chair every time.">Her reviews say it best: a perfect 5.0 across 66 verified reviews on Booksy, with clients who return for the exact same chair every time.</p>'
)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(198,143,118,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Vogue Nail Spa, nail artist Marcela" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(198,143,118,0.3)]" loading="lazy" />'
)
rep(
    '<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Vogue Nail Spa · <span class="text-[color:var(--ink-40)]" data-es="Nail Artist Marcela" data-en="Nail Artist Marcela">Nail Artist Marcela</span></span>'
)

# ---------------------------------------------------------------------------
# 10. EL METODO
# ---------------------------------------------------------------------------
rep(
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: manicure en gel, dip powder, Gel X o un pedicure spa, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: gel manicure, dip powder, Gel X or a spa pedicure, and confirm instantly.">Pick your service on Booksy with clear price and duration: gel manicure, dip powder, Gel X or a spa pedicure, and confirm instantly.</p>'
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de uñas" data-en="Nail consult">Nail consult</h3>'
)
rep(
    'data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    'data-es="La forma y salud de tus uñas, y el diseño que buscas, definen el plan: desde un set natural limpio hasta nail art pintado a mano." data-en="Your nail shape, health and the design you want set the plan, from a clean natural set to hand-painted art.">Your nail shape, health and the design you want set the plan, from a clean natural set to hand-painted art.</p>'
)
rep(
    'data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    'data-es="Desde un manicure en gel de 1 hora hasta un ritual completo de pedicure spa: cada cita recibe su tiempo completo, sin citas dobles ni apuros." data-en="From a 1-hour gel manicure to a full spa pedicure ritual: every appointment gets its full dedicated time, no double booking, no rushing.">From a 1-hour gel manicure to a full spa pedicure ritual: every appointment gets its full dedicated time, no double booking, no rushing.</p>'
)
rep(
    'data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    'data-es="Sales con un acabado en gel impecable que aguanta el sol de Florida, más las indicaciones para cuidarlo. Tu próxima cita queda agendada antes de irte." data-en="You leave with a flawless gel finish that holds up in the Florida sun, plus the care tips to make it last. Your next appointment is booked before you go.">You leave with a flawless gel finish that holds up in the Florida sun, plus the care tips to make it last. Your next appointment is booked before you go.</p>'
)

# ---------------------------------------------------------------------------
# 11. SERVICIOS: subtitulo + grid completa (4 destacados + menu completo, SIN acordeon)
# ---------------------------------------------------------------------------
rep(
    'data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Vogue Nail Spa en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Vogue Nail Spa on Booksy. Booking confirms instantly.">Prices and durations as published by Vogue Nail Spa on Booksy. Booking confirms instantly.</p>'
)

SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(198,143,118,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="La mas reservada" data-en="House favorite">House favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure en Gel" data-en="Gel Manicure">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Color en gel de larga duración sobre uña natural, limado y acabado a mano. El servicio mas reservado de Vogue Nail Spa en Booksy." data-en="Long-lasting gel color on natural nails, shaped and finished by hand. The most-booked service on Vogue Nail Spa's Booksy.">Long-lasting gel color on natural nails, shaped and finished by hand. The most-booked service on Vogue Nail Spa's Booksy.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/736882_vogue-nail-spa_nail-salon_15649_pompano-beach" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Esculpido" data-en="Sculpted">Sculpted</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel X</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set esculpido de extensión construido directo sobre la uña, sin tips pegados, para largo y forma que duran." data-en="Full sculpted extension set built directly on the nail, no glue-on tips needed, for length and shape that lasts.">Full sculpted extension set built directly on the nail, no glue-on tips needed, for length and shape that lasts.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p></div>
            <a href="https://booksy.com/en-us/736882_vogue-nail-spa_nail-salon_15649_pompano-beach" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Dip Powder" data-en="Dip Powder">Dip Powder</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Dip Powder con Tips" data-en="Dip Powder with Tips">Dip Powder with Tips</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Color en dip powder sobre tips de extensión para un acabado duradero y resistente que mantiene la forma por semanas." data-en="Dip powder color over extension tips for a durable, chip-resistant finish that holds shape for weeks.">Dip powder color over extension tips for a durable, chip-resistant finish that holds shape for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$68+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/736882_vogue-nail-spa_nail-salon_15649_pompano-beach" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicure Spa" data-en="Spa Pedicure">Spa Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Boujee Butter Gel Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El ritual de pedicure de mayor nivel: remojo, exfoliación, mascarilla y acabado en gel para un reset completo." data-en="The top-tier pedicure ritual: soak, scrub, mask and a gel polish finish for a full spa reset.">The top-tier pedicure ritual: soak, scrub, mask and a gel polish finish for a full spa reset.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p></div>
            <a href="https://booksy.com/en-us/736882_vogue-nail-spa_nail-salon_15649_pompano-beach" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>

      <div class="grid sm:grid-cols-2 gap-5 mt-8">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Menú completo · Manicures" data-en="Full menu · Manicures">Full menu · Manicures</p>
          <div class="space-y-3 text-sm">
            <div class="flex items-baseline justify-between gap-3"><span data-es="Manicure en Gel" data-en="Gel Manicure">Gel Manicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$40 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span>Dip Powder</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$58 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span data-es="Builder Gel" data-en="Builder Gel">Builder Gel</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$62 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span data-es="Dip Powder con Tips" data-en="Dip Powder with Tips">Dip Powder with Tips</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$68 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span>Gel X</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$90</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:90ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Menú completo · Pedicures" data-en="Full menu · Pedicures">Full menu · Pedicures</p>
          <div class="space-y-3 text-sm">
            <div class="flex items-baseline justify-between gap-3"><span>Dr. Teal Express Gel Pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$57 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span>VOESH Spa Gel Pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$64 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span>Be Natural Athletic Gel Pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$74 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span>Farmhouse Fresh Luxury Gel Pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$82 · 1h</span></div>
            <div class="flex items-baseline justify-between gap-3"><span>Boujee Butter Gel Pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$90</span></div>
          </div>
        </div>
      </div>
      </div>
      <div style="display:none">'''
# El regex de abajo consume hasta justo antes del <p class="reveal text-center...">,
# asi que cerramos manualmente los divs que el regex se come y abrimos uno vacio
# invisible para que el reemplazo quede balanceado sin alterar el resto del layout.
services_pattern = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    flags=re.S
)
assert len(services_pattern.findall(h)) == 1, 'regex de servicios no matchea 1 vez'
h = services_pattern.sub(SERVICES_GRID, h, count=1)

rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 10 servicios de arriba son el menú completo, con el precio exacto de Booksy. El nail art y los add-ons se cotizan en tu cita." data-en="All 10 services above are the full menu, priced exactly as on Booksy. Nail art and add-ons are quoted at your appointment.">All 10 services above are the full menu, priced exactly as on Booksy. Nail art and add-ons are quoted at your appointment.</span></p>'
)

# ---------------------------------------------------------------------------
# 12. GALERIA
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nails">nails</span></h2>'
)

GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Elegancia diaria" data-en="Everyday elegance">Everyday elegance</span><img src="assets/raw/bk-20.jpg" alt="Manicure nude brillante sobre encimera de granito" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Stiletto cromado" data-en="Chrome stiletto">Chrome stiletto</span><img src="assets/raw/bk-5.jpg" alt="Uñas stiletto en cromo azul y verde holográfico" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Arte a mano" data-en="Hand-painted art">Hand-painted art</span><img src="assets/raw/bk-21.jpg" alt="Nail art de tortuga marina, estrella y flor pintado a mano" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Color a medida" data-en="Custom color work">Custom color work</span><img src="assets/raw/bk-22.jpg" alt="Diseño de uñas con remolinos de color neón" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Rojo clásico" data-en="Classic red">Classic red</span><img src="assets/raw/bk-3.jpg" alt="Manicure clásico en rojo brillante" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Francés moderno" data-en="Modern french">Modern french</span><img src="assets/raw/bk-23.jpg" alt="Manicure francés moderno en forma almendrada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
gallery_pattern = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    flags=re.S
)
assert len(gallery_pattern.findall(h)) == 1, 'regex de galeria no matchea 1 vez'
h = gallery_pattern.sub(GALLERY_GRID, h, count=1)

# ---------------------------------------------------------------------------
# 13. OPINIONES (quotes reales, verbatim, del dossier de Booksy)
# ---------------------------------------------------------------------------
rep(
    'data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    'data-es="5.0 de 5 · 66 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 66 verified reviews on Booksy">5.0 out of 5 · 66 verified reviews on Booksy</span>'
)
rep(
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
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
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Marcela is the absolute best!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Leigh Anne C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I love my nails! They are beautiful and works of art."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Claire S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Marcela ALWAYS does an amazing job on my nails I won't go anywhere else!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Amber W.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>'''
)
rep(
    'data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Leer las 66 reseñas en Booksy" data-en="Read all 66 reviews on Booksy">Read all 66 reviews on Booksy</a>'
)

# ---------------------------------------------------------------------------
# 14. UBICACION
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Pompano Beach</span></h2>'
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(198,143,118,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1 N Ocean Blvd, Suite 101, Pompano Beach, FL 33062</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(198,143,118,0.4)]" href="https://www.google.com/maps?q=1+N+Ocean+Blvd,+Suite+101,+Pompano+Beach,+FL+33062" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(
    '<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Mapa: Vogue Nail Spa, 1 N Ocean Blvd, Pompano Beach FL"\n          src="https://www.google.com/maps?q=1+N+Ocean+Blvd,+Suite+101,+Pompano+Beach,+FL+33062&output=embed"'
)

# ---------------------------------------------------------------------------
# 15. CTA FINAL
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>'
)
rep(
    'data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: tu manicure en gel, ese set de Gel X que quieres, o un pedicure spa completo." data-en="Book online in seconds: your gel manicure, that Gel X set you have been wanting, or a full spa pedicure.">Book online in seconds: your gel manicure, that Gel X set you have been wanting, or a full spa pedicure.</p>'
)

# ---------------------------------------------------------------------------
# 16. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Vogue Nail Spa</span>')
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,195,171,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Vogue Nail Spa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,195,171,0.35)]" loading="lazy" />'
)
rep(
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Vogue Nail Spa</span>'
)
rep(
    'data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Estudio privado de uñas en Pompano Beach, FL. Solo con cita previa." data-en="Private nail studio in Pompano Beach, FL. By appointment only.">Private nail studio in Pompano Beach, FL. By appointment only.</p>'
)
rep(
    '<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p>1 N Ocean Blvd, Suite 101, Pompano Beach, FL 33062</p>'
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Vogue Nail Spa.</p>')

# ---------------------------------------------------------------------------
# 17. Aria-labels genericos con nombre de marca vieja (si quedara alguno)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 18. Blanket seguro: "234" -> "66" en cualquier resto textual (no toca IDs de URL)
# ---------------------------------------------------------------------------
assert '234' in h
h = h.replace('234', '66')

open(PATH, 'w').write(h)
print('OK:', PATH, len(h), 'bytes')
