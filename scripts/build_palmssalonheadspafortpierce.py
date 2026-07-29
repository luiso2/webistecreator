#!/usr/bin/env python3
"""Deriva output/palms-salon-head-spa-fort-pierce/index.html desde templates/dark-v2/index.html
(esqueleto congelado = pureartistry) via transformacion anclada (assert-then-replace).
Metodo: templates/SKELETONS-V2.md
"""
import re

SLUG = 'palms-salon-head-spa-fort-pierce'
PATH = f'output/{SLUG}/index.html'

h = open(PATH, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert h.count(a) >= n, f'NO encontrado (necesita >= {n}, tiene {h.count(a)}): {a[:120]!r}'
    h = h.replace(a, b, n)


def rep_all(a, b, min_count=1):
    global h
    c = h.count(a)
    assert c >= min_count, f'NO encontrado (necesita >= {min_count}): {a[:120]!r}'
    h = h.replace(a, b)


# ---------------------------------------------------------------------------
# 1) Proteger el badge Merktop (bloque CSS .merktop-badge ... @keyframes mkPulse)
# ---------------------------------------------------------------------------
m = re.search(r'    \.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque merktop-badge'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ---------------------------------------------------------------------------
# 2) Paleta: "black jungle canopy + antique gold" (bg oscuro real del local,
#    accent-deep = verde palma profundo tomado del papel tapiz de hojas real,
#    accent-mid = dorado antiguo tomado del logo real). Distinta de:
#    coral fairy #c04e62, caramelo #a86a2e, esmeralda #2f7d5a, teal acero #4fb8b8,
#    violeta dark #b18ae8, rosa dark, gold dark original (#d4a84b/#b8934a, el
#    propio esqueleto pureartistry).
# ---------------------------------------------------------------------------
pairs = [
    # bg / bg-2 / accent-soft (near-black warm, ligero ajuste)
    ('#0f0b07', '#120f0c'),
    ('#171207', '#191510'),
    ('#241c0e', '#1e2418'),
    # accent-deep (verde palma) y accent-mid (dorado) -- roles intercambiados
    # respecto al esqueleto para que el verde domine visualmente (shine/botones)
    ('#d4a84b', '#4a6b42'),
    ('#b8934a', '#c9973f'),
    ('rgba(212,168,75,', 'rgba(74,107,66,'),
    # shimmer / step-num stops
    ('#f0dc9e', '#9dbf8e'),
    ('#9a7431', '#2d4328'),
    ('#e5c374', '#7fa66f'),
    # btn-3d / book-float gradient (verde)
    ('#e8c476', '#86ad78'),
    ('#c9a04a', '#4a6b42'),
    ('#96742c', '#2e4128'),
    ('#6b5222', '#263a22'),
    ('#1c1408', '#10190d'),
    ('rgba(80,58,18,', 'rgba(40,58,36,'),
    ('rgba(54,42,38,0.14)', 'rgba(42,54,38,0.14)'),
    # orbs hero (variedad verde + dorado)
    ('rgba(122,90,30,0.28)', 'rgba(168,122,45,0.28)'),
    ('rgba(180,140,60,0.18)', 'rgba(190,150,80,0.18)'),
    # dark-band (CTA final + footer): variantes claras en verde salvia
    ('#e8cf96', '#cfe0bd'),
    ('#f8eed3', '#eef5e6'),
    ('#bfa060', '#7c9c6f'),
    ('#f0dcae', '#d8e6c9'),
    ('#faf1dc', '#eef3e6'),
    ('#ecd9a8', '#cfe0bd'),
    ('#c9ab6b', '#8fa77e'),
    ('#e9c3ab', '#b9cf9e'),
    ('#8a744a', '#4a5c3f'),
    ('rgba(232,207,150,', 'rgba(207,224,189,'),
    ('rgba(185,138,128,0.14)', 'rgba(150,158,110,0.14)'),
    ('rgba(110,85,35,', 'rgba(70,86,55,'),
    ('rgba(232,210,160,0.16)', 'rgba(180,204,166,0.16)'),
    # near-black bg de secciones CTA/footer (ajuste leve)
    ('#191307', '#171a13'),
    ('#100c05', '#0e100b'),
    ('#0c0905', '#0e100b'),
]
for a, b in pairs:
    rep_all(a, b)

h = h.replace('@@BADGE@@', badge_block)

# ---------------------------------------------------------------------------
# 3) Globales: URL de booking (Comb), URL de IG, @handle
# ---------------------------------------------------------------------------
OLD_BOOK = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOK = 'https://palmssalonspa.comb.works/booking'
rep_all(OLD_BOOK, NEW_BOOK)

OLD_IG = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG = 'https://www.instagram.com/palmssalonandheadspa/'
rep_all(OLD_IG, NEW_IG)

rep_all('@pure.artistrysk', '@palmssalonandheadspa')

# ---------------------------------------------------------------------------
# 4) HEAD: title, meta, og:*, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Palms Salon &amp; Head Spa · Head Spa &amp; Hair Studio in Fort Pierce, FL | Balayage &amp; Blonde Specialists</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Palms Salon &amp; Head Spa, Fort Pierce FL: head spa scalp treatments, custom balayage, blonde specialists and hand-tied extensions. Rated 5.0 from 23 Google reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Palms Salon &amp; Head Spa · Head Spa &amp; Hair Studio in Fort Pierce, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Head spa treatments, custom balayage and hand-tied extensions. 5.0 rating on Google, 23 reviews. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />', '<meta property="og:image" content="assets/hero-balayage.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">\n.*?\n  </script>', h, flags=re.S)
assert old_jsonld, 'no se encontro JSON-LD'
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Palms Salon & Head Spa",
    "description": "Head spa and hair studio in Fort Pierce, FL: scalp treatments, custom balayage and blonding, and hand-tied extensions, in a private one-on-one suite.",
    "address": { "@type": "PostalAddress", "streetAddress": "5105 Feather Creek Dr", "addressLocality": "Fort Pierce", "addressRegion": "FL", "postalCode": "34951", "addressCountry": "US" },
    "telephone": "+17725590805",
    "sameAs": ["https://palmssalonspa.comb.works/", "https://www.instagram.com/palmssalonandheadspa/", "https://www.facebook.com/Palms.Salon.Suite/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "23", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday"], "opens": "10:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "10:00", "closes": "16:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "10:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Head spa and hair services", "itemListElement": [
      { "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luxury Head Spa Treatment" } },
      { "@type": "Offer", "price": "115", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic Head Spa" } },
      { "@type": "Offer", "price": "395", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Custom Color" } },
      { "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Extensions - Installation" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld.group(0), new_jsonld, 1)

# ---------------------------------------------------------------------------
# 5) Idioma: negocio en ingles -> mismo default que el esqueleto (EN). No hay
#    que tocar <html lang> ni applyLang default.
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h

# ---------------------------------------------------------------------------
# 6) NAV (desktop + mobile): quitar el link a #opiniones (sin reviews reales
#    con nombre verificables, ver data.json > reviews_note), resto igual.
# ---------------------------------------------------------------------------
rep(
    '<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>\n',
    '',
)
rep(
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>\n',
    '',
)

# Logo del nav + avatar experiencia + footer -> assets/logo.jpg (logo real dorado)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,107,66,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Palms Salon &amp; Head Spa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,107,66,0.35)]" />',
)
rep(
    'Pure <span class="text-[color:var(--accent-deep)]">Artistry</span>',
    'Palms <span class="text-[color:var(--accent-deep)]">Salon</span>',
)

# ---------------------------------------------------------------------------
# 7) HERO
# ---------------------------------------------------------------------------
rep(
    'data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Fort Pierce, FL · Head Spa" data-en="Fort Pierce, FL · Head Spa">Fort Pierce, FL · Head Spa</p>',
)
rep(
    'data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Revive tus raíces, rejuvenece tu cuero cabelludo." data-en="Revive your roots, rejuvenate your scalp.">Revive your roots, rejuvenate your scalp.</p>',
    n=2,
)
rep(
    '<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Rituales de head spa," data-en="Head spa rituals,">Head spa rituals,</span><br /><span data-es="con color de " data-en="styled with ">styled with </span><span class="text-shine" data-es="lujo" data-en="luxury color">luxury color</span>',
)
rep(
    'data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Un estudio dedicado a head spa y color en Fort Pierce: tratamientos de limpieza profunda para el cuero cabelludo, balayage y rubios a medida, y extensiones hand-tied, todo en una suite privada. Calificación 5.0 con 23 reseñas en Google." data-en="A dedicated head spa and color studio in Fort Pierce: deep-cleansing scalp treatments, custom balayage and blonding, and hand-tied extensions, all in a private, stylish suite. Rated 5.0 from 23 Google reviews.">A dedicated head spa and color studio in Fort Pierce: deep-cleansing scalp treatments, custom balayage and blonding, and hand-tied extensions, all in a private, stylish suite. Rated 5.0 from 23 Google reviews.</p>',
)
rep(
    'data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 23 reseñas en Google" data-en="5.0 · 23 reviews on Google">5.0 · 23 reviews on Google</span>',
)
rep(
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar cita" data-en="Book now">Book now</span>',
    n=1,
)
rep(
    f'<a href="{NEW_IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">',
    f'<a href="{NEW_IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">',
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-balayage.jpg" alt="Real balayage and blonde result at Palms Salon &amp; Head Spa, Fort Pierce" class="blur-up w-full h-full object-cover" />',
)
rep(
    'data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Silk Press</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Luxury Head Spa</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $150 · 1h 30min" data-en="From $150 · 1h 30min">From $150 · 1h 30min</p>',
)

# ---------------------------------------------------------------------------
# 8) STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="23">23</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Head <span class="text-shine">Spa</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="De clásico a lujo" data-en="Classic to Luxury rituals">Classic to Luxury rituals</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Blonde <span class="text-shine">&amp;</span> Balayage</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Especialistas en color" data-en="Custom color specialists">Custom color specialists</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Fort Pierce</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">5105 Feather Creek Dr</p></div>')

# ---------------------------------------------------------------------------
# 9) MARQUEE (2 bloques, 4 repeticiones de cada palabra)
# ---------------------------------------------------------------------------
marquee_words = [
    ('Silk Press', 'Head Spa'),
    ('Loc Retwist', 'Scalp Treatments'),
    ('Knotless Braids', 'Blonde &amp; Balayage'),
    ('K-Tip Extensions', 'Hand-Tied Extensions'),
    ('Keratin', 'Keratin'),
    ('Orlando, FL', 'Fort Pierce, FL'),
]
for old_w, new_w in marquee_words:
    old_span = f'<span class="marquee-word">{old_w}</span>'
    cnt = h.count(old_span)
    assert cnt == 4, f'{old_w!r} deberia aparecer 4 veces, aparece {cnt}'
    h = h.replace(old_span, f'<span class="marquee-word">{new_w}</span>')

# ---------------------------------------------------------------------------
# 10) LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-interior-1.jpg" alt="Interior of Palms Salon &amp; Head Spa: backwash station with tropical wallpaper and neon sign" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-interior-2.jpg" alt="Styling chair and mirror at Palms Salon &amp; Head Spa" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="total hair care" data-en="total hair care">total hair care</span></h2>',
)
rep(
    'data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Palms Salon &amp; Head Spa es una suite privada y elegante en Fort Pierce construida alrededor del cuidado capilar total, el balayage y el diseño. Además de los servicios de salón tradicionales, la experiencia de head spa aporta un toque relajante y restaurador que cuida el cuero cabelludo mientras el color y el corte hacen el resto." data-en="Palms Salon &amp; Head Spa is a stylish, welcoming suite in Fort Pierce built around total hair care, balayage and design. Beyond traditional salon services, the head spa experience brings a relaxing, restorative touch that cares for the scalp while the color and cut do the rest.">Palms Salon &amp; Head Spa is a stylish, welcoming suite in Fort Pierce built around total hair care, balayage and design. Beyond traditional salon services, the head spa experience brings a relaxing, restorative touch that cares for the scalp while the color and cut do the rest.</p>',
)
rep(
    'data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="De un tratamiento de head spa clásico a un balayage completo a medida: cada cita es uno-a-uno, sin prisas, y termina con las indicaciones para cuidar tu color y tu cuero cabelludo en casa." data-en="From a classic head spa treatment to a full custom balayage, every visit is one-on-one, unhurried, and finished with the guidance to keep your color and scalp healthy at home.">From a classic head spa treatment to a full custom balayage, every visit is one-on-one, unhurried, and finished with the guidance to keep your color and scalp healthy at home.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="23">23</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Suite privada" data-en="Private suite">Private suite</p></div>',
)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,107,66,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo.jpg" alt="Palms Salon &amp; Head Spa logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,107,66,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Palms Salon &amp; Head Spa · <span class="text-[color:var(--ink-40)]" data-es="Especialistas en rubio" data-en="Blonde Specialists">Blonde Specialists</span></span>',
)

# ---------------------------------------------------------------------------
# 11) EL METODO (4 pasos)
# ---------------------------------------------------------------------------
rep(
    'data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    'data-es="Así es tu cita" data-en="How your visit">How your visit</span> <span class="text-shine" data-es="funciona" data-en="works">works</span>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en nuestra página de reservas con precio y duración claros: head spa, color o corte, y confirmas al instante." data-en="Choose your service on our booking page: head spa, color or a haircut, with price and duration shown up front, and confirm instantly.">Choose your service on our booking page: head spa, color or a haircut, with price and duration shown up front, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de cuero cabelludo" data-en="Scalp &amp; hair consult">Scalp &amp; hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Miramos primero tu cuero cabelludo y tu cabello: qué necesita limpieza, equilibrio o un impulso define el tratamiento o la técnica de color." data-en="We look at your scalp and hair health first: what needs cleansing, balancing or reviving guides the treatment or color technique.">We look at your scalp and hair health first: what needs cleansing, balancing or reviving guides the treatment or color technique.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="El ritual" data-en="The ritual">The ritual</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un Lite Head Spa de 40 minutos a un color a medida de 4 horas: cada cita recibe su tiempo completo en una suite privada, uno-a-uno." data-en="From a 40-minute Lite Head Spa to a 4-hour custom color, every appointment gets its full dedicated time in a private, one-on-one suite.">From a 40-minute Lite Head Spa to a 4-hour custom color, every appointment gets its full dedicated time in a private, one-on-one suite.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con las indicaciones para cuidar tu color y tu cuero cabelludo en casa, y tu próxima cita agendada antes de irte." data-en="You leave with scalp and color care instructions to keep results fresh at home, and your next visit booked before you go.">You leave with scalp and color care instructions to keep results fresh at home, and your next visit booked before you go.</p>',
)

# ---------------------------------------------------------------------------
# 12) SERVICIOS: titulo/subtitulo + grid de 4 cards reemplazado entero (real:
#     17 servicios de https://palmssalonspa.comb.works/services, agrupados)
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Palms Salon &amp; Head Spa. Reserva con confirmación inmediata." data-en="Prices and durations as published by Palms Salon &amp; Head Spa. Booking confirms instantly.">Prices and durations as published by Palms Salon &amp; Head Spa. Booking confirms instantly.</p>',
)

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
assert services_grid_re.search(h), 'no se encontro el grid de servicios'
BOOK = NEW_BOOK
new_services_grid = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(74,107,66,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luxury Head Spa" data-en="Luxury Head Spa">Luxury Head Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Analisis de cuero cabelludo, limpieza profunda, masaje y mascarilla de calor para ojos, cuello, brazos y manos, mas masaje facial con varita fria. Desde $150, 1h 30min dedicados." data-en="Scalp analysis, deep cleansing, massage and a heated eye, neck, arm and hand treatment, plus a cooling facial wand massage. From $150, a dedicated 1h 30min.">Scalp analysis, deep cleansing, massage and a heated eye, neck, arm and hand treatment, plus a cooling facial wand massage. From $150, a dedicated 1h 30min.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$150+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Head Spa" data-en="Head Spa">Head Spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Classic, Lite &amp; Bond Repair" data-en="Classic, Lite &amp; Bond Repair">Classic, Lite &amp; Bond Repair</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Lite Head Spa desde $100 (40min), Classic Head Spa $115 (55min), Bond Repair desde $120 (55min) y Balancing Head Spa desde $120 (1h): limpieza, exfoliacion y masaje de cuero cabelludo." data-en="Lite Head Spa from $100 (40min), Classic Head Spa $115 (55min), Bond Repair from $120 (55min) and Balancing Head Spa from $120 (1h): cleansing, exfoliation and scalp massage.">Lite Head Spa from $100 (40min), Classic Head Spa $115 (55min), Bond Repair from $120 (55min) and Balancing Head Spa from $120 (1h): cleansing, exfoliation and scalp massage.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min+</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Color" data-en="Color">Color</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Custom Color &amp; Balayage" data-en="Custom Color &amp; Balayage">Custom Color &amp; Balayage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Mini Custom Color $200 (2h), Partial Custom Color desde $295 (3h) y Full Custom Color desde $395 (4h). Consulta de color gratuita antes de agendar." data-en="Mini Custom Color $200 (2h), Partial Custom Color from $295 (3h) and Full Custom Color from $395 (4h). Free color consultation before you book.">Mini Custom Color $200 (2h), Partial Custom Color from $295 (3h) and Full Custom Color from $395 (4h). Free color consultation before you book.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$200+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h+</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Corte y extensiones" data-en="Cuts &amp; Extensions">Cuts &amp; Extensions</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Haircuts &amp; Extensions" data-en="Haircuts &amp; Extensions">Haircuts &amp; Extensions</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Haircut $50 (30min), haircut y blowdry desde $75 (1h), Keratin Treatment desde $250 (2h) y Extensions Installation desde $150 (1h 30min)." data-en="Haircut $50 (30min), haircut and blowdry from $75 (1h), Keratin Treatment from $250 (2h) and Extensions Installation from $150 (1h 30min).">Haircut $50 (30min), haircut and blowdry from $75 (1h), Keratin Treatment from $250 (2h) and Extensions Installation from $150 (1h 30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min+</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = services_grid_re.sub(new_services_grid, h, count=1)

rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: Toner/Glaze $50 (30min), bang trim $15, curl/style $35 y consultas gratuitas de color y extensiones. Menú completo y disponibilidad en el enlace de reservas." data-en="Also: Toner/Glaze $50 (30min), bang trim $15, curl/style $35, and free color and extension consultations. Full menu and live availability on our booking page.">Also: Toner/Glaze $50 (30min), bang trim $15, curl/style $35, and free color and extension consultations. Full menu and live availability on our booking page.</span></p>',
)

