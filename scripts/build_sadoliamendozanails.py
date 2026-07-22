import re, os, shutil

SLUG = "sadolia-mendoza-nails"
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

# PALETTE: hue rotation +75.91deg from base pink -> warm gold/olive (champagne)
PALETTE = [
    ("#faf2f6", "#faf8f2"), ("#f3e0ea", "#f3eee0"), ("#a04a72", "#a08f4a"),
    ("#c47a9c", "#c4b67a"), ("#c9789f", "#c9b778"), ("#5f2c48", "#5f512c"),
    ("#b25a85", "#b29e5a"), ("#f2d5e3", "#f2ecd5"), ("#d9a8c2", "#d9cca8"),
    ("#e5c1d4", "#e5dcc1"), ("#7d3457", "#7d6d34"), ("#5c2140", "#5c4d21"),
    ("#f0bed7", "#f0e4be"), ("#f8dfeb", "#f8f3df"), ("#f2cfe0", "#f2eacf"),
    ("#fbeff5", "#fbf8ef"), ("#efd0e0", "#efe7d0"), ("#d3a2bc", "#d3c6a2"),
    ("#8a5573", "#8a7a55"), ("#dc9dbe", "#dccc9d"), ("#2a1722", "#2a2417"),
    ("#1f0f18", "#1f1a0f"), ("#1c0f16", "#1c180f"), ("#f6f1ea", "#ecf6ea"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(160,143,74"),
    ("rgba(125,52,87", "rgba(125,109,52"),
    ("rgba(185,138,128", "rgba(160,185,128"),
    ("rgba(233,205,186", "rgba(202,233,186"),
    ("rgba(240,190,215", "rgba(240,228,190"),
    ("rgba(250,242,246", "rgba(250,248,242"),
    ("rgba(253,246,250", "rgba(253,251,246"),
    ("rgba(40,16,30", "rgba(40,32,16"),
    ("rgba(70,25,50", "rgba(70,57,25"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/1303630_sadolia-mendoza-nails_nail-salon_15886_hialeah'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/sadoliamendozanails/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@sadoliamendozanails')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Sadolia Mendoza Nails · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Sadolia Mendoza Nails, Hialeah FL: builder gel, rubber base, Apres Gel-X and freehand nail art with Leidy, 5.0 across 15 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Sadolia Mendoza Nails · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Builder gel, rubber base and freehand nail art. 5.0 on Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-16.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-3.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Sadolia Mendoza Nails",
    "description": "Nail salon in Hialeah, FL: builder gel, rubber base, Apres Gel-X, acrylic and freehand nail art.",
    "address": { "@type": "PostalAddress", "streetAddress": "18505 NW 75th Place, Suite 118", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33015", "addressCountry": "US" },
    "sameAs": ["''' + BK_URL + '''", "https://www.instagram.com/sadoliamendozanails/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "15", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Gel" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Gel-X" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel" } },
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Cejas" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">SM</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Sadolia Mendoza Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,143,74,0.35)]" />',
    '<img src="assets/raw/bk-3.jpg" alt="Sadolia Mendoza Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,143,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Sadolia <span class="text-[color:var(--accent-deep)]">Mendoza</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Nail Salon" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas con pasion, hechas a mano." data-en="Nails with passion, made by hand.">Nails with passion, made by hand.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Builder gel, rubber base" data-en="Builder gel, rubber base">Builder gel, rubber base</span><br /><span data-es="y arte a mano, pensados para " data-en="and freehand art, made to ">and freehand art, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Builder gel, rubber base, Apres Gel-X, polygel y acrilico, con arte a mano alzada que Leidy disena con precision. Clientas la describen como meticulosa y llevan mas de 2 anos confiando solo en ella." data-en="Builder gel, rubber base, Apres Gel-X, polygel and acrylic, with freehand art Leidy designs with precision. Clients describe her as meticulous, and some have trusted only her for over 2 years.">Builder gel, rubber base, Apres Gel-X, polygel y acrilico, con arte a mano alzada que Leidy disena con precision. Clientas la describen como meticulosa y llevan mas de 2 anos confiando solo en ella.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 15 reseñas en Booksy" data-en="5.0 · 15 reviews on Booksy">5.0 · 15 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-16.jpg" alt="Diseno de unas floral colorido en Sadolia Mendoza Nails" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Apres Gel-X" data-en="Apres Gel-X">Apres Gel-X</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$70 · Precio fijo" data-en="$70 · Flat rate">$70 · Flat rate</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="15">15</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">+2 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles" data-en="Clients who stay">Clients who stay</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Por cita" data-en="By appt">By appt</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atencion personalizada" data-en="Personalized care">Personalized care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">NW 75th Place</p></div>')

