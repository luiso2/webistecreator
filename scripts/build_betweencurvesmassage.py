import re, shutil

shutil.copy('templates/light-v2/index.html', 'output/betweencurvesmassage/index.html')
h = open('output/betweencurvesmassage/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'badge block not found'
BADGE = m.group(0)
h = h.replace(BADGE, '@@BADGE@@', 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum/pink (lashbloom) -> gold/emerald (Between Curves Massage)
# ---------------------------------------------------------------------------
PALETTE = [
    ('#a04a72', '#9c7c3f'),
    ('#c47a9c', '#c9a768'),
    ('#5c2140', '#5c4620'),
    ('#f0bed7', '#e8d29a'),
    ('#faf2f6', '#faf6ee'),
    ('#c9789f', '#cfa96a'),
    ('#8a5573', '#8a7040'),
    ('#f3e0ea', '#f1e6cf'),
    ('#d9a8c2', '#dfc48a'),
    ('#7d3457', '#6b5527'),
    ('#5f2c48', '#6b5527'),
    ('#33222c', '#2b2419'),
    ('#fbf3f8', '#faf6ee'),
    ('#fbeff5', '#faf3df'),
    ('#f8dfeb', '#f3e8c8'),
    ('#f2d5e3', '#f0e2bf'),
    ('#f2cfe0', '#eddcac'),
    ('#efd0e0', '#ecdcb0'),
    ('#e5c1d4', '#eadcb8'),
    ('#dc9dbe', '#d4b877'),
    ('#d3a2bc', '#cbab6c'),
    ('#b25a85', '#b8944f'),
    ('#2a1722', '#16261b'),
    ('#1f0f18', '#0f1a12'),
    ('#1c0f16', '#101b13'),
    ('#f6f1ea', '#faf6ee'),
]
for a, b in PALETTE:
    h = h.replace(a, b)

RGBA_PAIRS = [
    ('rgba(160,74,114,', 'rgba(156,124,63,'),
    ('rgba(51,34,44,', 'rgba(43,36,25,'),
    ('rgba(70,25,50,', 'rgba(80,60,25,'),
    ('rgba(240,190,215,', 'rgba(232,210,154,'),
    ('rgba(233,205,186,', 'rgba(212,178,110,'),
    ('rgba(185,138,128,', 'rgba(196,156,90,'),
    ('rgba(125,52,87,', 'rgba(107,85,39,'),
    ('rgba(253,246,250,', 'rgba(253,250,242,'),
    ('rgba(250,242,246,', 'rgba(250,246,238,'),
    ('rgba(40,16,30,', 'rgba(26,20,10,'),
]
for a, b in RGBA_PAIRS:
    h = h.replace(a, b)

h = h.replace('@@BADGE@@', BADGE, 1)
print('STEP 1-2 OK (badge protected + palette shifted)')

# ---------------------------------------------------------------------------
# 3. Globales: URL de Booksy, IG, handle, logo
# ---------------------------------------------------------------------------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1602943_between-curves-massage_massage_15761_tampa'
cnt = h.count(OLD_BOOKSY)
assert cnt >= 1
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/betweencurves_massage/'
assert h.count(OLD_IG_URL) >= 1
h = h.replace(OLD_IG_URL, NEW_IG_URL)

h = h.replace('@_lashbloom', '@betweencurves_massage')

print('STEP 3 OK (booksy/ig globals)')

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, JSON-LD
# ---------------------------------------------------------------------------
rep(
'  <title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>\n  <meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />\n  <meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />\n  <meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />\n  <meta property="og:type" content="website" />\n  <meta property="og:image" content="assets/raw/bk-6.jpg" />\n  <link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
'  <title>Between Curves Massage · Masajes y Faciales en Tampa, FL | 5.0 en Booksy</title>\n  <meta name="description" content="Between Curves Massage, Tampa FL: masaje de cuerpo completo, drenaje linfatico, reflexologia y faciales correctivos con esteticista certificada. 5.0 en 13 resenas de Booksy. Reserva online." />\n  <meta property="og:title" content="Between Curves Massage · Masajes y Faciales en Tampa, FL" />\n  <meta property="og:description" content="Masaje de cuerpo completo, drenaje linfatico, reflexologia y faciales. 5.0 en Booksy. Reserva online." />\n  <meta property="og:type" content="website" />\n  <meta property="og:image" content="assets/raw/bk-9.jpg" />\n  <link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />'
)

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert old_jsonld, 'jsonld not found'
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "Between Curves Massage",
    "description": "Massage and facial studio in Tampa, FL: full body massage, lymphatic drainage, reflexology and corrective facials with a certified massage therapist and esthetician.",
    "address": { "@type": "PostalAddress", "streetAddress": "4311 W Water Ave, Suite 602", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33614", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.9865, "longitude": -82.51344 },
    "openingHoursSpecification": { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "09:30", "closes": "20:00" },
    "sameAs": ["https://booksy.com/en-us/1602943_between-curves-massage_massage_15761_tampa", "https://www.instagram.com/betweencurves_massage/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "13", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios", "itemListElement": [
      { "@type": "Offer", "price": "99", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Customized Full Body Massage" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lymphatic Drainage" } },
      { "@type": "Offer", "price": "109", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Signature Deep Clean Facial" } },
      { "@type": "Offer", "price": "39", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Reflexology" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld.group(0), new_jsonld, 1)
print('STEP 4 OK (head + jsonld)')

# ---------------------------------------------------------------------------
# 5. Idioma principal = ES
# ---------------------------------------------------------------------------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep(
"    let lang = localStorage.getItem('lang') || (navigator.language || 'es').slice(0, 2);\n    applyLang(lang === 'es' ? 'es' : 'en');",
"    let lang = localStorage.getItem('lang') || (navigator.language || 'es').slice(0, 2);\n    applyLang(lang === 'en' ? 'en' : 'es');"
)
print('STEP 5 OK (idioma)')

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep(
'<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,124,63,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
'<img src="assets/raw/logo.jpg" alt="Between Curves Massage" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,124,63,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Between <span class="text-[color:var(--accent-deep)]">Curves</span></span>'
)
rep('<a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
    '<a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>')
rep('<a class="nav-link" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
    '<a class="nav-link" href="#metodo" data-es="Tu Cita" data-en="Your Visit">Tu Cita</a>', 2)
rep('<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>',
    '<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>', 2)
rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>',
    '<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>', 2)
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>', 2)
assert h.count('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>') == 1
h = h.replace('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
              '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="Tu Cita" data-en="Your Visit">Tu Cita</a>', 1)
rep('<a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>',
    '<a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>')
print('STEP 6 OK (nav)')

# ---------------------------------------------------------------------------
# 6b. PRELOADER
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>\n    <span class="pre-word">Lash Bloom</span>',
    '<span class="pre-mono">BCM</span>\n    <span class="pre-word">Between Curves Massage</span>')
print('STEP 6b OK (preloader)')

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Masajes y Faciales" data-en="Tampa, FL · Massage &amp; Facials">Tampa, FL · Massage &amp; Facials</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Tu cuerpo, en las manos correctas." data-en="Your body, in the right hands.">Tu cuerpo, en las manos correctas.</p>', 2)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Masajes y faciales" data-en="Massage and facials">Masajes y faciales</span><br /><span data-es="hechos para que " data-en="made so results ">hechos para que </span><span class="text-shine" data-es="se note" data-en="show">se note</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Masaje de cuerpo completo, drenaje linfático, reflexología y faciales correctivos, en un estudio boutique en Tampa. Terapeuta y esteticista certificada, con resultados que sus clientas notan sesión tras sesión." data-en="Full body massage, lymphatic drainage, reflexology and corrective facials, in a boutique studio in Tampa. Certified massage therapist and esthetician, with results her clients notice session after session.">Masaje de cuerpo completo, drenaje linfático, reflexología y faciales correctivos, en un estudio boutique en Tampa. Terapeuta y esteticista certificada, con resultados que sus clientas notan sesión tras sesión.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 13 reseñas en Booksy" data-en="5.0 · 13 reviews on Booksy">5.0 · 13 reseñas en Booksy</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>', 2)
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-9.jpg" alt="Terapeuta haciendo masaje profundo de espalda en Between Curves Massage" class="blur-up w-full h-full object-cover" />')
rep('data-es="Reserva online" data-en="Book online">Reserva online</p>',
    'data-es="Reserva online" data-en="Book online">Reserva online</p>', 2)
rep('<p class="font-display text-lg">Volume Full Set</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="font-display text-lg">Customized Full Body Massage</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$99 · 1h" data-en="$99 · 1h">$99 · 1h</p>')
print('STEP 7 OK (hero)')

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="13">13</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p>',
    '<p class="font-display text-2xl">Cuerpo <span class="text-shine">&amp;</span> Rostro</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Masaje · Faciales · Reflexología" data-en="Massage · Facials · Reflexology">Masaje · Faciales · Reflexología</p>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p>',
    '<p class="font-display text-2xl">18 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo, precios reales" data-en="Full menu, real prices">Menú completo, precios reales</p>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p>',
    '<p class="font-display text-2xl">Tampa, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4311 W Water Ave</p>')
print('STEP 8 OK (strip)')

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2 tracks, cada palabra aparece 4 veces en total)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ('Classic Set', 'Full Body Massage'),
    ('Hybrid Set', 'Lymphatic Drainage'),
    ('Volume Set', 'Reflexology'),
    ('Mega Volume', 'Signature Facial'),
    ('Bottom Lashes', 'Body Contouring'),
    ('West Palm Beach, FL', 'Tampa, FL'),
]
for old_w, new_w in MARQUEE_WORDS:
    old_span = f'<span class="marquee-word">{old_w}</span>'
    cnt = h.count(old_span)
    assert cnt == 4, f'{old_w} count={cnt}'
    h = h.replace(old_span, f'<span class="marquee-word">{new_w}</span>')
