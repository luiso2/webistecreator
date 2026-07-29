import re, os, shutil

SLUG = "natural-nails-by-jabev"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, 1)


def repall(a, b):
    global h
    assert a in h, "NO ANCHOR (all): " + a[:120]
    h = h.replace(a, b)


badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# PALETTE: pink/plum -> muted teal/blue-green (matches the salon's real plant decor)
PALETTE = [
    ("#faf2f6", "#f3f9f8"), ("#f3e0ea", "#e2f1ef"), ("#a04a72", "#559592"),
    ("#c47a9c", "#83bbb8"), ("#c9789f", "#82bfbb"), ("#5f2c48", "#325954"),
    ("#b25a85", "#65a7a2"), ("#f2d5e3", "#d9eeed"), ("#d9a8c2", "#aed3cf"),
    ("#e5c1d4", "#c5e0dd"), ("#7d3457", "#3d7470"), ("#5c2140", "#285550"),
    ("#f0bed7", "#c4eae7"), ("#f8dfeb", "#e2f5f4"), ("#f2cfe0", "#d3eeec"),
    ("#fbeff5", "#f0faf9"), ("#efd0e0", "#d4ebe9"), ("#d3a2bc", "#a8cdc9"),
    ("#8a5573", "#5c837d"), ("#dc9dbe", "#a5d4cf"), ("#2a1722", "#192825"),
    ("#1f0f18", "#111d1b"), ("#1c0f16", "#111a19"), ("#f6f1ea", "#ececf4"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(85,149,146"), ("rgba(125,52,87", "rgba(61,116,112"),
    ("rgba(185,138,128", "rgba(135,153,178"), ("rgba(233,205,186", "rgba(192,198,227"),
    ("rgba(240,190,215", "rgba(196,234,231"), ("rgba(250,242,246", "rgba(243,249,248"),
    ("rgba(253,246,250", "rgba(247,252,251"), ("rgba(40,16,30", "rgba(19,37,34"),
    ("rgba(70,25,50", "rgba(31,64,60"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/1626358_natural-nails-by-jabev_nail-salon_15889_miami'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
repall('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
repall('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/naturalnailsbyjabev/')
assert '@_lashbloom' in h
repall('@_lashbloom', '@naturalnailsbyjabev')
print("GLOBAL URLS done")

# ---------- HEAD ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Natural Nails by Jabev · Salon de Unas en Coral Gables, FL | 5.0 en Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Natural Nails by Jabev, Coral Gables FL: manicure y pedicure gel, apres, efecto cromo y disenos, con un 5.0 perfecto en 17 resenas de Booksy. Reserva en linea." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Natural Nails by Jabev · Salon de Unas en Coral Gables, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure y pedicure gel, apres y efecto cromo. 5.0 en Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-4.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-4.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Natural Nails by Jabev",
    "description": "Salon de unas en Coral Gables, FL: manicure y pedicure gel, apres, dip power y disenos de efecto cromo.",
    "address": { "@type": "PostalAddress", "streetAddress": "1430 Madruga Ave, Suite 29", "addressLocality": "Coral Gables", "addressRegion": "FL", "postalCode": "33146", "addressCountry": "US" },
    "sameAs": ["''' + BK_URL + '''", "https://www.instagram.com/naturalnailsbyjabev/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "17", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "10:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday"], "opens": "09:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "11:00", "closes": "16:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "MANICURE GEL" } },
      { "@type": "Offer", "price": "68", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "PEDICURE GEL" } },
      { "@type": "Offer", "price": "95", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "APRESS LARGA" } },
      { "@type": "Offer", "price": "23", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "EFECTO CROMO" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- NAV ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NJ</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Natural Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(85,149,146,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Natural Nails by Jabev" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(85,149,146,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Natural <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# ---------- HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Coral Gables, FL · Salon de Unas" data-en="Coral Gables, FL · Nail Salon">Coral Gables, FL · Salon de Unas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas naturales, bien cuidadas." data-en="Natural nails, beautifully cared for.">Unas naturales, bien cuidadas.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicure y pedicure gel," data-en="Gel manicure and pedicure,">Manicure y pedicure gel,</span><br /><span data-es="apres y disenos hechos para " data-en="apres sets and art made to ">apres y disenos hechos para </span><span class="text-shine" data-es="lucir" data-en="stand out">lucir</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicure y pedicure regular o gel, base rubber/builder, apress, dip power y efecto cromo, en un salon lleno de plantas en Coral Gables. Detallista, limpio y con un 5.0 perfecto en Booksy." data-en="Regular and gel manicure and pedicure, rubber/builder base, apres, dip power and chrome effect, in a plant-filled studio in Coral Gables. Detailed, clean, and a perfect 5.0 on Booksy.">Manicure y pedicure regular o gel, base rubber/builder, apress, dip power y efecto cromo, en un salon lleno de plantas en Coral Gables. Detallista, limpio y con un 5.0 perfecto en Booksy.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 17 reseñas en Booksy" data-en="5.0 · 17 reviews on Booksy">5.0 · 17 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-4.jpg" alt="Manicure gel color lila en Natural Nails by Jabev" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Manicure Gel" data-en="Gel Manicure">Manicure Gel</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$45" data-en="$45">$45</p>')
print("HERO done")

# ---------- STRIP DE CONFIANZA ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="17">17</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Apres</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicure y pedicure" data-en="Manicure and pedicure">Manicure y pedicure</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="36 servicios" data-en="36 services">36 servicios</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo en Booksy" data-en="Full menu on Booksy">Menu completo en Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Coral Gables</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Madruga Ave, Suite 29</p></div>')

for old, new in [
    ('Classic Set', 'Manicure Gel'),
    ('Hybrid Set', 'Pedicure Gel'),
    ('Volume Set', 'Apress Larga'),
    ('Mega Volume', 'Efecto Cromo'),
    ('Bottom Lashes', 'Nails Art'),
    ('West Palm Beach, FL', 'Coral Gables, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("STRIP+MARQUEE done")

# ---------- LA EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Interior de Natural Nails by Jabev con plantas y estaciones de manicure" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Letrero Natural Nails By Jabev junto a un olivo en el salon" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">La experiencia</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un salon lleno" data-en="A studio full">A studio full</span><br /><span class="text-shine" data-es="de plantas y detalle" data-en="of plants and detail">of plants and detail</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Natural Nails by Jabev es un salon de unas en Coral Gables donde las plantas naturales le dan nombre y ambiente al espacio. Sus clientas destacan lo profesional, detallista y limpio que es cada servicio." data-en="Natural Nails by Jabev is a nail salon in Coral Gables where real plants give the space its name and its calm. Clients highlight how professional, detailed and clean every service is.">Natural Nails by Jabev es un salon de unas en Coral Gables donde las plantas naturales le dan nombre y ambiente al espacio. Sus clientas destacan lo profesional, detallista y limpio que es cada servicio.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 17 resenas verificadas en Booksy, con clientas que repiten cita por el acabado perfecto y el ambiente relajante." data-en="The result: a perfect 5.0 across 17 verified Booksy reviews, with clients who come back for the perfect finish and the relaxing atmosphere.">El resultado: 5.0 perfecto en 17 resenas verificadas en Booksy, con clientas que repiten cita por el acabado perfecto y el ambiente relajante.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="17">17</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(85,149,146,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-15.jpg" alt="Fundadora de Natural Nails by Jabev" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(85,149,146,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Jabev · <span class="text-[color:var(--ink-40)]" data-es="Equipo de manicuristas" data-en="Nail artist team">Equipo de manicuristas</span></span>')
print("EXPERIENCIA done")

# ---------- EL METODO ----------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, unas" data-en="Your visit, nails">Tu cita, unas</span> <span class="text-shine" data-es="con detalle" data-en="with detail">con detalle</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duracion claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duracion claros, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu diagnostico" data-en="Your assessment">Tu diagnostico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Estado de tu una natural y el efecto que buscas: de ahi sale el sistema, gel, rubber, apres o dip." data-en="The state of your natural nail and the effect you want: that is where the system comes from, gel, rubber, apres or dip.">Estado de tu una natural y el efecto que buscas: de ahi sale el sistema, gel, rubber, apres o dip.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">Manos a la obra</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te relajas mientras se trabaja con calma y detalle, hasta 2h en los combos mas completos de estructura." data-en="You relax while the work happens calmly and with detail, up to 2h for the most complete structure combos.">Te relajas mientras se trabaja con calma y detalle, hasta 2h en los combos mas completos de estructura.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El acabado" data-en="The finish">El acabado</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con unas naturales, parejas y con el efecto que elegiste, lista para tu proxima cita." data-en="You leave with natural, even nails and the effect you chose, ready for your next visit.">Sales con unas naturales, parejas y con el efecto que elegiste, lista para tu proxima cita.</p>''')
print("METODO done")

# ---------- SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Natural Nails by Jabev en Booksy. Reserva con confirmacion inmediata." data-en="Prices and durations as published by Natural Nails by Jabev on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Natural Nails by Jabev en Booksy. Reserva con confirmacion inmediata.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diario" data-en="Everyday">Diario</p>
          <h3 class="font-display text-2xl leading-snug mb-3">MANICURE GEL</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure con esmaltado en gel de larga duracion, acabado limpio y brillante todos los dias." data-en="Manicure with long-lasting gel polish, a clean and glossy everyday finish.">Manicure con esmaltado en gel de larga duracion, acabado limpio y brillante todos los dias.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(85,149,146,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salon" data-en="Salon favorite">Favorito del salon</p>
          <h3 class="font-display text-2xl leading-snug mb-3">PEDICURE GEL</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicure completa con esmaltado en gel, pies suaves y color perfecto por semanas." data-en="Full pedicure with gel polish, soft feet and perfect color for weeks.">Pedicure completa con esmaltado en gel, pies suaves y color perfecto por semanas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$68</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extension" data-en="Extension">Extension</p>
          <h3 class="font-display text-2xl leading-snug mb-3">APRESS LARGA</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Apres de largo completo para un efecto dramatico e impecable, con acabado de salon." data-en="Full-length apres set for a dramatic, flawless salon finish.">Apres de largo completo para un efecto dramatico e impecable, con acabado de salon.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$95</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efectos" data-en="Effects">Efectos</p>
          <h3 class="font-display text-2xl leading-snug mb-3">EFECTO CROMO</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pigmento cromado con brillo espejo sobre tu gel o apres, para un toque diferente." data-en="Chrome pigment with a mirror shine over your gel or apres, for a different look.">Pigmento cromado con brillo espejo sobre tu gel o apres, para un toque diferente.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$23</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: manicure y pedicure regular, base rubber/builder, dip power, spa manicure/pedicure y fransesas. Menu completo de 36 servicios y disponibilidad en Booksy." data-en="Also available: regular manicure and pedicure, rubber/builder base, dip power, spa manicure/pedicure and french tips. Full 36-service menu and availability on Booksy.">Tambien: manicure y pedicure regular, base rubber/builder, dip power, spa manicure/pedicure y fransesas. Menu completo de 36 servicios y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# ---------- GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Unas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nail art">reales</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Manicure francesa con anillos" data-en="French manicure with rings">Manicure francesa con anillos</span><img src="assets/raw/bk-6.jpg" alt="Manicure francesa con anillos en Natural Nails by Jabev" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Manicure gel lila" data-en="Lilac gel manicure">Manicure gel lila</span><img src="assets/raw/bk-4.jpg" alt="Manicure gel en tono lila oval" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Apress rojo intenso" data-en="Deep red apres">Apress rojo intenso</span><img src="assets/raw/bk-8.jpg" alt="Apress largo en rojo intenso" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Efecto cromo con fransesa" data-en="Chrome effect with french tip">Efecto cromo con fransesa</span><img src="assets/raw/bk-10.jpg" alt="Diseno de efecto cromo con borde fransesa en punticos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Fransesa clasica con anillos" data-en="Classic french with rings">Fransesa clasica con anillos</span><img src="assets/raw/bk-5.jpg" alt="Manicure francesa clasica con anillos de plata" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Nuestro espacio" data-en="Our space">Nuestro espacio</span><img src="assets/raw/bk-7.jpg" alt="Interior del estudio Natural Nails by Jabev con plantas y estacion de trabajo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- OPINIONES ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What our">What our</span> <span class="text-shine" data-es="nuestras clientas" data-en="clients say">nuestras clientas</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 17 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 17 verified reviews on Booksy">5.0 de 5 · 17 resenas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Dazzle Dry is great"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Daisy V…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Servicio de manicure y pedicure espectacular, muy profesional y detallista. Ambiente relajante y acabado perfecto. Sin duda volvere!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium" data-es="Cliente verificada" data-en="Verified client">Cliente verificada</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great experience, clean smooth nails, detailed"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yanelys M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 17 reseñas en Booksy" data-en="Read all 17 reviews on Booksy">Leer las 17 resenas en Booksy</a>')
print("OPINIONES done")

# ---------- UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visitanos en</span> <span class="text-shine">Coral Gables</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1430 Madruga Ave, Suite 29, Coral Gables, FL 33146</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=1430+Madruga+Ave,+Suite+29,+Coral+Gables,+FL+33146"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa via Booksy: eliges servicio, dia y hora, y la confirmacion es inmediata. Abierto de domingo a sabado." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Sunday through Saturday.">Con cita previa via Booksy: eliges servicio, dia y hora, y la confirmacion es inmediata. Abierto de domingo a sabado.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(85,149,146,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(85,149,146,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes del salon y escribe por DM cualquier duda antes de tu cita." data-en="See the salon\'s latest designs and DM any questions before your appointment.">Mira los disenos mas recientes del salon y escribe por DM cualquier duda antes de tu cita.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Natural Nails by Jabev, 1430 Madruga Ave, Coral Gables FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=1430+Madruga+Ave,+Suite+29,+Coral+Gables,+FL+33146&output=embed"')
print("UBICACION done")

# ---------- CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas naturales, bien cuidadas." data-en="Natural nails, beautifully cared for.">Unas naturales, bien cuidadas.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tus unas nuevas" data-en="Your new nails">Tus unas nuevas</span> <span class="text-shine" data-es="te estan esperando" data-en="are waiting">te estan esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu manicure gel, tu pedicure, tu apress o el efecto cromo que quieres probar." data-en="Book online in seconds: your gel manicure, your pedicure, your apres or the chrome effect you want to try.">Reserva en linea en segundos: tu manicure gel, tu pedicure, tu apress o el efecto cromo que quieres probar.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# ---------- FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Natural Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(196,234,231,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Natural Nails by Jabev" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(196,234,231,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Natural Nails by Jabev</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Coral Gables, FL. Atencion con cita previa." data-en="Nail salon in Coral Gables, FL. By appointment only.">Salon de unas en Coral Gables, FL. Atencion con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>1430 Madruga Ave, Suite 29, Coral Gables, FL 33146</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#c4eae7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#c4eae7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/naturalnailsbyjabev/" target="_blank" rel="noopener" class="hover:text-[#c4eae7]">Instagram · @naturalnailsbyjabev</a></p>',
    '<p><a href="https://www.instagram.com/naturalnailsbyjabev/" target="_blank" rel="noopener" class="hover:text-[#c4eae7]">Instagram · @naturalnailsbyjabev</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Natural Nails by Jabev.</p>')
print("FOOTER done")

# ---------- book-float ----------
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

# ---------- IDIOMA: default ES ----------
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")
print("IDIOMA done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
