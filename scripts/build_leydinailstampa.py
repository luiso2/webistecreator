import re, os, shutil

SLUG = "leydinailstampa"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


# ---------- 1. Proteger el badge Merktop ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------- 2. Paleta: lavanda-azulado (dada, no hue-shift calculado aqui) ----------
PALETTE = [
    ("#faf2f6", "#f3f4f9"), ("#f3e0ea", "#e3e4f0"), ("#a04a72", "#575a93"),
    ("#c47a9c", "#8587b9"), ("#c9789f", "#8488bd"), ("#5f2c48", "#343857"),
    ("#b25a85", "#676ca5"), ("#f2d5e3", "#d9dbee"), ("#d9a8c2", "#afb3d2"),
    ("#e5c1d4", "#c6c9e0"), ("#7d3457", "#3f4272"), ("#5c2140", "#2a2e53"),
    ("#f0bed7", "#c6c8e8"), ("#f8dfeb", "#e3e4f4"), ("#f2cfe0", "#d4d6ed"),
    ("#fbeff5", "#f1f2f9"), ("#efd0e0", "#d5d7ea"), ("#d3a2bc", "#a9adcc"),
    ("#8a5573", "#5d6282"), ("#dc9dbe", "#a6abd3"), ("#2a1722", "#1a1c27"),
    ("#1f0f18", "#11131d"), ("#1c0f16", "#11121a"), ("#f6f1ea", "#f4ecf4"),
]
for old, new in PALETTE:
    assert old in h, "NO PALETTE ANCHOR: " + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(87,90,147"), ("rgba(125,52,87", "rgba(63,66,114"),
    ("rgba(185,138,128", "rgba(160,137,176"), ("rgba(233,205,186", "rgba(220,193,226"),
    ("rgba(240,190,215", "rgba(198,200,232"), ("rgba(250,242,246", "rgba(243,244,249"),
    ("rgba(253,246,250", "rgba(247,248,252"), ("rgba(40,16,30", "rgba(20,22,36"),
    ("rgba(70,25,50", "rgba(32,36,63"),
]
for old, new in RGBA_PAIRS:
    assert old in h, "NO RGBA ANCHOR: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------- 3. Globales: Booksy, Instagram, handle ----------
BK_URL = 'https://booksy.com/en-us/1649004_leydi-nails_nail-salon_15761_tampa'
IG_URL = 'https://www.instagram.com/leydi920910/'
HANDLE = '@leydi920910'

OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, BK_URL)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
assert OLD_IG in h
h = h.replace(OLD_IG, IG_URL)

OLD_HANDLE = '@_lashbloom'
assert OLD_HANDLE in h
h = h.replace(OLD_HANDLE, HANDLE)
print("GLOBALS done")

# ---------- 4. HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Leydi Nails · Nail Salon in Tampa, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Leydi Nails, Tampa FL: acrylic, Gel X, dip powder and spa pedicures from a patient, detail-driven nail tech with a perfect 5.0 across 12 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Leydi Nails · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, Gel X and spa pedicures. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-1.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Leydi Nails",
    "description": "Nail salon in Tampa, FL: acrylic, Gel X, dip powder and spa pedicures, plus lash and brow extras.",
    "address": { "@type": "PostalAddress", "streetAddress": "1003 W Hillsborough Ave suite 1", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33603", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.99634257, "longitude": -82.47232508 },
    "sameAs": ["''' + BK_URL + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "12", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Full Set" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Spa Deluxe" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel X" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 5. Idioma: EN default, sin cambios (skeleton light-v2 ya es EN default) ----------

# ---------- 6. PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Leydi Nails</span>')

# ---------- 7. NAV ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(87,90,147,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Leydi Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(87,90,147,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Leydi <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Salón de uñas" data-en="Tampa, FL · Nail Salon">Tampa, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Uñas hechas con paciencia y pasión." data-en="Nails made with patience and passion.">Nails made with patience and passion.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrílico, Gel X y arte" data-en="Acrylic, Gel X and nail">Acrylic, Gel X and nail</span><br /><span data-es="en uñas, hechas solo para " data-en="art, made just for ">art, made just for </span><span class="text-shine" data-es="ti" data-en="you">you</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets completos de acrílico, Gel X, dip powder y pedicuras spa, de una manicurista conocida por su paciencia, precisión y diseños que duran. Leydi Cervantes convierte tu inspiración en arte, detalle a detalle." data-en="Full acrylic sets, Gel X, dip powder and spa pedicures, from a nail tech known for patience, precision and designs that last. Leydi Cervantes brings your inspiration to life, one detail at a time.">Full acrylic sets, Gel X, dip powder and spa pedicures, from a nail tech known for patience, precision and designs that last. Leydi Cervantes brings your inspiration to life, one detail at a time.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 12 reseñas en Booksy" data-en="5.0 · 12 reviews on Booksy">5.0 · 12 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="French manicure with a gold ring at Leydi Nails" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Pedicure Spa Deluxe</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$100 · 2h 30min" data-en="$100 · 2h 30min">$100 · 2h 30min</p>')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="12">12</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Gel X</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sistemas premium de uñas" data-en="Premium nail systems">Premium nail systems</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">25 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo de servicios" data-en="Full service menu">Full service menu</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Hillsborough Ave</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Classic Set', 'Acrylic Full Set'),
    ('Hybrid Set', 'Gel X'),
    ('Volume Set', 'Dip Powder'),
    ('Mega Volume', 'Spa Pedicure'),
    ('Bottom Lashes', 'Nail Art'),
    ('West Palm Beach, FL', 'Tampa, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 11. EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Pedicure prep with fresh towels and gloves at Leydi Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Closeup of hand-painted green floral nail art at Leydi Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una sola artista," data-en="One nail artist,">One nail artist,</span><br /><span class="text-shine" data-es="hecha para tu visión" data-en="made for your vision">made for your vision</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Leydi Nails es el estudio de Leydi Cervantes en Tampa. Sus clientas dicen que es paciente, talentosa y muy detallista: le llevas una idea y la convierte en algo aún más hermoso de lo que imaginabas." data-en="Leydi Nails is the Tampa studio of Leydi Cervantes. Clients say she is patient, talented and endlessly detail-oriented: bring an idea and she turns it into something even more beautiful than you imagined.">Leydi Nails is the Tampa studio of Leydi Cervantes. Clients say she is patient, talented and endlessly detail-oriented: bring an idea and she turns it into something even more beautiful than you imagined.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 12 reseñas verificadas en Booksy, con clientas que destacan que sus rellenos duran tres semanas sin levantarse ni despostillarse." data-en="The result: a perfect 5.0 across 12 verified Booksy reviews, with clients praising fills that last three weeks without lifting or chipping.">The result: a perfect 5.0 across 12 verified Booksy reviews, with clients praising fills that last three weeks without lifting or chipping.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="12">12</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(87,90,147,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Leydi Cervantes" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(87,90,147,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Leydi · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 12. METODO ----------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, diseño" data-en="Your visit, design">Your visit, design</span> <span class="text-shine" data-es="por diseño" data-en="by design">by design</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu inspiración" data-en="Your inspo">Your inspo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Traes una foto de referencia o una idea, y Leydi define el diseño y el sistema para hacerla realidad." data-en="Bring a reference photo or idea, and Leydi maps out the design and system to bring it to life.">Bring a reference photo or idea, and Leydi maps out the design and system to bring it to life.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Leydi trabaja con cuidado y precisión, hasta 2h 30min en los combos spa más completos." data-en="Leydi works with care and precision, taking up to 2h 30min for the most complete spa combos.">Leydi works with care and precision, taking up to 2h 30min for the most complete spa combos.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El resultado final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el diseño que imaginaste hecho realidad, y unas que se mantienen fuertes por semanas." data-en="You leave with the design you imagined made real, and nails that stay strong for weeks.">You leave with the design you imagined made real, and nails that stay strong for weeks.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Leydi Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Leydi Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Leydi Nails on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="acabado" data-en="finish">finish</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una manicura clásica impecable: forma, cutícula y esmaltado, hechos con paciencia y precisión." data-en="A clean classic manicure: shape, cuticle care and polish, done with patience and precision.">A clean classic manicure: shape, cuticle care and polish, done with patience and precision.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(87,90,147,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Pedicure Spa Deluxe</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Dos horas y media de mimos spa completos: remojo, exfoliación, masaje y esmaltado de pies a cabeza." data-en="Two and a half hours of full spa pampering: soak, scrub, massage and polish from head to toe.">Two and a half hours of full spa pampering: soak, scrub, massage and polish from head to toe.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema de la casa" data-en="Signature system">Signature system</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un set completo de acrílico con fuerza y forma, listo para cualquier color o diseño encima." data-en="A full acrylic set built for strength and shape, ready for any color or nail art on top.">A full acrylic set built for strength and shape, ready for any color or nail art on top.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tendencia" data-en="Trending finish">Trending finish</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel X</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensiones de gel ligeras con apariencia natural y esmaltado en gel brillante, sin olor a acrílico." data-en="Lightweight gel extensions with a natural look and glossy gel polish, no acrylic smell.">Lightweight gel extensions with a natural look and glossy gel polish, no acrylic smell.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]
print("SERVICIOS grid done")

# Bloque de menu completo agrupado (21 servicios restantes de los 25 reales, precio real, sin acordeon)
CATS = [
    ("Manicura", "Manicure", [
        ("Manicure for men", 30, "35min"), ("Acrylic fill", 50, None), ("Dip Power", 50, None),
        ("Dip Power With Tips", 60, None), ("Acrylic overlay", 50, None), ("Poly Gel", 60, None),
        ("Ruber Base", 60, None), ("Builder Gel", 60, None), ("Only Gel polish change", 25, None),
    ]),
    ("Pedicura", "Pedicure", [
        ("Pedicure Regular", 40, "45min"), ("Pedicura Spa", 50, None), ("Volcano Pedicura Spa", 60, None),
        ("Acrylic pedicure", 50, None), ("Kids pedicure", 20, "30min"),
    ]),
    ("Pestañas y cejas", "Lash & brow", [
        ("Eyelash Lamination", 85, "1h 15min"), ("Eyelash Lift", 65, "1h"),
        ("Eyebrow", 15, None), ("Hena", 15, None),
    ]),
    ("Rostro y cera", "Face & wax", [
        ("Face", 45, "20min"), ("Lip", 10, "5min"), ("Chin", 10, "5min"),
    ]),
]
total_services = sum(len(items) for _, _, items in CATS)
assert total_services == 21, total_services

cat_cards = []
for es_label, en_label, items in CATS:
    rows = "\n".join(
        f'            <div class="flex items-baseline justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)] last:border-0"><span class="text-sm font-light">{name}{" (" + dur + ")" if dur else ""}</span><span class="text-sm font-medium whitespace-nowrap ml-3">${price}</span></div>'
        for name, price, dur in items
    )
    cat_cards.append(f'''        <div class="glass glass-hover rounded-3xl p-6 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="{es_label}" data-en="{en_label}">{en_label}</p>
{rows}
        </div>''')

FULL_MENU = '''      <div class="mt-8">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-6" data-es="El menú completo" data-en="The full menu">The full menu</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
''' + "\n".join(cat_cards) + '''
        </div>
      </div>
      '''

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    FULL_MENU + '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="25 servicios en total. Precios y disponibilidad exactos en Booksy." data-en="25 services in total. Exact prices and availability on Booksy.">25 services in total. Exact prices and availability on Booksy.</span></p>')
print("SERVICIOS full menu done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Diseño" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Francesa clásica" data-en="Classic french">Classic french</span><img src="assets/raw/bk-9.jpg" alt="Classic short french manicure at Leydi Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Mani en tono joya" data-en="Jewel-tone mani">Jewel-tone mani</span><img src="assets/raw/bk-10.jpg" alt="Manicure with lavender-toned nails and layered rings" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Acabado rosa nude" data-en="Pink nude finish">Pink nude finish</span><img src="assets/raw/bk-11.jpg" alt="Soft pink nude manicure with a pearl ring" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Blanco y nude" data-en="White & nude">White &amp; nude</span><img src="assets/raw/bk-12.jpg" alt="White and nude manicure with a pearl statement ring" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Arte floral" data-en="Floral nail art">Floral nail art</span><img src="assets/raw/bk-14.jpg" alt="Hand-painted green floral nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Neutro y perlas" data-en="Neutral & pearls">Neutral &amp; pearls</span><img src="assets/raw/bk-3.jpg" alt="Neutral manicure with delicate pearl details" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 12 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 12 verified reviews on Booksy">5.0 out of 5 · 12 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Ever since I found my nail technician, I wouldn't change her for anyone else. She is incredibly talented, patient, and passionate about what she does..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dunia D.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely amazing experience every single time! Leydi is incredibly talented and pays attention to every little detail..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maggie L.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Wonderful job! She took her time, no rush! Loved it!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jeff B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 12 reseñas en Booksy" data-en="Read all 12 reviews on Booksy">Read all 12 reviews on Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1003 W Hillsborough Ave suite 1, Tampa, FL 33603</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=1003+W+Hillsborough+Ave+suite+1,+Tampa,+FL+33603"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(87,90,147,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(87,90,147,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los diseños más recientes de Leydi y escribe por DM cualquier duda antes de tu cita." data-en="See Leydi\'s latest designs and DM any questions before your appointment.">See Leydi\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Leydi Nails, 1003 W Hillsborough Ave suite 1, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=1003+W+Hillsborough+Ave+suite+1,+Tampa,+FL+33603&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Uñas hechas con paciencia y pasión." data-en="Nails made with patience and passion.">Nails made with patience and passion.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="está a un toque de distancia" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu acrílico, tu Gel X, o la pedicura spa que tanto quieres." data-en="Book online in seconds: your acrylic, your Gel X, or the spa pedicure you have been wanting.">Book online in seconds: your acrylic, your Gel X, or the spa pedicure you have been wanting.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Leydi Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(198,200,232,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Leydi Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(198,200,232,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Leydi Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Tampa, FL. Atención con cita previa." data-en="Nail salon in Tampa, FL. By appointment only.">Nail salon in Tampa, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>1003 W Hillsborough Ave suite 1, Tampa, FL 33603</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#c6c8e8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#c6c8e8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#c6c8e8]">Instagram · ' + HANDLE + '</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#c6c8e8]">Instagram · ' + HANDLE + '</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Leydi Nails.</p>')
print("FOOTER done")

# ---------- 19. book-float (aria-label generico, sin cambios de contenido) ----------
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
