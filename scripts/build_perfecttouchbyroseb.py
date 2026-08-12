import re, os, shutil

SLUG = "perfect-touch-by-rose-belleview"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, 1)


BOOKSY = "https://booksy.com/en-us/912233_perfect-touch-by-rose_brows-lashes_15860_belleview"
IG_URL = "https://www.instagram.com/perfecttouchbyrose/"
IG_HANDLE = "@perfecttouchbyrose"
OLD_BOOKSY = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
OLD_IG_HANDLE = "@_lashbloom"

# ---- Proteger el badge Merktop ----
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---- PALETA: plum-pink original -> rosa-malva calido (hue +6, sat x0.60, luz x0.95) ----
PALETTE = [
    ("#faf2f6", "#efe4e9"), ("#f3e0ea", "#e7d5dd"), ("#a04a72", "#885769"), ("#c47a9c", "#af7f90"),
    ("#c9789f", "#b37e92"), ("#5f2c48", "#513341"), ("#b25a85", "#9b6479"), ("#f2d5e3", "#e4ccd5"),
    ("#d9a8c2", "#c8a6b5"), ("#e5c1d4", "#d6bbc7"), ("#7d3457", "#693f4f"), ("#5c2140", "#4c2b39"),
    ("#f0bed7", "#dfb9c8"), ("#f8dfeb", "#ecd4dd"), ("#f2cfe0", "#e4c7d2"), ("#fbeff5", "#f1e1e7"),
    ("#efd0e0", "#e1c8d2"), ("#d3a2bc", "#c2a0af"), ("#8a5573", "#795b69"), ("#dc9dbe", "#c99db0"),
    ("#2a1722", "#24191f"), ("#1f0f18", "#1a1116"), ("#1c0f16", "#181114"), ("#f6f1ea", "#eae6de"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(136,87,105"),
    ("rgba(125,52,87", "rgba(105,63,79"),
    ("rgba(185,138,128", "rgba(167,140,130"),
    ("rgba(233,205,186", "rgba(216,199,182"),
    ("rgba(240,190,215", "rgba(223,185,200"),
    ("rgba(250,242,246", "rgba(239,228,233"),
    ("rgba(253,246,250", "rgba(244,230,237"),
    ("rgba(40,16,30", "rgba(33,20,26"),
    ("rgba(70,25,50", "rgba(58,32,44"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---- Globales: Booksy, Instagram, favicon ----
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, BOOKSY)
assert h.count(OLD_IG_URL) >= 1
h = h.replace(OLD_IG_URL, IG_URL)
assert h.count(OLD_IG_HANDLE) >= 1
h = h.replace(OLD_IG_HANDLE, IG_HANDLE)

rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Perfect Touch By Rose · Cejas y Pestañas en Belleview, FL | 5.0 en Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Perfect Touch By Rose, Belleview FL: powder brows, microblading, lip blush y extensiones de pestañas con Rose Tirado, 5.0 en 133 reseñas de Booksy. Reserva en linea." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Perfect Touch By Rose · Cejas y Pestañas en Belleview, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Powder brows, microblading, lip blush y pestañas. 5.0 en Booksy. Reserva en linea." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-11.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "Perfect Touch By Rose",
    "description": "Estudio de micropigmentacion y pestañas en Belleview, FL: powder brows, microblading, combo brows, lip blush y extensiones de pestañas.",
    "address": { "@type": "PostalAddress", "streetAddress": "10117 SE Hwy 441", "addressLocality": "Belleview", "addressRegion": "FL", "postalCode": "34420", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 29.075752630330296, "longitude": -82.07274055773817 },
    "telephone": "+1-787-648-2458",
    "sameAs": ["https://booksy.com/en-us/912233_perfect-touch-by-rose_brows-lashes_15860_belleview", "https://www.instagram.com/perfecttouchbyrose/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "133", "bestRating": "5" },
    "openingHoursSpecification": [{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "10:00", "closes": "18:00" }],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de micropigmentacion y pestañas", "itemListElement": [
      { "@type": "Offer", "price": "300", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Sombreado De Cejas / Powder Brows" } },
      { "@type": "Offer", "price": "275", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Microblading" } },
      { "@type": "Offer", "price": "350", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Combo Brows" } },
      { "@type": "Offer", "price": "300", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lip Blush" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---- PRELOADER ----
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">PT</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Perfect Touch By Rose</span>')

# ---- NAV ----
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(136,87,105,0.35)]" />',
    '<img src="assets/raw/bk-1.jpg" alt="Perfect Touch By Rose" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(136,87,105,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Perfect <span class="text-[color:var(--accent-deep)]">Touch</span></span>')
print("NAV done")

# ---- HERO ----
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Belleview, FL · Micropigmentación &amp; Pestañas" data-en="Belleview, FL · Permanent Makeup &amp; Lashes">Belleview, FL · Micropigmentación &amp; Pestañas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Una mirada que no se borra." data-en="A look that never fades.">Una mirada que no se borra.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Cejas y pestañas" data-en="Brows and lashes">Cejas y pestañas</span><br /><span data-es="que se notan, hechas " data-en="that show, made ">que se notan, hechas </span><span class="text-shine" data-es="con cuidado" data-en="with care">con cuidado</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Powder brows, microblading, lip blush y sets completos de pestañas, hechos a mano por Rose Tirado, con casi 19 años de experiencia en micropigmentación. Un estudio en Belleview, cerca de Ocala, con clientas que confían en ella desde hace años." data-en="Powder brows, microblading, lip blush and full lash sets, hand done by Rose Tirado, with close to 19 years of experience in permanent makeup. A studio in Belleview, near Ocala, with clients who have trusted her for years.">Powder brows, microblading, lip blush y sets completos de pestañas, hechos a mano por Rose Tirado, con casi 19 años de experiencia en micropigmentación. Un estudio en Belleview, cerca de Ocala, con clientas que confían en ella desde hace años.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 133 reseñas en Booksy" data-en="5.0 · 133 reviews on Booksy">5.0 · 133 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-11.jpg" alt="Ojo con extensiones de pestañas terminadas, primer plano en Perfect Touch By Rose" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Microblading" data-en="Microblading">Microblading</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$275 · 2h" data-en="$275 · 2h">$275 · 2h</p>')
print("HERO done")

# ---- STRIP ----
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="133">133</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Cejas <span class="text-shine">&amp;</span> Pestañas</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Powder brows · Microblading" data-en="Powder brows · Microblading">Powder brows · Microblading</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">19 <span class="text-shine" data-es="años" data-en="years">años</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Experiencia de Rose" data-en="Rose experience">Experiencia de Rose</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Belleview</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">SE Hwy 441</p></div>')

for old, new in [
    ('Classic Set', 'Powder Brows'),
    ('Hybrid Set', 'Microblading'),
    ('Volume Set', 'Combo Brows'),
    ('Mega Volume', 'Lip Blush'),
    ('Bottom Lashes', 'Volume Lashes'),
    ('West Palm Beach, FL', 'Belleview, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("STRIP+MARQUEE done")

# ---- EXPERIENCIA ----
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Ceja y pestañas terminadas de cerca en Perfect Touch By Rose" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Set de pestañas de volumen terminado, mirada abierta" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">La experiencia</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un espacio" data-en="A space">Un espacio</span><br /><span class="text-shine" data-es="pensado para ti" data-en="made just for you">pensado para ti</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Perfect Touch By Rose es el estudio de micropigmentación y pestañas de Rose Tirado en Belleview, cerca de Ocala. Cada ceja y cada set de pestañas se diseña a mano, según la forma de tu rostro y lo que buscas, en un ambiente limpio y relajado." data-en="Perfect Touch By Rose is the permanent makeup and lash studio of Rose Tirado in Belleview, near Ocala. Every brow and every lash set is designed by hand around your face shape and what you are looking for, in a clean, relaxed space.">Perfect Touch By Rose es el estudio de micropigmentación y pestañas de Rose Tirado en Belleview, cerca de Ocala. Cada ceja y cada set de pestañas se diseña a mano, según la forma de tu rostro y lo que buscas, en un ambiente limpio y relajado.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 133 reseñas verificadas en Booksy, y clientas que solo confían en Rose para sus cejas, pestañas y labios." data-en="The result: a perfect 5.0 across 133 verified Booksy reviews, and clients who trust no one but Rose with their brows, lashes and lips.">El resultado: 5.0 perfecto en 133 reseñas verificadas en Booksy, y clientas que solo confían en Rose para sus cejas, pestañas y labios.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="133">133</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(136,87,105,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Rose Tirado" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(136,87,105,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Rose · <span class="text-[color:var(--ink-40)]" data-es="Esteticista y artista de micropigmentación" data-en="Esthetician &amp; permanent makeup artist">Esteticista y artista de micropigmentación</span></span>')
print("EXPERIENCIA done")

# ---- METODO ----
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, ceja" data-en="Your visit, brow">Tu cita, ceja</span> <span class="text-shine" data-es="por ceja" data-en="by brow">por ceja</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Diseño y mapeo" data-en="Design and mapping">Diseño y mapeo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Rose diseña la forma de tus cejas o el estilo de pestañas según tu rostro, antes de empezar." data-en="Rose designs the shape of your brows or your lash style around your face, before starting.">Rose diseña la forma de tus cejas o el estilo de pestañas según tu rostro, antes de empezar.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El trabajo" data-en="The work">El trabajo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Aplicación con calma y precisión, ceja por ceja o pestaña por pestaña, hasta 2 horas según el servicio." data-en="Calm, precise application, brow by brow or lash by lash, up to 2 hours depending on the service.">Aplicación con calma y precisión, ceja por ceja o pestaña por pestaña, hasta 2 horas según el servicio.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Cuidado y retoque" data-en="Aftercare and touch up">Cuidado y retoque</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con indicaciones de cuidado y, si aplica, tu cita de retoque a las 6 semanas ya planificada." data-en="You leave with aftercare instructions and, if it applies, your 6-week touch up already booked.">Sales con indicaciones de cuidado y, si aplica, tu cita de retoque a las 6 semanas ya planificada.</p>''')
print("METODO done")

# ---- SERVICIOS: intro ----
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Perfect Touch By Rose en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Perfect Touch By Rose on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Perfect Touch By Rose en Booksy. Reserva con confirmación inmediata.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto polvo" data-en="Powder effect">Efecto polvo</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Powder Brows</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sombreado de cejas con efecto polvo suave, ideal para piel grasa. Retoque a las 6 semanas disponible por $75." data-en="Powder brow shading with a soft, blended effect, ideal for oily skin. 6-week touch up available for $75.">Sombreado de cejas con efecto polvo suave, ideal para piel grasa. Retoque a las 6 semanas disponible por $75.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$300</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(136,87,105,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Microblading</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trazos finos hechos a mano, pelo por pelo, para un efecto muy natural. Ideal para piel normal a seca." data-en="Fine hand-drawn strokes, hair by hair, for a very natural effect. Ideal for normal to dry skin.">Trazos finos hechos a mano, pelo por pelo, para un efecto muy natural. Ideal para piel normal a seca.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$275</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mas completo" data-en="Most complete">Mas completo</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Combo Brows</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Combina microblading y sombreado en polvo para una ceja con textura y densidad total." data-en="Combines microblading and powder shading for a brow with full texture and density.">Combina microblading y sombreado en polvo para una ceja con textura y densidad total.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$350</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Labios" data-en="Lips">Labios</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lip Blush" data-en="Lip Blush">Lip Blush</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Color natural y definición en los labios que dura, con retoque disponible por $200." data-en="Natural, long-lasting color and definition on the lips, with a touch up available for $200.">Color natural y definición en los labios que dura, con retoque disponible por $200.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$300</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''.replace("__BOOKSY__", BOOKSY)
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo de 28 servicios abajo, con precio y duración exactos. Disponibilidad al instante en Booksy." data-en="Full 28-service menu below, with exact price and duration. Instant availability on Booksy.">Menú completo de 28 servicios abajo, con precio y duración exactos. Disponibilidad al instante en Booksy.</span></p>')
print("SERVICIOS destacados done")

# ---- SERVICIOS: menu completo agrupado (nueva seccion, nunca acordeon) ----
CATS = [
    ("Cejas y retoques", "Brows and touch-ups", [
        ("Airbrush Eyebrows", "$50", "1h"),
        ("Powder Brows Touch Up", "$150", "1h 30min"),
        ("Combo Brows Touch up", "$175", "1h 30min"),
        ("Microblading Touch up", "$125", "1h 30min"),
        ("Retoque de cejas (mas de 2 años)", "$200", "1h 30min"),
        ("Primer Retoque (6 semanas)", "$75", "1h 30min"),
        ("Primer Retoque Combo Brows (6 semanas)", "$85", "1h 30min"),
    ]),
    ("Delineado de ojos", "Eyeliner", [
        ("Línea de ojos arriba o abajo", "$150", "1h 30min"),
        ("Línea de ojos arriba y abajo", "$275", "2h"),
        ("Retoque línea de ojos arriba y abajo", "$200", "1h 30min"),
        ("Retoque línea de ojos arriba o abajo", "$125", "1h 30min"),
    ]),
    ("Labios", "Lips", [
        ("Retoque de Lip Blush", "$200", "1h 30min"),
    ]),
    ("Pestañas (sets nuevos)", "Lashes (new sets)", [
        ("U Lashes", "$145", "2h"),
        ("YY Lashes", "$145", "2h"),
        ("W Lashes", "$145", "2h"),
        ("Soft Volume", "$145", "2h"),
        ("Volume Lashes", "$160", "2h"),
    ]),
    ("Rellenos de pestañas", "Lash fills", [
        ("U Lashes fill", "$80", "2h"),
        ("YY Lashes fill", "$80", "2h"),
        ("W Lashes fill", "$80", "2h"),
        ("Soft Volume fill", "$80", "2h"),
        ("Volume fill", "$90", "2h"),
        ("Retiro de pestañas", "$35", "20min"),
    ]),
    ("Facial", "Facial", [
        ("Facial Profundo", "$95", "1h 30min"),
    ]),
]

CATS_EN_TITLE = {
    "Cejas y retoques": "Brows and touch-ups", "Delineado de ojos": "Eyeliner",
    "Labios": "Lips", "Pestañas (sets nuevos)": "Lashes (new sets)",
    "Rellenos de pestañas": "Lash fills", "Facial": "Facial",
}
ITEM_EN = {
    "Retoque de cejas (mas de 2 años)": "Brow touch up (over 2 years)",
    "Primer Retoque (6 semanas)": "First touch up (6 weeks)",
    "Primer Retoque Combo Brows (6 semanas)": "First touch up Combo Brows (6 weeks)",
    "Línea de ojos arriba o abajo": "Eyeliner top or bottom",
    "Línea de ojos arriba y abajo": "Eyeliner top and bottom",
    "Retoque línea de ojos arriba y abajo": "Eyeliner touch up top and bottom",
    "Retoque línea de ojos arriba o abajo": "Eyeliner touch up top or bottom",
    "Retoque de Lip Blush": "Lip Blush touch up",
    "Retiro de pestañas": "Lash removal",
    "Facial Profundo": "Deep Facial",
}

cards = []
delay = 0
for title_es, title_en, items in CATS:
    rows = []
    for name, price, dur in items:
        name_en = ITEM_EN.get(name, name)
        rows.append(f'''            <div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)] last:border-0">
              <span class="text-sm font-light" data-es="{name}" data-en="{name_en}">{name}</span>
              <span class="text-sm text-[color:var(--ink-60)] whitespace-nowrap ml-3">{price} · {dur}</span>
            </div>''')
    delay_style = f' style="transition-delay:{delay}ms"' if delay else ''
    cards.append(f'''        <div class="glass rounded-3xl p-7 reveal"{delay_style}>
          <h3 class="font-display text-xl mb-4" data-es="{title_es}" data-en="{title_en}">{title_es}</h3>
          <div>
{chr(10).join(rows)}
          </div>
        </div>''')
    delay += 90

FULL_MENU = '''      <div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Menú completo" data-en="Full menu">Menú completo</p>
        <h3 class="reveal text-center font-display text-2xl sm:text-3xl leading-tight mb-10"><span data-es="Los 28 servicios" data-en="All 28 services">Los 28 servicios</span> <span class="text-shine" data-es="de Booksy" data-en="on Booksy">de Booksy</span></h3>
        <div class="grid sm:grid-cols-2 gap-5">
''' + '\n'.join(cards) + '''
        </div>
      </div>
'''

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo de 28 servicios abajo, con precio y duración exactos. Disponibilidad al instante en Booksy." data-en="Full 28-service menu below, with exact price and duration. Instant availability on Booksy.">Menú completo de 28 servicios abajo, con precio y duración exactos. Disponibilidad al instante en Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo de 28 servicios abajo, con precio y duración exactos. Disponibilidad al instante en Booksy." data-en="Full 28-service menu below, with exact price and duration. Instant availability on Booksy.">Menú completo de 28 servicios abajo, con precio y duración exactos. Disponibilidad al instante en Booksy.</span></p>\n' + FULL_MENU)
print("MENU COMPLETO done")

# ---- GALERIA ----
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Resultados" data-en="Real">Resultados</span> <span class="text-shine" data-es="reales" data-en="results">reales</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Cejas y mirada" data-en="Brows and eyes">Cejas y mirada</span><img src="assets/raw/bk-8.jpg" alt="Ceja y pestañas terminadas de cerca en Perfect Touch By Rose" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Detalle de pestañas" data-en="Lash detail">Detalle de pestañas</span><img src="assets/raw/bk-9.jpg" alt="Pestañas y ceja terminadas, mirada abierta" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Volumen de pestañas" data-en="Lash volume">Volumen de pestañas</span><img src="assets/raw/bk-10.jpg" alt="Set de pestañas de volumen terminado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Mirada terminada" data-en="Finished look">Mirada terminada</span><img src="assets/raw/bk-11.jpg" alt="Ojo con extensiones de pestañas terminadas, primer plano" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---- MARQUEE 2 (mismos words, ya cambiados globalmente) ----

# ---- OPINIONES (reales, con autor) ----
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 133 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 133 verified reviews on Booksy">5.0 de 5 · 133 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"El lugar es super relajante y limpio. Me hice el sombreado de cejas (powder brows) con Rose y quedé encantada. No quiero que nadie más toque mis cejas. Ella es muy profesional, la considero una experta en los servicios que ofrece. 100% recomendada."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Janet B…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Love the services!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carla O…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encantan los trabajos que me realizado con Rose, es muy profesional y el lugar muy limpio y acogedor. Se las recomiendo al 100%"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Zulma S…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="__BOOKSY_OPINIONES__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>'.replace("__BOOKSY_OPINIONES__", BOOKSY),
    '<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 133 reseñas en Booksy" data-en="Read all 133 reviews on Booksy">Leer las 133 reseñas en Booksy</a>')
print("OPINIONES done")

# ---- UBICACION ----
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Belleview</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">10117 SE Hwy 441, Belleview, FL 34420</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=10117+SE+Hwy+441,+Belleview,+FL+34420"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(136,87,105,0.4)]" href="' + BOOKSY + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(136,87,105,0.4)]" href="' + BOOKSY + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('''            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(136,87,105,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">''' + IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">''',
    '''            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los resultados más recientes de Rose y escribe por DM cualquier duda antes de tu cita." data-en="See Rose's latest results and DM any questions before your appointment.">Mira los resultados más recientes de Rose y escribe por DM cualquier duda antes de tu cita.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(136,87,105,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">''' + IG_HANDLE + '''</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Teléfono" data-en="Phone">Teléfono</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Llama o escribe si prefieres coordinar tu cita por teléfono." data-en="Call or text if you would rather book your appointment by phone.">Llama o escribe si prefieres coordinar tu cita por teléfono.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(136,87,105,0.4)]" href="tel:+17876482458">+1 (787) 648-2458</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">''')
rep('<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>',
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Perfect Touch By Rose, 10117 SE Hwy 441, Belleview FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=10117+SE+Hwy+441,+Belleview,+FL+34420&output=embed"')
print("UBICACION done")

# ---- CTA FINAL ----
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Una mirada que no se borra." data-en="A look that never fades.">Una mirada que no se borra.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Tu próxima cita</span> <span class="text-shine" data-es="ya te está esperando" data-en="is already waiting">ya te está esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tus cejas, tus pestañas o tus labios, con Rose." data-en="Book online in seconds: your brows, your lashes or your lips, with Rose.">Reserva en línea en segundos: tus cejas, tus pestañas o tus labios, con Rose.</p>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# ---- FOOTER ----
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Perfect Touch</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(223,185,200,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Perfect Touch By Rose" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(223,185,200,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Perfect Touch By Rose</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de micropigmentación y pestañas en Belleview, FL. Atención con cita previa." data-en="Permanent makeup and lash studio in Belleview, FL. By appointment only.">Estudio de micropigmentación y pestañas en Belleview, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>10117 SE Hwy 441, Belleview, FL 34420</p>')
rep('<p><a href="' + BOOKSY + '" target="_blank" rel="noopener" class="hover:text-[#dfb9c8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="tel:+17876482458" class="hover:text-[#dfb9c8]">+1 (787) 648-2458</a></p>\n        <p><a href="' + BOOKSY + '" target="_blank" rel="noopener" class="hover:text-[#dfb9c8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#dfb9c8]">Instagram · ' + IG_HANDLE + '</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#dfb9c8]">Instagram · ' + IG_HANDLE + '</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Perfect Touch By Rose.</p>')
print("FOOTER done")

# ---- lang default -> es ----
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
