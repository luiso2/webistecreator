import re, os, shutil

SLUG = "305esthetics"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:90]
    h = h.replace(a, b, 1)


badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

PALETTE = [
    ("#faf2f6", "#faf2fa"), ("#f3e0ea", "#f2e0f3"), ("#a04a72", "#a04aa0"),
    ("#c47a9c", "#c47ac4"), ("#c9789f", "#c878c9"), ("#5f2c48", "#5b2c5f"),
    ("#b25a85", "#b05ab2"), ("#f2d5e3", "#f1d5f2"), ("#d9a8c2", "#d6a8d9"),
    ("#e5c1d4", "#e3c1e5"), ("#7d3457", "#7c347d"), ("#5c2140", "#58215c"),
    ("#f0bed7", "#eebef0"), ("#f8dfeb", "#f8dff8"), ("#f2cfe0", "#f1cff2"),
    ("#fbeff5", "#fbeffb"), ("#efd0e0", "#edd0ef"), ("#d3a2bc", "#d0a2d3"),
    ("#8a5573", "#85558a"), ("#dc9dbe", "#d89ddc"), ("#2a1722", "#28172a"),
    ("#1f0f18", "#1d0f1f"), ("#1c0f16", "#1b0f1c"), ("#f6f1ea", "#f6ebea"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(160,74,160"),
    ("rgba(125,52,87", "rgba(124,52,125"),
    ("rgba(185,138,128", "rgba(185,128,148"),
    ("rgba(233,205,186", "rgba(233,186,192"),
    ("rgba(240,190,215", "rgba(238,190,240"),
    ("rgba(250,242,246", "rgba(250,242,250"),
    ("rgba(253,246,250", "rgba(252,246,253"),
    ("rgba(40,16,30", "rgba(37,16,40"),
    ("rgba(70,25,50", "rgba(66,25,70"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://305esthetics.glossgenius.com')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/305esthetics/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@305esthetics')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>305 Esthetics · Brows, Lashes &amp; Skin in Miami, FL | Book Online</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="305 Esthetics, Downtown Miami FL: brow lamination, keratin lash lift, HydraFacial and dermaplane combos, precision threading. Real menu, real photos. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="305 Esthetics · Brows, Lashes &amp; Skin in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Brow lamination, lash lift and HydraFacial combos, precision first. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-14.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-16.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "305 Esthetics",
    "description": "Esthetics studio in Downtown Miami, FL: brow lamination, keratin lash lift, HydraFacial and dermaplane combos, precision threading and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "1442 NE Miami Court, Suite 217", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33132", "addressCountry": "US" },
    "telephone": "+13053060063",
    "sameAs": ["https://305esthetics.glossgenius.com", "https://www.instagram.com/305esthetics/"],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Esthetics services", "itemListElement": [
      { "@type": "Offer", "price": "99", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brow Lamination + Shape & Tint" } },
      { "@type": "Offer", "price": "99", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "HydroFacial + Dermaplane Combo" } },
      { "@type": "Offer", "price": "99", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Keratin Lash Lift + Tint" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Precision Brow Wax + Mapping" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# Preloader
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">305</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">305 Esthetics</span>')

# NAV
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,160,0.35)]" />',
    '<img src="assets/raw/bk-16.jpg" alt="305 Esthetics" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,160,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">305 <span class="text-[color:var(--accent-deep)]">Esthetics</span></span>')
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="nav-link" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Estudio de Estetica" data-en="Miami, FL · Esthetics Studio">Miami, FL · Esthetics Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Cejas, pestañas, piel." data-en="Brows, lashes, skin.">Brows, lashes, skin.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Laminado de cejas, lash lift" data-en="Brow lamination, lash lifts">Brow lamination, lash lifts</span><br /><span data-es="y tratamientos de piel " data-en="and skin treatments ">and skin treatments </span><span class="text-shine" data-es="hechos con precision" data-en="made precise">made precise</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Laminado y forma de cejas, lash lift de keratina, HydraFacial y combos de dermaplane, todo en un estudio privado en el centro de Miami. Cada tratamiento incluye mapeo experto y tecnicas hechas para tus rasgos." data-en="Brow lamination and shaping, keratin lash lifts, HydraFacials and dermaplane combos, all in one private studio in Downtown Miami. Every treatment includes expert mapping and techniques tailored to your features.">Brow lamination and shaping, keratin lash lifts, HydraFacials and dermaplane combos, all in one private studio in Downtown Miami. Every treatment includes expert mapping and techniques tailored to your features.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar cita" data-en="Book online">Book online</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-14.jpg" alt="Portrait with brow and skin styling, side profile" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">HydroFacial + Dermaplane</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$99 · 1h 15min" data-en="$99 · 1h 15min">$99 · 1h 15min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl">Brows <span class="text-shine">&amp;</span> Lashes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo, precios reales" data-en="Full menu, real prices">Full menu, real prices</p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Skin <span class="text-shine">&amp;</span> Facials</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="HydraFacial, dermaplane" data-en="HydraFacial, dermaplane">HydraFacial, dermaplane</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">By <span class="text-shine" data-es="cita" data-en="appt">appt</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención uno a uno" data-en="One-on-one care">One-on-one care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1442 NE Miami Ct</p></div>')

# MARQUEE
for old, new in [
    ('Classic Set', 'Brow Lamination'),
    ('Hybrid Set', 'Lash Lift'),
    ('Volume Set', 'HydraFacial'),
    ('Mega Volume', 'Dermaplane'),
    ('Bottom Lashes', 'Threading'),
    ('West Palm Beach, FL', 'Miami, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Facial mask being applied at 305 Esthetics" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Dermaplane treatment tool close-up" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="precision primero" data-en="precision first">precision first</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="305 Esthetics es un estudio privado en el centro de Miami especializado en cejas, pestañas y piel. Tratamientos de firma: laminado de cejas con tinte, lash lift de keratina, y un combo de HydraFacial con dermaplane." data-en="305 Esthetics is a private studio in Downtown Miami specializing in brows, lashes and skin. Signature treatments include brow lamination with tint, keratin lash lift, and a HydraFacial plus dermaplane combo.">305 Esthetics is a private studio in Downtown Miami specializing in brows, lashes and skin. Signature treatments include brow lamination with tint, keratin lash lift, and a HydraFacial plus dermaplane combo.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Cada cita empieza con un mapeo experto de cejas y un plan hecho para tus rasgos, para un brillo limpio, refinado y de bajo mantenimiento." data-en="Every visit starts with expert brow mapping and a plan built around your features, for a clean, refined and low-maintenance glow.">Every visit starts with expert brow mapping and a plan built around your features, for a clean, refined and low-maintenance glow.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Brows</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Especialidad" data-en="Specialty">Specialty</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Miami</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Ubicación" data-en="Location">Location</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,160,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="305 Esthetics" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,160,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Mercedes · <span class="text-[color:var(--ink-40)]" data-es="Esteticista licenciada" data-en="Licensed esthetician">Licensed esthetician</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, un paso" data-en="Your visit, one step">Your visit, one step</span> <span class="text-shine" data-es="a la vez" data-en="at a time">at a time</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu tratamiento con precio y duración claros, y confirmas al instante." data-en="Pick your treatment with clear price and duration, and confirm instantly.">Pick your treatment with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consultation">Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu piel, la forma de tus cejas y tus metas definen el mapeo y la tecnica que se usa." data-en="Your skin, brow shape and goals define the mapping and technique used.">Your skin, brow shape and goals define the mapping and technique used.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu tratamiento" data-en="Your treatment">Your treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De una cera de labios de 10 minutos a un laminado de cejas de 90: cada servicio recibe su tiempo completo." data-en="From a 10-minute lip wax to a 90-minute brow lamination, every service gets its full time.">From a 10-minute lip wax to a 90-minute brow lamination, every service gets its full time.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Brillo a casa" data-en="Glow home">Glow home</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un look refinado y de bajo mantenimiento, y las indicaciones para mantenerlo asi." data-en="You leave with a refined, low-maintenance look and the guidance to keep it that way.">You leave with a refined, low-maintenance look and the guidance to keep it that way.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por 305 Esthetics. Reserva con confirmación inmediata." data-en="Prices and durations as published by 305 Esthetics. Booking confirms instantly.">Prices and durations as published by 305 Esthetics. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">treatment</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas" data-en="Brows">Brows</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Laminado + Tinte" data-en="Lamination + Tint">Lamination + Tint</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Laminado de cejas con forma y tinte hibrido, mapeo experto incluido." data-en="Brow lamination with shape and hybrid tint, expert mapping included.">Brow lamination with shape and hybrid tint, expert mapping included.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$99</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,160,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Piel" data-en="Skin">Skin</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="HydroFacial + Dermaplane" data-en="HydroFacial + Dermaplane">HydroFacial + Dermaplane</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo de firma del estudio: hidratacion profunda y exfoliacion suave en una sola cita." data-en="The studio's signature combo: deep hydration and gentle exfoliation in one visit.">The studio's signature combo: deep hydration and gentle exfoliation in one visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$99</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pestañas" data-en="Lashes">Lashes</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lash Lift de Keratina" data-en="Keratin Lash Lift">Keratin Lash Lift</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Lash lift de keratina con tinte para un efecto abierto y natural, sin extensiones." data-en="Keratin lash lift with tint for an open, natural effect, no extensions needed.">Keratin lash lift with tint for an open, natural effect, no extensions needed.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$99</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Threading y Cera" data-en="Threading &amp; Wax">Threading &amp; Wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Precision brow wax o threading con mapeo desde $30, tinte de cejas desde $25." data-en="Precision brow wax or threading with mapping from $30, brow tint from $25.">Precision brow wax or threading with mapping from $30, brow tint from $25.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $25" data-en="From $25">From $25</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">10-30min</p></div>
            <a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: facial express, limpieza profunda, threading de rostro completo, cera de labios y menton, wood therapy y cavitacion ultrasonica. Menu completo y disponibilidad en el sitio de reservas." data-en="Also available: express facial, deep cleansing facial, full face threading, lip and chin wax, wood therapy and ultrasonic cavitation. Full menu and availability on the booking site.">Also available: express facial, deep cleansing facial, full face threading, lip and chin wax, wood therapy and ultrasonic cavitation. Full menu and availability on the booking site.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Facial en proceso" data-en="Facial in progress">Facial in progress</span><img src="assets/raw/bk-10.jpg" alt="Facial treatment being applied at 305 Esthetics" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Extensiones de pestañas" data-en="Lash extensions">Lash extensions</span><img src="assets/raw/bk-12.jpg" alt="Close-up of eyelash extensions" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Forma de cejas" data-en="Brow shaping">Brow shaping</span><img src="assets/raw/bk-5.jpg" alt="Brow shaping with tweezers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Tratamiento de luz" data-en="Light treatment">Light treatment</span><img src="assets/raw/bk-4.jpg" alt="Skin treatment close-up with blue light" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Cejas terminadas" data-en="Finished brows">Finished brows</span><img src="assets/raw/bk-2.jpg" alt="Close-up of shaped eyebrows, eyes closed" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Tratamiento facial" data-en="Facial treatment">Facial treatment</span><img src="assets/raw/bk-7.jpg" alt="Facial device treatment close-up" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES -> ESPECIALIDADES
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="El estudio" data-en="The studio">The studio</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Por qué" data-en="Why">Why</span> <span class="text-shine" data-es="305 Esthetics" data-en="305 Esthetics">305 Esthetics</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cejas, pestañas y tratamientos de piel diseñados para un brillo limpio y de bajo mantenimiento." data-en="Brows, lashes and skin treatments designed for a clean, low-maintenance glow.">Brows, lashes and skin treatments designed for a clean, low-maintenance glow.</p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_WHY = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="font-display text-2xl text-shine mb-3" data-es="Combos de firma" data-en="Signature combos">Signature combos</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Laminado de cejas con tinte, lash lift de keratina, y un combo de HydraFacial con dermaplane, pensados para ir juntos." data-en="Brow lamination with tint, keratin lash lift, and a HydraFacial plus dermaplane combo, all designed to go together.">Brow lamination with tint, keratin lash lift, and a HydraFacial plus dermaplane combo, all designed to go together.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Mapeo experto" data-en="Expert mapping">Expert mapping</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cada servicio de cejas y pestañas empieza con un mapeo hecho para tus rasgos, no una plantilla generica." data-en="Every brow and lash service starts with mapping built around your features, not a one-size template.">Every brow and lash service starts with mapping built around your features, not a one-size template.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Estudio privado" data-en="Private studio">Private studio</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Una clienta a la vez en un estudio privado en el centro de Miami, a minutos de Brickell y Edgewater." data-en="One client at a time in a private studio in Downtown Miami, minutes from Brickell and Edgewater.">One client at a time in a private studio in Downtown Miami, minutes from Brickell and Edgewater.</p>
        </div>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_WHY + h[reviews_grid.end():]

rep('<a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver el menu completo y reservar" data-en="See the full menu and book">See the full menu and book</a>')
print("ESPECIALIDADES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1442 NE Miami Court, Suite 217, Miami, FL 33132</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=1442+NE+Miami+Court,+Miami,+FL+33132"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa en linea: eliges servicio, dia y hora, y la confirmacion es inmediata." data-en="By appointment online: pick the service, day and time, and the confirmation is instant.">By appointment online: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,160,0.4)]" href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,160,0.4)]" href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los tratamientos mas recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest treatments and DM any questions before your appointment.">See the latest treatments and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: 305 Esthetics, 1442 NE Miami Court, Miami FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=1442+NE+Miami+Court,+Miami,+FL+33132&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Cejas, pestañas, piel." data-en="Brows, lashes, skin.">Brows, lashes, skin.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo brillo" data-en="Your next glow">Your next glow</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu laminado de cejas, tu lash lift, o tu combo de HydraFacial." data-en="Book online in seconds: your brow lamination, lash lift, or HydraFacial combo.">Book online in seconds: your brow lamination, lash lift, or HydraFacial combo.</p>')
rep('<a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">305 Esthetics</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(238,190,240,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="305 Esthetics" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(238,190,240,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">305 Esthetics</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de estetica en el centro de Miami, FL. Atencion con cita previa." data-en="Esthetics studio in Downtown Miami, FL. By appointment only.">Esthetics studio in Downtown Miami, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>1442 NE Miami Court, Suite 217, Miami, FL 33132</p>')
rep('<p><a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#eebef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#eebef0]" data-es="Reservas en linea" data-en="Online booking">Online booking</a></p>')
rep('<p><a href="https://www.instagram.com/305esthetics/" target="_blank" rel="noopener" class="hover:text-[#eebef0]">Instagram · @305esthetics</a></p>',
    '<p><a href="https://www.instagram.com/305esthetics/" target="_blank" rel="noopener" class="hover:text-[#eebef0]">Instagram · @305esthetics</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 305 Esthetics.</p>')
print("FOOTER done")

# book-float
rep('<a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://305esthetics.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