print('STEP 9 OK (marquee)')

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Letrero dorado Between Curves Massage en la pared del estudio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Terapia de ventosas (cupping) durante una sesion de masaje" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="La experiencia" data-en="The experience">La experiencia</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio boutique" data-en="A boutique studio">Un estudio boutique</span><br /><span class="text-shine" data-es="hecho a tu medida" data-en="built around you">hecho a tu medida</span></h2>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Between Curves Massage es el estudio de Yare, terapeuta de masajes y esteticista certificada en Tampa. Cada sesión se adapta a lo que tu cuerpo necesita ese día: relajación profunda, drenaje linfático, reflexología o un facial correctivo, siempre con atención personal de principio a fin." data-en="Between Curves Massage is the studio of Yare, a certified massage therapist and esthetician in Tampa. Every session is built around what your body needs that day: deep relaxation, lymphatic drainage, reflexology or a corrective facial, always with personal attention from start to finish.">Between Curves Massage es el estudio de Yare, terapeuta de masajes y esteticista certificada en Tampa. Cada sesión se adapta a lo que tu cuerpo necesita ese día: relajación profunda, drenaje linfático, reflexología o un facial correctivo, siempre con atención personal de principio a fin.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en Booksy, clientas que notan la diferencia sesión tras sesión, y un espacio pensado para que te desconectes de verdad mientras te cuidan." data-en="The result: a perfect 5.0 on Booksy, clients who notice the difference session after session, and a space designed to help you truly disconnect while you are taken care of.">El resultado: 5.0 perfecto en Booksy, clientas que notan la diferencia sesión tras sesión, y un espacio pensado para que te desconectes de verdad mientras te cuidan.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="13">13</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,124,63,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/bk-15.jpg" alt="Yare, terapeuta de masajes de Between Curves Massage" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,124,63,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yare · <span class="text-[color:var(--ink-40)]" data-es="Terapeuta certificada" data-en="Certified therapist">Certified therapist</span></span>')
print('STEP 10 OK (experiencia)')

