import re, os, shutil

SLUG = "any-nails-beauty-spa-hialeah"
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

# PALETTE: base plum-pink -> sage/emerald green (given hue-shift mapping)
PALETTE = [
    ("#faf2f6", "#f3f9f3"), ("#f3e0ea", "#e2f2e1"), ("#a04a72", "#509a53"),
    ("#c47a9c", "#80be82"), ("#c9789f", "#7ec37f"), ("#5f2c48", "#325b30"),
    ("#b25a85", "#61ab61"), ("#f2d5e3", "#d7f0d8"), ("#d9a8c2", "#add5ac"),
    ("#e5c1d4", "#c5e2c4"), ("#7d3457", "#39783b"), ("#5c2140", "#275825"),
    ("#f0bed7", "#c2ecc2"), ("#f8dfeb", "#e1f6e1"), ("#f2cfe0", "#d2efd2"),
    ("#fbeff5", "#f0faf0"), ("#efd0e0", "#d3edd2"), ("#d3a2bc", "#a7cfa6"),
    ("#8a5573", "#5c8659"), ("#dc9dbe", "#a3d7a2"), ("#2a1722", "#1a2918"),
    ("#1f0f18", "#111e10"), ("#1c0f16", "#101b10"), ("#f6f1ea", "#ebf4f5"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(80,154,83"), ("rgba(125,52,87", "rgba(57,120,59"),
    ("rgba(185,138,128", "rgba(132,181,165"), ("rgba(233,205,186", "rgba(190,229,226"),
    ("rgba(240,190,215", "rgba(194,236,194"), ("rgba(250,242,246", "rgba(243,249,243"),
    ("rgba(253,246,250", "rgba(247,252,247"), ("rgba(40,16,30", "rgba(20,38,18"),
    ("rgba(70,25,50", "rgba(30,67,28"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = "https://booksy.com/en-us/1208840_any-nails-beauty-spa_nail-salon_15886_hialeah"
IG_URL = "https://www.instagram.com/any_nails.21/"
IG_HANDLE = "@any_nails.21"

assert "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach" in h
h = h.replace("https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach", BK_URL)
assert "https://www.instagram.com/_lashbloom/" in h
h = h.replace("https://www.instagram.com/_lashbloom/", IG_URL)
assert "@_lashbloom" in h
h = h.replace("@_lashbloom", IG_HANDLE)

# HEAD
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Any Nails Beauty & Spa · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Any Nails Beauty & Spa, Hialeah FL: acrylic, gel, dip powder and freehand nail art with a perfect 5.0 across 89 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Any Nails Beauty & Spa · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, gel, dip powder and nail art. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-9.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Any Nails Beauty & Spa",
    "description": "Nail salon in Hialeah, FL: acrylic, gel, dip powder, Apres Gel-X and freehand nail art, with a perfect 5.0 rating on Booksy.",
    "address": { "@type": "PostalAddress", "streetAddress": "16251 NW 57th Ave, Ste 135", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33014", "addressCountry": "US" },
    "sameAs": ["''' + BK_URL + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "89", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Nails Full Set" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Deluxe Pedicure Gel" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel" } },
      { "@type": "Offer", "price": "10", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Nail Designs" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# PRELOADER + NAV
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">AN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Any Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(80,154,83,0.35)]" />',
    '<img src="assets/raw/bk-1.jpg" alt="Any Nails Beauty & Spa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(80,154,83,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Any <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salon de unas" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas hechas para lucir espectaculares." data-en="Nails made to turn heads.">Nails made to turn heads.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrilico, gel y dip powder," data-en="Acrylic, gel and dip powder,">Acrylic, gel and dip powder,</span><br /><span data-es="unas hechas para " data-en="nails made to ">nails made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets completos de acrilico, manicure y pedicura en gel, dip powder, Apres Gel-X, Luminary y disenos de unas a mano alzada, en un estudio relajado en Hialeah con una calificacion perfecta de 5.0 en 89 resenas de Booksy." data-en="Full acrylic sets, gel manicures and pedicures, dip powder, Apres Gel-X, Luminary and freehand nail art, in a relaxed studio in Hialeah with a perfect 5.0 across 89 Booksy reviews.">Full acrylic sets, gel manicures and pedicures, dip powder, Apres Gel-X, Luminary and freehand nail art, in a relaxed studio in Hialeah with a perfect 5.0 across 89 Booksy reviews.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 89 reseñas en Booksy" data-en="5.0 · 89 reviews on Booksy">5.0 · 89 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-9.jpg" alt="Unas cromadas rosa nude en Any Nails Beauty & Spa" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg" data-es="Pedicura Deluxe Gel" data-en="Deluxe Pedicure Gel">Deluxe Pedicure Gel</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$60 · 1h" data-en="$60 · 1h">$60 · 1h</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="89">89</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="24 servicios · Menu completo" data-en="24 services · Full menu">24 services · Full menu</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">6 <span class="text-shine" data-es="dias" data-en="days">days</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Abierto de lunes a sabado" data-en="Open Monday to Saturday">Open Monday to Saturday</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">16251 NW 57th Ave</p></div>')

for old, new in [
    ('Classic Set', 'Acrylic'),
    ('Hybrid Set', 'Dip Powder'),
    ('Volume Set', 'Apres Gel-X'),
    ('Mega Volume', 'Nail Art'),
    ('Bottom Lashes', 'Deluxe Pedicure'),
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
    '<img src="assets/raw/bk-13.jpg" alt="Manicura francesa rosa con dije de corazon en Any Nails Beauty & Spa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Diseno francés en tonos morados en Any Nails Beauty & Spa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="hecho para cada diseno" data-en="made for every design">made for every design</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Any Nails Beauty & Spa es el estudio de Any en Hialeah, con un menu completo de acrilico, gel, dip powder, Apres Gel-X y disenos de unas a mano alzada, en un espacio relajado y profesional." data-en="Any Nails Beauty & Spa is Any studio in Hialeah, with a full menu of acrylic, gel, dip powder, Apres Gel-X and freehand nail art, in a relaxed, professional space.">Any Nails Beauty & Spa is Any studio in Hialeah, with a full menu of acrylic, gel, dip powder, Apres Gel-X and freehand nail art, in a relaxed, professional space.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 89 resenas verificadas en Booksy, con clientas que llevan 3 anos con Any y citas que siempre corren a tiempo." data-en="The result: a perfect 5.0 across 89 verified Booksy reviews, with clients who have stayed with Any for 3 years and appointments that always run on time.">The result: a perfect 5.0 across 89 verified Booksy reviews, with clients who have stayed with Any for 3 years and appointments that always run on time.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="89">89</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(80,154,83,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Any" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(80,154,83,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Any · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, diseno" data-en="Your visit, design">Your visit, design</span> <span class="text-shine" data-es="por diseno" data-en="by design">by design</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duracion claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu inspiracion" data-en="Your inspo">Your inspo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Traes una foto de referencia o una idea, y Any te ayuda a elegir el sistema, la forma y el diseno para lograrlo." data-en="Bring a reference photo or an idea, and Any helps you pick the system, shape and design to match it.">Bring a reference photo or an idea, and Any helps you pick the system, shape and design to match it.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te sientas y Any trabaja con detalle, desde una manicure en gel rapida hasta un set completo de acrilico con diseno de unas." data-en="Sit back while Any works with detail, from a quick gel manicure to a full acrylic set with nail art.">Sit back while Any works with detail, from a quick gel manicure to a full acrylic set with nail art.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el diseno que querias, y tu proximo relleno o refill ya agendado en el calendario." data-en="You leave with the design you wanted, plus your next fill or refill already on the calendar.">You leave with the design you wanted, plus your next fill or refill already on the calendar.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Any Nails Beauty & Spa en Booksy. Reserva con confirmacion inmediata." data-en="Prices and durations as published by Any Nails Beauty & Spa on Booksy. Booking confirms instantly.">Prices and durations as published by Any Nails Beauty & Spa on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="estilo" data-en="style">style</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema" data-en="System">System</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Nails Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un set completo de acrilico, la base solida y duradera para cualquier forma o diseno a mano alzada." data-en="A complete acrylic set, the solid, long-lasting base for any nail shape or freehand design.">A complete acrylic set, the solid, long-lasting base for any nail shape or freehand design.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(80,154,83,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Deluxe Pedicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una pedicura podologica relajante con esmaltado en gel y tratamiento de parafina, para pies que se sienten renovados." data-en="A relaxing podiatric pedicure with gel polish and a paraffin treatment, for feet that feel brand new.">A relaxing podiatric pedicure with gel polish and a paraffin treatment, for feet that feel brand new.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure con esmaltado en gel de larga duracion, o combina con una pedicura en la misma cita." data-en="Manicure with long-lasting gel polish, or ask about combining it with a pedicure in the same visit.">Manicure with long-lasting gel polish, or ask about combining it with a pedicure in the same visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Nail Designs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Disenos de unas a mano alzada desde $10, o agrega un tratamiento de parafina para manos o pies por $10 mas." data-en="Freehand nail art from $10, or add a paraffin treatment for hands or feet for $10 more.">Freehand nail art from $10, or add a paraffin treatment for hands or feet for $10 more.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $10" data-en="From $10">From $10</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">20min+</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: dip powder, Apres Gel-X, Luminary, rubber base, Polygel y tratamientos de parafina. Menu completo y disponibilidad en Booksy." data-en="Also available: dip powder, Apres Gel-X, Luminary, rubber base, Polygel and paraffin treatments. Full menu and availability on Booksy.">Also available: dip powder, Apres Gel-X, Luminary, rubber base, Polygel and paraffin treatments. Full menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Diseno" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Acabado cromado azul" data-en="Chrome blue finish">Chrome blue finish</span><img src="assets/raw/bk-7.jpg" alt="Unas cromadas azules en forma coffin en Any Nails Beauty & Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Arte de lunares" data-en="Polka dot art">Polka dot art</span><img src="assets/raw/bk-12.jpg" alt="Diseno de unas blanco y negro con lunares y acentos rojos" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Francesa dorada" data-en="Golden French tip">Golden French tip</span><img src="assets/raw/bk-14.jpg" alt="Manicura francesa dorada nude con lineas finas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Francesa floral" data-en="Floral French">Floral French</span><img src="assets/raw/bk-15.jpg" alt="Manicura francesa color vino con acento floral" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Glam color vino" data-en="Wine glam">Wine glam</span><img src="assets/raw/bk-6.jpg" alt="Unas almendra color vino con acento de pedreria" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Flores pintadas a mano" data-en="Hand-painted florals">Hand-painted florals</span><img src="assets/raw/bk-3.jpg" alt="Unas nude con diseno de tulipanes pintados a mano" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 89 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 89 verified reviews on Booksy">5.0 out of 5 · 89 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily P…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing work and space, will definitely keep coming back."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yanelis</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente servicio y hermoso trabajo, super recomendado."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Daniela V…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 89 reseñas en Booksy" data-en="Read all 89 reviews on Booksy">Read all 89 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">16251 NW 57th Ave, Ste 135, Miami Gardens, FL 33014</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=16251+NW+57th+Ave,+Ste+135,+Miami+Gardens,+FL+33014"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Abierto lunes de 10am a 7pm, martes a viernes de 8am a 7pm y sabado de 7am a 4pm. Reserva por Booksy y tu cita se confirma al instante." data-en="Open Monday 10am to 7pm, Tuesday to Friday 8am to 7pm, and Saturday 7am to 4pm. Book via Booksy and your appointment confirms instantly.">Open Monday 10am to 7pm, Tuesday to Friday 8am to 7pm, and Saturday 7am to 4pm. Book via Booksy and your appointment confirms instantly.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(80,154,83,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(80,154,83,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Any y escribe por DM cualquier duda antes de tu cita." data-en="See Any\'s latest designs and DM any questions before your appointment.">See Any\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Any Nails Beauty & Spa, 16251 NW 57th Ave, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=16251+NW+57th+Ave,+Ste+135,+Miami+Gardens,+FL+33014&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas hechas para lucir espectaculares." data-en="Nails made to turn heads.">Nails made to turn heads.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo diseno" data-en="Your next design">Your next design</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu set de acrilico, tu manicure en gel, o la pedicura deluxe que te mereces." data-en="Book online in seconds: your acrylic set, gel manicure, or the deluxe pedicure you have been meaning to treat yourself to.">Book online in seconds: your acrylic set, gel manicure, or the deluxe pedicure you have been meaning to treat yourself to.</p>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Any Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(194,236,194,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Any Nails Beauty & Spa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(194,236,194,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Any Nails Beauty & Spa</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Hialeah, FL. Atencion con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Nail salon in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>16251 NW 57th Ave, Ste 135, Miami Gardens, FL 33014</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#c2ecc2]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#c2ecc2]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#c2ecc2]">Instagram · ' + IG_HANDLE + '</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#c2ecc2]">Instagram · ' + IG_HANDLE + '</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Any Nails Beauty & Spa.</p>')
print("FOOTER done")

# book-float aria-label (English, default lang)
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
