import re, os, shutil

SLUG = "stiletto-nails-miami-beach"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, 1)


badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# PALETTE: base mauve-pink (lash bloom) -> "sunset orchid flamingo" (hue rotated to ~312 deg,
# saturation boosted ~15%). New in this city+niche: not crimson-red (do-not-disturb-nails),
# not teal (k-nails), not violet-purple (solynails/bbnails), not the original mauve.
PALETTE = [
    ("#faf2f6", "#fbf1f9"), ("#f3e0ea", "#f4dff0"), ("#a04a72", "#a64493"),
    ("#c47a9c", "#ca74b9"), ("#c9789f", "#cf72bc"), ("#5f2c48", "#632857"),
    ("#b25a85", "#b953a4"), ("#f2d5e3", "#f4d3ee"), ("#d9a8c2", "#dda4d1"),
    ("#e5c1d4", "#e8bedf"), ("#7d3457", "#822f72"), ("#5c2140", "#601d53"),
    ("#f0bed7", "#f4bae8"), ("#f8dfeb", "#faddf4"), ("#f2cfe0", "#f5cced"),
    ("#fbeff5", "#fceef9"), ("#efd0e0", "#f1ceea"), ("#d3a2bc", "#d79ecb"),
    ("#8a5573", "#8e5182"), ("#dc9dbe", "#e198d2"), ("#2a1722", "#2b1627"),
    ("#1f0f18", "#200e1d"), ("#1c0f16", "#1d0e1a"), ("#f6f1ea", "#f7e9f4"),
]
for old, new in PALETTE:
    assert old in h, "PALETTE MISS: " + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(166,68,147"), ("rgba(125,52,87", "rgba(130,47,114"),
    ("rgba(185,138,128", "rgba(189,124,176"), ("rgba(233,205,186", "rgba(237,182,226"),
    ("rgba(240,190,215", "rgba(244,186,232"), ("rgba(250,242,246", "rgba(251,241,249"),
    ("rgba(253,246,250", "rgba(254,245,252"), ("rgba(40,16,30", "rgba(42,14,36"),
    ("rgba(70,25,50", "rgba(73,22,63"),
]
for old, new in RGBA_PAIRS:
    assert old in h, "RGBA MISS: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = "https://booksy.com/en-us/1627826_stiletto-nails-on-the-beach_nail-salon_15890_miami-beach"
IG_URL = "https://www.instagram.com/stilettonailsonthebeach/"
assert "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach" in h
h = h.replace("https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach", BK_URL)
assert "https://www.instagram.com/_lashbloom/" in h
h = h.replace("https://www.instagram.com/_lashbloom/", IG_URL)
assert "@_lashbloom" in h
h = h.replace("@_lashbloom", "@stilettonailsonthebeach")

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Stiletto Nails On The Beach · Nail Studio in Miami Beach, FL | 4.6 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Stiletto Nails On The Beach, Miami Beach FL: acrylic, gel, Russian manicures and spa pedicures from Andrea, Lindy and Vanessa, with a 4.6 rating across 46 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Stiletto Nails On The Beach · Nail Studio in Miami Beach, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, gel and Russian manicures, plus spa pedicures. 4.6 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-15.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-15.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Stiletto Nails On The Beach",
    "description": "Nail studio in Miami Beach, FL: acrylic, gel and Russian manicures, dip powder and spa pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "7449 Collins Ave", "addressLocality": "Miami Beach", "addressRegion": "FL", "postalCode": "33141", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.86018529597859, "longitude": -80.12084000000002 },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "10:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:30", "closes": "19:00" }
    ],
    "sameAs": ["''' + BK_URL + '''", "''' + IG_URL + '''", "https://www.facebook.com/share/17gP29ECtM/?mibextid=wwXIfr"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "46", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Nails" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Russian Manicure" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel X Apres" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luxury Volcalo pedicura" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# PRELOADER
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">SN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Stiletto Nails</span>')

# NAV
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(166,68,147,0.35)]" />',
    '<img src="assets/raw/bk-15.jpg" alt="Stiletto Nails On The Beach" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(166,68,147,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Stiletto <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami Beach, FL · Estudio de unas" data-en="Miami Beach, FL · Nail Studio">Miami Beach, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas stiletto, directo de la arena." data-en="Stiletto nails, straight off the sand.">Stiletto nails, straight off the sand.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrilico, gel y Apres," data-en="Acrylic, gel and Apres,">Acrylic, gel and Apres,</span><br /><span data-es="esculpidas en punta para " data-en="sculpted stiletto-sharp for ">sculpted stiletto-sharp for </span><span class="text-shine" data-es="la playa" data-en="the beach">the beach</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets completos de acrilico y gel, manicura rusa y pedicuras con masaje, hechas por Andrea, Lindy y Vanessa en Collins Avenue. Un 4.6 de calificacion en 46 resenas reales de Booksy y clientas que no reservan en ningun otro lugar." data-en="Full acrylic and gel sets, Russian manicures and pedicures with massage, done by Andrea, Lindy and Vanessa on Collins Avenue. A 4.6 rating from 46 real Booksy reviews and regulars who never book anywhere else.">Full acrylic and gel sets, Russian manicures and pedicures with massage, done by Andrea, Lindy and Vanessa on Collins Avenue. A 4.6 rating from 46 real Booksy reviews and regulars who never book anywhere else.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.6 · 46 reseñas en Booksy" data-en="4.6 · 46 reviews on Booksy">4.6 · 46 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Pink stiletto nail set with rings and butterfly wings at Stiletto Nails On The Beach" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Acrylic Nails</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$75 · 1h 45min" data-en="$75 · 1h 45min">$75 · 1h 45min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="46">46</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets stiletto hechos a mano" data-en="Hand-sculpted stiletto sets">Hand-sculpted stiletto sets</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span class="text-shine">3</span> <span data-es="artistas" data-en="artists">artists</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Andrea, Lindy y Vanessa" data-en="Andrea, Lindy &amp; Vanessa">Andrea, Lindy &amp; Vanessa</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">7449 Collins Ave</p></div>')

