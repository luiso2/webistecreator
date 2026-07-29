import re, os, shutil

SLUG = "magicfaces_tampa"
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

# PALETTE: uniform hue rotation (+65.907deg) + saturation x1.62 + lightness +0.015
# from base plum-pink (#a04a72) -> warm honey-gold amber (#c18c31, H38 L47.5% S59.5%)
# distinct from caramelo #a86a2e (H29.5 darker) and template gold #d4a84b (H41 lighter).
PALETTE = [
    ("#faf2f6", "#fefbf6"), ("#f3e0ea", "#faefe1"), ("#a04a72", "#c18c31"),
    ("#c47a9c", "#dcb369"), ("#c9789f", "#e3b365"), ("#5f2c48", "#754e1e"),
    ("#b25a85", "#cf9945"), ("#f2d5e3", "#fcecd3"), ("#d9a8c2", "#eac99f"),
    ("#e5c1d4", "#f1dbbc"), ("#7d3457", "#9a6b1f"), ("#5c2140", "#754a10"),
    ("#f0bed7", "#ffe2b7"), ("#f8dfeb", "#fff3e0"), ("#f2cfe0", "#fdeacc"),
    ("#fbeff5", "#fffaf3"), ("#efd0e0", "#f9e7cd"), ("#d3a2bc", "#e4c399"),
    ("#8a5573", "#a07647"), ("#dc9dbe", "#f0c890"), ("#2a1722", "#362513"),
    ("#1f0f18", "#2a1c0c"), ("#1c0f16", "#261b0d"), ("#f6f1ea", "#f6ead8"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(125,52,87", "rgba(154,107,31"),
    ("rgba(160,74,114", "rgba(193,140,49"),
    # dusty rose/tan outliers hand-tuned (formula pushed these into green, off-theme)
    ("rgba(185,138,128", "rgba(196,150,88"),
    ("rgba(233,205,186", "rgba(224,188,132"),
    ("rgba(240,190,215", "rgba(255,226,183"),
    ("rgba(250,242,246", "rgba(254,251,246"),
    ("rgba(253,246,250", "rgba(255,253,252"),
    ("rgba(70,25,50", "rgba(91,55,12"),
    ("rgba(40,16,30", "rgba(54,32,10"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/magicfaces2025/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@magicfaces2025')

# Idioma: negocio en espanol -> default es
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Magic Faces · Beauty Studio in Tampa, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Magic Faces, Tampa FL: henna brows, lash lift and tint, facials, chemical peels and waxing with a perfect 5.0 across 8 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Magic Faces · Beauty Studio in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Henna brows, facials and skin care. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-11.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Magic Faces",
    "description": "Beauty studio in Tampa, FL: henna brows, lash lift and tint, facials, chemical peels and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "6821 N Dale Mabry Hwy", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33614", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa", "https://www.instagram.com/magicfaces2025/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "8", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "10:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "09:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Beauty services", "itemListElement": [
      { "@type": "Offer", "price": "41", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Henna Brows" } },
      { "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Duo Glow Facial" } },
      { "@type": "Offer", "price": "117", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Chemical Peel" } },
      { "@type": "Offer", "price": "14", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Eyebrow Waxing" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">MF</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Magic Faces</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />'.replace("160,74,114", "193,140,49"),
    '<img src="assets/raw/bk-1.jpg" alt="Magic Faces" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(193,140,49,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Magic <span class="text-[color:var(--accent-deep)]">Faces</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Estudio de Belleza" data-en="Tampa, FL · Beauty Studio">Tampa, FL · Beauty Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="El cuidado que tu piel merece." data-en="The care your skin deserves.">The care your skin deserves.</p>\n        <h1',)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Cejas, piel y brillo," data-en="Brows, skin and glow,">Brows, skin and glow,</span><br /><span data-es="cuidados hechos para " data-en="care made to ">care made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Cejas con henna, lifting y tinte de pestañas, faciales, peelings químicos y depilación con Betsy Esquivel, el estudio de estética de Tampa. Resultados reales, reservados directo por Booksy." data-en="Henna brows, lash lift and tint, facials, chemical peels and waxing with Betsy Esquivel, Tampa\'s own esthetician studio. Real results, booked straight through Booksy.">Henna brows, lash lift and tint, facials, chemical peels and waxing with Betsy Esquivel, Tampa\'s own esthetician studio. Real results, booked straight through Booksy.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 8 reseñas en Booksy" data-en="5.0 · 8 reviews on Booksy">5.0 · 8 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-11.jpg" alt="Manicura roja francesa con diseño floral en Magic Faces" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Duo Glow Facial" data-en="Duo Glow Facial">Duo Glow Facial</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$150" data-en="$150">$150</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="8">8</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Brows <span class="text-shine">&amp;</span> Facials</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cejas, pestañas y piel" data-en="Brows, lashes and skin">Brows, lashes and skin</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">17 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">N Dale Mabry Hwy</p></div>')

for old, new in [
    ('Classic Set', 'Henna Brows'),
    ('Hybrid Set', 'Brow Lamination'),
    ('Volume Set', 'Chemical Peel'),
    ('Mega Volume', 'Duo Glow Facial'),
    ('Bottom Lashes', 'Lash Lift'),
    ('West Palm Beach, FL', 'Tampa, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Manicura blanca con perlas sobre satín en Magic Faces" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Resultado de tratamiento de labios hidratados en Magic Faces" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="cuidado personal" data-en="personal care">personal care</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Magic Faces es el estudio de belleza de Betsy Esquivel en Tampa. Betsy atiende ella misma todo el menú de esteticista, desde cejas con henna y lifting de pestañas hasta faciales, peelings químicos y depilación, siempre con cita previa en Booksy." data-en="Magic Faces is Betsy Esquivel\'s beauty studio in Tampa. Betsy covers the full esthetician menu herself, from henna brows and lash lift and tint to facials, chemical peels and waxing, all by appointment on Booksy.">Magic Faces is Betsy Esquivel\'s beauty studio in Tampa. Betsy covers the full esthetician menu herself, from henna brows and lash lift and tint to facials, chemical peels and waxing, all by appointment on Booksy.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 8 reseñas verificadas en Booksy, y un menú de 17 servicios que cubre piel, cejas y pestañas en un mismo lugar." data-en="The result: a perfect 5.0 across 8 verified Booksy reviews, and a menu of 17 services that covers skin, brows and lashes in one place.">The result: a perfect 5.0 across 8 verified Booksy reviews, and a menu of 17 services that covers skin, brows and lashes in one place.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="8">8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />'.replace("160,74,114", "193,140,49"),
    '<img src="assets/raw/bk-2.jpg" alt="Betsy Esquivel, esteticista y dueña de Magic Faces" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(193,140,49,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Betsy · <span class="text-[color:var(--ink-40)]" data-es="Esteticista" data-en="Esthetician">Esthetician</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita," data-en="Your visit,">Your visit,</span> <span class="text-shine" data-es="bien hecha" data-en="done right">done right</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Betsy revisa tu piel, cejas o pestañas y ajusta la técnica al resultado que buscas." data-en="Betsy checks your skin, brows or lashes and adjusts the technique to the result you want.">Betsy checks your skin, brows or lashes and adjusts the technique to the result you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El tratamiento" data-en="The treatment">The treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas y Betsy trabaja con calma, del henna al peeling, según el servicio elegido." data-en="You lie back and Betsy works calmly, from henna to peels, depending on the service you chose.">You lie back and Betsy works calmly, from henna to peels, depending on the service you chose.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El resultado" data-en="The result">The result</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el resultado terminado y, si aplica, la fecha de tu próximo retoque." data-en="You leave with the finished result and, if it applies, your next touch-up date.">You leave with the finished result and, if it applies, your next touch-up date.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios publicados por Magic Faces en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by Magic Faces on Booksy. Booking confirms instantly.">Prices as published by Magic Faces on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">treatment</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas" data-en="Brows">Brows</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Henna Brows</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas definidas con henna, un color natural que dura semanas." data-en="Brows defined with henna, a natural color that lasts for weeks.">Brows defined with henna, a natural color that lasts for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$41</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(193,140,49,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamiento estrella" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Duo Glow Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El facial más pedido del estudio: doble tratamiento para una piel luminosa de inmediato." data-en="The studio\'s most requested facial: a double treatment for instantly glowing skin.">The studio\'s most requested facial: a double treatment for instantly glowing skin.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$150</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Piel" data-en="Skin">Skin</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Chemical Peel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Peeling químico profesional para renovar la piel y parejar el tono." data-en="Professional chemical peel to renew skin and even out tone.">Professional chemical peel to renew skin and even out tone.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$117</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Depilación" data-en="Waxing">Waxing</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Eyebrow Waxing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Depilación de cejas con cera, perfilado rápido y preciso." data-en="Eyebrow waxing, a quick and precise shape.">Eyebrow waxing, a quick and precise shape.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$14</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">50min</p></div>
            <a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: eliminación de acrocordones, laminado de cejas, lifting y tinte de pestañas, alisado capilar, manicura y pedicura. Menú completo de 17 servicios y disponibilidad en Booksy." data-en="Also available: skin tag removal, brow lamination, lash lift and tint, hair straightening, manicure and pedicure. Full 17-service menu and availability on Booksy.">Also available: skin tag removal, brow lamination, lash lift and tint, hair straightening, manicure and pedicure. Full 17-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Estilo con manicura" data-en="Manicure in style">Manicure in style</span><img src="assets/raw/bk-15.jpg" alt="Manicura elegante junto a un bolso de diseñador y revista Vogue en Magic Faces" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Blanco brillante" data-en="Glossy white">Glossy white</span><img src="assets/raw/bk-1.jpg" alt="Manicura blanca con acabado brillante en Magic Faces" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalle nude" data-en="Nude detail">Nude detail</span><img src="assets/raw/bk-7.jpg" alt="Manicura nude con anillos, foto de detalle en Magic Faces" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Lunares en rojo" data-en="Red polka dots">Red polka dots</span><img src="assets/raw/bk-10.jpg" alt="Manicura blanca con diseño de lunares rojos en Magic Faces" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Francesa con flor" data-en="French with flower">French with flower</span><img src="assets/raw/bk-14.jpg" alt="Manicura francesa blanca con anillo floral en Magic Faces" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Rosa con anillos" data-en="Pink with rings">Pink with rings</span><img src="assets/raw/bk-8.jpg" alt="Manicura rosa con anillos sobre tela blanca en Magic Faces" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES (reales, verbatim, con autor)
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 8 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 8 verified reviews on Booksy">5.0 out of 5 · 8 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encantaron mis uñas 💖"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Arlines E…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"loved my eyebrows"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Katia R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very Good I will recommend it"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anonymous</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 8 reseñas en Booksy" data-en="Read all 8 reviews on Booksy">Read all 8 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tampa</span>')
rep('''<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'''.replace("160,74,114", "193,140,49"),
    '''<p class="text-sm text-[color:var(--ink-60)] font-light">6821 N Dale Mabry Hwy, Tampa, FL 33614</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light mt-1" data-es="Dom 10:00-19:00 · Lun-Sáb 9:00-19:00" data-en="Sun 10am-7pm · Mon-Sat 9am-7pm">Sun 10am-7pm · Mon-Sat 9am-7pm</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(193,140,49,0.4)]" href="https://www.google.com/maps?q=6821+N+Dale+Mabry+Hwy,+Tampa,+FL+33614" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("160,74,114", "193,140,49"),
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(193,140,49,0.4)]" href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('''data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.instagram.com/magicfaces2025/" target="_blank" rel="noopener">@magicfaces2025</a>'''.replace("160,74,114", "193,140,49"),
    '''data-es="Mira los resultados más recientes de Betsy y escribe por DM cualquier duda antes de tu cita." data-en="See Betsy's latest results and DM any questions before your appointment.">See Betsy's latest results and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(193,140,49,0.4)]" href="https://www.instagram.com/magicfaces2025/" target="_blank" rel="noopener">@magicfaces2025</a>''')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Magic Faces, 6821 N Dale Mabry Hwy, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=6821+N+Dale+Mabry+Hwy,+Tampa,+FL+33614&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="El cuidado que tu piel merece." data-en="The care your skin deserves.">The care your skin deserves.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="está a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: cejas, faciales, peelings o el retoque que ya te toca." data-en="Book online in seconds: brows, facials, peels, or the touch-up you are due for.">Book online in seconds: brows, facials, peels, or the touch-up you are due for.</p>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Magic Faces</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />'.replace("240,190,215", "255,226,183"),
    '<img src="assets/raw/bk-1.jpg" alt="Magic Faces" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(255,226,183,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Magic Faces</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de belleza en Tampa, FL. Atención con cita previa." data-en="Beauty studio in Tampa, FL. By appointment only.">Beauty studio in Tampa, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>6821 N Dale Mabry Hwy, Tampa, FL 33614</p>')
rep('<p><a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace("f0bed7", "ffe2b7"),
    '<p><a href="https://booksy.com/en-us/1540606_magic-faces_nail-salon_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#ffe2b7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/magicfaces2025/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @magicfaces2025</a></p>'.replace("f0bed7", "ffe2b7"),
    '<p><a href="https://www.instagram.com/magicfaces2025/" target="_blank" rel="noopener" class="hover:text-[#ffe2b7]">Instagram · @magicfaces2025</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Magic Faces.</p>')
print("FOOTER done")

# lang default -> es
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
