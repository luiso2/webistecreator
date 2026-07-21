import re, os, shutil

SLUG = "nailsbyarianne"
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
    ("#faf2f6", "#f5f2fa"), ("#f3e0ea", "#e7e0f3"), ("#a04a72", "#6e4aa0"),
    ("#c47a9c", "#997ac4"), ("#c9789f", "#9878c9"), ("#5f2c48", "#3d2c5f"),
    ("#b25a85", "#7d5ab2"), ("#f2d5e3", "#e1d5f2"), ("#d9a8c2", "#b9a8d9"),
    ("#e5c1d4", "#cec1e5"), ("#7d3457", "#51347d"), ("#5c2140", "#36215c"),
    ("#f0bed7", "#d1bef0"), ("#f8dfeb", "#e9dff8"), ("#f2cfe0", "#ddcff2"),
    ("#fbeff5", "#f4effb"), ("#efd0e0", "#dbd0ef"), ("#d3a2bc", "#b3a2d3"),
    ("#8a5573", "#66558a"), ("#dc9dbe", "#b49ddc"), ("#2a1722", "#1d172a"),
    ("#1f0f18", "#140f1f"), ("#1c0f16", "#130f1c"), ("#f6f1ea", "#f6eaf0"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(110,74,160"),
    ("rgba(125,52,87", "rgba(81,52,125"),
    ("rgba(185,138,128", "rgba(185,128,182"),
    ("rgba(233,205,186", "rgba(233,186,220"),
    ("rgba(240,190,215", "rgba(209,190,240"),
    ("rgba(250,242,246", "rgba(245,242,250"),
    ("rgba(253,246,250", "rgba(248,246,253"),
    ("rgba(40,16,30", "rgba(23,16,40"),
    ("rgba(70,25,50", "rgba(40,25,70"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://nailsbyarianne.glossgenius.com')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/nailsbyarianne_/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@nailsbyarianne_')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Nails By Arianne · Nail Studio in Miami Lakes, FL | Book Online</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nails By Arianne, Miami Lakes FL: intricate nail art, gel manicures, natural nail growth. Real menu, real photos. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nails By Arianne · Nail Studio in Miami Lakes, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Intricate nail art and gel manicures, one client at a time. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-4.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-9.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails By Arianne",
    "description": "Nail studio in Miami Lakes, FL: intricate nail art, gel manicures, natural nail growth and design sets.",
    "address": { "@type": "PostalAddress", "streetAddress": "15485 Eagle Nest Ln, Suite 110, Room 3", "addressLocality": "Miami Lakes", "addressRegion": "FL", "postalCode": "33014", "addressCountry": "US" },
    "telephone": "+17866348158",
    "sameAs": ["https://nailsbyarianne.glossgenius.com", "https://www.instagram.com/nailsbyarianne_/"],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "One Color Set" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Tier 2 Nail Art" } },
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Tier 4 Detailed Art" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Clear Gel Manicure" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NA</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nails By Arianne</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,74,160,0.35)]" />',
    '<img src="assets/raw/bk-9.jpg" alt="Nails By Arianne" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,74,160,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails By <span class="text-[color:var(--accent-deep)]">Arianne</span></span>')
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="nav-link" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami Lakes, FL · Estudio de Uñas" data-en="Miami Lakes, FL · Nail Studio">Miami Lakes, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Arte en cada mano." data-en="Art on every hand.">Art on every hand.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Nail art detallado" data-en="Intricate nail art">Intricate nail art</span><br /><span data-es="y cuidado de la uña " data-en="and natural nail ">and natural nail </span><span class="text-shine" data-es="natural" data-en="growth">growth</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Desde un color solido hasta arte cyber sigilism o kawaii nivel 4, cada set se construye a mano en un estudio privado en Miami Lakes, con la salud de tu uña natural siempre primero." data-en="From a simple one-color set to cyber sigilism or kawaii-level detailed art, every set is hand-built in a private studio in Miami Lakes, with the health of your natural nail always first.">From a simple one-color set to cyber sigilism or kawaii-level detailed art, every set is hand-built in a private studio in Miami Lakes, with the health of your natural nail always first.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar cita" data-en="Book online">Book online</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-4.jpg" alt="Hand-painted nail art set, close-up" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Tier 2, Moderado" data-en="Tier 2, Moderate">Tier 2, Moderate</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$90 · 1h 30min" data-en="$90 · 1h 30min">$90 · 1h 30min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl">Nail <span class="text-shine">Art</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo, precios reales" data-en="Full menu, real prices">Full menu, real prices</p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">4 <span class="text-shine" data-es="niveles" data-en="tiers">tiers</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Simple a arte avanzado" data-en="Simple to advanced art">Simple to advanced art</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">By <span class="text-shine" data-es="cita" data-en="appt">appt</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención uno a uno" data-en="One-on-one care">One-on-one care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Lakes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Eagle Nest Ln</p></div>')