for old, new in [
    ('Classic Set', 'Acrylic Nails'),
    ('Hybrid Set', 'Gel Nails'),
    ('Volume Set', 'Russian Manicure'),
    ('Mega Volume', 'Deluxe Pedicure'),
    ('Bottom Lashes', 'Jelly Spa Bath'),
    ('West Palm Beach, FL', 'Miami Beach, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Stiletto Nails On The Beach pink neon sign with floral wall and long stiletto nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Nude ombre nails with gold flower ring at Stiletto Nails On The Beach" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Tres artistas," data-en="Three artists,">Three artists,</span><br /><span class="text-shine" data-es="un solo estudio en Miami Beach" data-en="one Miami Beach studio">one Miami Beach studio</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Stiletto Nails On The Beach es un estudio en Collins Avenue formado por tres artistas: Andrea, Lindy y Vanessa Nobles. Entre las tres cubren desde gel clasico y dip powder hasta sets de acrilico stiletto hechos a mano y manicura rusa." data-en="Stiletto Nails On The Beach is a Collins Avenue studio built around three nail artists: Andrea, Lindy and Vanessa Nobles. Between them they cover everything from classic gel and dip powder to hand-built acrylic stiletto sets and Russian manicures.">Stiletto Nails On The Beach is a Collins Avenue studio built around three nail artists: Andrea, Lindy and Vanessa Nobles. Between them they cover everything from classic gel and dip powder to hand-built acrylic stiletto sets and Russian manicures.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 4.6 en 46 resenas reales de Booksy, clientas que piden a Andrea por su nombre para un set completo, y pedicuras con tiempo suficiente para relajarte de verdad." data-en="The result: a 4.6 rating across 46 real Booksy reviews, clients who ask for Andrea by name for a full set, and pedicures with enough time built in to actually relax.">The result: a 4.6 rating across 46 real Booksy reviews, clients who ask for Andrea by name for a full set, and pedicures with enough time built in to actually relax.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="46">46</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">3</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Artistas" data-en="Nail artists">Nail artists</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(166,68,147,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-14.jpg" alt="Nail artist at Stiletto Nails On The Beach" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(166,68,147,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light" data-es="El equipo de Stiletto Nails" data-en="The Stiletto Nails team">The Stiletto Nails team</span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, unas" data-en="Your visit, nails">Your visit, nails</span> <span class="text-shine" data-es="paso a paso" data-en="step by step">step by step</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy, desde una manicura en gel rapida hasta un set completo de acrilico stiletto, y confirmas al instante." data-en="Choose your service on Booksy, from a quick gel manicure to a full acrylic stiletto set, and confirm instantly.">Choose your service on Booksy, from a quick gel manicure to a full acrylic stiletto set, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y largo" data-en="Shape &amp; length">Shape &amp; length</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Andrea, Lindy o Vanessa conversan contigo sobre forma, largo y acabado antes de aplicar cualquier esmalte." data-en="Andrea, Lindy or Vanessa talk through shape, length and finish with you before any polish goes on.">Andrea, Lindy or Vanessa talk through shape, length and finish with you before any polish goes on.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="La construcción" data-en="The build">The build</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde gel y dip powder hasta acrilico esculpido a mano o manicura rusa, hasta 1h 45min de trabajo detallado." data-en="From gel and dip powder to hand-sculpted acrylic or a Russian manicure, up to 1h 45min of careful, detailed work.">From gel and dip powder to hand-sculpted acrylic or a Russian manicure, up to 1h 45min of careful, detailed work.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Acabado y relax" data-en="Finish &amp; relax">Finish &amp; relax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Las pedicuras incluyen tiempo de masaje, y sales con un set resistente que aguanta bien en la arena." data-en="Pedicures come with massage time built in, and you leave with a chip-resistant set that holds up on the sand.">Pedicures come with massage time built in, and you leave with a chip-resistant set that holds up on the sand.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Stiletto Nails On The Beach en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Stiletto Nails On The Beach on Booksy. Booking confirms instantly.">Prices and durations as published by Stiletto Nails On The Beach on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="acabado" data-en="finish">finish</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma" data-en="Signature">Signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Unas de acrilico esculpidas a mano segun tu forma y largo, el set completo mas pedido del estudio." data-en="Hand-sculpted acrylic nails built to your shape and length, the studio's most requested full set.">Hand-sculpted acrylic nails built to your shape and length, the studio's most requested full set.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(166,68,147,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Russian Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una tecnica de manicura rusa precisa y en seco que limpia la cuticula para un acabado ultra liso y duradero." data-en="A precise, dry manicure technique that cleans up the cuticle for an ultra-smooth, long-lasting finish.">A precise, dry manicure technique that cleans up the cuticle for an ultra-smooth, long-lasting finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema moderno" data-en="Modern system">Modern system</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel X Apres</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un sistema de extension en gel Apres, ligero, de aspecto natural y duradero, sin el olor del acrilico." data-en="A lightweight Apres gel extension system for a natural-looking, durable set without the acrylic smell.">A lightweight Apres gel extension system for a natural-looking, durable set without the acrylic smell.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Ritual de playa" data-en="Beach ritual">Beach ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luxury Volcalo pedicura" data-en="Luxury Volcalo pedicura">Luxury Volcalo pedicura</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El ritual de pedicura mas completo del estudio, con mas tiempo de remojo y masaje para desconectar antes de volver a la arena." data-en="The studio's top pedicure ritual, with extra soak and massage time for a full reset before you head back to the sand.">The studio's top pedicure ritual, with extra soak and massage time for a full reset before you head back to the sand.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-10">
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:120ms">
          <h3 class="font-display text-lg mb-4" data-es="Manicuras" data-en="Manicures">Manicures</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Manicura regular" data-en="Regular manicure">Regular manicure</span><span class="font-medium whitespace-nowrap">$30 · 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Gel Nails</span><span class="font-medium whitespace-nowrap">$45 · 45min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Dip powder" data-en="Dip powder">Dip powder</span><span class="font-medium whitespace-nowrap">$50</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light">Kaping Builder gel</span><span class="font-medium whitespace-nowrap">$50</span></div>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:200ms">
          <h3 class="font-display text-lg mb-4" data-es="Pedicuras y spa" data-en="Pedicures &amp; spa add-ons">Pedicures &amp; spa add-ons</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicura esencial" data-en="Essential Pedicure">Essential Pedicure</span><span class="font-medium whitespace-nowrap">$40 · 1h</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicura gel esencial" data-en="Essential Gel Pedicure">Essential Gel Pedicure</span><span class="font-medium whitespace-nowrap">$50</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicura deluxe con masaje" data-en="Deluxe Pedicure with massage">Deluxe Pedicure with massage</span><span class="font-medium whitespace-nowrap">$60 · 1h</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light">Jelly SPA BATH</span><span class="font-medium whitespace-nowrap">$15 · 15min</span></div>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal sm:col-span-2 lg:col-span-1" style="transition-delay:280ms">
          <h3 class="font-display text-lg mb-4" data-es="Combos de manicura y pedicura" data-en="Manicure &amp; pedicure combos">Manicure &amp; pedicure combos</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Manicura y pedicura" data-en="Manicure and pedicure">Manicure and pedicure</span><span class="font-medium whitespace-nowrap">$66 · 1h 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Manicura gel / podicure gel</span><span class="font-medium whitespace-nowrap">$95 · 1h 45min</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light">Many/ Ped regular</span><span class="font-medium whitespace-nowrap">$70 · 1h 30min</span></div>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menu completo y disponibilidad de Andrea, Lindy y Vanessa en Booksy." data-en="Full menu and availability with Andrea, Lindy and Vanessa on Booksy.">Full menu and availability with Andrea, Lindy and Vanessa on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Manicura y pedicura en pareja" data-en="Manicure and pedicure duo">Manicure and pedicure duo</span><img src="assets/raw/bk-6.jpg" alt="French manicure and matching pedicure at Stiletto Nails On The Beach" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Set cuadrado esculpido" data-en="Sculpted square set">Sculpted square set</span><img src="assets/raw/bk-3.jpg" alt="Mauve pink square-shaped acrylic nail set with rings" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Color gel soleado" data-en="Sunny gel color">Sunny gel color</span><img src="assets/raw/bk-4.jpg" alt="Bright yellow oval gel nails" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Acabado nude degradado" data-en="Nude ombre finish">Nude ombre finish</span><img src="assets/raw/bk-5.jpg" alt="Nude ombre nail set with a gold flower ring" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Acabado cromado" data-en="Chrome finish">Chrome finish</span><img src="assets/raw/bk-8.jpg" alt="Holographic chrome finish nail set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Frances blanco, forma stiletto" data-en="Classic white French, stiletto shape">Classic white French, stiletto shape</span><img src="assets/raw/bk-15.jpg" alt="Classic white French tip on long stiletto-shaped nails" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.6 de 5 · 46 reseñas verificadas en Booksy" data-en="4.6 out of 5 · 46 verified reviews on Booksy">4.6 out of 5 · 46 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"súper buen servicio y atención al cliente. yo seguro regreso pronto porque me encantararon los resultados!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lisbeth M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Andrea took care of me completely. She spent the extra time on my pedi that I really needed and I left there with the most beautiful full set as well."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Clarissa J…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great service"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yeiny M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 46 reseñas en Booksy" data-en="Read all 46 reviews on Booksy">Read all 46 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
MAPS_QUERY = "7449+Collins+Ave,+Miami+Beach,+FL+33141"
MAPS_URL = "https://www.google.com/maps?q=" + MAPS_QUERY
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Beach</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">7449 Collins Ave, Miami Beach, FL 33141</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="' + MAPS_URL + '"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')

old_ig_card = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(166,68,147,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@stilettonailsonthebeach</a>
            </div>
          </div>'''
new_ig_and_hours = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los disenos mas recientes del equipo y escribe por DM cualquier duda antes de tu cita." data-en="See the team's latest nail art and DM any questions before your appointment.">See the team's latest nail art and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(166,68,147,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@stilettonailsonthebeach</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Domingo, 10:00 am a 5:00 pm. Lunes a sabado, 9:30 am a 7:00 pm." data-en="Sunday, 10:00 am to 5:00 pm. Monday to Saturday, 9:30 am to 7:00 pm.">Sunday, 10:00 am to 5:00 pm. Monday to Saturday, 9:30 am to 7:00 pm.</p>
            </div>
          </div>'''
rep(old_ig_card, new_ig_and_hours)
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Stiletto Nails On The Beach, 7449 Collins Ave, Miami Beach FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="' + MAPS_URL + '&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas stiletto, directo de la arena." data-en="Stiletto nails, straight off the sand.">Stiletto nails, straight off the sand.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu set de acrilico, tu manicura rusa, o la pedicura playera que llevas planeando." data-en="Book online in seconds: your acrylic set, your Russian manicure, or the beach-ready pedicure you have been planning.">Book online in seconds: your acrylic set, your Russian manicure, or the beach-ready pedicure you have been planning.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Stiletto Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(244,186,232,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-15.jpg" alt="Stiletto Nails On The Beach" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(244,186,232,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Stiletto Nails On The Beach</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de unas en Miami Beach, FL. Atención con cita previa." data-en="Nail studio in Miami Beach, FL. By appointment only.">Nail studio in Miami Beach, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>7449 Collins Ave, Miami Beach, FL 33141</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f4bae8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f4bae8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f4bae8]">Instagram · @stilettonailsonthebeach</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f4bae8]">Instagram · @stilettonailsonthebeach</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Stiletto Nails On The Beach.</p>')
print("FOOTER done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
