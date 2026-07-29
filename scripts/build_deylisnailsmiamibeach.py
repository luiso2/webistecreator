import re, os, shutil

SLUG = "deylis-nails-miami-beach"
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

# PALETTE: base plum-pink -> jewel-tone magenta/fuchsia (chrome-lilac glam, distinct from
# coral fairy / caramelo / esmeralda / teal acero / violeta dark / rosa dark / gold dark already used)
PALETTE = [
    ("#faf2f6", "#fdf1f8"), ("#f3e0ea", "#f5def0"), ("#a04a72", "#9c1f6b"),
    ("#c47a9c", "#c94f9e"), ("#c9789f", "#cf3f9c"), ("#5f2c48", "#5a1145"),
    ("#b25a85", "#ad2f87"), ("#f2d5e3", "#f6d3f0"), ("#d9a8c2", "#dd8ccb"),
    ("#e5c1d4", "#ecc0e6"), ("#7d3457", "#7a1660"), ("#5c2140", "#57123f"),
    ("#f0bed7", "#f3aee6"), ("#f8dfeb", "#fadaf5"), ("#f2cfe0", "#f6c7ee"),
    ("#fbeff5", "#fdeafa"), ("#efd0e0", "#f3c2ec"), ("#d3a2bc", "#d884cd"),
    ("#8a5573", "#863f7e"), ("#dc9dbe", "#de7ecb"), ("#2a1722", "#260f24"),
    ("#1f0f18", "#1b0a1a"), ("#1c0f16", "#190818"), ("#f6f1ea", "#fdf1f8"),
]
for old, new in PALETTE:
    assert old in h, "PALETTE MISS: " + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(156,31,107"), ("rgba(125,52,87", "rgba(122,22,96"),
    ("rgba(185,138,128", "rgba(200,130,175"), ("rgba(233,205,186", "rgba(230,179,213"),
    ("rgba(240,190,215", "rgba(243,174,230"), ("rgba(250,242,246", "rgba(253,241,248"),
    ("rgba(253,246,250", "rgba(255,247,252"), ("rgba(40,16,30", "rgba(38,15,36"),
    ("rgba(70,25,50", "rgba(68,15,42"),
]
for old, new in RGBA_PAIRS:
    assert old in h, "RGBA MISS: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/975972_deylisnails_nail-salon_15890_miami-beach'
IG_URL = 'https://www.instagram.com/DeylisNails/'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', IG_URL)
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@DeylisNails')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>DeylisNails · Nail Art Studio in Miami Beach, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="DeylisNails, Miami Beach FL: acrylic, gel and Poly Gel nail sets, hand-painted nail art, chrome finishes and spa pedicures with a perfect 5.0 across 61 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="DeylisNails · Nail Art Studio in Miami Beach, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, gel and hand-painted nail art. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-13.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-16.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "DeylisNails",
    "description": "Nail art studio in Miami Beach, FL: acrylic, hard gel, Poly Gel and Apres/Gel X sets, hand-painted nail art, chrome finishes and spa pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "2170 Bay Dr", "addressLocality": "Miami Beach", "addressRegion": "FL", "postalCode": "33141", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.855000009708576, "longitude": -80.13024999999998 },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "10:00", "closes": "19:00" }
    ],
    "sameAs": ["''' + BK_URL + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "61", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full set acrylic Nails encapsulated." } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres, Gel X - Soft Gel." } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Poly Gel" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luxury SPA Pedicure &gel." } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# PRELOADER
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">DN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">DeylisNails</span>')

# NAV
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,31,107,0.35)]" />',
    '<img src="assets/raw/bk-16.jpg" alt="DeylisNails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,31,107,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Deylis<span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami Beach, FL · Estudio de Unas" data-en="Miami Beach, FL · Nail Art Studio">Miami Beach, FL · Nail Art Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas con actitud, hechas para lucirse." data-en="Bold nails, made to turn heads.">Bold nails, made to turn heads.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Diseño de uñas con" data-en="Nail art with">Nail art with</span><br /><span data-es="cromo, color y " data-en="chrome, color and ">chrome, color and </span><span class="text-shine" data-es="detalle" data-en="detail">detail</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Desde sets acrílicos encapsulados hasta arte pintado a mano, efectos cromados y pedicura spa completa: Deylis González arma cada set para que dure, con un menú de más de 35 servicios y una calificación perfecta de 5.0." data-en="From encapsulated acrylic sets to hand-painted nail art, chrome finishes and full spa pedicures: Deylis González builds every set to last, with a menu of over 35 services and a perfect 5.0 rating.">From encapsulated acrylic sets to hand-painted nail art, chrome finishes and full spa pedicures: Deylis González builds every set to last, with a menu of over 35 services and a perfect 5.0 rating.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 61 reseñas en Booksy" data-en="5.0 · 61 reviews on Booksy">5.0 · 61 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-13.jpg" alt="Lilac chrome pointed stiletto nail set by DeylisNails" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Full set acrilico encapsulado" data-en="Full set acrylic, encapsulated">Full set acrylic, encapsulated</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$100 · 2h 30min" data-en="$100 · 2h 30min">$100 · 2h 30min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="61">61</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">36<span class="text-shine">+</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicios: acrilico a pedicura" data-en="Services: acrylic to pedicure">Services: acrylic to pedicure</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2170 Bay Dr</p></div>')

