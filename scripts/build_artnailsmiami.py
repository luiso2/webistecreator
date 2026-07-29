import re, os, shutil

SLUG = "art-nails-miami"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, 1)


badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# PALETTE: base plum-pink -> warm coral/terracotta (precomputed hue-shift)
PALETTE = [
    ("#faf2f6", "#f9eee9"), ("#f3e0ea", "#f3ddd6"), ("#a04a72", "#a35d3c"),
    ("#c47a9c", "#cb8969"), ("#c9789f", "#d18666"), ("#5f2c48", "#5e3123"),
    ("#b25a85", "#ba6948"), ("#f2d5e3", "#f4d6c9"), ("#d9a8c2", "#ddab9a"),
    ("#e5c1d4", "#e7c2b5"), ("#7d3457", "#7e4328"), ("#5c2140", "#5b2918"),
    ("#f0bed7", "#f5c3af"), ("#f8dfeb", "#fadfd3"), ("#f2cfe0", "#f5d1c2"),
    ("#fbeff5", "#fbebe5"), ("#efd0e0", "#f1d0c4"), ("#d3a2bc", "#d6a594"),
    ("#8a5573", "#8a594b"), ("#dc9dbe", "#e2a38d"), ("#2a1722", "#251511"),
    ("#1f0f18", "#1a0e0a"), ("#1c0f16", "#170d0a"), ("#f6f1ea", "#eef5e1"),
]
for old, new in PALETTE:
    assert old in h, "PALETTE MISS: " + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(163,93,60"), ("rgba(125,52,87", "rgba(126,67,40"),
    ("rgba(185,138,128", "rgba(189,186,114"), ("rgba(233,205,186", "rgba(225,237,172"),
    ("rgba(240,190,215", "rgba(245,195,175"), ("rgba(250,242,246", "rgba(249,238,233"),
    ("rgba(253,246,250", "rgba(253,240,236"), ("rgba(40,16,30", "rgba(35,16,11"),
    ("rgba(70,25,50", "rgba(68,29,17"),
]
for old, new in RGBA_PAIRS:
    assert old in h, "RGBA MISS: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)

# The last PALETTE pair maps the <meta theme-color> to a stray green (#eef5e1),
# which contradicts the warm coral/terracotta brief (all 23 other pairs shift warm).
# Override just that one occurrence to match the actual --bg value (#f9eee9).
assert 'content="#eef5e1"' in h
h = h.replace('content="#eef5e1"', 'content="#f9eee9"', 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/978409_art-nails-miami_nail-salon_15886_hialeah'
IG_URL = 'https://www.instagram.com/ARTNAILSMIAMI/'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', IG_URL)
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@ARTNAILSMIAMI')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Art Nails Miami · Nail Art Studio in Miami Lakes, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Art Nails Miami, Miami Lakes / Hialeah FL: Apres and gel nail art with hand-painted Level 2 and Level 3 designs, plus skin tightening treatments, with a perfect 5.0 across 14 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Art Nails Miami · Nail Art Studio in Miami Lakes, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Apres and gel nail art, Level 2 and Level 3 designs. 5.0 on Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-4.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-16.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Art Nails Miami",
    "description": "Nail art studio in Miami Lakes / Hialeah, FL: Apres and gel manicures with hand-painted Level 2 and Level 3 designs, plus skin tightening and body contouring treatments.",
    "address": { "@type": "PostalAddress", "streetAddress": "330, 221, Miami Lakes, 33014", "addressLocality": "Hialeah, FL", "addressRegion": "Florida", "postalCode": "33014", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.912012085050584, "longitude": -80.30943732525509 },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "11:00", "closes": "16:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "18:00", "closes": "21:00" }
    ],
    "sameAs": ["''' + BK_URL + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "14", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail and body services", "itemListElement": [
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "APRES Plain (1 color)" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "LEVEL 2 nail design" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure Plain (1 color)" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Facial Skin Tightening (new client)" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# PRELOADER
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">AN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Art Nails Miami</span>')

# NAV
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(163,93,60,0.35)]" />',
    '<img src="assets/raw/bk-16.jpg" alt="Art Nails Miami" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(163,93,60,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Art Nails <span class="text-[color:var(--accent-deep)]">Miami</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami Lakes, FL · Nail Art Studio" data-en="Miami Lakes, FL · Nail Art Studio">Miami Lakes, FL · Nail Art Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Diseno de unas hecho para lucirse." data-en="Nail art, made to turn heads.">Nail art, made to turn heads.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Sets de Apres y gel," data-en="Apres and gel sets,">Apres and gel sets,</span><br /><span data-es="disenados nivel por " data-en="designed level by ">designed level by </span><span class="text-shine" data-es="nivel" data-en="level">level</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Color solido, Level 2 pintado a mano o Level 3 de detalle maximo, todo sobre bases de Apres o gel de larga duracion. Una sola artista, Kaitlyn, y clientas que vuelven por el detalle." data-en="Plain color, hand-painted Level 2 detail, or full Level 3 nail art, all built on long-wearing Apres or gel systems. One nail artist, Kaitlyn, and clients who keep coming back for the detail.">Plain color, hand-painted Level 2 detail, or full Level 3 nail art, all built on long-wearing Apres or gel systems. One nail artist, Kaitlyn, and clients who keep coming back for the detail.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 14 reseñas en Booksy" data-en="5.0 · 14 reviews on Booksy">5.0 · 14 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-4.jpg" alt="Long stiletto nail art set with rings by Art Nails Miami" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Diseno LEVEL 2" data-en="LEVEL 2 Design">LEVEL 2 Design</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$100 · 2h 30min" data-en="$100 · 2h 30min">$100 · 2h 30min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="14">14</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Apres <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Diseno de unas a mano" data-en="Hand-painted nail art">Hand-painted nail art</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Por cita" data-en="By appt">By appt</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atencion uno a uno" data-en="One-on-one care">One-on-one care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Lakes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Hialeah, FL</p></div>')

for old, new in [
    ('Classic Set', 'Apres Nails'),
    ('Hybrid Set', 'Gel Manicure'),
    ('Volume Set', 'Nail Art'),
    ('Mega Volume', 'Level 2 Design'),
    ('Bottom Lashes', 'Level 3 Design'),
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
    '<img src="assets/raw/bk-16.jpg" alt="Engraved Art Nails Miami nameplate" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="French-style nail design with rhinestone accent by Art Nails Miami" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="para cada diseno que traigas" data-en="for every design you bring">for every design you bring</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Art Nails Miami es el estudio de Kaitlyn en Miami Lakes / Hialeah, FL. Se especializa en sistemas de Apres y gel con disenos Level 2 y Level 3 pintados a mano, y ademas ofrece reafirmante y contorno corporal en el mismo estudio." data-en="Art Nails Miami is Kaitlyn'"'"'s studio in Miami Lakes / Hialeah, FL. She specializes in Apres and gel nail systems with hand-painted Level 2 and Level 3 designs, and also offers skin tightening and body contouring treatments in the same studio.">Art Nails Miami is Kaitlyn'"'"'s studio in Miami Lakes / Hialeah, FL. She specializes in Apres and gel nail systems with hand-painted Level 2 and Level 3 designs, and also offers skin tightening and body contouring treatments in the same studio.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 14 resenas verificadas en Booksy, con clientas que dicen que es detallista, divertida y siempre confirma que te encante el diseno antes de irte." data-en="The result: a perfect 5.0 across 14 verified Booksy reviews, with clients who say she is detail-oriented, fun, and always makes sure you love your design before you leave.">The result: a perfect 5.0 across 14 verified Booksy reviews, with clients who say she is detail-oriented, fun, and always makes sure you love your design before you leave.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="14">14</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(163,93,60,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Kaitlyn" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(163,93,60,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Kaitlyn · <span class="text-[color:var(--ink-40)]" data-es="Artista de unas" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, diseno" data-en="Your visit, design">Your visit, design</span> <span class="text-shine" data-es="por diseno" data-en="by design">by design</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set de Apres o gel en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your Apres or gel set on Booksy with clear price and duration, and confirm instantly.">Pick your Apres or gel set on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu inspiracion" data-en="Your inspo">Your inspo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Traes una foto de referencia y Kaitlyn define el nivel de detalle y el plan de color para tu diseno." data-en="Bring a reference photo or idea, and Kaitlyn maps out the level of detail and color plan for your design.">Bring a reference photo or idea, and Kaitlyn maps out the level of detail and color plan for your design.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="La aplicacion" data-en="The application">The application</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Kaitlyn construye tu set con detalle, hasta 2h 30min en los disenos Level 2 y Level 3 mas completos." data-en="Sit back while Kaitlyn builds your set with detail, up to 2h 30min for the most detailed Level 2 and Level 3 designs.">Sit back while Kaitlyn builds your set with detail, up to 2h 30min for the most detailed Level 2 and Level 3 designs.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Acabado final" data-en="Long-lasting finish">Long-lasting finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set de Apres o gel resistente, o con un resultado suave y contorneado si reservaste reafirmante corporal." data-en="You leave with a chip-resistant Apres or gel set, or a smoothed, contoured result if you booked a skin tightening treatment.">You leave with a chip-resistant Apres or gel set, or a smoothed, contoured result if you booked a skin tightening treatment.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Art Nails Miami en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Art Nails Miami on Booksy. Booking confirms instantly.">Prices and durations as published by Art Nails Miami on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="nivel" data-en="level">level</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Apres" data-en="Apres">Apres</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="APRES Plain (1 color)" data-en="APRES Plain (1 color)">APRES Plain (1 color)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un solo color en Apres de larga duracion, la base para cualquier nivel de diseno." data-en="One solid color in long-wearing Apres, the base finish for any level of nail art.">One solid color in long-wearing Apres, the base finish for any level of nail art.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(163,93,60,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">LEVEL 2</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseno pintado a mano sobre tu set de Apres, desde acentos simples hasta arte detallado." data-en="Hand-painted design work on top of your Apres set, from simple accents to detailed art.">Hand-painted design work on top of your Apres set, from simple accents to detailed art.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Detalle maximo" data-en="Maximum detail">Maximum detail</p>
          <h3 class="font-display text-2xl leading-snug mb-3">LEVEL 3</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El nivel de diseno mas detallado, pintado a mano sobre Apres para un acabado duradero." data-en="The most detailed hand-painted design level, built on Apres for a long-lasting finish.">The most detailed hand-painted design level, built on Apres for a long-lasting finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$125</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Manicure Plain (1 color)" data-en="Gel Manicure Plain (1 color)">Gel Manicure Plain (1 color)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un solo color en gel, una manicura diaria limpia con la misma resistencia al descascarado." data-en="One solid gel color, a clean everyday manicure with the same chip-resistant wear.">One solid gel color, a clean everyday manicure with the same chip-resistant wear.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 gap-5 mt-10">
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:120ms">
          <h3 class="font-display text-lg mb-4" data-es="Mas servicios de unas" data-en="More nail services">More nail services</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">LEVEL 2 (on Gel)</span><span class="font-medium whitespace-nowrap">$80 · 2h 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">LEVEL 3 (on Gel)</span><span class="font-medium whitespace-nowrap">$100 · 2h 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="APRES/Gel (retoque de otra artista)" data-en="APRES/Gel (not my work)">APRES/Gel (not my work)</span><span class="font-medium whitespace-nowrap">$10 · 30min</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light" data-es="Acrilico/Dip (retoque de otra artista)" data-en="Acrylic/Dip (not my work)">Acrylic/Dip (not my work)</span><span class="font-medium whitespace-nowrap">$20 · 30min</span></div>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:200ms">
          <h3 class="font-display text-lg mb-4" data-es="Reafirmante y contorno corporal" data-en="Skin tightening &amp; body contouring">Skin tightening &amp; body contouring</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Contorno de abdomen (cliente nueva)" data-en="Abdomen Contouring (new client)">Abdomen Contouring (new client)</span><span class="font-medium whitespace-nowrap">$60</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Contorno de abdomen (cliente frecuente)" data-en="Abdomen Contouring (repeat client)">Abdomen Contouring (repeat client)</span><span class="font-medium whitespace-nowrap">$75</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Reafirmante facial (cliente nueva)" data-en="Facial Skin Tightening (new client)">Facial Skin Tightening (new client)</span><span class="font-medium whitespace-nowrap">$30 · 45min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Reafirmante facial (cliente frecuente)" data-en="Facial Skin Tightening (repeat client)">Facial Skin Tightening (repeat client)</span><span class="font-medium whitespace-nowrap">$45 · 45min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Reduccion de celulitis (cliente nueva)" data-en="Cellulite Breakdown (new client)">Cellulite Breakdown (new client)</span><span class="font-medium whitespace-nowrap">$60</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Reduccion de celulitis (cliente frecuente)" data-en="Cellulite Breakdown (repeat client)">Cellulite Breakdown (repeat client)</span><span class="font-medium whitespace-nowrap">$75</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Piernas" data-en="Legs">Legs</span><span class="font-medium whitespace-nowrap">$20 · 30min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Brazos" data-en="Arms">Arms</span><span class="font-medium whitespace-nowrap">$20 · 30min</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light" data-es="Rostro" data-en="Face">Face</span><span class="font-medium whitespace-nowrap">$15 · 30min</span></div>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: Level 2 y Level 3 sobre gel, retoques rapidos, y tratamientos de reafirmante corporal. Menu completo y disponibilidad en Booksy." data-en="Also available: Level 2 and Level 3 on gel, quick touch-ups, and body skin-tightening treatments. Full menu and availability on Booksy.">Also available: Level 2 and Level 3 on gel, quick touch-ups, and body skin-tightening treatments. Full menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Diseno" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Set stiletto editorial" data-en="Editorial stiletto set">Editorial stiletto set</span><img src="assets/raw/bk-5.jpg" alt="Deep burgundy stiletto nail set with hand tattoo, editorial style at Art Nails Miami" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Arte con pedreria" data-en="Jeweled nail art">Jeweled nail art</span><img src="assets/raw/bk-3.jpg" alt="Colorful patterned nail art with rhinestone details" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Explosion de color" data-en="Playful color pop">Playful color pop</span><img src="assets/raw/bk-6.jpg" alt="Playful multicolor dotted nail art at Art Nails Miami" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Diseno floral" data-en="Floral swirl design">Floral swirl design</span><img src="assets/raw/bk-7.jpg" alt="Green and yellow floral swirl nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Acabado cromado rosa" data-en="Pink chrome finish">Pink chrome finish</span><img src="assets/raw/bk-8.jpg" alt="Pink chrome finish nail set by Art Nails Miami" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Mix de disenos" data-en="Mixed design set">Mixed design set</span><img src="assets/raw/bk-1.jpg" alt="Mixed nail art set with abstract, French tip and marble designs on both hands" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 14 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 14 verified reviews on Booksy">5.0 out of 5 · 14 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing work and excellent hospitality."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carolina N…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She's literally the best"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Vanessa L…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely obsessed with my nails!! Exactly what I wanted, will be booking again!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mindy A…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 14 reseñas en Booksy" data-en="Read all 14 reviews on Booksy">Read all 14 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
MAPS_URL = 'https://www.google.com/maps?q=25.912012085050584,-80.30943732525509'
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Lakes</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">330, 221, Miami Lakes, FL 33014</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="' + MAPS_URL + '"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(163,93,60,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(163,93,60,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')

old_ig_card = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(163,93,60,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@ARTNAILSMIAMI</a>
            </div>
          </div>'''
new_ig_and_hours = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los disenos mas recientes de Kaitlyn y escribe por DM cualquier duda antes de tu cita." data-en="See Kaitlyn's latest designs and DM any questions before your appointment.">See Kaitlyn's latest designs and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(163,93,60,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@ARTNAILSMIAMI</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Sabado y domingo, 11:00 am a 4:00 pm. Lunes a viernes, 6:00 pm a 9:00 pm." data-en="Saturday and Sunday, 11:00 am to 4:00 pm. Monday to Friday, 6:00 pm to 9:00 pm.">Saturday and Sunday, 11:00 am to 4:00 pm. Monday to Friday, 6:00 pm to 9:00 pm.</p>
            </div>
          </div>'''
rep(old_ig_card, new_ig_and_hours)
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Art Nails Miami, Miami Lakes FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="' + MAPS_URL + '&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Diseno de unas hecho para lucirse." data-en="Nail art, made to turn heads.">Nail art, made to turn heads.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo diseno" data-en="Your next design">Your next design</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu set de Apres, tu manicure en gel, o el diseno Level 2 / Level 3 que llevas planeando." data-en="Book online in seconds: your Apres set, your gel manicure, or the Level 2 / Level 3 design you have been planning.">Book online in seconds: your Apres set, your gel manicure, or the Level 2 / Level 3 design you have been planning.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Art Nails Miami</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(245,195,175,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="Art Nails Miami" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(245,195,175,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Art Nails Miami</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de arte en unas en Miami Lakes / Hialeah, FL. Atención con cita previa." data-en="Nail art studio in Miami Lakes / Hialeah, FL. By appointment only.">Nail art studio in Miami Lakes / Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>330, 221, Miami Lakes, FL 33014</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f5c3af]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f5c3af]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f5c3af]">Instagram · @ARTNAILSMIAMI</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f5c3af]">Instagram · @ARTNAILSMIAMI</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Art Nails Miami.</p>')
print("FOOTER done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
