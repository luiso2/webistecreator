import re, os, shutil

SLUG = "valashstudio"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:90]
    h = h.replace(a, b, 1)


# 1. Proteger el badge Merktop (dorado) antes de tocar paleta
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# 2. PALETA: rosa-pink brillante -> berenjena/ciruela (accent-deep ~#8a4a6b, accent-mid ~#b579a0)
PALETTE = [
    ("#faf2f6", "#f7f0f3"),   # bg
    ("#f3e0ea", "#ecdce6"),   # bg-2 / accent-soft
    ("#33222c", "#2f2430"),   # ink / dark-band btn-3d text
    ("#a04a72", "#8a4a6b"),   # accent-deep
    ("#c47a9c", "#b579a0"),   # accent-mid
    ("#c9789f", "#c690ae"),   # text-shine stop 2
    ("#5f2c48", "#5c2c46"),   # text-shine/step-num darkest
    ("#b25a85", "#a15b82"),   # text-shine stop 5
    ("#7d3457", "#74395a"),   # btn-3d gradient bottom / scroll-progress start
    ("#5c2140", "#4a1a35"),   # btn sole shadow / book-float sole
    ("#f2d5e3", "#eed3e2"),   # orb-a light
    ("#d9a8c2", "#c9a0bb"),   # orb-b light + dark-band text-shine stop 3
    ("#e5c1d4", "#ddc0d3"),   # orb-c light
    ("#f0bed7", "#e8bdd6"),   # dark-band text-shine stop 1/4, stars, footer hover
    ("#f8dfeb", "#f4e2ee"),   # dark-band text-shine stop 2
    ("#f2cfe0", "#e6cbdd"),   # dark-band text-shine stop 5
    ("#fbeff5", "#f7eef4"),   # dark-band btn-3d gradient stop 1
    ("#efd0e0", "#e9d0e2"),   # dark-band btn-3d gradient stop 2
    ("#d3a2bc", "#c9a2ba"),   # dark-band btn-3d gradient stop 3
    ("#8a5573", "#7a4d68"),   # dark-band btn-3d sole shadow
    ("#dc9dbe", "#d59bc0"),   # scroll-progress highlight stop
    ("#2a1722", "#2a1a26"),   # CTA final gradient stop 1
    ("#1f0f18", "#1c1016"),   # CTA final gradient stop 2
    ("#1c0f16", "#1b0f18"),   # footer bg
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(138,74,107"),   # accent-deep based (glass, ghost, glow, btn-ghost...)
    ("rgba(51,34,44", "rgba(47,36,48"),       # ink based shadows
    ("rgba(70,25,50", "rgba(60,26,46"),       # btn-3d dark inset shadow
    ("rgba(233,205,186", "rgba(201,160,187"), # dark-band accent-ghost
    ("rgba(240,190,215", "rgba(232,189,214"), # dark-band pink accent family
    ("rgba(185,138,128", "rgba(176,133,163"), # dark-band orb-b
    ("rgba(125,52,87", "rgba(107,51,80"),     # dark-band btn-3d shadow
    ("rgba(250,242,246", "rgba(247,240,243"), # dark-band ink-60/40 + nav.scrolled bg
    ("rgba(253,246,250", "rgba(250,244,248"), # glass-hover bg
    ("rgba(40,16,30", "rgba(35,17,29"),       # tile-cap dark overlay
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# 3. GLOBALES: Booksy, Instagram
BOOKSY = "https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami"
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BOOKSY)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/valash_studio.miami/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@valash_studio.miami')

# Idioma: negocio en espanol -> default es
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

# 4. HEAD
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Valash Studio · Salón de Belleza en Miami, FL | 4.9 en Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Valash Studio, Miami FL (Calle Ocho): cortes, keratinas, extensiones y blow-drys, mas unas, pestanas y cejas, con un 4.9 en 88 resenas de Booksy. Reserva online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Valash Studio · Salón de Belleza en Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Cortes, keratinas, extensiones y mas. 4.9 en Booksy. Reserva online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-3.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "Valash Studio",
    "description": "Salon de belleza en Miami, FL (Calle Ocho): cortes, keratinas, extensiones y blow-drys, ademas de unas, pestanas y cejas.",
    "address": { "@type": "PostalAddress", "streetAddress": "5798 SW 8th St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33144", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.76407000967013, "longitude": -80.27360000000002 },
    "sameAs": ["https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami", "https://www.instagram.com/valash_studio.miami/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "88", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday"], "opens": "09:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday", "Friday"], "opens": "09:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de belleza", "itemListElement": [
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hair cut" } },
      { "@type": "Offer", "price": "250", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Ybera keratin" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Blow-Dry" } },
      { "@type": "Offer", "price": "1000", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hair extensions" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# NAV / PRELOADER
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">VS</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Valash Studio</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />'.replace("160,74,114", "138,74,107"),
    '<img src="assets/raw/bk-1.jpg" alt="Valash Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,74,107,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Valash <span class="text-[color:var(--accent-deep)]">Studio</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Calle Ocho, Miami, FL · Salón de Belleza" data-en="Calle Ocho, Miami, FL · Hair &amp; Beauty Salon">Calle Ocho, Miami, FL · Hair &amp; Beauty Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Belleza real, resultados que se notan." data-en="Real beauty, results that show.">Real beauty, results that show.</p>\n        <h1',)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Cortes, keratinas" data-en="Haircuts, keratin treatments">Haircuts, keratin treatments</span><br /><span data-es="y extensiones, hechas para " data-en="and extensions, made to ">and extensions, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Valash Studio es el salón de belleza de Juliana en el corazón de Calle Ocho: cortes, keratinas, extensiones y blow-drys, además de uñas, pestañas y cejas en un solo lugar. Un 4.9 de calificación con 88 reseñas respaldan cada cita." data-en="Valash Studio is Juliana&#39;s beauty salon in the heart of Calle Ocho: haircuts, keratin treatments, extensions and blow-drys, plus nails, lashes and brows all under one roof. A 4.9 rating across 88 reviews backs every appointment.">Valash Studio is Juliana&#39;s beauty salon in the heart of Calle Ocho: haircuts, keratin treatments, extensions and blow-drys, plus nails, lashes and brows all under one roof. A 4.9 rating across 88 reviews backs every appointment.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.9 · 88 reseñas en Booksy" data-en="4.9 · 88 reviews on Booksy">4.9 · 88 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-3.jpg" alt="Clienta sonriendo con cabello largo ondulado frente al letrero neón de Valash Studio" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Ybera Keratin" data-en="Ybera Keratin">Ybera Keratin</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$250" data-en="$250">$250</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="88">88</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Cabello <span class="text-shine">&amp;</span> Belleza</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cortes, keratinas y más" data-en="Cuts, keratin and more">Cuts, keratin and more</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">26 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">SW 8th St · Calle Ocho</p></div>')

