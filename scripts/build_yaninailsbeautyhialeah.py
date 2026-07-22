import re, os, shutil

SLUG = "yani-nails-beauty-hialeah"
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

# PALETTE: base plum-pink -> jetsetter navy + champagne-gold (light-v2 base, tinted accents)
PALETTE = [
    ("#faf2f6", "#faf6ef"), ("#f3e0ea", "#ecdfc4"), ("#a04a72", "#33465e"),
    ("#c47a9c", "#c9a44c"), ("#c9789f", "#d9bb6c"), ("#5f2c48", "#22303f"),
    ("#b25a85", "#4a6485"), ("#f2d5e3", "#e9dcc0"), ("#d9a8c2", "#b9c6d8"),
    ("#e5c1d4", "#ddd0ac"), ("#7d3457", "#24344a"), ("#5c2140", "#15202e"),
    ("#f0bed7", "#e3c983"), ("#f8dfeb", "#f0e3bd"), ("#f2cfe0", "#ecdcae"),
    ("#fbeff5", "#f4ecd8"), ("#efd0e0", "#dcc383"), ("#d3a2bc", "#b89452"),
    ("#8a5573", "#7a5f2e"), ("#dc9dbe", "#c9a44c"), ("#2a1722", "#10151d"),
    ("#1f0f18", "#0b0e13"), ("#1c0f16", "#0d1119"), ("#f6f1ea", "#faf6ef"),
]
for old, new in PALETTE:
    assert old in h, "PALETTE MISS: " + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(51,70,94"), ("rgba(125,52,87", "rgba(36,52,74"),
    ("rgba(185,138,128", "rgba(139,151,168"), ("rgba(233,205,186", "rgba(214,196,150"),
    ("rgba(240,190,215", "rgba(227,201,131"), ("rgba(250,242,246", "rgba(250,246,239"),
    ("rgba(253,246,250", "rgba(253,250,241"), ("rgba(40,16,30", "rgba(12,16,22"),
    ("rgba(70,25,50", "rgba(18,24,34"),
]
for old, new in RGBA_PAIRS:
    assert old in h, "RGBA MISS: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/1445716_yani-nails-beauty_nail-salon_15886_hialeah'
IG_URL = 'https://www.instagram.com/carmonayanisleidi/'
MAPS_URL = 'https://www.google.com/maps?q=25.920403365931655,-80.29260999999997'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', IG_URL)
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@carmonayanisleidi')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Yani Nails Beauty · Nail Salon in Hialeah, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Yani Nails Beauty, Hialeah FL: Apres, gel and hand-painted nail art by Yanisleidi Carmona, with a perfect 5.0 across 40 Google reviews. Book online via Booksy." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Yani Nails Beauty · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Apres sets, gel manicures and hand-painted nail art. 5.0 on Google. Book on Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-6.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Yani Nails Beauty",
    "description": "Nail salon in Hialeah, FL run by Yanisleidi Carmona: Apres, gel, dip powder and Polygel sets with hand-painted nail art.",
    "address": { "@type": "PostalAddress", "streetAddress": "16251 NW 57th Ave, Miami Gardens, 33014", "addressLocality": "Hialeah, FL", "addressRegion": "Florida", "postalCode": "33014", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.920403365931655, "longitude": -80.29260999999997 },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "18:00" }
    ],
    "sameAs": ["''' + BK_URL + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "40", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Medium" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Spa" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel" } },
      { "@type": "Offer", "price": "10", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Diseno (Nail Art)" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# PRELOADER
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">YN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Yani Nails Beauty</span>')

# NAV
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(51,70,94,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Yani Nails Beauty" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(51,70,94,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Yani Nails <span class="text-[color:var(--accent-deep)]">Beauty</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Estudio de Unas" data-en="Hialeah, FL · Nail Studio">Hialeah, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas hechas para donde sea que vayas." data-en="Nails made for wherever you are headed next.">Nails made for wherever you are headed next.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Sets de Apres, arte pintado" data-en="Apres sets, hand-painted">Apres sets, hand-painted</span><br /><span data-es="a mano, hecho para " data-en="nail art, made to ">nail art, made to </span><span class="text-shine" data-es="viajar" data-en="travel">travel</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets de Apres y gel en Hialeah, desde manicura diaria hasta arte de unas pintado a mano con tematica de viaje, hecho por Yanisleidi (Yani) Carmona. Un 5.0 perfecto en 40 resenas de Google, con citas de martes a sabado." data-en="Apres and gel sets in Hialeah, from everyday manicures to hand-painted travel-themed nail art, done by Yanisleidi (Yani) Carmona. A perfect 5.0 across 40 Google reviews, with appointments Tuesday through Saturday.">Apres and gel sets in Hialeah, from everyday manicures to hand-painted travel-themed nail art, done by Yanisleidi (Yani) Carmona. A perfect 5.0 across 40 Google reviews, with appointments Tuesday through Saturday.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 40 reseñas en Google" data-en="5.0 · 40 reviews on Google">5.0 · 40 reviews on Google</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-6.jpg" alt="Burgundy and gold French tip nail set resting on a New York travel book" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Apres Medium" data-en="Apres Medium">Apres Medium</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$60 · 1h 30min" data-en="$60 · 1h 30min">$60 · 1h 30min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="40">40</span> <span data-es="reseñas en Google" data-en="reviews on Google">reseñas en Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Apres <span class="text-shine">&amp;</span> Design</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Arte de unas a mano" data-en="Hand-painted nail art">Hand-painted nail art</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Mar-Sab" data-en="Tue-Sat">Tue-Sat</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="9am a 6pm" data-en="9am to 6pm">9am to 6pm</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">16251 NW 57th Ave</p></div>')

for old, new in [
    ('Classic Set', 'Apres Nails'),
    ('Hybrid Set', 'Gel Manicure'),
    ('Volume Set', 'Nail Art'),
    ('Mega Volume', 'Pedicure Spa'),
    ('Bottom Lashes', 'Polygel'),
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
    '<img src="assets/raw/bk-9.jpg" alt="Blue French tip nail set with pearl accents resting on a Paris travel book" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Hand-painted ocean themed nail art with starfish, seahorse and turtle details" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="lista para donde sea que vayas" data-en="ready for wherever you are headed">ready for wherever you are headed</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Yani Nails Beauty es el estudio de Yanisleidi (Yani) Carmona en Hialeah, FL. Trabaja con sistemas de Apres, gel, dip powder y Polygel, y pinta a mano disenos personalizados, desde una punta francesa simple hasta los sets detallados con tematica de viaje que se ven en la galeria." data-en="Yani Nails Beauty is Yanisleidi (Yani) Carmona'"'"'s studio in Hialeah, FL. She works across Apres, gel, dip powder and Polygel systems, and hand-paints custom nail art, from a simple French tip to the detailed travel-themed sets in the gallery.">Yani Nails Beauty is Yanisleidi (Yani) Carmona'"'"'s studio in Hialeah, FL. She works across Apres, gel, dip powder and Polygel systems, and hand-paints custom nail art, from a simple French tip to the detailed travel-themed sets in the gallery.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 40 resenas verificadas de Google, con clientas que describen su trabajo como profesional y las unas siempre hermosas." data-en="The result: a perfect 5.0 across 40 verified Google reviews, with clients who describe her work as professional and always beautiful.">The result: a perfect 5.0 across 40 verified Google reviews, with clients who describe her work as professional and always beautiful.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="40">40</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(51,70,94,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Yani Nails Beauty" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(51,70,94,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Yani · <span class="text-[color:var(--ink-40)]" data-es="Artista de unas" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy, desde una manicura en gel rapida hasta un set completo de Apres, y confirmas al instante." data-en="Pick your service on Booksy, from a quick gel manicure to a full Apres set, and confirm instantly.">Pick your service on Booksy, from a quick gel manicure to a full Apres set, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu inspiracion" data-en="Your inspo">Your inspo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Muestrale a Yani una foto de referencia, un color o un diseno que viste, ella puede pintar a mano la mayoria de los estilos." data-en="Show Yani a travel photo, a color, or a design you saw online, she can hand-paint most looks.">Show Yani a travel photo, a color, or a design you saw online, she can hand-paint most looks.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="La aplicacion" data-en="The application">The application</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Relajate durante tu set de Apres, gel, dip powder o Polygel: la mayoria de los sets completos toman cerca de 1h 30min." data-en="Sit back for your Apres, gel, dip powder or Polygel set, most full sets take about 1h 30min.">Sit back for your Apres, gel, dip powder or Polygel set, most full sets take about 1h 30min.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Acabado final" data-en="Finish and go">Finish and go</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set resistente y terminado a mano (agrega una punta francesa, diseno o tratamiento de parafina antes de irte)." data-en="You leave with a chip-resistant, hand-finished set (add a French tip, design or paraffin treatment before you go).">You leave with a chip-resistant, hand-finished set (add a French tip, design or paraffin treatment before you go).</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Yani Nails Beauty en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Yani Nails Beauty on Booksy. Booking confirms instantly.">Prices and durations as published by Yani Nails Beauty on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="acabado" data-en="finish">finish</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Apres" data-en="Apres">Apres</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Apres Medium</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Apres semipermanente en unas de largo natural, la base diaria para color de larga duracion. Tambien en short ($55) y long ($65)." data-en="Semi-permanent Apres on natural-length nails, the everyday base for long-wearing color. Also available in short ($55) and long ($65).">Semi-permanent Apres on natural-length nails, the everyday base for long-wearing color. Also available in short ($55) and long ($65).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(51,70,94,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Pedicure Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una pedicura spa completa con remojo, exfoliacion y masaje, el upgrade relajante de la pedicura regular ($30)." data-en="A full spa pedicure with soak, scrub and massage, the relaxing upgrade from the regular pedicure ($30).">A full spa pedicure with soak, scrub and massage, the relaxing upgrade from the regular pedicure ($30).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un color solido en gel con resistencia al descascarado, la manicura diaria limpia. Tambien manicura regular por $20." data-en="One solid gel color with chip-resistant wear, the clean everyday manicure. Regular manicure also available for $20.">One solid gel color with chip-resistant wear, the clean everyday manicure. Regular manicure also available for $20.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma" data-en="Signature">Signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Diseno (Nail Art)" data-en="Diseno (Nail Art)">Diseno (Nail Art)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Arte de unas pintado a mano sobre cualquier set, desde una punta francesa simple hasta los disenos con tematica de viaje de la galeria." data-en="Hand-painted nail art added to any set, from a simple French tip to the travel-themed designs in the gallery.">Hand-painted nail art added to any set, from a simple French tip to the travel-themed designs in the gallery.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$10</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 gap-5 mt-10">
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:120ms">
          <h3 class="font-display text-lg mb-4" data-es="Manicura y pedicura" data-en="Manicure &amp; Pedicure">Manicure &amp; Pedicure</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Manicure regular" data-en="Manicure Regular">Manicure Regular</span><span class="font-medium whitespace-nowrap">$20 · 40min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicure regular" data-en="Pedicure Regular">Pedicure Regular</span><span class="font-medium whitespace-nowrap">$30</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicure gel" data-en="Pedicure Gel">Pedicure Gel</span><span class="font-medium whitespace-nowrap">$40 · 1h</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">French</span><span class="font-medium whitespace-nowrap">$10</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Remover" data-en="Remover">Remover</span><span class="font-medium whitespace-nowrap">$10</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light" data-es="Parafina" data-en="Parafina (Paraffin)">Parafina (Paraffin)</span><span class="font-medium whitespace-nowrap">$10</span></div>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:200ms">
          <h3 class="font-display text-lg mb-4" data-es="Sistemas de larga duracion" data-en="Long-wear Systems &amp; Extras">Long-wear Systems &amp; Extras</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Apres short" data-en="Apres Short">Apres Short</span><span class="font-medium whitespace-nowrap">$55 · 1h 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Apres long" data-en="Apres Long">Apres Long</span><span class="font-medium whitespace-nowrap">$65 · 1h 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Luminary</span><span class="font-medium whitespace-nowrap">$60 · 1h 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Builder</span><span class="font-medium whitespace-nowrap">$45</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Ruber Base</span><span class="font-medium whitespace-nowrap">$60 · 1h 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Dip powder" data-en="Dip Powder">Dip Powder</span><span class="font-medium whitespace-nowrap">$45</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light">Polygel</span><span class="font-medium whitespace-nowrap">$60 · 1h 30min</span></div>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Todos los precios y duraciones son los publicados por Yani Nails Beauty. Menu completo y disponibilidad en Booksy." data-en="All prices and durations are as published by Yani Nails Beauty. Full menu and availability on Booksy.">All prices and durations are as published by Yani Nails Beauty. Full menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Sets reales," data-en="Real sets,">Real sets,</span> <span class="text-shine" data-es="detalle real" data-en="real detail">real detail</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Cromado listo para Londres" data-en="London-ready chrome">London-ready chrome</span><img src="assets/raw/bk-5.jpg" alt="Shimmering lime-green chrome nail set resting on a London travel book" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Stiletto almendrado suave" data-en="Soft almond stiletto">Soft almond stiletto</span><img src="assets/raw/bk-1.jpg" alt="Soft pink almond-shaped stiletto nail set" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Frances clasico, elevado" data-en="Classic French, elevated">Classic French, elevated</span><img src="assets/raw/bk-3.jpg" alt="Classic white French tip manicure on almond nails resting on a plush blanket" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Ovalado nude brillante" data-en="Glossy nude oval">Glossy nude oval</span><img src="assets/raw/bk-7.jpg" alt="Glossy nude oval nail set with a diamond ring accent" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Diseno navideno pintado a mano" data-en="Hand-painted holiday design">Hand-painted holiday design</span><img src="assets/raw/bk-8.jpg" alt="Red manicure with hand-painted gold bow and polka dot nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En palabras de" data-en="In her clients">In her clients</span> <span class="text-shine" data-es="sus clientas" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 40 reseñas verificadas en Google" data-en="5.0 out of 5 · 40 verified reviews on Google">5.0 out of 5 · 40 verified reviews on Google</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Feliz con el servicio mis unas espectaculares"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yamile C&#8230;</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me gusto, buen servicio"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anabel R&#8230;</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encanta su trabajo, bien profesional y las unas siempre hermosas."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">karen G&#8230;</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver mas resenas en Google" data-en="See more reviews on Google">See more reviews on Google</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">16251 NW 57th Ave, Miami Gardens, FL 33014</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="' + MAPS_URL + '"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(51,70,94,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(51,70,94,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')

old_ig_card = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(51,70,94,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@carmonayanisleidi</a>
            </div>
          </div>'''
new_ig_and_hours = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los ultimos sets pintados a mano de Yani y escribe por DM cualquier duda antes de tu cita." data-en="See Yani's latest hand-painted sets and DM any questions before your appointment.">See Yani's latest hand-painted sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(51,70,94,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@carmonayanisleidi</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes a sabado, 9:00 am a 6:00 pm. Cerrado domingo y lunes." data-en="Tuesday to Saturday, 9:00 am to 6:00 pm. Closed Sunday and Monday.">Tuesday to Saturday, 9:00 am to 6:00 pm. Closed Sunday and Monday.</p>
            </div>
          </div>'''
rep(old_ig_card, new_ig_and_hours)
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Yani Nails Beauty, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="' + MAPS_URL + '&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas hechas para donde sea que vayas." data-en="Nails made for wherever you are headed next.">Nails made for wherever you are headed next.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo diseno" data-en="Your next design">Your next design</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu set de Apres, tu manicura en gel, o el diseno pintado a mano que has estado imaginando." data-en="Book online in seconds: your Apres set, your gel manicure, or the hand-painted design you have been picturing.">Book online in seconds: your Apres set, your gel manicure, or the hand-painted design you have been picturing.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Yani Nails Beauty</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(227,201,131,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Yani Nails Beauty" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(227,201,131,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Yani Nails Beauty</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de unas y belleza en Hialeah, FL. Atencion con cita previa." data-en="Nail and beauty studio in Hialeah, FL. By appointment only.">Nail and beauty studio in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>16251 NW 57th Ave, Miami Gardens, FL 33014</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#e3c983]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#e3c983]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#e3c983]">Instagram · @carmonayanisleidi</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#e3c983]">Instagram · @carmonayanisleidi</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Yani Nails Beauty.</p>')
print("FOOTER done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
