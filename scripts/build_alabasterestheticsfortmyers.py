import re, os

SLUG = "alabaster-esthetics-fort-myers"
PATH = f"output/{SLUG}/index.html"
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> alabaster cream / dusty terracotta-rose
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#9c5a4f"), ("#5c2140", "#5a352a"), ("#f0bed7", "#e8cdb0"),
    ("#faf2f6", "#f8f2ec"), ("#c47a9c", "#c08d7d"), ("#8a5573", "#8a6a52"),
    ("#f3e0ea", "#ecdcd0"), ("#d9a8c2", "#d9bcae"), ("#7d3457", "#7a4a3d"),
    ("#5f2c48", "#5a3327"), ("#33222c", "#33261f"), ("#fbf3f8", "#faf3ec"),
    ("#fbeff5", "#f7ede2"), ("#f8dfeb", "#f2e6d5"), ("#f6f1ea", "#f8f2ec"),
    ("#f2d5e3", "#ecdcd0"), ("#f2cfe0", "#ecdcc4"), ("#efd0e0", "#ecdfd2"),
    ("#e5c1d4", "#e8d5c8"), ("#dc9dbe", "#d3a68e"), ("#d3a2bc", "#d3b39e"),
    ("#c9789f", "#b9705f"), ("#b25a85", "#a8705f"), ("#2a1722", "#241a15"),
    ("#1f0f18", "#1b100c"), ("#1c0f16", "#1a100b"),
]
for old, new in HEX_PALETTE:
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(156,90,79"),
    ("rgba(51,34,44", "rgba(51,38,31"),
    ("rgba(240,190,215", "rgba(232,205,176"),
    ("rgba(70,25,50", "rgba(90,53,45"),
    ("rgba(250,242,246", "rgba(248,242,236"),
    ("rgba(125,52,87", "rgba(122,74,61"),
    ("rgba(253,246,250", "rgba(250,243,236"),
    ("rgba(40,16,30", "rgba(36,26,21"),
    ("rgba(233,205,186", "rgba(232,205,176"),
    ("rgba(185,138,128", "rgba(200,160,140"),
]
for old, new in RGBA_PALETTE:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: booking URL, IG url, IG handle
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_BOOK = "https://alabaster-esthetics.square.site/"
assert h.count(OLD_BOOK) >= 10
h = h.replace(OLD_BOOK, NEW_BOOK)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/alabaster.esthetics/"
assert h.count(OLD_IG_URL) >= 3
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@alabaster.esthetics"
assert h.count(OLD_IG_HANDLE) >= 3
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Alabaster Esthetic\'s · Facials &amp; Skin Studio in Fort Myers, FL | 5.0 Rating</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Alabaster Esthetic\'s, Fort Myers FL: facials, microneedling, dermaplaning, non-invasive laser lipo body contouring and PMU brows by licensed esthetician Jay. 5.0 rating, 21 Google reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Alabaster Esthetic\'s · Facials &amp; Skin Studio in Fort Myers, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Facials, microneedling, laser lipo body contouring and PMU brows. 5.0 on Google. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/massage.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/icon.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Alabaster Esthetic's",
    "description": "Esthetics studio in Fort Myers, FL offering facials, microneedling, dermaplaning, non-invasive laser lipo body contouring, HydroJelly body wraps and permanent makeup for brows.",
    "address": { "@type": "PostalAddress", "streetAddress": "12734 Kenwood Ln, Suite 63", "addressLocality": "Fort Myers", "addressRegion": "FL", "postalCode": "33907", "addressCountry": "US" },
    "telephone": "+12399615497",
    "sameAs": ["https://alabaster-esthetics.square.site/", "https://www.instagram.com/alabaster.esthetics/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "21", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday"], "opens": "10:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "10:00", "closes": "16:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "11:00", "closes": "15:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "11:00", "closes": "14:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Esthetics services", "itemListElement": [
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Decongesting Facial" } },
      { "@type": "Service", "name": "Non-Invasive Laser Lipo (Body Contouring)" },
      { "@type": "Service", "name": "HydroJelly Body Wrap & Scrub" },
      { "@type": "Service", "name": "Permanent Makeup (Brows)" },
      { "@type": "Service", "name": "Face & Body Waxing" }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. PRELOADER
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">AE</span>')
rep('<span class="pre-word">Lash Bloom</span>', "<span class=\"pre-word\">Alabaster Esthetic's</span>")
print("PRELOADER done")