for old, new in [
    ('Classic Set', 'Acrylic Sets'),
    ('Hybrid Set', 'Gel Manicures'),
    ('Volume Set', 'Chrome Effect'),
    ('Mega Volume', 'Hand-Painted Art'),
    ('Bottom Lashes', 'Spa Pedicures'),
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
    '<img src="assets/raw/bk-4.jpg" alt="Deylis applying an acrylic tip at her Miami Beach studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-15.jpg" alt="Delicate lace-inspired bridal nail set by DeylisNails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="cada detalle hecho a mano" data-en="every detail done by hand">every detail done by hand</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="DeylisNails es el estudio de Deylis González en Miami Beach, FL. Trabaja con sistemas de acrílico, hard gel, Poly Gel y Apres/Gel X, con un menú de más de 35 servicios: desde sets encapsulados hasta arte pintado a mano, acabados cromados y efecto ojo de gato." data-en="DeylisNails is Deylis González'"'"'s studio in Miami Beach, FL. She works across acrylic, hard gel, Poly Gel and Apres/Gel X systems, with a menu of over 35 services, from encapsulated full sets to hand-painted nail art, chrome and cat-eye finishes.">DeylisNails is Deylis González'"'"'s studio in Miami Beach, FL. She works across acrylic, hard gel, Poly Gel and Apres/Gel X systems, with a menu of over 35 services, from encapsulated full sets to hand-painted nail art, chrome and cat-eye finishes.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 61 reseñas verificadas en Booksy, con clientas que vuelven set tras set por el detalle y el acabado." data-en="The result: a perfect 5.0 across 61 verified Booksy reviews, with clients who come back set after set for the detail and the finish.">The result: a perfect 5.0 across 61 verified Booksy reviews, with clients who come back set after set for the detail and the finish.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="61">61</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,31,107,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Deylis Gonzalez" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,31,107,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Deylis González · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, detalle" data-en="Your visit, detail">Your visit, detail</span> <span class="text-shine" data-es="a detalle" data-en="by detail">by detail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set, relleno o pedicura en Booksy con precios claros y confirmas al instante." data-en="Pick your set, fill or pedicure on Booksy with clear pricing, and confirm instantly.">Pick your set, fill or pedicure on Booksy with clear pricing, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu inspiracion" data-en="Your inspo">Your inspo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Traes una foto o una idea y Deylis define la forma, el largo y el arte o acabado cromado que buscas." data-en="Bring a photo or an idea and Deylis maps out shape, length and the art or chrome finish you want.">Bring a photo or an idea and Deylis maps out shape, length and the art or chrome finish you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="La aplicacion" data-en="The application">The application</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Relajate mientras Deylis arma tu set de acrilico, gel o Poly Gel a mano, desde un relleno rapido hasta un set encapsulado completo de 2h 30min." data-en="Sit back while Deylis builds your acrylic, gel or Poly Gel set by hand, from a quick fill to a full 2h 30min encapsulated set.">Sit back while Deylis builds your acrylic, gel or Poly Gel set by hand, from a quick fill to a full 2h 30min encapsulated set.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Acabado duradero" data-en="Long-lasting finish">Long-lasting finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set resistente al descascarado, una pedicura fresca, o el diseno pintado a mano que tenias en mente." data-en="You leave with a chip-resistant set, a fresh pedicure, or the hand-painted design you had in mind.">You leave with a chip-resistant set, a fresh pedicure, or the hand-painted design you had in mind.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por DeylisNails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by DeylisNails on Booksy. Booking confirms instantly.">Prices and durations as published by DeylisNails on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="acabado" data-en="finish">finish</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Set insignia" data-en="Signature set">Signature set</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full set acrilico encapsulado" data-en="Full set acrylic Nails encapsulated.">Full set acrylic Nails encapsulated.</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Nuestro set de acrilico mas completo, encapsulado para un acabado tipo cristal que dura de punta a cuticula." data-en="Our most complete acrylic set, encapsulated for a glass-like, long-lasting finish from tip to cuticle.">Our most complete acrylic set, encapsulated for a glass-like, long-lasting finish from tip to cuticle.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(156,31,107,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apres, Gel X - Soft Gel." data-en="Apres, Gel X - Soft Gel.">Apres, Gel X - Soft Gel.</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un sistema de gel suave y flexible, con la resistencia necesaria para sostener arte de unas detallado." data-en="A soft, flexible gel system for a natural feel with the strength to hold detailed nail art.">A soft, flexible gel system for a natural feel with the strength to hold detailed nail art.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema moderno" data-en="Modern system">Modern system</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Poly Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un hibrido ligero de gel y acrilico esculpido directamente sobre tu una natural para un set duradero." data-en="A lightweight gel-acrylic hybrid built directly on your natural nail for a sculpted, durable set.">A lightweight gel-acrylic hybrid built directly on your natural nail for a sculpted, durable set.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para tus pies" data-en="For your feet">For your feet</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luxury SPA Pedicure &amp;gel." data-en="Luxury SPA Pedicure &amp;gel.">Luxury SPA Pedicure &amp;gel.</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una pedicura spa completa terminada en esmalte en gel, con remojo, exfoliacion y masaje incluidos." data-en="A full spa pedicure finished in gel polish, with soak, scrub and massage included.">A full spa pedicure finished in gel polish, with soak, scrub and massage included.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-10">
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:100ms">
          <h3 class="font-display text-lg mb-4" data-es="Sets, rellenos y remocion" data-en="Sets, fills &amp; removal">Sets, fills &amp; removal</h3>
          <div class="space-y-1.5 text-sm">
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Acrylic full set.</span><span class="font-medium whitespace-nowrap">$60 · 2h</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Acrylic fill.</span><span class="font-medium whitespace-nowrap">$50 · 1h 30min</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Acrylic removal.</span><span class="font-medium whitespace-nowrap">$15</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Obre full set.</span><span class="font-medium whitespace-nowrap">$75</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Obre refill.</span><span class="font-medium whitespace-nowrap">$65</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Acrylic bath on natural nails.</span><span class="font-medium whitespace-nowrap">$50 · 1h 30min</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Full set Hard gel overlay &amp; Builder.</span><span class="font-medium whitespace-nowrap">$75</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Hard gel refill</span><span class="font-medium whitespace-nowrap">$65</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Poly Gel fill</span><span class="font-medium whitespace-nowrap">$70 · 1h</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Nail repair.</span><span class="font-medium whitespace-nowrap">$10</span></div>
            <div class="flex justify-between gap-3 py-1.5"><span class="text-[color:var(--ink-60)] font-light">Gel removal.</span><span class="font-medium whitespace-nowrap">$10</span></div>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:180ms">
          <h3 class="font-display text-lg mb-4" data-es="Manicura, pedicura y esmalte" data-en="Manicure, pedicure &amp; polish">Manicure, pedicure &amp; polish</h3>
          <div class="space-y-1.5 text-sm">
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Acrylic pedicure.</span><span class="font-medium whitespace-nowrap">$65</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Rubber base coat.</span><span class="font-medium whitespace-nowrap">$55 · 1h 20min</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Manicure regular</span><span class="font-medium whitespace-nowrap">$20</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Polish change hansd regular.</span><span class="font-medium whitespace-nowrap">$15</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Pedicure regular.</span><span class="font-medium whitespace-nowrap">$35</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Polish change toes regular.</span><span class="font-medium whitespace-nowrap">$25</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Manicure gel</span><span class="font-medium whitespace-nowrap">$35</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Pedicure gel</span><span class="font-medium whitespace-nowrap">$45 · 1h</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Polish change hands gel.</span><span class="font-medium whitespace-nowrap">$25</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Polish change toes gel</span><span class="font-medium whitespace-nowrap">$35</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Paraffin Treatment.</span><span class="font-medium whitespace-nowrap">$15</span></div>
            <div class="flex justify-between gap-3 py-1.5"><span class="text-[color:var(--ink-60)] font-light">Callus remove.</span><span class="font-medium whitespace-nowrap">$15</span></div>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:260ms">
          <h3 class="font-display text-lg mb-4" data-es="Arte y acabados" data-en="Nail art &amp; finishes">Nail art &amp; finishes</h3>
          <div class="space-y-1.5 text-sm">
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Basic Nail art.</span><span class="font-medium whitespace-nowrap">$20</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Better nail art.</span><span class="font-medium whitespace-nowrap">$25</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Beast nail art.</span><span class="font-medium whitespace-nowrap">$35</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Classic French.</span><span class="font-medium whitespace-nowrap">$10</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Custom complex french.</span><span class="font-medium whitespace-nowrap">$20</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Oval shaped.</span><span class="font-medium whitespace-nowrap">$10</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Cat Eye Effect.</span><span class="font-medium whitespace-nowrap">$20</span></div>
            <div class="flex justify-between gap-3 py-1.5 border-b border-[color:var(--accent-ghost)]"><span class="text-[color:var(--ink-60)] font-light">Chrome Effect.</span><span class="font-medium whitespace-nowrap">$15</span></div>
            <div class="flex justify-between gap-3 py-1.5"><span class="text-[color:var(--ink-60)] font-light">Reflective.</span><span class="font-medium whitespace-nowrap">$15</span></div>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="36 servicios en total: sets, rellenos, arte de unas, pedicura y mas. Menu completo y disponibilidad en Booksy." data-en="36 services in total: sets, fills, nail art, pedicures and more. Full menu and availability on Booksy.">36 services in total: sets, fills, nail art, pedicures and more. Full menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Arte de" data-en="Real">Real</span> <span class="text-shine" data-es="unas real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Ombre nude firma" data-en="Signature nude ombre">Signature nude ombre</span><img src="assets/raw/bk-6.jpg" alt="Soft nude ombre coffin nail set by DeylisNails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Arte esmeralda" data-en="Emerald scale art">Emerald scale art</span><img src="assets/raw/bk-3.jpg" alt="Emerald and gold marble scale-pattern nail art" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Flor con pedreria" data-en="Floral rhinestone accent">Floral rhinestone accent</span><img src="assets/raw/bk-5.jpg" alt="Pink ombre coffin nails with hand-painted white flower and rhinestones" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Cromo neon" data-en="Neon chrome edge">Neon chrome edge</span><img src="assets/raw/bk-7.jpg" alt="Neon green chrome snake-pattern coffin nail set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Perlas 3D" data-en="3D pearl florals">3D pearl florals</span><img src="assets/raw/bk-9.jpg" alt="Long pink coffin nails with 3D flower and pearl details" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Pedicura con arte" data-en="Pedicure with art">Pedicure with art</span><img src="assets/raw/bk-8.jpg" alt="White pedicure with hand-painted paw print nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 61 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 61 verified reviews on Booksy">5.0 out of 5 · 61 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maria R...</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Las amo"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Amber</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Deylis es la mejor 💗✨"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Luisina A...</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 61 reseñas en Booksy" data-en="Read all 61 reviews on Booksy">Read all 61 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
MAPS_URL = 'https://www.google.com/maps?q=2170+Bay+Dr,+Miami+Beach,+FL+33141'
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Beach</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">2170 Bay Dr, Miami Beach, FL 33141</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="' + MAPS_URL + '"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,31,107,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,31,107,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')

old_ig_card = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,31,107,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@DeylisNails</a>
            </div>
          </div>'''
new_ig_and_hours = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los disenos mas recientes de Deylis y escribe por DM cualquier duda antes de tu cita." data-en="See Deylis's latest designs and DM any questions before your appointment.">See Deylis's latest designs and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,31,107,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@DeylisNails</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sabado, 10:00 am a 7:00 pm." data-en="Monday to Saturday, 10:00 am to 7:00 pm.">Monday to Saturday, 10:00 am to 7:00 pm.</p>
            </div>
          </div>'''
rep(old_ig_card, new_ig_and_hours)
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: DeylisNails, 2170 Bay Dr, Miami Beach FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="' + MAPS_URL + '&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas con actitud, hechas para lucirse." data-en="Bold nails, made to turn heads.">Bold nails, made to turn heads.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu set de acrilico, tu relleno en gel, o el diseno pintado a mano y acabado cromado que has estado planeando." data-en="Book online in seconds: your acrylic set, your gel fill, or the hand-painted design and chrome finish you have been planning.">Book online in seconds: your acrylic set, your gel fill, or the hand-painted design and chrome finish you have been planning.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">DeylisNails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(243,174,230,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="DeylisNails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(243,174,230,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">DeylisNails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de uñas en Miami Beach, FL. Atención con cita previa." data-en="Nail studio in Miami Beach, FL. By appointment only.">Nail studio in Miami Beach, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>2170 Bay Dr, Miami Beach, FL 33141</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f3aee6]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f3aee6]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f3aee6]">Instagram · @DeylisNails</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f3aee6]">Instagram · @DeylisNails</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 DeylisNails.</p>')
print("FOOTER done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
