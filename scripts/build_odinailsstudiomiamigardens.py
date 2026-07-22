import re, os, shutil

SLUG = "odi-nails-studio-miami-gardens"
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

# PALETTE: base plum-pink -> dusty rose / soft peach-blush (new, unused hue for Miami Gardens nails)
PALETTE = [
    ("#faf2f6", "#fdf3ef"), ("#f3e0ea", "#f6e2d9"), ("#a04a72", "#b5677a"),
    ("#c47a9c", "#d99a86"), ("#c9789f", "#dba692"), ("#5f2c48", "#6e3d4a"),
    ("#b25a85", "#c17b74"), ("#f2d5e3", "#f6ddd0"), ("#d9a8c2", "#e0b6a8"),
    ("#e5c1d4", "#ecd0c2"), ("#7d3457", "#8a5049"), ("#5c2140", "#63362f"),
    ("#f0bed7", "#f3cdb8"), ("#f8dfeb", "#fbe8db"), ("#f2cfe0", "#f5dcc9"),
    ("#fbeff5", "#fdf1e9"), ("#efd0e0", "#f2ddc9"), ("#d3a2bc", "#dbb39a"),
    ("#8a5573", "#8a5d49"), ("#dc9dbe", "#e2ac93"), ("#2a1722", "#241712"),
    ("#1f0f18", "#1a0f0b"), ("#1c0f16", "#170e0a"),
]
for old, new in PALETTE:
    assert old in h, "PALETTE MISS: " + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(181,103,122"), ("rgba(125,52,87", "rgba(138,80,73"),
    ("rgba(185,138,128", "rgba(201,152,138"), ("rgba(233,205,186", "rgba(237,206,190"),
    ("rgba(240,190,215", "rgba(243,205,184"), ("rgba(250,242,246", "rgba(253,243,239"),
    ("rgba(253,246,250", "rgba(253,245,238"), ("rgba(40,16,30", "rgba(36,18,14"),
    ("rgba(70,25,50", "rgba(75,40,34"),
]
for old, new in RGBA_PAIRS:
    assert old in h, "RGBA MISS: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)

assert 'content="#f6f1ea"' in h
h = h.replace('content="#f6f1ea"', 'content="#fdf3ef"', 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/1704071_odi-nails-studio_nail-salon_15891_miami-gardens'
IG_URL = 'https://www.instagram.com/odicelisnails444/'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', IG_URL)
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@odicelisnails444')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Odi Nails &amp; Studio · Nail Studio in Miami Gardens, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Odi Nails &amp; Studio, Miami Gardens FL: sculpted acrylic full sets, builder gel with hand-painted art, Apres, dip powder, manicures and pedicures, with a perfect 5.0 across 21 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Odi Nails &amp; Studio · Nail Studio in Miami Gardens, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Sculpted acrylics, builder gel nail art, Apres and dip powder. 5.0 on Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-7.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Odi Nails & Studio",
    "description": "Nail studio in Miami Gardens, FL run by Odicelis Llorente: sculpted acrylic full sets, builder gel with hand-painted art, Apres press-ons, dip powder, manicures and pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "5433 NW 184th St", "addressLocality": "Miami Gardens", "addressRegion": "FL", "postalCode": "33055", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.92573, "longitude": -80.27805 },
    "telephone": "+17864245827",
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "10:00", "closes": "13:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday"], "opens": "10:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:30", "closes": "13:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "14:30", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "14:30", "closes": "17:00" }
    ],
    "sameAs": ["''' + BK_URL + '''", "''' + IG_URL + '''", "https://www.tiktok.com/@odicelisllorente"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "21", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set Estructura Basica" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Gel + Diseno Artistico" } },
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Regular" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Gel" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# PRELOADER
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">OL</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Odi Nails Studio</span>')