# ---------------------------------------------------------------------------
# 13) GALERIA: titulo + grid de 6 tiles reemplazado con fotos reales de IG
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="El" data-en="The">The</span> <span class="text-shine" data-es="estudio" data-en="studio &amp; results">studio &amp; results</span></h2>',
)

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
assert gallery_grid_re.search(h), 'no se encontro el grid de galeria'
new_gallery_grid = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="La suite" data-en="The suite">The suite</span><img src="assets/gallery-station-wide.jpg" alt="Backwash station with tropical wallpaper, neon sign and gold logo at Palms Salon &amp; Head Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Ritual de head spa" data-en="Head spa ritual">Head spa ritual</span><img src="assets/gallery-headspa-treatment.jpg" alt="Head spa scalp treatment in progress at Palms Salon &amp; Head Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Terminado con bata Palms" data-en="Finished in a Palms robe">Finished in a Palms robe</span><img src="assets/gallery-palm-robe.jpg" alt="Client with finished blonde hair wearing a Palms Salon robe" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Balayage rubio con ondas" data-en="Wavy blonde balayage">Wavy blonde balayage</span><img src="assets/gallery-wavy-blonde.jpg" alt="Long wavy blonde balayage result" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Rubio con estilo" data-en="Glam blonde">Glam blonde</span><img src="assets/gallery-glam-blonde.jpg" alt="Glam blonde hair result at Palms Salon &amp; Head Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Estacion del espejo" data-en="Mirror station">Mirror station</span><img src="assets/gallery-mirror-station.jpg" alt="Arch mirror and styling chair at Palms Salon &amp; Head Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = gallery_grid_re.sub(new_gallery_grid, h, count=1)

