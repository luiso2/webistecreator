import re, os, shutil

SLUG = "zornailsart"
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

# PALETTE: hue rotation +165deg from base pink -> emerald green
PALETTE = [
    ("#faf2f6", "#f2faf4"), ("#f3e0ea", "#e0f3e4"), ("#a04a72", "#4aa063"),
    ("#c47a9c", "#7ac490"), ("#c9789f", "#78c98e"), ("#5f2c48", "#2c5f36"),
    ("#b25a85", "#5ab271"), ("#f2d5e3", "#d5f2dd"), ("#d9a8c2", "#a8d9b3"),
    ("#e5c1d4", "#c1e5c9"), ("#7d3457", "#347d48"), ("#5c2140", "#215c2e"),
    ("#f0bed7", "#bef0cb"), ("#f8dfeb", "#dff8e6"), ("#f2cfe0", "#cff2d8"),
    ("#fbeff5", "#effbf2"), ("#efd0e0", "#d0efd7"), ("#d3a2bc", "#a2d3ad"),
    ("#8a5573", "#558a5f"), ("#dc9dbe", "#9ddcab"), ("#2a1722", "#172a1a"),
    ("#1f0f18", "#0f1f12"), ("#1c0f16", "#0f1c12"), ("#f6f1ea", "#eaf2f6"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(74,160,99"),
    ("rgba(125,52,87", "rgba(52,125,72"),
    ("rgba(185,138,128", "rgba(128,185,181"),
    ("rgba(233,205,186", "rgba(186,226,233"),
    ("rgba(240,190,215", "rgba(190,240,203"),
    ("rgba(250,242,246", "rgba(242,250,244"),
    ("rgba(253,246,250", "rgba(246,253,247"),
    ("rgba(40,16,30", "rgba(16,40,20"),
    ("rgba(70,25,50", "rgba(25,70,34"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/zornailsart/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@zornailsart')

# Idioma: negocio en espanol -> default es
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Zor Nails Art · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Zor Nails Art, Hialeah FL: acrylic, Luminary, rubber and dip nail systems plus spa manicures and pedicures, with a perfect 5.0 across 17 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Zor Nails Art · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, Luminary and spa nail systems. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-11.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Zor Nails Art",
    "description": "Nail salon in Hialeah, FL: acrylic, Luminary, rubber and dip nail systems, spa manicures and pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "5392 W 12th Ave (inside Lasher Miami)", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33012", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah", "https://www.instagram.com/zornailsart/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "17", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrilicas" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Refill + Pedi Gel" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luminary" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura Spa Con Parafina" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">ZN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Zor Nails Art</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.35)]" />'.replace("160,77,74", "74,160,99"),
    '<img src="assets/raw/bk-1.jpg" alt="Zor Nails Art" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,99,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Zor <span class="text-[color:var(--accent-deep)]">Nails Art</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Estudio de Unas" data-en="Hialeah, FL · Nail Studio">Hialeah, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas que cuentan tu historia." data-en="Nails that tell your story.">Nails that tell your story.</p>\n        <h1',)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrilico, Luminary y" data-en="Acrylic, Luminary and">Acrylic, Luminary and</span><br /><span data-es="disenos, hechos para " data-en="nail art, made to ">nail art, made to </span><span class="text-shine" data-es="destacar" data-en="stand out">stand out</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Acrilicas, Luminary, rubber, dip y disenos a mano, mas pedicura y manicura spa con parafina. Zormarys atiende en Hialeah, dentro de Lasher Miami, con detalle en cada set." data-en="Acrylics, Luminary, rubber, dip and hand-painted nail art, plus spa manicures and pedicures with paraffin. Zormarys works out of Hialeah, inside Lasher Miami, with detail in every set.">Acrylics, Luminary, rubber, dip and hand-painted nail art, plus spa manicures and pedicures with paraffin. Zormarys works out of Hialeah, inside Lasher Miami, with detail in every set.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 17 reseñas en Booksy" data-en="5.0 · 17 reviews on Booksy">5.0 · 17 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-11.jpg" alt="Manicura francesa degradada con anillo dorado en Zor Nails Art" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Luminary" data-en="Luminary">Luminary</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$50" data-en="$50">$50</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="17">17</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Luminary</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sistemas y disenos" data-en="Systems and nail art">Systems and nail art</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">20 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W 12th Ave</p></div>')

for old, new in [
    ('Classic Set', 'Acrilicas'),
    ('Hybrid Set', 'Luminary'),
    ('Volume Set', 'Rubber'),
    ('Mega Volume', 'Dip'),
    ('Bottom Lashes', 'Disenos'),
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
    '<img src="assets/raw/bk-16.jpg" alt="Diseno de unas blanco y negro geometrico en Zor Nails Art" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Zormarys, artista de Zor Nails Art" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="atencion personal" data-en="personal attention">personal attention</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Zor Nails Art es el estudio de Zormarys en Hialeah, dentro de Lasher Miami. Sus clientas describen la atencion como calida desde que llegan, con trabajo detallista en cada diseno." data-en="Zor Nails Art is Zormarys studio in Hialeah, inside Lasher Miami. Her clients describe the welcome as warm from the moment they arrive, with detailed work on every design.">Zor Nails Art is Zormarys studio in Hialeah, inside Lasher Miami. Her clients describe the welcome as warm from the moment they arrive, with detailed work on every design.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 17 reseñas verificadas en Booksy, y clientas que repiten cita porque quedan encantadas con el trabajo terminado." data-en="The result: a perfect 5.0 across 17 verified Booksy reviews, and clients who rebook because they leave delighted with the finished work.">The result: a perfect 5.0 across 17 verified Booksy reviews, and clients who rebook because they leave delighted with the finished work.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="17">17</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,72,0.3)]" loading="lazy" />'.replace("74,160,72", "74,160,99"),
    '<img src="assets/raw/bk-1.jpg" alt="Zormarys" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,99,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Zormarys · <span class="text-[color:var(--ink-40)]" data-es="Artista de unas" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, un set" data-en="Your visit, one set">Your visit, one set</span> <span class="text-shine" data-es="hecho a mano" data-en="made by hand">made by hand</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y sistema" data-en="Shape and system">Shape and system</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges el largo, la forma y el sistema: acrilico, Luminary, rubber o dip, segun lo que buscas." data-en="You choose the length, shape and system: acrylic, Luminary, rubber or dip, based on what you want.">You choose the length, shape and system: acrylic, Luminary, rubber or dip, based on what you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Zormarys trabaja con calma y detalle, hasta 2h 30min segun el sistema y el diseno que elijas." data-en="Zormarys works calmly and with detail, up to 2h 30min depending on the system and design you choose.">Zormarys works calmly and with detail, up to 2h 30min depending on the system and design you choose.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu set terminado y el diseno que hayas elegido, listo para lucirlo." data-en="You leave with your finished set and the design you chose, ready to show off.">You leave with your finished set and the design you chose, ready to show off.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Zor Nails Art en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Zor Nails Art on Booksy. Booking confirms instantly.">Prices and durations as published by Zor Nails Art on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="set" data-en="set">set</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clasico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Acrilicas" data-en="Acrylics">Acrylics</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrilico, base solida para cualquier diseno. Retiro y reparaciones desde $10." data-en="Full acrylic set, a solid base for any design. Removal and repairs starting at $10.">Full acrylic set, a solid base for any design. Removal and repairs starting at $10.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(74,160,99,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Refill + Pedi Gel" data-en="Refill + Pedi Gel">Refill + Pedi Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo mas pedido: relleno de manos mas pedicura en gel el mismo dia, en una sola cita." data-en="The most requested combo: hand refill plus a gel pedicure the same day, in one visit.">The most requested combo: hand refill plus a gel pedicure the same day, in one visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema premium" data-en="Premium system">Premium system</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luminary" data-en="Luminary">Luminary</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sistema Luminary ligero y flexible. Tambien disponible en Rubber o Dip por el mismo precio." data-en="Light, flexible Luminary system. Also available in Rubber or Dip at the same price.">Light, flexible Luminary system. Also available in Rubber or Dip at the same price.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Spa" data-en="Spa">Spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Spa con Parafina" data-en="Spa Manicure with Paraffin">Spa Manicure with Paraffin</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura spa con tratamiento de parafina. Pedicure spa completa disponible por $60." data-en="Spa manicure with a paraffin treatment. Full spa pedicure also available for $60.">Spa manicure with a paraffin treatment. Full spa pedicure also available for $60.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: manicura y pedicure regular, manicure gel y mani-pedi para hombres. Menu completo de 20 servicios y disponibilidad en Booksy." data-en="Also available: regular manicure and pedicure, gel manicure and mani-pedi for men. Full 20-service menu and availability on Booksy.">Also available: regular manicure and pedicure, gel manicure and mani-pedi for men. Full 20-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Girasol en la mano" data-en="Sunflower in hand">Sunflower in hand</span><img src="assets/raw/bk-13.jpg" alt="Clienta sosteniendo un girasol con unas amarillas en Zor Nails Art" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rojo con corazones" data-en="Red with hearts">Red with hearts</span><img src="assets/raw/bk-15.jpg" alt="Unas rojas con diseno de corazones" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Rojo clasico en grupo" data-en="Classic red set">Classic red set</span><img src="assets/raw/bk-7.jpg" alt="Manos con unas rojas clasicas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Blanco y negro geometrico" data-en="Black and white geometric">Black and white geometric</span><img src="assets/raw/bk-16.jpg" alt="Diseno geometrico blanco y negro con leopardo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Nude con anillo" data-en="Nude with ring">Nude with ring</span><img src="assets/raw/bk-10.jpg" alt="Unas nude con anillo dorado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Diseno artistico" data-en="Art design">Art design</span><img src="assets/raw/bk-8.jpg" alt="Diseno artistico de unas en negro y blanco" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES (reales, con autor)
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 17 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 17 verified reviews on Booksy">5.0 out of 5 · 17 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Quede encantada con el servicio de manicura. Desde que llegue me hicieron sentir bienvenida. La atencion fue excelente."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Beatriz L…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Gracias Zormarys, excelente experiencia! Quede encantada con el trabajo realizado. La atencion fue de primera."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yoandra D…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Zor me hizo las unas y quede enamorada. Super detallista, profesional y con una vibra increible."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Cliente verificada</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 17 reseñas en Booksy" data-en="Read all 17 reviews on Booksy">Read all 17 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">5392 W 12th Ave (inside Lasher Miami), Hialeah, FL 33012</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=5392+W+12th+Ave,+Hialeah,+FL+33012"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,77,74,0.4)]" href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("160,77,74", "74,160,99").replace("166337_belleciia-nails_nail-salon_15886_hialeah", "1489133_zor-nails-art_nail-salon_15886_hialeah"),
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,99,0.4)]" href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Zormarys y escribe por DM cualquier duda antes de tu cita." data-en="See Zormarys\'s latest designs and DM any questions before your appointment.">See Zormarys\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Zor Nails Art, 5392 W 12th Ave, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=5392+W+12th+Ave,+Hialeah,+FL+33012&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas que cuentan tu historia." data-en="Nails that tell your story.">Nails that tell your story.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu acrilico, tu Luminary o el relleno que ya te toca." data-en="Book online in seconds: your acrylic, your Luminary, or the refill you are due for.">Book online in seconds: your acrylic, your Luminary, or the refill you are due for.</p>')
rep('<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("166337_belleciia-nails_nail-salon_15886_hialeah", "1489133_zor-nails-art_nail-salon_15886_hialeah"),
    '<a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Zor Nails Art</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,203,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Zor Nails Art" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,203,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Zor Nails Art</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de unas en Hialeah, FL. Atencion con cita previa." data-en="Nail studio in Hialeah, FL. By appointment only.">Nail studio in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>5392 W 12th Ave, Hialeah, FL 33012</p>')
rep('<p><a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="hover:text-[#f0c0be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace("166337_belleciia-nails_nail-salon_15886_hialeah", "1489133_zor-nails-art_nail-salon_15886_hialeah").replace("f0c0be", "bef0cb"),
    '<p><a href="https://booksy.com/en-us/1489133_zor-nails-art_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="hover:text-[#bef0cb]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/zornailsart/" target="_blank" rel="noopener" class="hover:text-[#f0c0be]">Instagram · @zornailsart</a></p>'.replace("f0c0be", "bef0cb"),
    '<p><a href="https://www.instagram.com/zornailsart/" target="_blank" rel="noopener" class="hover:text-[#bef0cb]">Instagram · @zornailsart</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Zor Nails Art.</p>')
print("FOOTER done")

# lang default -> es
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