for old, new in [
    ('Classic Set', 'Corte'),
    ('Hybrid Set', 'Keratin'),
    ('Volume Set', 'Extensiones'),
    ('Mega Volume', 'Blow-Dry'),
    ('Bottom Lashes', 'Uñas y Pestañas'),
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
    '<img src="assets/raw/bk-16.jpg" alt="Tratamiento facial en Valash Studio con mascarilla en forma de corazón" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-12.jpg" alt="Depilación de cejas con hilo en proceso en Valash Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">La experiencia</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un salón," data-en="One salon,">One salon,</span><br /><span class="text-shine" data-es="hecho a tu medida" data-en="made just for you">made just for you</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Valash Studio es el salón de belleza de Juliana Ramirez en Calle Ocho, Miami. Cortes, keratinas, blow-drys y extensiones conviven con uñas, pestañas y cejas en un mismo espacio, pensado para que salgas con el look completo en una sola visita." data-en="Valash Studio is Juliana Ramirez&#39;s beauty salon on Calle Ocho, Miami. Haircuts, keratin treatments, blow-drys and extensions share the space with nails, lashes and brows, so you can leave with the full look in one visit.">Valash Studio is Juliana Ramirez&#39;s beauty salon on Calle Ocho, Miami. Haircuts, keratin treatments, blow-drys and extensions share the space with nails, lashes and brows, so you can leave with the full look in one visit.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 4.9 de calificación en 88 reseñas verificadas en Booksy, y clientas que repiten cita por la atención y el ambiente del salón." data-en="The result: a 4.9 rating across 88 verified Booksy reviews, and clients who rebook for the care and the vibe of the salon.">The result: a 4.9 rating across 88 verified Booksy reviews, and clients who rebook for the care and the vibe of the salon.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="88">88</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />'.replace("160,74,114", "138,74,107"),
    '<img src="assets/raw/bk-1.jpg" alt="Juliana" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,74,107,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Juliana · <span class="text-[color:var(--ink-40)]" data-es="Estilista principal" data-en="Lead stylist">Lead stylist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, con" data-en="Your visit, with">Your visit, with</span> <span class="text-shine" data-es="calma y detalle" data-en="care and detail">care and detail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy, desde un corte hasta un set de uñas, con precio y duración claros." data-en="Pick your service on Booksy, from a haircut to a nail set, with clear price and duration.">Pick your service on Booksy, from a haircut to a nail set, with clear price and duration.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Diagnóstico" data-en="Consultation">Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Antes de cualquier tratamiento, Juliana evalúa tu cabello, uñas o mirada para armar el resultado que buscas." data-en="Before any treatment, Juliana checks your hair, nails or eyes to build exactly the look you want.">Before any treatment, Juliana checks your hair, nails or eyes to build exactly the look you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="Hands at work">Hands at work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te sientas, te relajas y el equipo trabaja con calma, desde una keratina hasta un set completo de pestañas." data-en="You sit back and relax while the team works with care, from a keratin treatment to a full lash set.">You sit back and relax while the team works with care, from a keratin treatment to a full lash set.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida lista" data-en="Ready to go">Ready to go</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el look terminado y, si aplica, tu próxima cita de mantenimiento ya agendada." data-en="You leave with the finished look and, if needed, your next touch-up already booked.">You leave with the finished look and, if needed, your next touch-up already booked.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Valash Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Valash Studio on Booksy. Booking confirms instantly.">Prices and durations as published by Valash Studio on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cabello" data-en="Hair">Hair</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte de Cabello" data-en="Haircut">Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte personalizado según tu tipo de cabello y el look que buscas, con acabado profesional." data-en="A personalized cut based on your hair type and the look you want, finished to a professional standard.">A personalized cut based on your hair type and the look you want, finished to a professional standard.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(138,74,107,0.4); box-shadow: 0 18px 50px rgba(47,36,48,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Ybera Keratin" data-en="Ybera Keratin">Ybera Keratin</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tratamiento de keratina Ybera que alisa, nutre y da brillo, ideal para controlar el frizz por semanas." data-en="Ybera keratin treatment that smooths, nourishes and adds shine, built to control frizz for weeks.">Ybera keratin treatment that smooths, nourishes and adds shine, built to control frizz for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$250</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Rápido y con estilo" data-en="Quick &amp; styled">Quick &amp; styled</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Blow-Dry</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Secado y peinado profesional para salir lista en minutos, perfecto antes de cualquier evento." data-en="Professional blow-dry and style to walk out ready in minutes, perfect before any event.">Professional blow-dry and style to walk out ready in minutes, perfect before any event.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Transformación total" data-en="Full transformation">Full transformation</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Extensiones de Cabello" data-en="Hair Extensions">Hair Extensions</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensiones para más largo y densidad, aplicadas a la medida de tu cabello natural." data-en="Extensions for extra length and density, applied to match your natural hair.">Extensions for extra length and density, applied to match your natural hair.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$1,000</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

old_note = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>'
assert old_note in h
CATEGORY_BLOCKS = '''<div class="grid sm:grid-cols-3 gap-5 mt-10">
        <div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-xl mb-4" data-es="Uñas" data-en="Nails">Nails</h3>
          <ul class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span data-es="Manicura Regular" data-en="Regular Manicure">Regular Manicure</span><span class="text-[color:var(--ink)] font-medium">$25</span></li>
            <li class="flex justify-between gap-3"><span data-es="Manicura Gel" data-en="Gel Manicure">Gel Manicure</span><span class="text-[color:var(--ink)] font-medium">$35</span></li>
            <li class="flex justify-between gap-3"><span data-es="Pedicura Regular" data-en="Regular Pedicure">Regular Pedicure</span><span class="text-[color:var(--ink)] font-medium">$35</span></li>
            <li class="flex justify-between gap-3"><span data-es="Pedicura Gel · 1h 15min" data-en="Gel Pedicure · 1h 15min">Gel Pedicure · 1h 15min</span><span class="text-[color:var(--ink)] font-medium">$45</span></li>
            <li class="flex justify-between gap-3"><span data-es="Uñas Acrílicas" data-en="Acrylic Nails">Acrylic Nails</span><span class="text-[color:var(--ink)] font-medium">$60</span></li>
            <li class="flex justify-between gap-3"><span data-es="Relleno Acrílico" data-en="Refill Acrylic">Refill Acrylic</span><span class="text-[color:var(--ink)] font-medium">$50</span></li>
            <li class="flex justify-between gap-3"><span data-es="Rubber Base" data-en="Rubber Base">Rubber Base</span><span class="text-[color:var(--ink)] font-medium">$60</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:90ms">
          <h3 class="font-display text-xl mb-4" data-es="Pestañas" data-en="Lashes">Lashes</h3>
          <ul class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span>Apress</span><span class="text-[color:var(--ink)] font-medium">$65</span></li>
            <li class="flex justify-between gap-3"><span data-es="Pack Classic" data-en="Pack Classic">Pack Classic</span><span class="text-[color:var(--ink)] font-medium">$50</span></li>
            <li class="flex justify-between gap-3"><span data-es="Long Apress" data-en="Long Apress">Long Apress</span><span class="text-[color:var(--ink)] font-medium">$75</span></li>
            <li class="flex justify-between gap-3"><span data-es="Pestañas Classic" data-en="Classic Lashes">Classic Lashes</span><span class="text-[color:var(--ink)] font-medium">$80</span></li>
            <li class="flex justify-between gap-3"><span data-es="Pestañas Hybrid" data-en="Hybrid Lashes">Hybrid Lashes</span><span class="text-[color:var(--ink)] font-medium">$85</span></li>
            <li class="flex justify-between gap-3"><span data-es="Full Set Lashes" data-en="Full Set Lashes">Full Set Lashes</span><span class="text-[color:var(--ink)] font-medium">$90</span></li>
            <li class="flex justify-between gap-3"><span data-es="Lash Lift" data-en="Lash Lift">Lash Lift</span><span class="text-[color:var(--ink)] font-medium">$85</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:180ms">
          <h3 class="font-display text-xl mb-4" data-es="Cejas y Rostro" data-en="Brows &amp; Face">Brows &amp; Face</h3>
          <ul class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span data-es="Depilación de Cejas con Hilo" data-en="Eyebrow Threading">Eyebrow Threading</span><span class="text-[color:var(--ink)] font-medium">$25</span></li>
            <li class="flex justify-between gap-3"><span data-es="Tinte + Diseño" data-en="Tint + Desing">Tint + Desing</span><span class="text-[color:var(--ink)] font-medium">$25</span></li>
            <li class="flex justify-between gap-3"><span data-es="Laminado de Cejas" data-en="Brow Lamination">Brow Lamination</span><span class="text-[color:var(--ink)] font-medium">$80</span></li>
            <li class="flex justify-between gap-3"><span data-es="Depilación de Cejas con Cera" data-en="Eyebrow Waxing">Eyebrow Waxing</span><span class="text-[color:var(--ink)] font-medium">$25</span></li>
            <li class="flex justify-between gap-3"><span data-es="Powder Brows · 1h 30min" data-en="Powder Brows · 1h 30min">Powder Brows · 1h 30min</span><span class="text-[color:var(--ink)] font-medium">$150</span></li>
            <li class="flex justify-between gap-3"><span data-es="Microblading · 1h 30min" data-en="Microblading · 1h 30min">Microblading · 1h 30min</span><span class="text-[color:var(--ink)] font-medium">$150</span></li>
            <li class="flex justify-between gap-3"><span data-es="Limpieza Facial" data-en="Facial Cleansing">Facial Cleansing</span><span class="text-[color:var(--ink)] font-medium">$120</span></li>
          </ul>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: Detox capilar $150 (1h 30min). Menú completo de 26 servicios y disponibilidad en Booksy." data-en="Also: hair detox $150 (1h 30min). Full 26-service menu and availability on Booksy.">Also: hair detox $150 (1h 30min). Full 26-service menu and availability on Booksy.</span></p>'''
h = h.replace(old_note, CATEGORY_BLOCKS, 1)
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="work">work</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Spa de pies con rosas" data-en="Rose petal foot spa">Rose petal foot spa</span><img src="assets/raw/bk-4.jpg" alt="Pedicura spa con pétalos de rosa en Valash Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Stiletto azul con moño" data-en="Blue stiletto with bow">Blue stiletto with bow</span><img src="assets/raw/bk-8.jpg" alt="Uñas stiletto azules con detalle de moño dorado en Valash Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Ombré frente al letrero" data-en="Ombre by the sign">Ombre by the sign</span><img src="assets/raw/bk-5.jpg" alt="Manicura ombré con el letrero de Valash Studio de fondo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Mirada verde, pestañas nuevas" data-en="Green eyes, new lashes">Green eyes, new lashes</span><img src="assets/raw/bk-9.jpg" alt="Closeup de ojos verdes con extensiones de pestañas en Valash Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Lash lift natural" data-en="Natural lash lift">Natural lash lift</span><img src="assets/raw/bk-15.jpg" alt="Closeup de ojo azul con pestañas naturales realzadas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Detalle de powder brow" data-en="Powder brow detail">Powder brow detail</span><img src="assets/raw/bk-13.jpg" alt="Closeup de ceja con diseño de powder brow en Valash Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES (reales, con autor)
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 88 reseñas verificadas en Booksy" data-en="4.9 out of 5 · 88 verified reviews on Booksy">4.9 out of 5 · 88 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Juliana delivers every time, 10/10!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Aileen w…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing place I love the aesthetic and the service was perfect as well. They are all lovely"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Oriana A…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Un servicio increíble, el lugar es muy hermoso"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Valentina C…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>'.replace('519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', '1316533_valash-studio_brows-lashes_15889_miami'),
    '<a href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 88 reseñas en Booksy" data-en="Read all 88 reviews on Booksy">Read all 88 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Calle Ocho</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">5798 SW 8th St, Miami, FL 33144</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=5798+SW+8th+St,+Miami,+FL+33144"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: lunes a miércoles 9am-7pm, jueves y viernes 9am-8pm, sábados 10am-6pm." data-en="By appointment via Booksy: Monday to Wednesday 9am-7pm, Thursday and Friday 9am-8pm, Saturdays 10am-6pm.">By appointment via Booksy: Monday to Wednesday 9am-7pm, Thursday and Friday 9am-8pm, Saturdays 10am-6pm.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("160,74,114", "138,74,107").replace("166337_belleciia-nails_nail-salon_15886_hialeah", "1316533_valash-studio_brows-lashes_15889_miami"),
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,74,107,0.4)]" href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('''data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>''',
    '''data-es="Mira los looks más recientes de Juliana y escribe por DM cualquier duda antes de tu cita." data-en="See Juliana's latest looks and DM any questions before your appointment.">See Juliana's latest looks and DM any questions before your appointment.</p>''')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Valash Studio, 5798 SW 8th St, Miami FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=5798+SW+8th+St,+Miami,+FL+33144&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Belleza real, resultados que se notan." data-en="Real beauty, results that show.">Real beauty, results that show.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu corte, tu keratina o el servicio que ya te toca." data-en="Book online in seconds: your haircut, your keratin treatment, or whatever service you are due for.">Book online in seconds: your haircut, your keratin treatment, or whatever service you are due for.</p>')
