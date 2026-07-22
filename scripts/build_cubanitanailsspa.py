import re, os, shutil

SLUG = "cubanita-nails-spa"
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

# PALETTE: hue rotation +202.91deg from base pink -> deep teal (spa)
PALETTE = [
    ("#faf2f6", "#f2faf9"), ("#f3e0ea", "#e0f3f0"), ("#a04a72", "#4aa099"),
    ("#c47a9c", "#7ac4be"), ("#c9789f", "#78c9c1"), ("#5f2c48", "#2c5f56"),
    ("#b25a85", "#5ab2a9"), ("#f2d5e3", "#d5f2ef"), ("#d9a8c2", "#a8d9d2"),
    ("#e5c1d4", "#c1e5e0"), ("#7d3457", "#347d76"), ("#5c2140", "#215c54"),
    ("#f0bed7", "#bef0ea"), ("#f8dfeb", "#dff8f6"), ("#f2cfe0", "#cff2ee"),
    ("#fbeff5", "#effbfa"), ("#efd0e0", "#d0efeb"), ("#d3a2bc", "#a2d3cc"),
    ("#8a5573", "#558a80"), ("#dc9dbe", "#9ddcd3"), ("#2a1722", "#172a26"),
    ("#1f0f18", "#0f1f1c"), ("#1c0f16", "#0f1c1a"), ("#f6f1ea", "#eaeaf6"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(74,160,153"),
    ("rgba(125,52,87", "rgba(52,125,118"),
    ("rgba(185,138,128", "rgba(128,153,185"),
    ("rgba(233,205,186", "rgba(186,196,233"),
    ("rgba(240,190,215", "rgba(190,240,234"),
    ("rgba(250,242,246", "rgba(242,250,249"),
    ("rgba(253,246,250", "rgba(246,253,252"),
    ("rgba(40,16,30", "rgba(16,40,35"),
    ("rgba(70,25,50", "rgba(25,70,62"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/1221575_cubanita-nails-spa_nail-salon_15886_hialeah'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/ismarelynails_cubanita/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@ismarelynails_cubanita')

# idioma principal: espanol
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Cubanita Nails Spa · Salon de Unas en Hialeah, FL | 5.0 en Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Cubanita Nails Spa, Hialeah FL: unas apres, disenos elaborados, pedicura spa de lujo y mas, con 5.0 perfecto en 220 resenas de Booksy. Reserva en linea." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Cubanita Nails Spa · Salon de Unas en Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Unas Apres, pedicura spa de lujo y disenos elaborados. 5.0 en Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-15.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-15.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Cubanita Nails Spa",
    "description": "Salon de unas y spa en Hialeah, FL: unas Apres, disenos elaborados, pedicura podologica y pedicura spa de lujo.",
    "address": { "@type": "PostalAddress", "streetAddress": "17712 NW 59th Ave, Unit 102", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33015", "addressCountry": "US" },
    "sameAs": ["''' + BK_URL + '''", "https://www.instagram.com/ismarelynails_cubanita/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "220", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de unas", "itemListElement": [
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Unas Apres Basicas" } },
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Unas con diseno elaborado + pedicura spa de lujo" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicura Podologia Spa de Lujo" } },
      { "@type": "Offer", "price": "27", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Cejas" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">CN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Cubanita Nails Spa</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,153,0.35)]" />',
    '<img src="assets/raw/bk-15.jpg" alt="Cubanita Nails Spa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,153,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Cubanita <span class="text-[color:var(--accent-deep)]">Nails Spa</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salon de Unas y Spa" data-en="Hialeah, FL · Nail Salon and Spa">Hialeah, FL · Salon de Unas y Spa</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas de lujo, cuidado de verdad." data-en="Luxury nails, real care.">Unas de lujo, cuidado de verdad.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Unas Apres, disenos elaborados" data-en="Apres nails, elaborate designs">Unas Apres, disenos elaborados</span><br /><span data-es="y pedicura spa, pensados para " data-en="and spa pedicures, made to ">y pedicura spa, pensados para </span><span class="text-shine" data-es="consentirte" data-en="pamper you">consentirte</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Unas Apres con diseno basico o elaborado, pedicura podologia, cejas, limpieza facial e hidratacion capilar, todo con Ismarely en un ambiente de spa pensado para relajarte." data-en="Apres nails with basic or elaborate design, podiatric pedicure, brows, facial cleansing and hair hydration, all with Ismarely in a spa setting designed to help you relax.">Unas Apres con diseno basico o elaborado, pedicura podologia, cejas, limpieza facial e hidratacion capilar, todo con Ismarely en un ambiente de spa pensado para relajarte.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 220 reseñas en Booksy" data-en="5.0 · 220 reviews on Booksy">5.0 · 220 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-15.jpg" alt="Diseno de unas dorado con conchas en Cubanita Nails Spa" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Diseno Elaborado + Spa" data-en="Elaborate Design + Spa">Diseno Elaborado + Spa</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$130 · Pedicura incluida" data-en="$130 · Pedicure included">$130 · Pedicura incluida</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="220">220</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Unas <span class="text-shine">&amp;</span> Spa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Disenos y pedicura de lujo" data-en="Designs and luxury pedicures">Disenos y pedicura de lujo</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">años</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clientas fieles por años</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">NW 59th Ave</p></div>')

for old, new in [
    ('Classic Set', 'Unas Apres'),
    ('Hybrid Set', 'Diseno Elaborado'),
    ('Volume Set', 'Pedicura Spa'),
    ('Mega Volume', 'Cejas'),
    ('Bottom Lashes', 'Limpieza Facial'),
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
    '<img src="assets/raw/bk-10.jpg" alt="Equipo de spa facial en Cubanita Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Clienta recibiendo tratamiento en Cubanita Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">La experiencia</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un spa completo," data-en="A full spa,">Un spa completo,</span><br /><span class="text-shine" data-es="hecho para consentirte" data-en="made to pamper you">hecho para consentirte</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Cubanita Nails Spa es el salon de Ismarely Quintana Vazquez en Hialeah. Ademas de unas Apres y disenos elaborados, ofrece pedicura podologia, pedicura spa de lujo, cejas, limpieza facial e hidratacion capilar en un mismo lugar." data-en="Cubanita Nails Spa is Ismarely Quintana Vazquez studio in Hialeah. Beyond Apres nails and elaborate designs, it offers podiatric pedicure, luxury spa pedicure, brows, facial cleansing and hair hydration all in one place.">Cubanita Nails Spa es el salon de Ismarely Quintana Vazquez en Hialeah. Ademas de unas Apres y disenos elaborados, ofrece pedicura podologia, pedicura spa de lujo, cejas, limpieza facial e hidratacion capilar en un mismo lugar.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 220 resenas verificadas en Booksy, y clientas que llevan mas de 5 anos confiando solo en ella para sus unas." data-en="The result: a perfect 5.0 across 220 verified Booksy reviews, and clients who have trusted only her with their nails for over 5 years.">El resultado: 5.0 perfecto en 220 resenas verificadas en Booksy, y clientas que llevan mas de 5 anos confiando solo en ella para sus unas.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="220">220</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,153,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-15.jpg" alt="Ismarely Quintana Vazquez" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,153,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Ismarely · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Manicurista</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, detalle" data-en="Your visit, detail">Tu cita, detalle</span> <span class="text-shine" data-es="por detalle" data-en="by detail">por detalle</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Diagnostico" data-en="Consultation">Diagnostico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de la una y el nivel de diseno que buscas: de ahi sale si es un Apres basico o un diseno elaborado." data-en="Nail shape and the level of design you want: that is where a basic Apres set or an elaborate design comes from.">Forma de la una y el nivel de diseno que buscas: de ahi sale si es un Apres basico o un diseno elaborado.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">Manos a la obra</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Ismarely trabaja con calma cada detalle, hasta 3 horas de sesion en los disenos mas elaborados." data-en="Ismarely works calmly on every detail, up to 3 hours of session for the most elaborate designs.">Ismarely trabaja con calma cada detalle, hasta 3 horas de sesion en los disenos mas elaborados.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">Salida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus unas terminadas y, si elegiste el combo, con la pedicura spa incluida." data-en="You leave with your finished nails and, if you chose the combo, with the spa pedicure included.">Sales con tus unas terminadas y, si elegiste el combo, con la pedicura spa incluida.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Cubanita Nails Spa en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Cubanita Nails Spa on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Cubanita Nails Spa en Booksy. Reserva con confirmación inmediata.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diseno basico" data-en="Basic design">Diseno basico</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Unas Apres Basicas" data-en="Basic Apres Nails">Unas Apres Basicas</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Unas Apres con acabado limpio, listas en poco mas de una hora." data-en="Apres nails with a clean finish, ready in a little over an hour.">Unas Apres con acabado limpio, listas en poco mas de una hora.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 25min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(74,160,153,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del spa" data-en="Spa favorite">Favorito del spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Diseno Elaborado + Spa" data-en="Elaborate Design + Spa">Diseno Elaborado + Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Unas con diseno elaborado mas pedicura spa de lujo, el combo mas pedido del salon." data-en="Elaborate design nails plus a luxury spa pedicure, the salon most requested combo.">Unas con diseno elaborado mas pedicura spa de lujo, el combo mas pedido del salon.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$130</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Spa" data-en="Spa">Spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicura Spa de Lujo" data-en="Luxury Spa Pedicure">Pedicura Spa de Lujo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura podologia con esmalte en gel disponible por $36, o el ritual completo de lujo." data-en="Podiatric pedicure with gel polish available for $36, or the full luxury ritual.">Pedicura podologia con esmalte en gel disponible por $36, o el ritual completo de lujo.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 20min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cejas y Faciales" data-en="Brows and Facials">Cejas y Faciales</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas desde $27, limpieza facial desde $90 e hidratacion capilar con botox mas peinado desde $80." data-en="Brows from $27, facial cleansing from $90 and hair hydration with botox plus blowout from $80.">Cejas desde $27, limpieza facial desde $90 e hidratacion capilar con botox mas peinado desde $80.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $27" data-en="From $27">Desde $27</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min+</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: unas extralargas, Luminary con esmalte en gel, keratina y parafina. Menu completo y disponibilidad en Booksy." data-en="Also available: extra-long nails, Luminary with gel polish, keratin and paraffin. Full menu and availability on Booksy.">Tambien: unas extralargas, Luminary con esmalte en gel, keratina y parafina. Menu completo y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Trabajo</span> <span class="text-shine" data-es="real" data-en="nail work">real</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseno sirena azul" data-en="Blue mermaid design">Diseno sirena azul</span><img src="assets/raw/bk-2.jpg" alt="Diseno de unas sirena azul con conchas en Cubanita Nails Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Corazon en rojo" data-en="Red heart accent">Corazon en rojo</span><img src="assets/raw/bk-16.jpg" alt="Manicura francesa con acento de corazon rojo" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Ombre morado" data-en="Purple ombre">Ombre morado</span><img src="assets/raw/bk-4.jpg" alt="Unas con ombre morado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Remolino azul y morado" data-en="Blue and purple swirl">Remolino azul y morado</span><img src="assets/raw/bk-5.jpg" alt="Unas con remolino azul y morado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Diseno sirena" data-en="Mermaid design">Diseno sirena</span><img src="assets/raw/bk-7.jpg" alt="Unas con diseno sirena azul" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Equipo del spa" data-en="Spa equipment">Equipo del spa</span><img src="assets/raw/bk-10.jpg" alt="Equipo de spa facial en Cubanita Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">En sus</span> <span class="text-shine" data-es="propias palabras" data-en="own words">propias palabras</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 220 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 220 verified reviews on Booksy">5.0 de 5 · 220 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor de todas una excellente calidad y atención"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Brianna P…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Para mí la mejor manicurista de todo Miami, cuida de cada detalle hasta lograr la perfección 💕, llevo más de 5 años con ella y cada día supera mis expectativas. Estoy amando mis uñas 💅🏾"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">liset c…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing service! Beautiful manicure and pedicure, friendly staff, and a relaxing atmosphere. Highly recommended. I love my nails! Thank you for making me feel beautiful and relaxed. I'll definitely be back!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yohany G…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 220 reseñas en Booksy" data-en="Read all 220 reviews on Booksy">Leer las 220 reseñas en Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">17712 NW 59th Ave, Unit 102, Hialeah, FL 33015</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=17712+NW+59th+Ave,+Hialeah,+FL+33015"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,153,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,153,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Ismarely y escribe por DM cualquier duda antes de tu cita." data-en="See Ismarely\'s latest designs and DM any questions before your appointment.">Mira los disenos mas recientes de Ismarely y escribe por DM cualquier duda antes de tu cita.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Cubanita Nails Spa, 17712 NW 59th Ave, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=17712+NW+59th+Ave,+Hialeah,+FL+33015&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas de lujo, cuidado de verdad." data-en="Luxury nails, real care.">Unas de lujo, cuidado de verdad.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proxima cita" data-en="Your next appointment">Tu proxima cita</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">esta a un toque</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tus unas Apres, tu diseno elaborado o la pedicura spa que ya te toca." data-en="Book online in seconds: your Apres nails, your elaborate design, or the spa pedicure you are due for.">Reserva en linea en segundos: tus unas Apres, tu diseno elaborado o la pedicura spa que ya te toca.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Cubanita Nails Spa</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,234,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-15.jpg" alt="Cubanita Nails Spa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,234,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Cubanita Nails Spa</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas y spa en Hialeah, FL. Atención con cita previa." data-en="Nail salon and spa in Hialeah, FL. By appointment only.">Salon de unas y spa en Hialeah, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>17712 NW 59th Ave, Unit 102, Hialeah, FL 33015</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#bef0ea]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#bef0ea]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/ismarelynails_cubanita/" target="_blank" rel="noopener" class="hover:text-[#bef0ea]">Instagram · @ismarelynails_cubanita</a></p>',
    '<p><a href="https://www.instagram.com/ismarelynails_cubanita/" target="_blank" rel="noopener" class="hover:text-[#bef0ea]">Instagram · @ismarelynails_cubanita</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Cubanita Nails Spa.</p>')
print("FOOTER done")

# book-float
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

# idioma por defecto: espanol (negocio ES)
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