# ---------------------------------------------------------------------------
# 11. EL METODO -> TU CITA
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita," data-en="Your visit,">Tu cita,</span> <span class="text-shine" data-es="a tu ritmo" data-en="at your pace">a tu ritmo</span></h2>')
rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta inicial" data-en="Initial consult">Consulta inicial</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Antes de empezar, Yare revisa qué necesita tu cuerpo o tu piel ese día para ajustar la sesión." data-en="Before starting, Yare checks what your body or skin needs that day to tailor the session.">Antes de empezar, Yare revisa qué necesita tu cuerpo o tu piel ese día para ajustar la sesión.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Tu sesión" data-en="Your session">Tu sesión</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Masaje, drenaje linfático, reflexología o facial: te recuestas y te dejas cuidar de principio a fin." data-en="Massage, lymphatic drainage, reflexology or facial: you lie back and let yourself be taken care of, start to finish.">Masaje, drenaje linfático, reflexología o facial: te recuestas y te dejas cuidar de principio a fin.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Plan de seguimiento" data-en="Follow-up plan">Plan de seguimiento</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con recomendaciones claras y, si aplica, tu próxima sesión del programa ya agendada." data-en="You leave with clear recommendations and, if it applies, your next program session already booked.">Sales con recomendaciones claras y, si aplica, tu próxima sesión del programa ya agendada.</p>')
print('STEP 11 OK (metodo)')

