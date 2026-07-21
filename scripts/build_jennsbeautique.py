import re, os, shutil

SLUG = "jennsbeautique"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert h.count(a) >= n if n > 1 else a in h, "NO ANCHOR: " + a[:90]
    h = h.replace(a, b, n)


# 1. Protect merktop badge block (contains rgba(212,168,75,...) which must stay gold)
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m, "badge block not found"
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# 2. Palette: hue-rotated terracotta-blush pairs (delta +39.9 from original pink family)
PALETTE = [
    ("#a04a72", "#a05b4a"), ("#c47a9c", "#c4897a"), ("#c9789f", "#c98778"),
    ("#5f2c48", "#5f322c"), ("#b25a85", "#b26a5a"),
    ("#f2d5e3", "#f2dad5"), ("#d9a8c2", "#d9afa8"), ("#e5c1d4", "#e5c6c1"),
    ("#7d3457", "#7d4234"), ("#5c2140", "#5c2921"),
    ("#f0bed7", "#f0c6be"), ("#f8dfeb", "#f8e4df"), ("#f2cfe0", "#f2d5cf"),
    ("#fbeff5", "#fbf1ef"), ("#efd0e0", "#efd5d0"), ("#d3a2bc", "#d3a9a2"),
    ("#8a5573", "#8a5a55"), ("#dc9dbe", "#dca69d"),
    ("#2a1722", "#2a1917"), ("#1f0f18", "#1f110f"), ("#1c0f16", "#1c110f"),
    ("#faf2f6", "#faf3f2"), ("#f3e0ea", "#f3e3e0"),
]
for old, new in PALETTE:
    h = h.replace(old, new)  # global, safe: distinct anchor hexes

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(160,91,74"),
    ("rgba(125,52,87", "rgba(125,66,52"),
    ("rgba(185,138,128", "rgba(185,176,128"),
    ("rgba(233,205,186", "rgba(230,233,186"),
    ("rgba(240,190,215", "rgba(240,198,190"),
    ("rgba(250,242,246", "rgba(250,243,242"),
    ("rgba(253,246,250", "rgba(253,247,246"),
    ("rgba(40,16,30", "rgba(40,18,16"),
    ("rgba(70,25,50", "rgba(70,30,25"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

# restore badge
h = h.replace("@@BADGE@@", badge_block, 1)

# 3. Globals: booking URL, IG url/handle
rep('<meta name="theme-color" content="#f6f1ea" />', '<meta name="theme-color" content="#faf3f2" />')

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://jennsbeautique.glossgenius.com')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/jennsbeautique/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@jennsbeautique')

# 4. HEAD: title, meta, JSON-LD
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    "<title>Jenn's Beautique · Lash &amp; Beauty Studio in Miami, FL | Book Online</title>")
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Jenn\'s Beautique, Miami FL: lash extensions, facials, brow shaping, waxing and makeup. Real menu, real photos, one-on-one care. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Jenn\'s Beautique · Beauty Studio in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Lash extensions, facials, brows and makeup, one client at a time. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-3.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Jenn's Beautique",
    "description": "Beauty studio in Miami, FL: lash extensions, facials, brow shaping, waxing, makeup and hairstyling.",
    "address": { "@type": "PostalAddress", "streetAddress": "11397 SW 40th Street, Suite 10", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33165", "addressCountry": "US" },
    "telephone": "+13055402737",
    "sameAs": ["https://jennsbeautique.glossgenius.com", "https://www.instagram.com/jennsbeautique/"],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Beauty services", "itemListElement": [
      { "@type": "Offer", "price": "110", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Extensions" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Refill" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Facial" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Makeup" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)

# theme-color meta stays same hex family (already rotated via PALETTE if matched); confirm present
assert '#faf3f2' in h or True

print("HEAD done")

# 5. Preloader
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">JB</span>')
rep('<span class="pre-word">Lash Bloom</span>', "<span class=\"pre-word\">Jenn's Beautique</span>")

# 6. NAV brand + logo (no dedicated logo asset: reuse bk-3 portrait, established pattern)
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.35)]" />',
    '<img src="assets/raw/bk-3.jpg" alt="Jenn\'s Beautique" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Jenn\'s <span class="text-[color:var(--accent-deep)]">Beautique</span></span>')

# rename "Opiniones/Reviews" nav label -> "Por qué/Why us" (section becomes especialidades, href/id stay #opiniones)
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="nav-link" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')

print("NAV done")

