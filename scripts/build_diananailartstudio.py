import re, os, shutil

SLUG = "diana-nail-art-studio"
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

# PALETTE: hue rotation +312.91deg from base pink -> violet/plum (nail art)
PALETTE = [
    ("#faf2f6", "#f8f2fa"), ("#f3e0ea", "#ede0f3"), ("#a04a72", "#8b4aa0"),
    ("#c47a9c", "#b27ac4"), ("#c9789f", "#b378c9"), ("#5f2c48", "#4e2c5f"),
    ("#b25a85", "#9a5ab2"), ("#f2d5e3", "#ead5f2"), ("#d9a8c2", "#caa8d9"),
    ("#e5c1d4", "#dac1e5"), ("#7d3457", "#6a347d"), ("#5c2140", "#4a215c"),
    ("#f0bed7", "#e2bef0"), ("#f8dfeb", "#f1dff8"), ("#f2cfe0", "#e9cff2"),
    ("#fbeff5", "#f8effb"), ("#efd0e0", "#e6d0ef"), ("#d3a2bc", "#c4a2d3"),
    ("#8a5573", "#77558a"), ("#dc9dbe", "#c99ddc"), ("#2a1722", "#23172a"),
    ("#1f0f18", "#190f1f"), ("#1c0f16", "#180f1c"), ("#f6f1ea", "#f6eaec"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(139,74,160"),
    ("rgba(125,52,87", "rgba(106,52,125"),
    ("rgba(185,138,128", "rgba(185,128,163"),
    ("rgba(233,205,186", "rgba(233,186,204"),
    ("rgba(240,190,215", "rgba(226,190,240"),
    ("rgba(250,242,246", "rgba(248,242,250"),
    ("rgba(253,246,250", "rgba(251,246,253"),
    ("rgba(40,16,30", "rgba(31,16,40"),
    ("rgba(70,25,50", "rgba(55,25,70"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/1775494_diana-nail-art-studio-llc_nail-salon_15886_hialeah'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/nailsbydiana88/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@nailsbydiana88')

# idioma principal: espanol
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Diana Nail Art Studio · Salon de Unas en Hialeah, FL | 5.0 en Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Diana Nail Art Studio, Hialeah FL: manicura rusa, builder gel, acrilico y disenos a mano, con 5.0 perfecto en 23 resenas de Booksy. Reserva en linea." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Diana Nail Art Studio · Salon de Unas en Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicura rusa, builder gel y nail art a mano. 5.0 en Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-3.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-3.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Diana Nail Art Studio",
    "description": "Salon de unas en Hialeah, FL: manicura rusa con builder gel, dip powder, acrilico y disenos de nail art a mano.",
    "address": { "@type": "PostalAddress", "streetAddress": "234 E 17th St", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33010", "addressCountry": "US" },
    "sameAs": ["''' + BK_URL + '''", "https://www.instagram.com/nailsbydiana88/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "23", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de unas", "itemListElement": [
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura Rusa con Builder Gel" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Nails" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Regular Gel" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">DN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Diana Nail Art Studio</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.35)]" />',
    '<img src="assets/raw/bk-3.jpg" alt="Diana Nail Art Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Diana <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Nail Art Studio" data-en="Hialeah, FL · Nail Art Studio">Hialeah, FL · Nail Art Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Arte en cada una, hecho a mano." data-en="Art on every nail, made by hand.">Arte en cada una, hecho a mano.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura rusa, builder gel" data-en="Russian manicure, builder gel">Manicura rusa, builder gel</span><br /><span data-es="y disenos a mano, pensados para " data-en="and hand-painted art, made to ">y disenos a mano, pensados para </span><span class="text-shine" data-es="lucir" data-en="stand out">lucir</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura rusa con builder gel, dip powder, acrilico y disenos personalizados, todo con Dianamarys en su estudio de Hialeah, donde cada arreglo se hace a mano y con calma." data-en="Russian manicure with builder gel, dip powder, acrylic and custom designs, all with Dianamarys in her Hialeah studio, where every set is hand-made and unhurried.">Manicura rusa con builder gel, dip powder, acrilico y disenos personalizados, todo con Dianamarys en su estudio de Hialeah, donde cada arreglo se hace a mano y con calma.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 23 reseñas en Booksy" data-en="5.0 · 23 reviews on Booksy">5.0 · 23 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-3.jpg" alt="Unas negras estilo stiletto con dije en Diana Nail Art Studio" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Manicura Rusa" data-en="Russian Manicure">Manicura Rusa</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$80 · 2h" data-en="$80 · 2h">$80 · 2h</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="23">23</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Nail <span class="text-shine">Art</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Disenos a mano alzada" data-en="Hand-painted designs">Disenos a mano alzada</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Por cita" data-en="By appt">Por cita</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atencion uno a uno" data-en="One-on-one care">Atencion uno a uno</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">E 17th St</p></div>')

for old, new in [
    ('Classic Set', 'Manicura Rusa'),
    ('Hybrid Set', 'Builder Gel'),
    ('Volume Set', 'Acrylic'),
    ('Mega Volume', 'Dip Powder'),
    ('Bottom Lashes', 'Nail Art'),
    ('West Palm Beach, FL', 'Hialeah, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Unas negras con acabado brillante en Diana Nail Art Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Ombre en tono vino en Diana Nail Art Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">La experiencia</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">Un estudio,</span><br /><span class="text-shine" data-es="hecho a mano y con calma" data-en="made by hand and unhurried">hecho a mano y con calma</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Diana Nail Art Studio es el estudio de Dianamarys Echazabal en Hialeah. Sus clientas la describen como profesional, detallista y con un espacio acogedor, con arreglos que califican de espectaculares." data-en="Diana Nail Art Studio is Dianamarys Echazabal studio in Hialeah. Her clients describe her as professional, detail-oriented, with a cozy space, and sets they call spectacular.">Diana Nail Art Studio es el estudio de Dianamarys Echazabal en Hialeah. Sus clientas la describen como profesional, detallista y con un espacio acogedor, con arreglos que califican de espectaculares.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 23 resenas verificadas en Booksy, y clientas que agendan su proxima cita antes de salir del estudio." data-en="The result: a perfect 5.0 across 23 verified Booksy reviews, and clients who book their next appointment before leaving the studio.">El resultado: 5.0 perfecto en 23 resenas verificadas en Booksy, y clientas que agendan su proxima cita antes de salir del estudio.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="23">23</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Dianamarys Echazabal" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Dianamarys · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Manicurista</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, una" data-en="Your visit, nail">Tu cita, una</span> <span class="text-shine" data-es="por una" data-en="by nail">por una</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Diseno" data-en="Design">Diseno</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de la una, sistema y referencias que traigas definen el diseno, de un color solido a arte a mano." data-en="Nail shape, system and any references you bring define the design, from a solid color to hand-painted art.">Forma de la una, sistema y referencias que traigas definen el diseno, de un color solido a arte a mano.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">Manos a la obra</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Dianamarys trabaja con calma, hasta 2 horas de aplicacion segun el sistema y el diseno que elijas." data-en="Dianamarys works calmly, up to 2 hours of application depending on the system and design you choose.">Dianamarys trabaja con calma, hasta 2 horas de aplicacion segun el sistema y el diseno que elijas.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">Salida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu diseno terminado y, si quieres, tu proxima cita ya agendada." data-en="You leave with your finished design and, if you want, your next appointment already booked.">Sales con tu diseno terminado y, si quieres, tu proxima cita ya agendada.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Diana Nail Art Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Diana Nail Art Studio on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Diana Nail Art Studio en Booksy. Reserva con confirmación inmediata.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="sistema" data-en="system">sistema</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Basico" data-en="Basic">Basico</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Rusa" data-en="Russian Manicure">Manicura Rusa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura rusa con builder gel, cuidado preciso de la cuticula y acabado duradero." data-en="Russian manicure with builder gel, precise cuticle work and a long-lasting finish.">Manicura rusa con builder gel, cuidado preciso de la cuticula y acabado duradero.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(139,74,160,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Rusa Completa" data-en="Full Russian Manicure">Manicura Rusa Completa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La version completa de la manicura rusa con builder gel, el set mas pedido del estudio." data-en="The full Russian manicure with builder gel, the studio most requested set.">La version completa de la manicura rusa con builder gel, el set mas pedido del estudio.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema" data-en="System">Sistema</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Acrylic Nails" data-en="Acrylic Nails">Acrylic Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrilico, tambien disponible el relleno por $45 y Apres por $50." data-en="Full acrylic set, refills also available for $45 and Apres for $50.">Set completo de acrilico, tambien disponible el relleno por $45 y Apres por $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies" data-en="Feet">Pies</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicure" data-en="Pedicure">Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicure regular en gel, o el pedicure spa completo desde $60." data-en="Regular gel pedicure, or the full spa pedicure from $60.">Pedicure regular en gel, o el pedicure spa completo desde $60.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: dip powder basico, builder gel sin manicura rusa y retiro de sistema. Menu completo y disponibilidad en Booksy." data-en="Also available: basic dip powder, builder gel without the Russian manicure and system removal. Full menu and availability on Booksy.">Tambien: dip powder basico, builder gel sin manicura rusa y retiro de sistema. Menu completo y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Arte" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseno invernal" data-en="Winter design">Diseno invernal</span><img src="assets/raw/bk-4.jpg" alt="Unas con diseno invernal azul en Diana Nail Art Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Verde oliva" data-en="Olive green">Verde oliva</span><img src="assets/raw/bk-5.jpg" alt="Unas en tono verde oliva" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Francesa clasica" data-en="Classic french">Francesa clasica</span><img src="assets/raw/bk-6.jpg" alt="Manicura francesa clasica" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Diseno de huellas" data-en="Paw print design">Diseno de huellas</span><img src="assets/raw/bk-7.jpg" alt="Unas azul marino con diseno de huellas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Ombre azul stiletto" data-en="Blue stiletto ombre">Ombre azul stiletto</span><img src="assets/raw/bk-8.jpg" alt="Unas stiletto con ombre azul" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Diseno navideno" data-en="Holiday design">Diseno navideno</span><img src="assets/raw/bk-9.jpg" alt="Unas con diseno navideno rojo y blanco" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">En sus</span> <span class="text-shine" data-es="propias palabras" data-en="own words">propias palabras</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 23 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 23 verified reviews on Booksy">5.0 de 5 · 23 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Beautiful work"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karinet</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"excelente trabajo, les garatizo una grata experiencia pues los arreglos son espectaculares, agenda tu cita!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Hilia</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encanta."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emibel L…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 23 reseñas en Booksy" data-en="Read all 23 reviews on Booksy">Leer las 23 reseñas en Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">234 E 17th St, Hialeah, FL 33010</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=234+E+17th+St,+Hialeah,+FL+33010"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(139,74,160,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(139,74,160,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Dianamarys y escribe por DM cualquier duda antes de tu cita." data-en="See Dianamarys\'s latest designs and DM any questions before your appointment.">Mira los disenos mas recientes de Dianamarys y escribe por DM cualquier duda antes de tu cita.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Diana Nail Art Studio, 234 E 17th St, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=234+E+17th+St,+Hialeah,+FL+33010&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Arte en cada una, hecho a mano." data-en="Art on every nail, made by hand.">Arte en cada una, hecho a mano.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo diseno" data-en="Your next design">Tu proximo diseno</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">esta a un toque</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu manicura rusa, tu acrilico o el diseno que llevas planeando." data-en="Book online in seconds: your Russian manicure, your acrylic, or the design you have been planning.">Reserva en linea en segundos: tu manicura rusa, tu acrilico o el diseno que llevas planeando.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Diana Nail Art Studio</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(226,190,240,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Diana Nail Art Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(226,190,240,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Diana Nail Art Studio</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Salon de unas en Hialeah, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>234 E 17th St, Hialeah, FL 33010</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#e2bef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#e2bef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/nailsbydiana88/" target="_blank" rel="noopener" class="hover:text-[#e2bef0]">Instagram · @nailsbydiana88</a></p>',
    '<p><a href="https://www.instagram.com/nailsbydiana88/" target="_blank" rel="noopener" class="hover:text-[#e2bef0]">Instagram · @nailsbydiana88</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Diana Nail Art Studio.</p>')
print("FOOTER done")

# book-float
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

# idioma por defecto: espanol (negocio ES)
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