# NAV
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,103,122,0.35)]" />',
    '<img src="assets/raw/bk-1.jpg" alt="Odi Nails &amp; Studio logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,103,122,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Odi <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami Gardens, FL · Nail Studio" data-en="Miami Gardens, FL · Nail Studio">Miami Gardens, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas disenadas para sentirse como arte." data-en="Nails designed to feel like art.">Nails designed to feel like art.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Sets completos, esculpidos" data-en="Full sets, sculpted">Full sets, sculpted</span><br /><span data-es="a mano, hechos para " data-en="by hand, made to ">by hand, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets completos en acrilico, builder gel con detalle pintado a mano, Apres y dip powder, ademas de manicure y pedicure, todo hecho por una sola artista, Odicelis Llorente, en su estudio de Miami Gardens." data-en="Full acrylic sets, builder gel with hand-painted detail, Apres press-ons and dip powder, plus manicures and pedicures, all built by one nail artist, Odicelis Llorente, in her Miami Gardens studio.">Full acrylic sets, builder gel with hand-painted detail, Apres press-ons and dip powder, plus manicures and pedicures, all built by one nail artist, Odicelis Llorente, in her Miami Gardens studio.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 21 reseñas en Booksy" data-en="5.0 · 21 reviews on Booksy">5.0 · 21 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-7.jpg" alt="Milky white sculpted coffin nail set finished at Odi Nails &amp; Studio" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Full Set Estructura Basica" data-en="Full Set Estructura Basica">Full Set Estructura Basica</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$70 · 1h 30min" data-en="$70 · 1h 30min">$70 · 1h 30min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="21">21</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos y retoques" data-en="Full sets · touch-ups">Full sets · touch-ups</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Por cita" data-en="By appt">By appt</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atencion uno a uno" data-en="One-on-one care">One-on-one care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Gardens</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">5433 NW 184th St</p></div>')

