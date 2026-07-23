import re, os

SLUG = "ml-esthetics-pompano-beach"
PATH = f"output/{SLUG}/index.html"
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> rosewood / dusty mauve (ML Esthetics PMU)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#8a4a52"), ("#5c2140", "#4a2e28"), ("#f0bed7", "#e8b8a8"),
    ("#faf2f6", "#faf4f1"), ("#c47a9c", "#bd8089"), ("#8a5573", "#6b4038"),
    ("#f3e0ea", "#f0e0da"), ("#d9a8c2", "#d8b6a0"), ("#7d3457", "#5c332c"),
    ("#5f2c48", "#4a2c26"), ("#33222c", "#332422"), ("#fbf3f8", "#faf3ee"),
    ("#fbeff5", "#f7ece4"), ("#f8dfeb", "#ecd2c4"), ("#f6f1ea", "#f8f2ed"),
    ("#f2d5e3", "#f0ddd0"), ("#f2cfe0", "#ecd6c8"), ("#efd0e0", "#e8d2c4"),
    ("#e5c1d4", "#dcc0ac"), ("#dc9dbe", "#cf9e8e"), ("#d3a2bc", "#d0a494"),
    ("#c9789f", "#b07872"), ("#b25a85", "#96574f"), ("#2a1722", "#241714"),
    ("#1f0f18", "#1c110d"), ("#1c0f16", "#1a100c"),
]
for old, new in HEX_PALETTE:
    assert old in h, "NO HEX: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(138,74,82"),
    ("rgba(51,34,44", "rgba(51,36,34"),
    ("rgba(240,190,215", "rgba(232,184,168"),
    ("rgba(70,25,50", "rgba(58,35,30"),
    ("rgba(250,242,246", "rgba(250,244,241"),
    ("rgba(125,52,87", "rgba(92,51,44"),
    ("rgba(253,246,250", "rgba(250,243,238"),
    ("rgba(40,16,30", "rgba(36,20,15"),
    ("rgba(233,205,186", "rgba(216,182,160"),
    ("rgba(185,138,128", "rgba(176,130,118"),
]
for old, new in RGBA_PALETTE:
    assert old in h, "NO RGBA: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: booking URL, IG url, IG handle
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_BOOK = "https://booksy.com/en-us/1680270_ml-esthetics_brows-lashes_15649_pompano-beach"
assert h.count(OLD_BOOK) >= 10
h = h.replace(OLD_BOOK, NEW_BOOK)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/ml_esthetics1/"
assert h.count(OLD_IG_URL) >= 3
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@ml_esthetics1"
assert h.count(OLD_IG_HANDLE) >= 3
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>ML Esthetics · PMU &amp; Lash Studio in Pompano Beach, FL | 5.0 Rating</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="ML Esthetics, Pompano Beach FL: microblading, powder brows, lip blush, permanent eyeliner, lash lifts, brow lamination and facials with esthetician Monica Leyva. 5.0 rating, 124 reviews on Booksy. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="ML Esthetics · PMU &amp; Lash Studio in Pompano Beach, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Microblading, powder brows, lip blush, lash lifts and facials. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-15.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-15.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "ML Esthetics",
    "description": "Permanent makeup, lash and brow studio in Pompano Beach, FL run by esthetician Monica Leyva: microblading, powder brows, lip blush, permanent eyeliner, eyelash extensions, lash lifts, brow lamination, facials and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "575 S Cypress Rd", "addressLocality": "Pompano Beach", "addressRegion": "FL", "postalCode": "33060", "addressCountry": "US" },
    "telephone": "+13057206197",
    "sameAs": ["https://booksy.com/en-us/1680270_ml-esthetics_brows-lashes_15649_pompano-beach", "https://www.instagram.com/ml_esthetics1/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "124", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "21:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Permanent makeup, lash & brow services", "itemListElement": [
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Lift" } },
      { "@type": "Offer", "price": "450", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Microblading" } },
      { "@type": "Offer", "price": "450", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lip Blush" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Detoxing Facial" } },
      { "@type": "Service", "name": "Powder Brows / Microshading" },
      { "@type": "Service", "name": "Brow Lamination" }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. PRELOADER
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">ML</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">ML Esthetics</span>')
print("PRELOADER done")

# ---------------------------------------------------------------------------
# 6. NAV (logo -> text monogram, no invented photo-logo; brand name)
# ---------------------------------------------------------------------------
MONO_NAV = '<span class="w-10 h-10 rounded-full ring-1 ring-[rgba(138,74,82,0.35)] bg-[color:var(--accent-ghost)] flex items-center justify-center font-display text-sm text-[color:var(--accent-deep)]" aria-hidden="true">ML</span>'
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,74,82,0.35)]" />',
    MONO_NAV)
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">ML <span class="text-[color:var(--accent-deep)]">Esthetics</span></span>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Pompano Beach, FL · Estudio de PMU y Pestañas" data-en="Pompano Beach, FL · PMU &amp; Lash Studio">Pompano Beach, FL · PMU &amp; Lash Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Belleza que dura, hecha a tu medida." data-en="Beauty that lasts, made just for you.">Beauty that lasts, made just for you.</p>\n        <h1')
rep('''          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
    '''          <span data-es="Maquillaje permanente, pestañas" data-en="Permanent makeup, lashes">Permanent makeup, lashes</span><br /><span data-es="y cejas hechas para " data-en="and brows made to ">and brows made to </span><span class="text-shine" data-es="resaltar" data-en="stand out">stand out</span>''')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Microblading, cejas en polvo, lip blush, delineado permanente, extensiones y lifting de pestañas, laminado de cejas y faciales, todo de la mano de la esteticista Monica Leyva. Un estudio privado en Pompano Beach con clientas que regresan cita tras cita." data-en="Microblading, powder brows, lip blush, permanent eyeliner, lash extensions and lifts, brow lamination and facials, all from esthetician Monica Leyva. A private studio in Pompano Beach with clients who keep coming back appointment after appointment.">Microblading, powder brows, lip blush, permanent eyeliner, lash extensions and lifts, brow lamination and facials, all from esthetician Monica Leyva. A private studio in Pompano Beach with clients who keep coming back appointment after appointment.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 124 reseñas en Booksy" data-en="5.0 · 124 reviews on Booksy">5.0 · 124 reviews on Booksy</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-15.jpg" alt="Client smiling with finished permanent makeup and lash work at ML Esthetics" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Microblading</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$450" data-en="$450">$450</p>')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="124">124</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">PMU <span class="text-shine">&amp;</span> Lashes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cejas, labios y delineado" data-en="Brows, lips &amp; eyeliner">Brows, lips &amp; eyeliner</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">124 <span class="text-shine" data-es="reseñas" data-en="reviews">reviews</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Perfecto 5.0 en Booksy" data-en="Perfect 5.0 on Booksy">Perfect 5.0 on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Pompano Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">575 S Cypress Rd</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2 en la pagina, 4 ocurrencias por palabra)
# ---------------------------------------------------------------------------
for old, new in [
    ('Classic Set', 'Microblading'),
    ('Hybrid Set', 'Powder Brows'),
    ('Volume Set', 'Lip Blush'),
    ('Mega Volume', 'Lash Lift'),
    ('Bottom Lashes', 'Brow Lamination'),
    ('West Palm Beach, FL', 'Pompano Beach, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Monica applying microblading strokes to a client\'s brow at ML Esthetics" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Before and after microbladed eyebrows at ML Esthetics" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="una artista, tu mirada" data-en="one artist, your look">one artist, your look</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="ML Esthetics es el estudio de Monica Leyva, nacida en Miami de ascendencia cubana. Tras años trabajando en el área de la salud, hoy dedica su cuidado y precisión al maquillaje permanente, las cejas y las pestañas, diseñando cada resultado alrededor de tu rostro." data-en="ML Esthetics is the studio of Monica Leyva, born in Miami of Cuban descent. After years working in healthcare, she now brings that same care and precision to permanent makeup, brows and lashes, designing every result around your face.">ML Esthetics is the studio of Monica Leyva, born in Miami of Cuban descent. After years working in healthcare, she now brings that same care and precision to permanent makeup, brows and lashes, designing every result around your face.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 124 reseñas verificadas en Booksy, y clientas que llegan por una recomendación de Groupon y se quedan por años de microblading, lash lifts y faciales." data-en="The result: a perfect 5.0 across 124 verified reviews on Booksy, and clients who arrive through a Groupon recommendation and stay for years of microblading, lash lifts and facials.">The result: a perfect 5.0 across 124 verified reviews on Booksy, and clients who arrive through a Groupon recommendation and stay for years of microblading, lash lifts and facials.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="124">124</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
MONO_EXP = '<span class="blur-up w-10 h-10 rounded-full ring-1 ring-[rgba(138,74,82,0.3)] bg-[color:var(--accent-ghost)] flex items-center justify-center font-display text-sm text-[color:var(--accent-deep)]" aria-hidden="true">ML</span>'
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,74,82,0.3)]" loading="lazy" />',
    MONO_EXP)
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Monica Leyva · <span class="text-[color:var(--ink-40)]" data-es="Esteticista" data-en="Esthetician">Esthetician</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio claro, y confirmas tu cita al instante." data-en="Pick your service on Booksy with clear pricing, and confirm your appointment instantly.">Pick your service on Booksy with clear pricing, and confirm your appointment instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta y diseño" data-en="Consultation &amp; mapping">Consultation &amp; mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Monica evalúa la forma de tu rostro, tu piel y el efecto que buscas antes de diseñar cejas, labios o mirada." data-en="Monica evaluates your face shape, skin and the effect you want before mapping out brows, lips or eyes.">Monica evaluates your face shape, skin and the effect you want before mapping out brows, lips or eyes.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu tratamiento" data-en="Your treatment">Your treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un lash lift de 45 minutos a una sesión completa de microblading, cada procedimiento recibe su tiempo sin prisa." data-en="From a 45-minute lash lift to a full microblading session, every procedure gets its unhurried, full time.">From a 45-minute lash lift to a full microblading session, every procedure gets its unhurried, full time.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con indicaciones claras de cuidado en casa y, si tu servicio lo requiere, tu cita de retoque ya agendada." data-en="You leave with clear home-care guidance and, if your service calls for one, your touch-up appointment already booked.">You leave with clear home-care guidance and, if your service calls for one, your touch-up appointment already booked.</p>''')
print("METODO done")

open(PATH, "w", encoding="utf-8").write(h)
print("PART 1 saved,", len(h))
