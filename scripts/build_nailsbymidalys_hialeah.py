import re, os, shutil

SLUG = "nailsbymidalys_hialeah"
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

# PALETTE: hue rotation -5.5deg (rose-pink -> deep plum/wine berry) + L*0.74 / S*1.08
# on mid-lightness tones only (backgrounds and near-blacks keep their L, hue-only shift).
PALETTE = [
    ("#faf2f6", "#faf2f7"), ("#f3e0ea", "#f3e0ec"), ("#a04a72", "#79345a"),
    ("#c47a9c", "#a7457b"), ("#c9789f", "#ae407f"), ("#5f2c48", "#481f39"),
    ("#b25a85", "#8a3c69"), ("#f2d5e3", "#f2d5e6"), ("#d9a8c2", "#be5f9a"),
    ("#e5c1d4", "#e5c1d7"), ("#7d3457", "#5f2446"), ("#5c2140", "#461734"),
    ("#f0bed7", "#f0bedc"), ("#f8dfeb", "#f8dfed"), ("#f2cfe0", "#f2cfe3"),
    ("#fbeff5", "#fbeff6"), ("#efd0e0", "#efd0e3"), ("#d3a2bc", "#b75d95"),
    ("#8a5573", "#683d59"), ("#dc9dbe", "#c75099"), ("#2a1722", "#2a1724"),
    ("#1f0f18", "#1f0f19"), ("#1c0f16", "#1c0f17"), ("#f6f1ea", "#f6f0ea"),
    ("#fbf3f8", "#fbf3f9"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(121,52,90"),
    ("rgba(125,52,87", "rgba(95,36,70"),
    ("rgba(185,138,128", "rgba(152,86,80"),
    ("rgba(233,205,186", "rgba(233,201,186"),
    ("rgba(240,190,215", "rgba(240,190,220"),
    ("rgba(250,242,246", "rgba(250,242,247"),
    ("rgba(253,246,250", "rgba(253,246,251"),
    ("rgba(40,16,30", "rgba(40,16,32"),
    ("rgba(70,25,50", "rgba(70,25,54"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/nailsbymidalys1992/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@nailsbymidalys1992')

# Idioma: negocio en espanol -> default es
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Nailsbymidalys · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nailsbymidalys, Hialeah FL: acrylic, dip powder, hard gel and rubber base nail systems plus spa pedicures, with a perfect 5.0 across 64 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nailsbymidalys · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, dip powder and hard gel nail systems. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-10.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nailsbymidalys",
    "description": "Nail salon in Hialeah, FL: acrylic, dip powder, hard gel and rubber base nail systems, plus spa pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "2503 W 71st Place", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33016", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah", "https://www.instagram.com/nailsbymidalys1992/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "64", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "95", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic nails corta" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Refill Acrilico" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Dip powder" } },
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicura gel" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NM</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nailsbymidalys</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(121,52,90,0.35)]" />',
    '<img src="assets/raw/bk-1.jpg" alt="Nailsbymidalys" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(121,52,90,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails <span class="text-[color:var(--accent-deep)]">by Midalys</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Nail Studio" data-en="Hialeah, FL · Nail Studio">Hialeah, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Uñas hechas con calma y detalle." data-en="Nails made with calm and detail.">Uñas hechas con calma y detalle.</p>\n        <h1',)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrílico, dip powder" data-en="Acrylic, dip powder">Acrílico, dip powder</span><br /><span data-es="y gel, hechos para " data-en="and gel, made to ">and gel, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Acrílico, dip powder, hard gel y rubber base, más pedicura en gel, todo con cita previa vía Booksy. Midalys López atiende en Hialeah con detalle en cada set." data-en="Acrylic, dip powder, hard gel and rubber base, plus gel pedicures, all by appointment via Booksy. Midalys López works out of Hialeah with detail in every set.">Acrylic, dip powder, hard gel and rubber base, plus gel pedicures, all by appointment via Booksy. Midalys López works out of Hialeah with detail in every set.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 64 reseñas en Booksy" data-en="5.0 · 64 reviews on Booksy">5.0 · 64 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-10.jpg" alt="Manicura en gel color berenjena sobre uñas almendradas con acabado brillante" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Acrylic nails corta" data-en="Acrylic nails corta">Acrylic nails corta</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$95 · 2h 45min" data-en="$95 · 2h 45min">$95 · 2h 45min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="64">64</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrílico <span class="text-shine">&amp;</span> Dip</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sistemas y diseños" data-en="Systems and nail art">Systems and nail art</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">16 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W 71st Place</p></div>')

for old, new in [
    ('Classic Set', 'Acrílico'),
    ('Hybrid Set', 'Dip Powder'),
    ('Volume Set', 'Rubber Base'),
    ('Mega Volume', 'Luminary'),
    ('Bottom Lashes', 'Hard Gel'),
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
    '<img src="assets/raw/bk-1.jpg" alt="Interior del estudio Nailsbymidalys con iluminación dorada y el logo en la pared" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Detalle de uñas nude con punta blanca, gema iridiscente y pulsera dorada" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="que se siente como en casa" data-en="that feels like home">that feels like home</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Nailsbymidalys es el estudio de Midalys López en Hialeah, con cita previa vía Booksy. Clientas cuentan que las reciben con un espresso y una galleta, y que el trato se siente como en casa desde que llegan." data-en="Nailsbymidalys is Midalys López studio in Hialeah, by appointment via Booksy. Clients say they are greeted with an espresso and a biscuit, and that the welcome feels like home from the moment they arrive.">Nailsbymidalys is Midalys López studio in Hialeah, by appointment via Booksy. Clients say they are greeted with an espresso and a biscuit, and that the welcome feels like home from the moment they arrive.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 64 reseñas verificadas en Booksy, con un menú de acrílico, dip powder, hard gel, rubber base y pedicura en gel." data-en="The result: a perfect 5.0 across 64 verified Booksy reviews, with a menu of acrylic, dip powder, hard gel, rubber base and gel pedicures.">The result: a perfect 5.0 across 64 verified Booksy reviews, with a menu of acrylic, dip powder, hard gel, rubber base and gel pedicures.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="64">64</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(121,52,90,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Midalys López" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(121,52,90,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Midalys · <span class="text-[color:var(--ink-40)]" data-es="Dueña y técnica de uñas" data-en="Owner and nail technician">Owner and nail technician</span></span>')
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges el largo, la forma y el sistema: acrílico, dip powder, hard gel o rubber base, según lo que buscas." data-en="You choose the length, shape and system: acrylic, dip powder, hard gel or rubber base, based on what you want.">You choose the length, shape and system: acrylic, dip powder, hard gel or rubber base, based on what you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Midalys trabaja con calma y detalle, hasta 2h 55min según el sistema y el diseño que elijas." data-en="Midalys works calmly and with detail, up to 2h 55min depending on the system and design you choose.">Midalys works calmly and with detail, up to 2h 55min depending on the system and design you choose.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu set terminado, listo para lucirlo." data-en="You leave with your finished set, ready to show off.">You leave with your finished set, ready to show off.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nailsbymidalys en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nailsbymidalys on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Nailsbymidalys en Booksy. Reserva con confirmación inmediata.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="set" data-en="set">set</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
BOOKSY = "https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah"
NEW_SERVICES = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clasico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Acrylic Nails Corta" data-en="Acrylic Nails Corta">Acrylic Nails Corta</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrílico en largo corto, base solida para cualquier diseño." data-en="Full acrylic set in a short length, a solid base for any design.">Full acrylic set in a short length, a solid base for any design.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$95</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 45min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(121,52,90,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Refill Acrilico" data-en="Refill Acrilico">Refill Acrilico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio que mas se repite: mantén tu set de acrílico en perfecto estado cada pocas semanas." data-en="The most repeated service: keep your acrylic set in perfect shape every few weeks.">The most repeated service: keep your acrylic set in perfect shape every few weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 50min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema en polvo" data-en="Powder system">Powder system</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Dip Powder" data-en="Dip Powder">Dip Powder</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sistema dip powder resistente y con acabado natural. También disponible en Apres gel por el mismo precio." data-en="Durable dip powder system with a natural finish. Also available in Apres gel at the same price.">Durable dip powder system with a natural finish. Also available in Apres gel at the same price.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies" data-en="Feet">Feet</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicura Gel" data-en="Gel Pedicure">Gel Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura con esmaltado en gel de larga duración, terminación pulida y pareja." data-en="Pedicure with long-lasting gel polish, a polished and even finish.">Pedicure with long-lasting gel polish, a polished and even finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: hard gel, rubber base, builder gel, cambio de cover y más. Menú completo de 16 servicios y disponibilidad en Booksy." data-en="Also available: hard gel, rubber base, builder gel, cover changes and more. Full 16-service menu and availability on Booksy.">Also available: hard gel, rubber base, builder gel, cover changes and more. Full 16-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Manicura roja brillante" data-en="Glossy red manicure">Glossy red manicure</span><img src="assets/raw/bk-4.jpg" alt="Manos entrelazadas con manicura roja brillante y anillos dorados" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rojo intenso" data-en="Bold red">Bold red</span><img src="assets/raw/bk-13.jpg" alt="Uñas almendradas rojas con acabado espejo" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Diseño floral holográfico" data-en="Holographic floral art">Holographic floral art</span><img src="assets/raw/bk-11.jpg" alt="Diseño de uñas holográfico con flores en relieve y delineado dorado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Ombré con lámina dorada" data-en="Ombré with gold foil">Ombré with gold foil</span><img src="assets/raw/bk-12.jpg" alt="Uñas nude degradadas con lámina dorada y anillo de esmeraldas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Stiletto con cristales" data-en="Stiletto with crystals">Stiletto with crystals</span><img src="assets/raw/bk-7.jpg" alt="Uñas blancas estilo stiletto con cristales rojos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Nude con brillo" data-en="Nude with glitter">Nude with glitter</span><img src="assets/raw/bk-3.jpg" alt="Uña nude con acento de brillo iridiscente" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES (reales, con autor)
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 64 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 64 verified reviews on Booksy">5.0 out of 5 · 64 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"la mejor"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chinita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encantaron"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anisleidy V…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The place is so welcoming! She greeted me with an espresso and a biscuit. Felt right at home. My service was amazing. My nails were exactly what I wanted. Looking forward to going back."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Diana M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 64 reseñas en Booksy" data-en="Read all 64 reviews on Booksy">Read all 64 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">2503 W 71st Place, Hialeah, FL 33016</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=2503+W+71st+Place,+Hialeah,+FL+33016"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: los horarios varían según el día, y la confirmación es inmediata." data-en="By appointment via Booksy: hours vary by day, and the confirmation is instant.">By appointment via Booksy: hours vary by day, and the confirmation is instant.</p>')
assert '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(121,52,90,0.4)]" href="https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>' in h
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los diseños más recientes de Midalys y escribe por DM cualquier duda antes de tu cita." data-en="See Midalys\'s latest designs and DM any questions before your appointment.">See Midalys\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Nailsbymidalys, 2503 W 71st Place, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=2503+W+71st+Place,+Hialeah,+FL+33016&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Uñas hechas con calma y detalle." data-en="Nails made with calm and detail.">Uñas hechas con calma y detalle.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu acrílico, tu dip powder o el refill que ya te toca." data-en="Book online in seconds: your acrylic, your dip powder, or the refill you are due for.">Book online in seconds: your acrylic, your dip powder, or the refill you are due for.</p>')
rep('<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("166337_belleciia-nails_nail-salon_15886_hialeah", "994954_nailsbymidalys_nail-salon_15886_hialeah"),
    '<a href="https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Nailsbymidalys</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,220,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Nailsbymidalys" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,220,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Nailsbymidalys</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de uñas en Hialeah, FL. Atención con cita previa." data-en="Nail studio in Hialeah, FL. By appointment only.">Nail studio in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>2503 W 71st Place, Hialeah, FL 33016</p>')
assert '<p><a href="https://booksy.com/en-us/994954_nailsbymidalys_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="hover:text-[#f0bedc]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>' in h
assert '<p><a href="https://www.instagram.com/nailsbymidalys1992/" target="_blank" rel="noopener" class="hover:text-[#f0bedc]">Instagram · @nailsbymidalys1992</a></p>' in h
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nailsbymidalys.</p>')
print("FOOTER done")

# lang default -> es
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