for old, new in [
    ('Classic Set', 'One Color'),
    ('Hybrid Set', 'Tier 2 Art'),
    ('Volume Set', 'Tier 4 Art'),
    ('Mega Volume', 'Gel Manicure'),
    ('Bottom Lashes', 'Kawaii Style'),
    ('West Palm Beach, FL', 'Miami Lakes, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Blue chrome nail art design, close-up" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Orange and black nail art design, close-up" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="tu uña natural primero" data-en="your natural nail first">your natural nail first</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Nails By Arianne es el estudio privado de Ari, tecnica de uñas licenciada en Miami especializada en nail art detallado y crecimiento de uña natural. Sus estilos favoritos: cyber sigilism y kawaii." data-en="Nails By Arianne is the private studio of Ari, a licensed nail technician in Miami specializing in intricate nail art and natural nail growth. Her go-to styles: cyber sigilism and kawaii.">Nails By Arianne is the private studio of Ari, a licensed nail technician in Miami specializing in intricate nail art and natural nail growth. Her go-to styles: cyber sigilism and kawaii.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Cada set se construye segun el nivel de detalle que elijas, de un color solido a arte tier 4, siempre cuidando que tu uña natural crezca sana." data-en="Every set is built to the level of detail you choose, from a solid color to tier 4 art, always keeping your natural nail growing healthy.">Every set is built to the level of detail you choose, from a solid color to tier 4 art, always keeping your natural nail growing healthy.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Arte" data-en="Art">Art</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Especialidad" data-en="Specialty">Specialty</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Miami Lakes" data-en="Miami Lakes">Miami Lakes</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Ubicación" data-en="Location">Location</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,74,160,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Nails By Arianne" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,74,160,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Ari · <span class="text-[color:var(--ink-40)]" data-es="Tecnica de uñas licenciada" data-en="Licensed nail technician">Licensed nail technician</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu set, uña" data-en="Your set, nail">Your set, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu nivel de arte con precio y duración claros, y confirmas al instante." data-en="Pick your art tier with clear price and duration, and confirm instantly.">Pick your art tier with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Diseño" data-en="Design">Design</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de uña, referencias que traigas y el nivel de detalle definen el diseño, de simple a arte avanzado." data-en="Nail shape, any references you bring and the level of detail define the design, from simple to advanced art.">Nail shape, any references you bring and the level of detail define the design, from simple to advanced art.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un color solido de 1 hora a un tier 4 de 3 horas: cada set recibe el tiempo completo que necesita." data-en="From a 1-hour one-color set to a 3-hour tier 4: every set gets the full time it needs.">From a 1-hour one-color set to a 3-hour tier 4: every set gets the full time it needs.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu set terminado y las indicaciones para mantener tu uña natural sana." data-en="You leave with your finished set and the guidance to keep your natural nail growing healthy.">You leave with your finished set and the guidance to keep your natural nail growing healthy.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nails By Arianne. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nails By Arianne. Booking confirms instantly.">Prices and durations as published by Nails By Arianne. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="nivel" data-en="tier">tier</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Nivel 1" data-en="Tier 1">Tier 1</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Color Solido" data-en="One Color">One Color</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un color solido perfecto, sin arte, con acabado en gel de larga duracion." data-en="A perfect solid color set, no art, with a long-lasting gel finish.">A perfect solid color set, no art, with a long-lasting gel finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(110,74,160,0.4); box-shadow: 0 18px 50px rgba(51,35,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Nivel 2" data-en="Tier 2">Tier 2</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Arte Moderado" data-en="Moderate Art">Moderate Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseños con mas detalle: lineas finas, degradados o acentos, un balance entre simple y elaborado." data-en="More detailed designs: fine lines, gradients or accents, a balance between simple and elaborate.">More detailed designs: fine lines, gradients or accents, a balance between simple and elaborate.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Nivel 4" data-en="Tier 4">Tier 4</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Arte Detallado" data-en="Detailed Art">Detailed Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cyber sigilism, kawaii y otros disenos de alta complejidad, hechos a mano uno por uno." data-en="Cyber sigilism, kawaii and other high-complexity designs, hand-painted one by one.">Cyber sigilism, kawaii and other high-complexity designs, hand-painted one by one.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$130</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h</p></div>
            <a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel y Freestyle" data-en="Gel &amp; Freestyle">Gel &amp; Freestyle</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Clear gel manicure desde $30, o dejale a Ari el diseño completo con el freestyle/nail tech's choice." data-en="Clear gel manicure from $30, or let Ari design it freestyle with the nail tech's choice option.">Clear gel manicure from $30, or let Ari design it freestyle with the nail tech's choice option.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $30" data-en="From $30">From $30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min+</p></div>
            <a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: soak off, fix up y toe gel polish. Menu completo y disponibilidad en el sitio de reservas." data-en="Also available: soak off, fix up and toe gel polish. Full menu and availability on the booking site.">Also available: soak off, fix up and toe gel polish. Full menu and availability on the booking site.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Arte" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Detalle abstracto" data-en="Abstract detail">Abstract detail</span><img src="assets/raw/bk-8.jpg" alt="Orange and black abstract nail art design" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cromo azul" data-en="Blue chrome">Blue chrome</span><img src="assets/raw/bk-5.jpg" alt="Blue chrome nail art design" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Negro elegante" data-en="Sleek black">Sleek black</span><img src="assets/raw/bk-3.jpg" alt="Glossy black stiletto nail set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Blanco y negro" data-en="Black and white">Black and white</span><img src="assets/raw/bk-4.jpg" alt="Black and white nail art design" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Marmol francés" data-en="Marble french">Marble french</span><img src="assets/raw/bk-6.jpg" alt="Marbled french tip nail design" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Uña natural" data-en="Natural nail">Natural nail</span><img src="assets/raw/bk-9.jpg" alt="Simple natural nail finish" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES -> ESPECIALIDADES
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="El estudio" data-en="The studio">The studio</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Por qué" data-en="Why">Why</span> <span class="text-shine" data-es="Nails By Arianne" data-en="Nails By Arianne">Nails By Arianne</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Arte detallado y crecimiento de uña natural, del color solido al tier 4." data-en="Intricate art and natural nail growth, from a solid color to tier 4.">Intricate art and natural nail growth, from a solid color to tier 4.</p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_WHY = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="font-display text-2xl text-shine mb-3" data-es="Arte a tu nivel" data-en="Art at your level">Art at your level</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cuatro niveles claros, de un color solido a un tier 4 detallado, para que elijas exactamente cuanto arte quieres." data-en="Four clear tiers, from a solid color to detailed tier 4 art, so you choose exactly how much art you want.">Four clear tiers, from a solid color to detailed tier 4 art, so you choose exactly how much art you want.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Uña natural primero" data-en="Natural nail first">Natural nail first</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El crecimiento y la salud de tu uña natural son parte del servicio, no una idea de ultimo momento." data-en="Growth and health of your natural nail are part of the service, not an afterthought.">Growth and health of your natural nail are part of the service, not an afterthought.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Estudio privado" data-en="Private studio">Private studio</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Una clienta a la vez con Ari en su estudio privado en Miami Lakes, sin apuros ni citas dobles." data-en="One client at a time with Ari in her private studio in Miami Lakes, no rushing, no double booking.">One client at a time with Ari in her private studio in Miami Lakes, no rushing, no double booking.</p>
        </div>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_WHY + h[reviews_grid.end():]

rep('<a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver el menu completo y reservar" data-en="See the full menu and book">See the full menu and book</a>')
print("ESPECIALIDADES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Lakes</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">15485 Eagle Nest Ln, Suite 110 Room 3, Miami Lakes, FL 33014</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=15485+Eagle+Nest+Ln,+Miami+Lakes,+FL+33014"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa en linea: eliges servicio, dia y hora, y la confirmacion es inmediata." data-en="By appointment online: pick the service, day and time, and the confirmation is instant.">By appointment online: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,74,160,0.4)]" href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,74,160,0.4)]" href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los sets mas recientes de Ari y escribe por DM cualquier duda antes de tu cita." data-en="See Ari\'s latest sets and DM any questions before your appointment.">See Ari\'s latest sets and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Nails By Arianne, 15485 Eagle Nest Ln, Miami Lakes FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=15485+Eagle+Nest+Ln,+Miami+Lakes,+FL+33014&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Arte en cada mano." data-en="Art on every hand.">Art on every hand.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu color solido, tu tier 2, o ese diseño tier 4 que llevas planeando." data-en="Book online in seconds: your one color set, your tier 2, or that tier 4 design you have been planning.">Book online in seconds: your one color set, your tier 2, or that tier 4 design you have been planning.</p>')
rep('<a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Nails By Arianne</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(209,190,240,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Nails By Arianne" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(209,190,240,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Nails By Arianne</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de uñas en Miami Lakes, FL. Atencion con cita previa." data-en="Nail studio in Miami Lakes, FL. By appointment only.">Nail studio in Miami Lakes, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>15485 Eagle Nest Ln, Suite 110 Room 3, Miami Lakes, FL 33014</p>')
rep('<p><a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#d1bef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#d1bef0]" data-es="Reservas en linea" data-en="Online booking">Online booking</a></p>')
rep('<p><a href="https://www.instagram.com/nailsbyarianne_/" target="_blank" rel="noopener" class="hover:text-[#d1bef0]">Instagram · @nailsbyarianne_</a></p>',
    '<p><a href="https://www.instagram.com/nailsbyarianne_/" target="_blank" rel="noopener" class="hover:text-[#d1bef0]">Instagram · @nailsbyarianne_</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nails By Arianne.</p>')
print("FOOTER done")

# book-float
rep('<a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://nailsbyarianne.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