# ---------------------------------------------------------------------------
# 12. SERVICIOS (seccion completa reemplazada por regex, header + 4 cards + menu agrupado)
# ---------------------------------------------------------------------------
serv_re = re.compile(r'<section id="servicios".*?</section>', re.S)
assert serv_re.search(h), 'servicios section not found'

def row(name, price, dur):
    dur_html = f'<span class="text-[color:var(--ink-40)]"> · {dur}</span>' if dur else ''
    return f'<div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)] last:border-0"><p class="text-sm font-light">{name}{dur_html}</p><p class="text-sm font-display">${price}</p></div>'

massage_rows = [
    row('Customized Full Body Massage', 99, '1h'),
    row('Customized Full Body Massage', 139, '1h 30min'),
    row('Back', 50, '30min'),
    row('Prenatal Massage', 79, '1h'),
    row('Lymphatic Drainage', 85, '1h'),
    row('Kids Relaxation Massage', 45, '30min'),
    row('Deep Back Cleanse', 120, '1h'),
]
reflex_rows = [
    row('Reflexology', 39, '30min'),
    row('Reflexology', 59, '1h'),
    row('Ionic Foot Detox', 29, '30min'),
]
facial_rows = [
    row('Skin Consultation &amp; Analysis', 25, '30min'),
    row('Signature Deep Clean Facial', 109, '1h 15min'),
    row('Monthly Glow Facial', 120, '1h'),
    row('Acne Corrective', 150, None),
    row('Melasma Corrective Facial', 150, None),
    row('Microneedling Facial', 180, '1h 30min'),
]
program_rows = [
    row('Body Contouring Program – 5 Sessions', 450, '1h 15min c/sesión'),
    row('Ultimate Body Transformation Program - 10 Sessions', 850, '1h 20min c/sesión'),
]

def block(title_es, title_en, rows_html):
    return f'''<div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-lg mb-4 text-[color:var(--accent-deep)]" data-es="{title_es}" data-en="{title_en}">{title_es}</h3>
          {''.join(rows_html)}
        </div>'''