rep('<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("166337_belleciia-nails_nail-salon_15886_hialeah", "1316533_valash-studio_brows-lashes_15889_miami"),
    '<a href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Valash Studio</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,189,214,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Valash Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,189,214,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Valash Studio</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de belleza en Miami, FL. Atención con cita previa." data-en="Beauty salon in Miami, FL. By appointment only.">Beauty salon in Miami, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>5798 SW 8th St, Miami, FL 33144</p>')
rep('<p><a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="hover:text-[#f0c0be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace("166337_belleciia-nails_nail-salon_15886_hialeah", "1316533_valash-studio_brows-lashes_15889_miami").replace("f0c0be", "e8bdd6"),
    '<p><a href="https://booksy.com/en-us/1316533_valash-studio_brows-lashes_15889_miami" target="_blank" rel="noopener" class="hover:text-[#e8bdd6]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/valash_studio.miami/" target="_blank" rel="noopener" class="hover:text-[#f0c0be]">Instagram · @valash_studio.miami</a></p>'.replace("f0c0be", "e8bdd6"),
    '<p><a href="https://www.instagram.com/valash_studio.miami/" target="_blank" rel="noopener" class="hover:text-[#e8bdd6]">Instagram · @valash_studio.miami</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Valash Studio.</p>')
print("FOOTER done")

# lang default -> es
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