for old, new in [
    ('Classic Set', 'Builder Gel'),
    ('Hybrid Set', 'Rubber Base'),
    ('Volume Set', 'Apres Gel-X'),
    ('Mega Volume', 'Polygel'),
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
    '<img src="assets/raw/bk-6.jpg" alt="Manicura francesa blanca con acentos dorados en Sadolia Mendoza Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Unas nude con diseno de joyeria dorada en Sadolia Mendoza Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="hecho con pasion y precision" data-en="made with passion and precision">made with passion and precision</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Sadolia Mendoza Nails es el estudio de Leidy Sadolia en Hialeah. Sus clientas la describen como meticulosa y detallista, con arte a mano alzada que califican de obra de arte, y atencion personalizada por cita." data-en="Sadolia Mendoza Nails is Leidy Sadolia studio in Hialeah. Her clients describe her as meticulous and detail-oriented, with freehand art they call a work of art, and personalized care by appointment.">Sadolia Mendoza Nails es el estudio de Leidy Sadolia en Hialeah. Sus clientas la describen como meticulosa y detallista, con arte a mano alzada que califican de obra de arte, y atencion personalizada por cita.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 15 resenas verificadas en Booksy, y clientas que llevan mas de 2 anos sin dejarse las unas con nadie mas." data-en="The result: a perfect 5.0 across 15 verified Booksy reviews, and clients who have not trusted anyone else with their nails for over 2 years.">El resultado: 5.0 perfecto en 15 resenas verificadas en Booksy, y clientas que llevan mas de 2 anos sin dejarse las unas con nadie mas.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="15">15</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,143,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Sadolia Mendoza Nails" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,143,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Leidy · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, detalle" data-en="Your visit, detail">Your visit, detail</span> <span class="text-shine" data-es="por detalle" data-en="by detail">by detail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Diagnostico" data-en="Consultation">Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de la una y el sistema que buscas: builder gel, rubber base, Apres o acrilico." data-en="Nail shape and the system you want: builder gel, rubber base, Apres or acrylic.">Nail shape and the system you want: builder gel, rubber base, Apres or acrylic.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Leidy trabaja cada detalle con precision, del color solido al arte a mano alzada mas elaborado." data-en="Leidy works every detail with precision, from a solid color to the most elaborate freehand art.">Leidy works every detail with precision, from a solid color to the most elaborate freehand art.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus unas terminadas y, si quieres, tu proximo relleno ya agendado." data-en="You leave with your finished nails and, if you want, your next fill already booked.">You leave with your finished nails and, if you want, your next fill already booked.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Sadolia Mendoza Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Sadolia Mendoza Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Sadolia Mendoza Nails on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="sistema" data-en="system">system</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Basico" data-en="Basic">Basic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Gel" data-en="Gel Manicure">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure en gel con acabado impecable, tambien disponible con pedicura regular por $50." data-en="Gel manicure with a flawless finish, also available bundled with a regular pedicure for $50.">Gel manicure with a flawless finish, also available bundled with a regular pedicure for $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,143,74,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apres Gel-X" data-en="Apres Gel-X">Apres Gel-X</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensiones Apres Gel-X, ligeras y con acabado natural, el set mas pedido del estudio." data-en="Apres Gel-X extensions, lightweight with a natural finish, the studio most requested set.">Apres Gel-X extensions, lightweight with a natural finish, the studio most requested set.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema" data-en="System">System</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Builder Gel" data-en="Builder Gel">Builder Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Builder gel o rubber base, la base solida y natural para tu diseno." data-en="Builder gel or rubber base, the solid, natural base for your design.">Builder gel or rubber base, the solid, natural base for your design.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cejas" data-en="Brows">Cejas</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas desde $20, o el combo manicure y pedicure para hombre por $50." data-en="Brows from $20, or the men manicure and pedicure combo for $50.">Brows from $20, or the men manicure and pedicure combo for $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $20" data-en="From $20">From $20</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">15min+</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: extensiones con tip, polygel, acrilico, gel pedicure y bigote. Menu completo y disponibilidad en Booksy." data-en="Also available: tip extensions, polygel, acrylic, gel pedicure and mustache wax. Full menu and availability on Booksy.">Also available: tip extensions, polygel, acrylic, gel pedicure and mustache wax. Full menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Diseno" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Francesa con encaje" data-en="Lace french">Francesa con encaje</span><img src="assets/raw/bk-8.jpg" alt="Manicura francesa nude con fondo de encaje en Sadolia Mendoza Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Minimalista negro" data-en="Minimal black tip">Minimalista negro</span><img src="assets/raw/bk-4.jpg" alt="Unas nude con punta negra minimalista" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Acento amarillo" data-en="Yellow tip accent">Acento amarillo</span><img src="assets/raw/bk-5.jpg" alt="Unas nude con acento amarillo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Flor azul" data-en="Blue flower accent">Flor azul</span><img src="assets/raw/bk-9.jpg" alt="Unas blancas con flor azul" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Ombre rosa" data-en="Pink ombre">Ombre rosa</span><img src="assets/raw/bk-10.jpg" alt="Unas con ombre rosa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Flor delicada" data-en="Delicate flower">Flor delicada</span><img src="assets/raw/bk-15.jpg" alt="Unas nude con flor delicada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 15 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 15 verified reviews on Booksy">5.0 out of 5 · 15 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing service as usual"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jessica F…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I've trusted Leidy with my nails for over 2 years, and I wouldn't go anywhere else! She is so kind, professional, and incredibly talented. Every design she creates is a work of art, especially her amazing freehand work."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Prisy F…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Muy buen trabajo, la recomiendo 100%"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yurkia L…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 15 reseñas en Booksy" data-en="Read all 15 reviews on Booksy">Read all 15 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">18505 NW 75th Place, Suite 118, Hialeah, FL 33015</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=18505+NW+75th+Place,+Hialeah,+FL+33015"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,143,74,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,143,74,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Leidy y escribe por DM cualquier duda antes de tu cita." data-en="See Leidy\'s latest designs and DM any questions before your appointment.">See Leidy\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Sadolia Mendoza Nails, 18505 NW 75th Place, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=18505+NW+75th+Place,+Hialeah,+FL+33015&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas con pasion, hechas a mano." data-en="Nails with passion, made by hand.">Nails with passion, made by hand.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu builder gel, tu Apres Gel-X o el diseno a mano que llevas planeando." data-en="Book online in seconds: your builder gel, your Apres Gel-X, or the freehand design you have been planning.">Book online in seconds: your builder gel, your Apres Gel-X, or the freehand design you have been planning.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Sadolia Mendoza Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,228,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Sadolia Mendoza Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,228,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Sadolia Mendoza Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Nail salon in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>18505 NW 75th Place, Suite 118, Hialeah, FL 33015</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f0e4be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f0e4be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/sadoliamendozanails/" target="_blank" rel="noopener" class="hover:text-[#f0e4be]">Instagram · @sadoliamendozanails</a></p>',
    '<p><a href="https://www.instagram.com/sadoliamendozanails/" target="_blank" rel="noopener" class="hover:text-[#f0e4be]">Instagram · @sadoliamendozanails</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Sadolia Mendoza Nails.</p>')
print("FOOTER done")

# book-float
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