new_servicios = '''<section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="sesión" data-en="session">sesión</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Between Curves Massage en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Between Curves Massage on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Between Curves Massage en Booksy. Reserva con confirmación inmediata.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más pedido" data-en="Most booked">Más pedido</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Customized Full Body Massage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Masaje relajante de cuerpo completo, adaptado a la zona que más lo necesita. Disponible en 1h o 1h 30min." data-en="Relaxing full body massage, adapted to the area that needs it most. Available in 1h or 1h 30min.">Masaje relajante de cuerpo completo, adaptado a la zona que más lo necesita. Disponible en 1h o 1h 30min.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$99</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1602943_between-curves-massage_massage_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(156,124,63,0.4); box-shadow: 0 18px 50px rgba(43,36,25,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito de las clientas" data-en="Client favorite">Favorito de las clientas</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Lymphatic Drainage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La técnica que más mencionan las reseñas: drenaje linfático para desinflamar y ayudar a que el cuerpo se vea y se sienta mejor." data-en="The technique reviews mention most: lymphatic drainage to reduce inflammation and help your body look and feel better.">La técnica que más mencionan las reseñas: drenaje linfático para desinflamar y ayudar a que el cuerpo se vea y se sienta mejor.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1602943_between-curves-massage_massage_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cuidado facial" data-en="Facial care">Cuidado facial</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Signature Deep Clean Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Limpieza facial profunda de la mano de una esteticista certificada, para piel más clara y descongestionada." data-en="Deep facial cleanse by a certified esthetician, for clearer, decongested skin.">Limpieza facial profunda de la mano de una esteticista certificada, para piel más clara y descongestionada.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$109</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="https://booksy.com/en-us/1602943_between-curves-massage_massage_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies y bienestar" data-en="Feet &amp; wellness">Pies y bienestar</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Reflexology</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Reflexología de pies para liberar tensión desde la planta hacia el resto del cuerpo. Disponible en 30min o 1h." data-en="Foot reflexology to release tension from the sole through the rest of the body. Available in 30min or 1h.">Reflexología de pies para liberar tensión desde la planta hacia el resto del cuerpo. Disponible en 30min o 1h.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$39</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="https://booksy.com/en-us/1602943_between-curves-massage_massage_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo con los 18 servicios de Between Curves Massage, agrupados por categoría." data-en="Full menu with all 18 Between Curves Massage services, grouped by category.">Menú completo con los 18 servicios de Between Curves Massage, agrupados por categoría.</span></p>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-10">
        ''' + block('Masaje y Cuerpo', 'Massage &amp; Body', massage_rows) + '''
        ''' + block('Reflexología y Detox', 'Reflexology &amp; Detox', reflex_rows) + '''
        ''' + block('Faciales', 'Facials', facial_rows) + '''
        ''' + block('Programas de Transformación', 'Transformation Programs', program_rows) + '''
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Precios en dólares (USD), publicados por Between Curves Massage en Booksy. Disponibilidad y reserva online en Booksy." data-en="Prices in US dollars, as published by Between Curves Massage on Booksy. Availability and online booking on Booksy.">Precios en dólares (USD), publicados por Between Curves Massage en Booksy. Disponibilidad y reserva online en Booksy.</span></p>
    </div>
  </section>'''

h = serv_re.sub(lambda _: new_servicios.replace('\\', '\\\\'), h, count=1)
print('STEP 12 OK (servicios)')

# ---------------------------------------------------------------------------
# 13. GALERIA (seccion completa reemplazada por regex)
# ---------------------------------------------------------------------------
gal_re = re.compile(r'<section id="galeria".*?</section>', re.S)
assert gal_re.search(h), 'galeria section not found'