# ---------------------------------------------------------------------------
# 14) OPINIONES: eliminar la seccion completa (sin quotes reales con nombre
#     verificables tras busqueda exhaustiva, ver data.json > reviews_note).
#     Renumerar Ubicacion de 06 -> 05.
# ---------------------------------------------------------------------------
opiniones_re = re.compile(r'\n  <!-- OPINIONES -->\n  <section id="opiniones".*?</section>\n', re.S)
assert opiniones_re.search(h), 'no se encontro la seccion opiniones'
h = opiniones_re.sub('\n', h, count=1)
rep('<span class="sec-num" aria-hidden="true">06</span>', '<span class="sec-num" aria-hidden="true">05</span>')

# ---------------------------------------------------------------------------
# 15) UBICACION
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Fort Pierce</span></h2>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,107,66,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">5105 Feather Creek Dr, Fort Pierce, FL 34951</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,107,66,0.4)]" href="https://www.google.com/maps?q=5105+Feather+Creek+Dr,+Fort+Pierce,+FL+34951" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>',
)
rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,107,66,0.4)]" href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    'data-es="Con cita previa en nuestra página de reservas: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via our online booking page: pick the service, day and time, and the confirmation is instant.">By appointment via our online booking page: pick the service, day and time, and the confirmation is instant.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,107,66,0.4)]" href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" data-es="Reservar cita" data-en="Book now">Book now</a>',
)
rep(
    'data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira transformaciones reales y escribe por DM cualquier duda antes de tu cita." data-en="See real transformations and DM any questions before your visit.">See real transformations and DM any questions before your visit.</p>',
)
rep(
    '<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Map: Palms Salon &amp; Head Spa, 5105 Feather Creek Dr, Fort Pierce FL"\n          src="https://www.google.com/maps?q=5105+Feather+Creek+Dr,+Fort+Pierce,+FL+34951&output=embed"',
)