for old, new in [
    ('Classic Set', 'Acrylic Full Set'),
    ('Hybrid Set', 'Builder Gel'),
    ('Volume Set', 'Apres Nails'),
    ('Mega Volume', 'Dip Powder'),
    ('Bottom Lashes', 'Gel Manicure'),
    ('West Palm Beach, FL', 'Miami Gardens, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Odi Nails &amp; Studio pink circular logo with the OL monogram" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="Nude nails with tiny hand-set colorful flower gems by Odi Nails &amp; Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="esculpido con precision" data-en="sculpted with precision">sculpted with precision</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Odi Nails &amp; Studio es el estudio de Odicelis Llorente en Miami Gardens, FL. Cada set (acrilico, builder gel o Apres) se esculpe y se termina a mano, con diseno pintado detalle por detalle, para clientas que buscan un trabajo preciso, sin apuros." data-en="Odi Nails &amp; Studio is the home base of Odicelis Llorente in Miami Gardens, FL. Every set (acrylic, builder gel or Apres) is sculpted and finished by hand, with hand-painted art added detail by detail, for clients who want their nails to look precise, not rushed.">Odi Nails &amp; Studio is the home base of Odicelis Llorente in Miami Gardens, FL. Every set (acrylic, builder gel or Apres) is sculpted and finished by hand, with hand-painted art added detail by detail, for clients who want their nails to look precise, not rushed.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 21 resenas verificadas, con clientas que regresan porque el trabajo es detallado y preciso, y porque cada visita se siente personal." data-en="The result: a perfect 5.0 across 21 verified reviews, with clients who come back because the work is detailed and precise, and because every visit feels personal.">The result: a perfect 5.0 across 21 verified reviews, with clients who come back because the work is detailed and precise, and because every visit feels personal.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="21">21</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,103,122,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Odicelis Llorente" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,103,122,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Odicelis Llorente · <span class="text-[color:var(--ink-40)]" data-es="Artista de unas" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="por paso" data-en="by step">by step</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set completo, builder gel, manicure o pedicure en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your full set, builder gel, mani or pedi on Booksy with clear price and duration, and confirm instantly.">Pick your full set, builder gel, mani or pedi on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu inspiracion" data-en="Your inspiration">Your inspiration</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Traes una foto de referencia o una idea, y Odi define la forma y el diseño pintado a mano antes de empezar." data-en="Bring a reference photo or idea, and Odi maps out your shape and any hand-painted design before she starts.">Bring a reference photo or idea, and Odi maps out your shape and any hand-painted design before she starts.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El esculpido" data-en="The sculpting">The sculpting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Ella arma tu set a mano, capa por capa, hasta 1h 30min para un full set en acrilico o Apres con diseño." data-en="She builds your set by hand, layer by layer, up to 1h 30min for a full acrylic or Apres set with design.">She builds your set by hand, layer by layer, up to 1h 30min for a full acrylic or Apres set with design.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Acabado fresco" data-en="Fresh finish">Fresh finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set esculpido resistente al descascarado, o con una manicure o pedicure impecable, lista para lucir." data-en="You leave with a chip-resistant sculpted set, or a polished mani or pedi, ready to show off.">You leave with a chip-resistant sculpted set, or a polished mani or pedi, ready to show off.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Odi Nails &amp; Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Odi Nails &amp; Studio on Booksy. Booking confirms instantly.">Prices and durations as published by Odi Nails &amp; Studio on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="acabado" data-en="finish">finish</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Acrilico esculpido" data-en="Sculpted acrylic">Sculpted acrylic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Set Estructura Básica" data-en="Full Set Estructura Básica">Full Set Estructura Básica</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Acrilico esculpido desde cero sobre tu una natural, la base para cualquier forma y largo que quieras." data-en="Acrylic sculpted from scratch over your natural nail, the foundation for any shape and length you want.">Acrylic sculpted from scratch over your natural nail, the foundation for any shape and length you want.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(181,103,122,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Builder Gel + Diseño Artístico" data-en="Builder Gel + Diseño Artístico">Builder Gel + Diseño Artístico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Refuerzo en builder gel terminado con diseño pintado a mano, para un set resistente que igual se siente como una obra." data-en="Builder gel reinforcement finished with hand-painted nail art, for a durable set that still feels like a design.">Builder gel reinforcement finished with hand-painted nail art, for a durable set that still feels like a design.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema press-on" data-en="Press-on system">Press-on system</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apress Full Set + Diseño" data-en="Apress Full Set + Diseño">Apress Full Set + Diseño</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Base completa de Apres con diseño pintado encima, para una sensacion mas ligera con el mismo detalle." data-en="A full Apres press-on base with hand-painted design on top, for a lighter feel with the same detail.">A full Apres press-on base with hand-painted design on top, for a lighter feel with the same detail.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Regular" data-en="Manicure Regular">Manicure Regular</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una manicure clasica y prolija para los dias que solo quieres tus uñas naturales pulidas." data-en="A clean, classic manicure for the days you just want your natural nails polished and neat.">A clean, classic manicure for the days you just want your natural nails polished and neat.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$20</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 gap-5 mt-10">
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:120ms">
          <h3 class="font-display text-lg mb-4" data-es="Retoques y mantenimiento" data-en="Touch-ups &amp; maintenance">Touch-ups &amp; maintenance</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Retoque / Relleno de Acrílico" data-en="Retoque / Relleno de Acrílico">Retoque / Relleno de Acrílico</span><span class="font-medium whitespace-nowrap">$55</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Builder Gel / Kapping" data-en="Builder Gel / Kapping">Builder Gel / Kapping</span><span class="font-medium whitespace-nowrap">$50</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Retoque de Builder Gel + Diseño" data-en="Retoque de Builder Gel + Diseño">Retoque de Builder Gel + Diseño</span><span class="font-medium whitespace-nowrap">$55</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light" data-es="Retoque de Apres / Builder Gel" data-en="Retoque de Apres / Builder Gel">Retoque de Apres / Builder Gel</span><span class="font-medium whitespace-nowrap">$50</span></div>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:200ms">
          <h3 class="font-display text-lg mb-4" data-es="Pedicure y mas" data-en="Pedicures &amp; more">Pedicures &amp; more</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Apres Full Set Base" data-en="Apres Full Set Base">Apres Full Set Base</span><span class="font-medium whitespace-nowrap">$55</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Gel Nails</span><span class="font-medium whitespace-nowrap">$30</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicure Gel" data-en="Pedicure Gel">Pedicure Gel</span><span class="font-medium whitespace-nowrap">$40 · 45min</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicure Regular" data-en="Pedicure Regular">Pedicure Regular</span><span class="font-medium whitespace-nowrap">$30</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light" data-es="Pedicure Gel + Acrílico" data-en="Pedicure Gel + Acrílico">Pedicure Gel + Acrílico</span><span class="font-medium whitespace-nowrap">$55</span></div>
            <div class="flex justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Dip Powder</span><span class="font-medium whitespace-nowrap">$50</span></div>
            <div class="flex justify-between gap-3 py-2"><span class="text-[color:var(--ink-60)] font-light">Dip Powder</span><span class="font-medium whitespace-nowrap">$60 · 1h</span></div>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menu completo, precios exactos y disponibilidad en Booksy. Retoques y pedicure disponibles por encargo." data-en="Full menu, exact pricing and availability on Booksy. Touch-ups and pedicure add-ons available by request.">Full menu, exact pricing and availability on Booksy. Touch-ups and pedicure add-ons available by request.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Color brillante, lista para lucir" data-en="Glossy color, ready to shine">Glossy color, ready to shine</span><img src="assets/raw/bk-12.jpg" alt="Glossy coral-red gel nails photographed against greenery outside Odi Nails &amp; Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Arte de estrella de mar" data-en="Hand-painted starfish art">Hand-painted starfish art</span><img src="assets/raw/bk-13.jpg" alt="Blue and white hand-painted starfish nail art on almond-shaped nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Francesa con detalle floral" data-en="French tip with floral detail">French tip with floral detail</span><img src="assets/raw/bk-15.jpg" alt="White French tip nails with hand-painted floral accents and rhinestones" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Acabado glitter blanco nieve" data-en="Snow-white glitter finish">Snow-white glitter finish</span><img src="assets/raw/bk-8.jpg" alt="Textured white and gold glitter acrylic nails with outlined tips" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Set nude almendra diario" data-en="Everyday nude almond set">Everyday nude almond set</span><img src="assets/raw/bk-14.jpg" alt="Milky nude almond-shaped acrylic nails, close up" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Pedicure recien terminado" data-en="Fresh pedicure finish">Fresh pedicure finish</span><img src="assets/raw/bk-9.jpg" alt="Freshly finished glossy nude pedicure on a pink towel" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 21 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 21 verified reviews on Booksy">5.0 out of 5 · 21 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"excelente atención y servicio❤️"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ángeles O…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing nails, clean studio and very nice. 10/10"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Estefany M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mágica experiencia!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yaremis</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 21 reseñas en Booksy" data-en="Read all 21 reviews on Booksy">Read all 21 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
MAPS_URL = 'https://www.google.com/maps?q=25.92573,-80.27805'
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Gardens</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">5433 NW 184th St, Miami Gardens, FL 33055</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="' + MAPS_URL + '"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,103,122,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,103,122,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')

old_ig_card = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(163,93,60,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@odicelisnails444</a>
            </div>
          </div>'''
new_ig_and_hours = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets mas recientes de Odi y escribe por DM cualquier duda antes de tu cita." data-en="See Odi's latest sets and DM any questions before your appointment.">See Odi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,103,122,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@odicelisnails444</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lun 10am-7pm · Mar-Vie 9:30am-1:30pm y 2:30-7pm · Sab 9:30am-1:30pm y 2:30-5pm · Dom 10am-1pm" data-en="Mon 10am-7pm · Tue-Fri 9:30am-1:30pm &amp; 2:30-7pm · Sat 9:30am-1:30pm &amp; 2:30-5pm · Sun 10am-1pm">Mon 10am-7pm · Tue-Fri 9:30am-1:30pm &amp; 2:30-7pm · Sat 9:30am-1:30pm &amp; 2:30-5pm · Sun 10am-1pm</p>
            </div>
          </div>'''
rep(old_ig_card, new_ig_and_hours)
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Odi Nails &amp; Studio, 5433 NW 184th St, Miami Gardens FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="' + MAPS_URL + '&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas disenadas para sentirse como arte." data-en="Nails designed to feel like art.">Nails designed to feel like art.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a una visita" data-en="is one visit away">is one visit away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu proximo set completo, el retoque de builder gel, o el mani-pedi que has estado posponiendo." data-en="Book online in seconds: your next full set, a builder gel touch-up, or the mani-pedi you have been meaning to schedule.">Book online in seconds: your next full set, a builder gel touch-up, or the mani-pedi you have been meaning to schedule.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Odi Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(245,195,175,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Odi Nails &amp; Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(243,205,184,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Odi Nails &amp; Studio</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de uñas en Miami Gardens, FL. Atención con cita previa." data-en="Nail studio in Miami Gardens, FL. By appointment only.">Nail studio in Miami Gardens, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>5433 NW 184th St, Miami Gardens, FL 33055</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f5c3af]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f3cdb8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f5c3af]">Instagram · @odicelisnails444</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f3cdb8]">Instagram · @odicelisnails444</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Odi Nails &amp; Studio.</p>')
print("FOOTER done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