# ---------------------------------------------------------------------------
# 6. NAV (logo + brand name only; link labels/CTA text are generic, kept)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,90,79,0.35)]" />',
    '<img src="assets/raw/logo.jpg" alt="Alabaster Esthetic\'s" class="h-9 w-auto object-contain rounded-md" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Alabaster <span class="text-[color:var(--accent-deep)]">Esthetic\'s</span></span>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Fort Myers, FL · Estudio de Estética" data-en="Fort Myers, FL · Esthetics Studio">Fort Myers, FL · Esthetics Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Cuidado de la piel, con intención." data-en="Skin care, done with intention.">Skin care, done with intention.</p>\n        <h1')
rep('''          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
    '''          <span data-es="Faciales, microneedling" data-en="Facials, microneedling">Facials, microneedling</span><br /><span data-es="y contorno corporal, " data-en="and body contouring, ">and body contouring, </span><span class="text-shine" data-es="bien hechos." data-en="done right.">done right.</span>''')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Microdermoabrasión, microneedling, dermaplaning y faciales descongestionantes. Contorno corporal con laser lipo no invasivo, envolturas HydroJelly y maquillaje permanente de cejas. Un estudio privado en Fort Myers, a cargo de la esteticista licenciada Jay, sirviendo al condado de Lee desde 2023." data-en="Microdermabrasion, microneedling, dermaplaning and decongesting facials. Non-invasive laser lipo body contouring, HydroJelly wraps, and permanent makeup for brows. One private studio in Fort Myers, run by licensed esthetician Jay, serving Lee County since 2023.">Microdermabrasion, microneedling, dermaplaning and decongesting facials. Non-invasive laser lipo body contouring, HydroJelly wraps, and permanent makeup for brows. One private studio in Fort Myers, run by licensed esthetician Jay, serving Lee County since 2023.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 21 reseñas en Google" data-en="5.0 · 21 reviews on Google">5.0 · 21 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar en línea" data-en="Book Online">Book Online</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/massage.jpg" alt="Relaxing facial and body treatment at Alabaster Esthetic\'s in Fort Myers" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Decongesting Facial</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$100" data-en="$100">$100</p>')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="21">21</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Facials <span class="text-shine">&amp;</span> Skin</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Microneedling, dermaplaning" data-en="Microneedling, dermaplane">Microneedling, dermaplane</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Body <span class="text-shine" data-es="Contorno" data-en="Contouring">Contouring</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Laser lipo no invasivo" data-en="Non-invasive laser lipo">Non-invasive laser lipo</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Fort Myers</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">12734 Kenwood Ln</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2 en la pagina, 4 ocurrencias por palabra)
# ---------------------------------------------------------------------------
for old, new in [
    ('Classic Set', 'Facials'),
    ('Hybrid Set', 'Microneedling'),
    ('Volume Set', 'Dermaplane'),
    ('Mega Volume', 'Laser Lipo'),
    ('Bottom Lashes', 'PMU Brows'),
    ('West Palm Beach, FL', 'Fort Myers, FL'),
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
    '<img src="assets/raw/scrub.jpg" alt="Body scrub treatment at Alabaster Esthetic\'s" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/wrap.jpg" alt="HydroJelly body wrap treatment at Alabaster Esthetic\'s" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="precisión y cuidado" data-en="precision &amp; care">precision &amp; care</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Alabaster Esthetic\'s es un estudio de estética privado en Fort Myers a cargo de la esteticista licenciada Jay. Los tratamientos de firma incluyen faciales descongestionantes e hidratantes, microneedling, dermaplaning, contorno corporal con laser lipo no invasivo, envolturas HydroJelly y maquillaje permanente de cejas." data-en="Alabaster Esthetic\'s is a private esthetics studio in Fort Myers run by licensed esthetician Jay. Signature treatments include decongesting and hydrating facials, microneedling, dermaplaning, non-invasive laser lipo body contouring, HydroJelly wraps, and permanent makeup for brows.">Alabaster Esthetic\'s is a private esthetics studio in Fort Myers run by licensed esthetician Jay. Signature treatments include decongesting and hydrating facials, microneedling, dermaplaning, non-invasive laser lipo body contouring, HydroJelly wraps, and permanent makeup for brows.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 21 reseñas de Google, clientas que regresan tanto por sus faciales como por sus series de laser lipo, y un estudio construido para la atención personalizada." data-en="The result: a perfect 5.0 across 21 Google reviews, clients who return for facials and laser lipo series alike, and a studio built around one-on-one attention.">The result: a perfect 5.0 across 21 Google reviews, clients who return for facials and laser lipo series alike, and a studio built around one-on-one attention.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="21">21</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,90,79,0.3)]" loading="lazy" />',
    '<img src="assets/raw/icon.jpg" alt="Alabaster Esthetic\'s" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,90,79,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Jay · <span class="text-[color:var(--ink-40)]" data-es="Esteticista licenciada" data-en="Licensed esthetician">Licensed esthetician</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, un paso" data-en="Your visit, one step">Your visit, one step</span> <span class="text-shine" data-es="a la vez" data-en="at a time">at a time</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elige tu tratamiento en nuestro sitio de reservas con detalles claros, y confirma tu cita al instante." data-en="Pick your treatment through our booking site with clear details, and confirm your spot instantly.">Pick your treatment through our booking site with clear details, and confirm your spot instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consultation">Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu piel, tus metas y tu historial guían el plan de tratamiento, desde un facial descongestionante hasta una serie de laser lipo." data-en="Your skin, goals and history guide the treatment plan, from a decongesting facial to a laser lipo series.">Your skin, goals and history guide the treatment plan, from a decongesting facial to a laser lipo series.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu tratamiento" data-en="Your treatment">Your treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un dermaplaning rápido a una sesión completa de contorno corporal, cada tratamiento recibe su tiempo completo." data-en="From a quick dermaplane to a full body contouring session, every treatment gets its full, unhurried time.">From a quick dermaplane to a full body contouring session, every treatment gets its full, unhurried time.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con indicaciones de cuidado en casa y, para series como laser lipo, tu próxima sesión ya agendada." data-en="You leave with home-care guidance and, for series like laser lipo, your next session already booked.">You leave with home-care guidance and, for series like laser lipo, your next session already booked.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">treatment</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Tratamientos y categorías reales de Alabaster Esthetic\'s. Reserva en línea para precios y disponibilidad actuales." data-en="Real treatments and categories from Alabaster Esthetic\'s. Book online for current pricing and availability.">Real treatments and categories from Alabaster Esthetic\'s. Book online for current pricing and availability.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Depilación" data-en="Waxing">Waxing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Rostro y Cuerpo" data-en="Face &amp; Body">Face &amp; Body</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Depilación de cejas, labio y rostro completo para una forma limpia y precisa." data-en="Brow, lip and full-face waxing for a clean, precise shape.">Brow, lip and full-face waxing for a clean, precise shape.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-xl text-shine" data-es="Reserva para ver precios" data-en="Book to see pricing">Book to see pricing</p></div>
            <a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(156,90,79,0.4); box-shadow: 0 18px 50px rgba(51,38,31,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Faciales" data-en="Facials">Facials</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Facial Descongestionante" data-en="Decongesting Facial">Decongesting Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un tratamiento profundo para piel grasa, congestionada o con acné, que limpia puntos negros, blancos e impurezas." data-en="A deep-pore treatment for oily, congested or acne-prone skin, clearing blackheads, whiteheads and buildup.">A deep-pore treatment for oily, congested or acne-prone skin, clearing blackheads, whiteheads and buildup.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p></div>
            <a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Contorno Corporal" data-en="Body Contouring">Body Contouring</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Laser Lipo No Invasivo" data-en="Non-Invasive Laser Lipo">Non-Invasive Laser Lipo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Series de laser lipo de 3 o 6 sesiones, más envolturas y exfoliaciones HydroJelly para una piel más firme y suave." data-en="3 or 6-session laser lipo series, plus HydroJelly body wraps and scrubs for smoother, firmer skin.">3 or 6-session laser lipo series, plus HydroJelly body wraps and scrubs for smoother, firmer skin.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-xl text-shine" data-es="Por consulta" data-en="By consultation">By consultation</p></div>
            <a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Maquillaje Permanente" data-en="Permanent Makeup">Permanent Makeup</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cejas PMU" data-en="PMU Brows">PMU Brows</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trabajo de cejas con pigmento Perm Blend para una definición natural y duradera." data-en="Perm Blend pigment brow work for natural, long-lasting definition.">Perm Blend pigment brow work for natural, long-lasting definition.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-xl text-shine" data-es="Por consulta" data-en="By consultation">By consultation</p></div>
            <a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También disponible: terapia de luz LED, extracciones y tratamientos de rostro completo. Menú completo y precios actuales en nuestro sitio de reservas." data-en="Also available: LED light therapy, extractions and full-face treatments. Full menu and current pricing on our booking site.">Also available: LED light therapy, extractions and full-face treatments. Full menu and current pricing on our booking site.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (reducida a 3 tiles reales: la escasez de fotos manda)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Antes y Después · Facial Descongestionante" data-en="Before &amp; After · Decongesting Facial">Before &amp; After · Decongesting Facial</span><img src="assets/raw/before-after.jpg" alt="Before and after skin result of a decongesting facial treatment" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Exfoliación Corporal" data-en="Body Scrub">Body Scrub</span><img src="assets/raw/scrub.jpg" alt="Body scrub treatment at Alabaster Esthetic's" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Envoltura HydroJelly" data-en="HydroJelly Wrap">HydroJelly Wrap</span><img src="assets/raw/wrap.jpg" alt="HydroJelly body wrap treatment at Alabaster Esthetic's" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES (4 reseñas reales, verbatim)
# ---------------------------------------------------------------------------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 21 reseñas verificadas en Google" data-en="5.0 out of 5 · 21 verified reviews on Google">5.0 out of 5 · 21 verified reviews on Google</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal flex flex-col">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"I have been going to Jay at Alabaster Esthetic's since June 2024 and she is a true professional and I highly recommend her! She makes the spa experience relaxing, fun and enjoyable as it should be but she is also extremely knowledgeable about her art. She is amazing. Thank you Jay"</blockquote>
          <figcaption class="text-sm mt-auto"><span class="font-medium">Victoria Clarke-Payton</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal flex flex-col" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Jaysalee explains her procedure very well while providing a calm, relaxing experience, even with micro-needling using numbing cream. I have noticed much improvement in the lines around my mouth and eyes plus lessened acne scarring."</blockquote>
          <figcaption class="text-sm mt-auto"><span class="font-medium">D Pierce</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal flex flex-col" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"HUGE THANK YOU to Jaysalee! She did a Hydrafacial on my face (I suffer from horrible dry skin esp the nose area). She was VERY knowledgeable, informed me on so many things that not even Dermatologists tell you about. A few days later my skin is still hydrated, soft and the complexion looks soo good!"</blockquote>
          <figcaption class="text-sm mt-auto"><span class="font-medium">Alyssa Nunez</span> <span class="text-[color:var(--ink-40)]">· Facebook</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal flex flex-col" style="transition-delay:330ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Highly Recommend!! 6 visits dropped 20 lbs. Of course I had to put in some work with proper diet and exercise but definitely worth it. Jay is the best. Great customer service and cares about her clients."</blockquote>
          <figcaption class="text-sm mt-auto"><span class="font-medium">Jason</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://search.google.com/local/reviews?placeid=ChIJQzWr3w4Z24gR_HaxVJD2XPU" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer todas las reseñas en Google" data-en="Read all reviews on Google">Read all reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Fort Myers</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">12734 Kenwood Ln, Suite 63, Fort Myers, FL 33907</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=12734+Kenwood+Ln,+Suite+63,+Fort+Myers,+FL+33907"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa: elige tu tratamiento, día y hora en línea, y tu confirmación es inmediata." data-en="By appointment: pick your treatment, day and time online, and your confirmation is instant.">By appointment: pick your treatment, day and time online, and your confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,90,79,0.4)]" href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,90,79,0.4)]" href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" data-es="Reservar en línea" data-en="Book Online">Book Online</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira tratamientos y resultados reales del estudio, y escribe por DM cualquier duda antes de tu cita." data-en="See real treatments and results from the studio, and DM any questions before your visit.">See real treatments and results from the studio, and DM any questions before your visit.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Map: Alabaster Esthetic\'s, 12734 Kenwood Ln, Fort Myers FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=12734+Kenwood+Ln,+Suite+63,+Fort+Myers,+FL+33907&output=embed"')

# Nuevo bloque: Horario y Telefono (dato real de Birdeye/IG), se agrega tras el bloque de Instagram
ig_block_anchor = '''          <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira tratamientos y resultados reales del estudio, y escribe por DM cualquier duda antes de tu cita." data-en="See real treatments and results from the studio, and DM any questions before your visit.">See real treatments and results from the studio, and DM any questions before your visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,90,79,0.4)]" href="https://www.instagram.com/alabaster.esthetics/" target="_blank" rel="noopener">@alabaster.esthetics</a>
            </div>
          </div>
        </div>'''
assert ig_block_anchor in h, "NO ANCHOR: ig_block_anchor"
HOURS_BLOCK = '''          <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira tratamientos y resultados reales del estudio, y escribe por DM cualquier duda antes de tu cita." data-en="See real treatments and results from the studio, and DM any questions before your visit.">See real treatments and results from the studio, and DM any questions before your visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,90,79,0.4)]" href="https://www.instagram.com/alabaster.esthetics/" target="_blank" rel="noopener">@alabaster.esthetics</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario y Teléfono" data-en="Hours &amp; Phone">Hours &amp; Phone</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes a jueves 10am-6pm · Viernes 10am-4pm · Sábado 11am-3pm · Domingo 11am-2pm · Lunes cerrado" data-en="Tue-Thu 10am-6pm · Fri 10am-4pm · Sat 11am-3pm · Sun 11am-2pm · Closed Monday">Tue-Thu 10am-6pm · Fri 10am-4pm · Sat 11am-3pm · Sun 11am-2pm · Closed Monday</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,90,79,0.4)]" href="tel:+12399615497">(239) 961-5497</a>
            </div>
        </div>'''
h = h.replace(ig_block_anchor, HOURS_BLOCK, 1)
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Cuidado de la piel, con intención." data-en="Skin care, done with intention.">Skin care, done with intention.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próximo" data-en="Your next">Your next</span> <span class="text-shine" data-es="brillo está a una visita" data-en="glow is one visit away">glow is one visit away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu facial, tu sesión de laser lipo, o tu consulta de PMU con Jay." data-en="Book online in seconds: your facial, laser lipo session, or PMU consultation with Jay.">Book online in seconds: your facial, laser lipo session, or PMU consultation with Jay.</p>')
rep('<a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en línea" data-en="Book Online">Book Online</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Alabaster Esthetics</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,205,176,0.35)]" loading="lazy" />',
    '<img src="assets/raw/icon.jpg" alt="Alabaster Esthetic\'s" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,205,176,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Alabaster Esthetic\'s</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de estética en Fort Myers, FL. Atención con cita previa." data-en="Esthetics studio in Fort Myers, FL. By appointment only.">Esthetics studio in Fort Myers, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>12734 Kenwood Ln, Suite 63, Fort Myers, FL 33907</p>')
rep('<p><a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="hover:text-[#e8cdb0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '''<p><a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="hover:text-[#e8cdb0]" data-es="Reservas en línea" data-en="Online booking">Online booking</a></p>
        <p><a href="tel:+12399615497" class="hover:text-[#e8cdb0]">(239) 961-5497</a></p>
        <p><a href="mailto:AlabasterEsthetics@gmail.com" class="hover:text-[#e8cdb0]">AlabasterEsthetics@gmail.com</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Alabaster Esthetic\'s.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. book-float
# ---------------------------------------------------------------------------
rep('<a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://alabaster-esthetics.square.site/" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')

print("ALL DONE")
open(PATH, "w", encoding="utf-8").write(h)
print(len(h))