new_galeria = '''<section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Momentos" data-en="Real">Momentos</span> <span class="text-shine" data-es="reales" data-en="moments">reales</span></h2>
        </div>
        <a href="https://www.instagram.com/betweencurves_massage/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @betweencurves_massage
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Masaje de cuerpo completo" data-en="Full body massage">Masaje de cuerpo completo</span><img src="assets/raw/bk-6.jpg" alt="Masaje de espalda de cuerpo completo al aire libre en Between Curves Massage" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Reflexología" data-en="Reflexology">Reflexología</span><img src="assets/raw/bk-7.jpg" alt="Reflexologia de pies con herramienta de madera" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Masaje craneal" data-en="Scalp massage">Masaje craneal</span><img src="assets/raw/bk-8.jpg" alt="Masaje craneal al aire libre" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Masaje para niños" data-en="Kids massage">Masaje para niños</span><img src="assets/raw/bk-5.jpg" alt="Masaje relajante para ninos en Between Curves Massage" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Ambiente del estudio" data-en="Studio ambience">Ambiente del estudio</span><img src="assets/raw/bk-10.jpg" alt="Ambiente relajante del estudio Between Curves Massage" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Trabajo profundo" data-en="Deep tissue work">Trabajo profundo</span><img src="assets/raw/bk-9.jpg" alt="Masaje profundo de espalda en Between Curves Massage" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''

h = gal_re.sub(lambda _: new_galeria, h, count=1)
print('STEP 13 OK (galeria)')

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    'data-es="5.0 de 5 · 13 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 13 verified reviews on Booksy">5.0 de 5 · 13 reseñas verificadas en Booksy</span>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"En mi cuarta sesión confirmo que los resultados se notan. Su técnica en drenaje linfático y maderoterapia es muy buena, además de ser puntual, profesional y atenta. El espacio es cómodo y adecuado para relajarse durante el servicio."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Yailise C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great massage!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Alex S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Rejuvenation at its peak. I’m speechless at this point."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Mustafa J.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 13 reseñas en Booksy" data-en="Read all 13 reviews on Booksy">Leer las 13 reseñas en Booksy</a>')
print('STEP 14 OK (opiniones)')

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    'data-es="Visítanos" data-en="Visit us">Visítanos</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa</span></h2>')
rep('<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,124,63,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light">4311 W Water Ave, Suite 602, Tampa, FL 33614</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light mt-1" data-es="Todos los días · 9:30am - 8:00pm" data-en="Every day · 9:30am - 8:00pm">Todos los días · 9:30am - 8:00pm</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,124,63,0.4)]" href="https://www.google.com/maps?q=4311+W+Water+Ave,+Tampa,+FL+33614" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>')
rep('<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    '<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,124,63,0.4)]" href="https://www.instagram.com/betweencurves_massage/" target="_blank" rel="noopener">@betweencurves_massage</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira el trabajo más reciente de Yare y escribe por DM cualquier duda antes de tu cita." data-en="See Yare\'s latest work and DM any questions before your appointment.">Mira el trabajo más reciente de Yare y escribe por DM cualquier duda antes de tu cita.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,124,63,0.4)]" href="https://www.instagram.com/betweencurves_massage/" target="_blank" rel="noopener">@betweencurves_massage</a>')
rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Between Curves Massage, 4311 W Water Ave, Tampa FL"\n          src="https://www.google.com/maps?q=4311+W+Water+Ave,+Tampa,+FL+33614&output=embed"')
print('STEP 15 OK (ubicacion)')

# ---------------------------------------------------------------------------
# 16. CTA FINAL (la linea script ya se cambio en el hero con n=2)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima sesión" data-en="Your next session">Tu próxima sesión</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span></h2>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu masaje, tu drenaje linfático o el facial que ya te toca." data-en="Book online in seconds: your massage, your lymphatic drainage, or the facial you are due for.">Reserva online en segundos: tu masaje, tu drenaje linfático o el facial que ya te toca.</p>')
rep('data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="https://www.instagram.com/betweencurves_massage/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="https://www.instagram.com/betweencurves_massage/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print('STEP 16 OK (cta final)')

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Between Curves Massage</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,210,154,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<img src="assets/raw/logo.jpg" alt="Between Curves Massage" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,210,154,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Between Curves Massage</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de masajes y faciales en Tampa, FL. Atención con cita previa." data-en="Massage and facial studio in Tampa, FL. By appointment only.">Estudio de masajes y faciales en Tampa, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>4311 W Water Ave, Suite 602, Tampa, FL 33614</p>')
rep('data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a>',
    'data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a>')
rep('<a href="https://www.instagram.com/betweencurves_massage/" target="_blank" rel="noopener" class="hover:text-[#e8d29a]">Instagram · @betweencurves_massage</a>',
    '<a href="https://www.instagram.com/betweencurves_massage/" target="_blank" rel="noopener" class="hover:text-[#e8d29a]">Instagram · @betweencurves_massage</a>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Between Curves Massage.</p>')
print('STEP 17 OK (footer)')

# ---------------------------------------------------------------------------
# 18. Guardar SIEMPRE, y luego verificar leftovers (para poder inspeccionar si falla)
# ---------------------------------------------------------------------------
open('output/betweencurvesmassage/index.html', 'w').write(h)
print('SAVED FINAL (pre-check)')

for bad in ['Lash Bloom', 'lashbloom', '_lashbloom', 'West Palm Beach', '519855', 'Yesi', 'Cresthaven']:
    assert bad not in h, 'LEFTOVER: ' + bad
print('STEP 18 OK (sin leftovers criticos)')