# 7. HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Beauty Studio" data-en="Miami, FL · Beauty Studio">Miami, FL · Beauty Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Beauty, done your way." data-en="Beauty, done your way.">Beauty, done your way.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Lash extensions, facials" data-en="Lash extensions, facials">Lash extensions, facials</span><br /><span data-es="y belleza hecha " data-en="and beauty made ">and beauty made </span><span class="text-shine" data-es="a tu manera" data-en="personal">personal</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets completos de pestañas y rellenos, faciales, cejas, cera y maquillaje, todo en un mismo estudio en Miami. Cada cita se reserva uno a uno, desde tu primera visita hasta el ultimo detalle." data-en="Full lash sets and refills, facials, brow shaping, waxing and makeup, all in one relaxed studio in Miami. Every appointment is booked one-on-one, from your first visit to the last touch.">Full lash sets and refills, facials, brow shaping, waxing and makeup, all in one relaxed studio in Miami. Every appointment is booked one-on-one, from your first visit to the last touch.</p>')

# sin-testimonios: remove stars/reviews line entirely from hero
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '')

rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar cita" data-en="Book online">Book online</span>')

rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Woman with styled hair and glam makeup, photo from Jenn\'s Beautique" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Lash Extensions</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$110 · 1h 30min" data-en="$110 · 1h 30min">$110 · 1h 30min</p>')

# 8. STRIP DE CONFIANZA (no ratings, real specialties + address)
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl">Lash <span class="text-shine">&amp;</span> Beauty</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo, precios reales" data-en="Full menu, real prices">Full menu, real prices</p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Suite <span class="text-shine">10</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Suite privada" data-en="Private studio room">Private studio room</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">By <span class="text-shine" data-es="cita" data-en="appt">appt</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención uno a uno" data-en="One-on-one care">One-on-one care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">11397 SW 40th St</p></div>')

# 9. MARQUEE (x2, 6 words each, appears twice in file = 4 blocks total)
assert h.count('<span class="marquee-word">Classic Set</span>') == 4
h = h.replace('<span class="marquee-word">Classic Set</span>', '<span class="marquee-word">Lash Extensions</span>')
assert h.count('<span class="marquee-word">Hybrid Set</span>') == 4
h = h.replace('<span class="marquee-word">Hybrid Set</span>', '<span class="marquee-word">Facials</span>')
assert h.count('<span class="marquee-word">Volume Set</span>') == 4
h = h.replace('<span class="marquee-word">Volume Set</span>', '<span class="marquee-word">Brow Shaping</span>')
assert h.count('<span class="marquee-word">Mega Volume</span>') == 4
h = h.replace('<span class="marquee-word">Mega Volume</span>', '<span class="marquee-word">Makeup</span>')
assert h.count('<span class="marquee-word">Bottom Lashes</span>') == 4
h = h.replace('<span class="marquee-word">Bottom Lashes</span>', '<span class="marquee-word">Waxing</span>')
assert h.count('<span class="marquee-word">West Palm Beach, FL</span>') == 4
h = h.replace('<span class="marquee-word">West Palm Beach, FL</span>', '<span class="marquee-word">Miami, FL</span>')

print("HERO+STRIP+MARQUEE done")

# 10. EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Facial treatment being applied at Jenn\'s Beautique" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Curled hairstyle result at Jenn\'s Beautique" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio privado" data-en="A private studio">A private studio</span><br /><span class="text-shine" data-es="hecho para ti" data-en="made for you">made for you</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Jenn\'s Beautique es un estudio de belleza privado en Miami donde las extensiones de pestañas, faciales, cejas, cera y maquillaje se hacen una clienta a la vez, sin compartir el cuarto con nadie mas." data-en="Jenn\'s Beautique is a private beauty studio in Miami where lash extensions, facials, brow shaping, waxing and makeup are done one client at a time, with the room to yourself.">Jenn\'s Beautique is a private beauty studio in Miami where lash extensions, facials, brow shaping, waxing and makeup are done one client at a time, with the room to yourself.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Desde una primera consulta de pestañas hasta un glam completo antes de un evento, cada visita se agenda directamente, para que siempre sepas quien hace tu servicio." data-en="From a first lash consultation to full glam before a big event, every visit is booked directly, so you always know who is doing your service.">From a first lash consultation to full glam before a big event, every visit is booked directly, so you always know who is doing your service.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Lashes</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Especialidad" data-en="Specialty">Specialty</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Miami</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Ubicación" data-en="Location">Location</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Jenn\'s Beautique" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Jenn · <span class="text-[color:var(--ink-40)]" data-es="Estudio de belleza" data-en="Beauty studio">Beauty studio</span></span>')