# ---------------------------------------------------------------------------
# 16) CTA FINAL
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo" data-en="Your next">Your next</span> <span class="text-shine" data-es="head spa" data-en="head spa">head spa</span> <span data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: un tratamiento de head spa, un balayage nuevo o ese corte que llevas posponiendo." data-en="Book online in seconds: a head spa treatment, a fresh balayage, or the cut you have been putting off.">Book online in seconds: a head spa treatment, a fresh balayage, or the cut you have been putting off.</p>',
)
rep(
    '<a href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar cita" data-en="Book now">Book now</a>',
)

# ---------------------------------------------------------------------------
# 17) FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Palms Salon</span>')
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(207,224,189,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/logo.jpg" alt="Palms Salon &amp; Head Spa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(207,224,189,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Palms Salon</span>',
)
rep(
    'data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Head spa y estudio de cabello en Fort Pierce, FL. Atención con cita previa." data-en="Head spa and hair studio in Fort Pierce, FL. By appointment only.">Head spa and hair studio in Fort Pierce, FL. By appointment only.</p>',
)
rep(
    '<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n        <p><a href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p>5105 Feather Creek Dr, Fort Pierce, FL 34951</p>\n        <p><a href="tel:+17725590805" class="hover:text-[#b9cf9e]">(772) 559-0805</a></p>\n        <p><a href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]" data-es="Reservas online" data-en="Online booking">Online booking</a></p>',
)
rep(
    '<p><a href="https://www.instagram.com/palmssalonandheadspa/" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]">Instagram · @palmssalonandheadspa</a></p>',
    '<p><a href="https://www.instagram.com/palmssalonandheadspa/" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]">Instagram · @palmssalonandheadspa</a></p>\n        <p><a href="https://www.facebook.com/Palms.Salon.Suite/" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]">Facebook · Palm&#8217;s Salon and Head Spa</a></p>',
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Palms Salon &amp; Head Spa.</p>')

# ---------------------------------------------------------------------------
# 18) Boton flotante + preloader
# ---------------------------------------------------------------------------
rep('<a href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">', '<a href="https://palmssalonspa.comb.works/booking" target="_blank" rel="noopener" class="book-float" aria-label="Book an appointment online">')
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">PS</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Palms Salon &amp; Head Spa</span>')

print('OK build completo, escribiendo index.html final...')
open(PATH, 'w', encoding='utf-8').write(h)