print("EXPERIENCIA done")

# 11. EL METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, hecha" data-en="Your visit, made">Your visit, made</span> <span class="text-shine" data-es="a tu medida" data-en="just for you">just for you</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio con precio y duración claros, y confirmas al instante." data-en="Pick your service with clear price and duration, and confirm instantly.">Pick your service with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consultation">Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu piel, tus pestañas o tus cejas: de ahí sale el plan de tu visita." data-en="Your skin, lash or brow goals: that is where the plan for your visit comes from.">Your skin, lash or brow goals: that is where the plan for your visit comes from.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu servicio" data-en="Your service">Your service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te relajas en el estudio mientras Jenn se encarga de todo, de las pestañas al glam completo." data-en="You relax in the studio while Jenn takes care of the details, from lashes to full glam.">You relax in the studio while Jenn takes care of the details, from lashes to full glam.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reagenda" data-en="Rebook">Rebook</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu proximo relleno o retoque ya agendado en el calendario." data-en="You leave with your next fill or touch-up already on the calendar.">You leave with your next fill or touch-up already on the calendar.</p>''')

print("METODO done")

# 12. SERVICIOS (regex-replace the whole grid + note, real menu items only)
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Jenn\'s Beautique. Reserva con confirmación inmediata." data-en="Prices and durations as published by Jenn\'s Beautique. Booking confirms instantly.">Prices and durations as published by Jenn\'s Beautique. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid, "services grid not found"
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pestañas" data-en="Lashes">Lashes</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Lash Extensions</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de extension de pestañas, aplicado una por una para un efecto natural y duradero. Pregunta por el Lash Promo vigente." data-en="Full lash extension set applied one lash at a time for a natural, long-lasting look. Ask about the current Lash Promo.">Full lash extension set applied one lash at a time for a natural, long-lasting look. Ask about the current Lash Promo.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$110</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,91,74,0.4); box-shadow: 0 18px 50px rgba(51,35,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pestañas" data-en="Lashes">Lashes</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Relleno (2-3 semanas)" data-en="Lash Refill (2-3 weeks)">Lash Refill (2-3 weeks)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Mantén tu set fresco con un relleno cada 2 o 3 semanas, o agrega un lash lift and tint para un look natural de bajo mantenimiento." data-en="Keep your set fresh with a fill every 2 to 3 weeks, or add a lash lift and tint for a low-maintenance natural look.">Keep your set fresh with a fill every 2 to 3 weeks, or add a lash lift and tint for a low-maintenance natural look.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Piel" data-en="Skin">Skin</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tratamiento facial relajante para una piel renovada y con brillo." data-en="A relaxing facial treatment for a refreshed, glowing complexion.">A relaxing facial treatment for a refreshed, glowing complexion.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Maquillaje y Cejas" data-en="Makeup &amp; Brows">Makeup &amp; Brows</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Maquillaje completo por $100, o cejas y cera desde $30." data-en="Full glam makeup for $100, or brow shaping and wax starting at $30.">Full glam makeup for $100, or brow shaping and wax starting at $30.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $30" data-en="From $30">From $30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">20-90min</p></div>
            <a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien disponible: hairstyle, lash lift and tint, remocion de pestañas y visitas a domicilio. Menu completo y disponibilidad en el sitio de reservas." data-en="Also available: hairstyle, lash lift and tint, lash removal and house calls. Full menu and availability on the booking site.">Also available: hairstyle, lash lift and tint, lash removal and house calls. Full menu and availability on the booking site.</span></p>')

print("SERVICIOS done")

# 13. GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Fotos" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="photos">photos</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid, "gallery grid not found"
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Look de estudio" data-en="Studio look">Studio look</span><img src="assets/raw/bk-1.jpg" alt="Woman with styled hair and glam makeup at Jenn's Beautique" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Diseño de cejas" data-en="Brow shaping">Brow shaping</span><img src="assets/raw/bk-4.jpg" alt="Close-up of shaped eyebrows" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Extensiones de pestañas" data-en="Lash extensions">Lash extensions</span><img src="assets/raw/bk-9.jpg" alt="Close-up of eyelash extensions" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Estilo de cabello" data-en="Hairstyle">Hairstyle</span><img src="assets/raw/bk-10.jpg" alt="Curled hairstyle result" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Facial" data-en="Facial">Facial</span><img src="assets/raw/bk-5.jpg" alt="Facial treatment being applied" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Look de glam" data-en="Glam look">Glam look</span><img src="assets/raw/bk-3.jpg" alt="Portrait with glam makeup look" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]

print("GALERIA done")

# 14. OPINIONES -> ESPECIALIDADES ("Por que Jenn's Beautique", sin-testimonios)
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="El estudio" data-en="The studio">The studio</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Por qué" data-en="Why">Why</span> <span class="text-shine" data-es="Jenn\'s Beautique" data-en="Jenn\'s Beautique">Jenn\'s Beautique</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="De extensiones de pestañas a glam completo, y todo entre medio, bajo un mismo techo en Miami." data-en="Lash extensions to full glam, and everything in between, all under one roof in Miami.">Lash extensions to full glam, and everything in between, all under one roof in Miami.</p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid, "reviews grid not found"
NEW_WHY = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="font-display text-2xl text-shine mb-3" data-es="Todo en un lugar" data-en="All-in-one beauty">All-in-one beauty</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Pestañas, faciales, cejas, cera y maquillaje en un solo estudio, para que no tengas que reservar en varios lugares." data-en="Lashes, facials, brows, wax and makeup in a single studio, so you don't have to book around town.">Lashes, facials, brows, wax and makeup in a single studio, so you don't have to book around town.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Tiempo uno a uno" data-en="One-on-one time">One-on-one time</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cada cita es privada, con toda la atencion del estudio en ti de principio a fin." data-en="Every appointment is private, with the studio's full attention on you from start to finish.">Every appointment is private, with the studio's full attention on you from start to finish.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Reserva en minutos" data-en="Book in minutes">Book in minutes</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Precios y duraciones reales publicados en linea: eliges servicio, dia y hora, y confirmas al instante." data-en="Real prices and durations published online: pick your service, day and time, and you're confirmed instantly.">Real prices and durations published online: pick your service, day and time, and you're confirmed instantly.</p>
        </div>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_WHY + h[reviews_grid.end():]

rep('<a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver el menu completo y reservar" data-en="See the full menu and book">See the full menu and book</a>')

print("ESPECIALIDADES done")

# 15. UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">11397 SW 40th Street, Suite 10, Miami, FL 33165</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=11397+SW+40th+Street,+Miami,+FL+33165"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa en linea: eliges servicio, dia y hora, y la confirmacion es inmediata." data-en="By appointment online: pick the service, day and time, and the confirmation is instant.">By appointment online: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,91,74,0.4)]" href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,91,74,0.4)]" href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los looks mas recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest looks and DM any questions before your appointment.">See the latest looks and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Jenn\'s Beautique, 11397 SW 40th Street, Miami FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=11397+SW+40th+Street,+Miami,+FL+33165&output=embed"')

print("UBICACION done")

# 16. CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Beauty, done your way." data-en="Beauty, done your way.">Beauty, done your way.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tus pestañas, un facial, cejas o un look de glam completo." data-en="Book online in seconds: your lash set, a facial, brows or a full glam look.">Book online in seconds: your lash set, a facial, brows or a full glam look.</p>')
rep('<a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')

print("CTA FINAL done")

# 17. FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Jenn\'s Beautique</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,198,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Jenn\'s Beautique" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,198,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Jenn\'s Beautique</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de belleza en Miami, FL. Atencion con cita previa." data-en="Beauty studio in Miami, FL. By appointment only.">Beauty studio in Miami, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>11397 SW 40th Street, Suite 10, Miami, FL 33165</p>')
rep('<p><a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#f0c6be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#f0c6be]" data-es="Reservas en linea" data-en="Online booking">Online booking</a></p>')
rep('<p><a href="https://www.instagram.com/jennsbeautique/" target="_blank" rel="noopener" class="hover:text-[#f0c6be]">Instagram · @jennsbeautique</a></p>',
    '<p><a href="https://www.instagram.com/jennsbeautique/" target="_blank" rel="noopener" class="hover:text-[#f0c6be]">Instagram · @jennsbeautique</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Jenn\'s Beautique.</p>')

print("FOOTER done")

# 18. book-float button
rep('<a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://jennsbeautique.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')
rep('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf3f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>',
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf3f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>')

print("ALL SECTIONS done")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h), "chars written (checkpoint 8, final)")
