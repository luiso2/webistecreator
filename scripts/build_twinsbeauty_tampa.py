import re, os, shutil, colorsys

SLUG = "twinsbeauty_tampa"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# 1. Protect the Merktop badge (gold, must stay unchanged)
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Palette: rotate base pink -> deep ocean navy-teal via uniform hue rotation
#    (Python colorsys). Two tiers:
#      - "accent" tier (buttons, CTA gradients, stars, shine): hue rotated AND
#        deepened (higher saturation, lower value) so accent-deep lands in the
#        requested #235c72-#2a6a82 navy-teal territory.
#      - "surface" tier (pale backgrounds, orbs, dark bands): hue rotated only,
#        keeping the same lightness so the light base still reads airy.
# ---------------------------------------------------------------------------
DELTA = -135  # degrees; source pink hue ~332 -> target teal-blue hue ~197
KV = 0.766
KS = 1.264


def rotate_hex(hexcode, deepen=False):
    hexcode = hexcode.lstrip('#')
    r, g, b = int(hexcode[0:2], 16) / 255, int(hexcode[2:4], 16) / 255, int(hexcode[4:6], 16) / 255
    hh, s, v = colorsys.rgb_to_hsv(r, g, b)
    hh = (hh + DELTA / 360.0) % 1.0
    if deepen:
        s = min(1.0, s * KS)
        v = max(0.0, v * KV)
    r2, g2, b2 = colorsys.hsv_to_rgb(hh, s, v)
    return '#%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def rotate_rgb(r, g, b, deepen=False):
    hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    hh = (hh + DELTA / 360.0) % 1.0
    if deepen:
        s = min(1.0, s * KS)
        v = max(0.0, v * KV)
    r2, g2, b2 = colorsys.hsv_to_rgb(hh, s, v)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


ACCENT_TIER = ["#a04a72", "#c47a9c", "#c9789f", "#5f2c48", "#b25a85", "#7d3457",
               "#5c2140", "#8a5573", "#dc9dbe", "#d3a2bc"]
SURFACE_TIER = ["#faf2f6", "#f3e0ea", "#f2d5e3", "#d9a8c2", "#e5c1d4", "#f0bed7",
                "#f8dfeb", "#f2cfe0", "#fbeff5", "#efd0e0", "#2a1722", "#1f0f18",
                "#1c0f16", "#f6f1ea"]

PALETTE = [(x, rotate_hex(x, deepen=True)) for x in ACCENT_TIER] + \
          [(x, rotate_hex(x, deepen=False)) for x in SURFACE_TIER]

print("PALETTE MAP:")
for a, b in PALETTE:
    print(" ", a, "->", b)

for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_ACCENT = [(160, 74, 114), (125, 52, 87), (70, 25, 50)]
RGBA_SURFACE = [(185, 138, 128), (233, 205, 186), (240, 190, 215), (250, 242, 246),
                (253, 246, 250), (40, 16, 30)]

RGBA_PAIRS = [(f"rgba({r},{g},{b}", "rgba(%d,%d,%d" % rotate_rgb(r, g, b, deepen=True))
              for r, g, b in RGBA_ACCENT] + \
             [(f"rgba({r},{g},{b}", "rgba(%d,%d,%d" % rotate_rgb(r, g, b, deepen=False))
              for r, g, b in RGBA_SURFACE]

for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done. accent-deep ->", rotate_hex("#a04a72", deepen=True))

# ---------------------------------------------------------------------------
# 3. Globals: Booksy URL, Instagram URL/handle, logo/avatar image
# ---------------------------------------------------------------------------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/twinsbeautyLLC/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@twinsbeautyLLC')

rep('<html lang="en" class="scroll-smooth">', '<html lang="en" class="scroll-smooth">')  # already EN default, no-op confirm

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Twins Beuty · Nail Salon in Tampa, FL | 4.9 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="TwinsBeutyLLC, Tampa FL: Russian manicure, rubber, builder and chrome nail systems plus hand-painted nail art, rated 4.9 across 31 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Twins Beuty · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Russian manicure, rubber, builder and chrome nails. 4.9 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-9.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-9.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "TwinsBeutyLLC",
    "description": "Nail salon inside Salon Genevi in Tampa, FL: Russian manicure, rubber, builder and chrome nail systems, plus hand-painted nail art.",
    "address": { "@type": "PostalAddress", "streetAddress": "Salon Genevi, 4410 W Hillsborough Ave Suite L", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33614", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.995266751866485, "longitude": -82.5193089991808 },
    "sameAs": ["https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa", "https://www.instagram.com/twinsbeautyLLC/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "31", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "09:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Polish + Manicure Ruso" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Ruber + Manicure Ruso" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder + Manicure Ruso" } },
      { "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Nail Art" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Language: business is EN-default already (matches light-v2 default) -> no flip needed.
#    Confirmed no-op at the bottom of this script (applyLang default stays 'en').
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 6. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">TB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Twins Beuty</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />'.replace("160,74,114", "39,99,123"),
    '<img src="assets/raw/bk-1.jpg" alt="Twins Beuty" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(39,99,123,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Twins <span class="text-[color:var(--accent-deep)]">Beuty</span></span>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Nail Studio" data-en="Tampa, FL · Nail Studio">Tampa, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Detalle en cada set." data-en="Detail in every set.">Detail in every set.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicure ruso, rubber" data-en="Russian manicure, rubber">Russian manicure, rubber</span><br /><span data-es="y builder, hechos para " data-en="and builder sets, made to ">and builder sets, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicure ruso, rubber, builder, cromado y nail art hecho a mano. Zoraida atiende dentro de Salon Genevi en Hillsborough Ave, Tampa, con precios y duracion claros en Booksy." data-en="Russian manicure, rubber, builder, chrome and hand-painted nail art. Zoraida works inside Salon Genevi on Hillsborough Ave, Tampa, with clear prices and duration on Booksy.">Russian manicure, rubber, builder, chrome and hand-painted nail art. Zoraida works inside Salon Genevi on Hillsborough Ave, Tampa, with clear prices and duration on Booksy.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.9 · 31 reseñas en Booksy" data-en="4.9 · 31 reviews on Booksy">4.9 · 31 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-9.jpg" alt="Glazed nude almond manicure with a gold ring, a finished set from Twins Beuty" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Ruber + Manicure Ruso" data-en="Ruber + Manicure Ruso">Ruber + Manicure Ruso</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$65 · 1h 30min" data-en="$65 · 1h 30min">$65 · 1h 30min</p>')

# ---------------------------------------------------------------------------
# 8. STRIP
# ---------------------------------------------------------------------------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="31">31</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Ruso <span class="text-shine">&amp;</span> Rubber</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicure ruso y sistemas" data-en="Russian mani and systems">Russian mani and systems</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">22 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Hillsborough Ave</p></div>')

for old, new in [
    ('Classic Set', 'Manicure Ruso'),
    ('Hybrid Set', 'Rubber'),
    ('Volume Set', 'Builder'),
    ('Mega Volume', 'Chrome'),
    ('Bottom Lashes', 'Nail Art'),
    ('West Palm Beach, FL', 'Tampa, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# ---------------------------------------------------------------------------
# 9. EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Nude glazed manicure with a gold leaf accent nail" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="White French manicure with a hand-painted heart accent nail" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un solo artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="detalle en cada set" data-en="detail in every set">detail in every set</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="TwinsBeutyLLC es el estudio de unas de Zoraida dentro de Salon Genevi, 4410 W Hillsborough Ave, Tampa. Su especialidad es la tecnica de manicure ruso, combinada con rubber, builder, cromado y nail art hecho a mano." data-en="TwinsBeutyLLC is Zoraida\'s nail studio inside Salon Genevi, 4410 W Hillsborough Ave, Tampa. Her focus is the Russian manicure technique, paired with rubber, builder, chrome and hand-painted nail art.">TwinsBeutyLLC is Zoraida\'s nail studio inside Salon Genevi, 4410 W Hillsborough Ave, Tampa. Her focus is the Russian manicure technique, paired with rubber, builder, chrome and hand-painted nail art.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 4.9 de 5 en 31 reseñas en Booksy, con clientas que escriben que siempre salen complacidas y en las mejores manos." data-en="The result: 4.9 out of 5 across 31 reviews on Booksy, with clients writing that they always leave happy and in the best hands.">The result: 4.9 out of 5 across 31 reviews on Booksy, with clients writing that they always leave happy and in the best hands.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="31">31</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />'.replace("160,74,114", "39,99,123"),
    '<img src="assets/raw/bk-1.jpg" alt="Zoraida" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(39,99,123,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Zoraida · <span class="text-[color:var(--ink-40)]" data-es="Propietaria y tecnica" data-en="Owner & nail tech">Owner & nail tech</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 10. METODO
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, set" data-en="Your visit, set">Your visit, set</span> <span class="text-shine" data-es="hecho a mano" data-en="made by hand">made by hand</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manicure ruso" data-en="Russian manicure prep">Russian manicure prep</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Trabajo de cuticula preciso con torno electrico: la base de cada set en TwinsBeutyLLC." data-en="Precise cuticle work with the e-file, the base of every set at TwinsBeutyLLC.">Precise cuticle work with the e-file, the base of every set at TwinsBeutyLLC.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu sistema" data-en="Your system">Your system</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Rubber, builder, dual sistem o gel polish, mas cromado o nail art a mano si lo quieres." data-en="Rubber, builder, dual system or gel polish, plus chrome or hand-painted art if you want it.">Rubber, builder, dual system or gel polish, plus chrome or hand-painted art if you want it.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El resultado" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set limpio y de larga duracion, listo para lucirlo." data-en="You leave with a clean, long-wearing set, ready to show off.">You leave with a clean, long-wearing set, ready to show off.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 11. SERVICIOS
# ---------------------------------------------------------------------------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por TwinsBeutyLLC en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by TwinsBeutyLLC on Booksy. Booking confirms instantly.">Prices and durations as published by TwinsBeutyLLC on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Entrada" data-en="Entry">Entry</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Polish + Manicure Ruso" data-en="Gel Polish + Manicure Ruso">Gel Polish + Manicure Ruso</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gel polish sobre la tecnica de manicure ruso: cuticula precisa y color parejo." data-en="Gel polish over the Russian manicure technique: precise cuticle work and even color.">Gel polish over the Russian manicure technique: precise cuticle work and even color.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(39,99,123,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Ruber + Manicure Ruso" data-en="Ruber + Manicure Ruso">Ruber + Manicure Ruso</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema mas pedido: base rubber sobre manicure ruso para un acabado flexible y duradero." data-en="The most requested system: rubber base over a Russian manicure for a flexible, long-wearing finish.">The most requested system: rubber base over a Russian manicure for a flexible, long-wearing finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Larga duracion" data-en="Long-wear">Long-wear</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Builder + Manicure Ruso" data-en="Builder + Manicure Ruso">Builder + Manicure Ruso</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gel constructor sobre manicure ruso para reforzar y alargar la uña natural." data-en="Builder gel over a Russian manicure to strengthen and add length to the natural nail.">Builder gel over a Russian manicure to strengthen and add length to the natural nail.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Arte" data-en="Art">Art</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Nail Art" data-en="Nail Art">Nail Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseno hecho a mano, agregado a cualquier set: desde detalles simples hasta piezas a la medida." data-en="Hand-painted design added to any set, from simple details to custom pieces.">Hand-painted design added to any set, from simple details to custom pieces.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$15</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien disponible: cromado, French, dual sistem, extensiones de gel y pedicure con manicure ruso. Menu completo de 22 servicios y disponibilidad en Booksy." data-en="Also available: chrome, French, dual system, gel extensions and pedicure with Russian manicure. Full 22-service menu and availability on Booksy.">Also available: chrome, French, dual system, gel extensions and pedicure with Russian manicure. Full 22-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 12. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nails">nails</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Acabado brillante de pedicure" data-en="Glossy pedicure finish">Glossy pedicure finish</span><img src="assets/raw/bk-13.jpg" alt="Glossy pale yellow gel pedicure on a spa towel" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Puntas negras con mariquita" data-en="Cat-eye tips with a ladybug">Cat-eye tips with a ladybug</span><img src="assets/raw/bk-3.jpg" alt="Black cat-eye tip nails with a hand-painted ladybug accent" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Set rojo clasico" data-en="Classic red almond set">Classic red almond set</span><img src="assets/raw/bk-5.jpg" alt="Glossy deep red almond-shaped manicure" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Nude con brillo y anillo" data-en="Glazed nude with a ring">Glazed nude with a ring</span><img src="assets/raw/bk-9.jpg" alt="Glazed nude almond manicure with a gold ring" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Nude con hoja de oro" data-en="Nude with a gold accent">Nude with a gold accent</span><img src="assets/raw/bk-4.jpg" alt="Nude glazed manicure with a gold leaf accent nail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="French con corazon a mano" data-en="French with a hand-drawn heart">French with a hand-drawn heart</span><img src="assets/raw/bk-8.jpg" alt="White French manicure with a hand-painted heart accent nail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 13. OPINIONES (reales, con autor)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 31 reseñas en Booksy" data-en="4.9 out of 5 · 31 reviews on Booksy">4.9 out of 5 · 31 reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Siempre salgo complacida de aqui, estoy en las mejores manos😍"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Irene Thalia A...</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"good"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Terrell H...</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Muy linda la atencion"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Marian P...</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 31 reseñas en Booksy" data-en="Read all 31 reviews on Booksy">Read all 31 reviews on Booksy</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 14. UBICACION
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">Salon Genevi, 4410 W Hillsborough Ave Suite L, Tampa, FL 33614</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=Salon+Genevi,+4410+W+Hillsborough+Ave+Suite+L,+Tampa,+FL+33614"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Abierto lunes a viernes de 7am a 5pm y sabado y domingo de 9am a 5pm. Con cita previa via Booksy: eliges servicio, dia y hora, y la confirmacion es inmediata." data-en="Open Monday to Friday 7am-5pm and Saturday and Sunday 9am-5pm. By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Open Monday to Friday 7am-5pm and Saturday and Sunday 9am-5pm. By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("160,74,114", "39,99,123"),
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(39,99,123,0.4)]" href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('''data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>''',
    '''data-es="Mira los sets mas recientes de Zoraida y escribe por DM cualquier duda antes de tu cita." data-en="See Zoraida's latest sets and DM any questions before your appointment.">See Zoraida's latest sets and DM any questions before your appointment.</p>''')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: TwinsBeutyLLC, 4410 W Hillsborough Ave, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=Salon+Genevi,+4410+W+Hillsborough+Ave+Suite+L,+Tampa,+FL+33614&output=embed"')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 15. CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Detalle en cada set." data-en="Detail in every set.">Detail in every set.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu manicure ruso, rubber, builder o el nail art que quieras agregar." data-en="Book online in seconds: your Russian manicure, rubber, builder, or the nail art you want to add.">Book online in seconds: your Russian manicure, rubber, builder, or the nail art you want to add.</p>')
rep('<a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 16. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Twins Beuty</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />'.replace("240,190,215", "190,227,240"),
    '<img src="assets/raw/bk-1.jpg" alt="Twins Beuty" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,227,240,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Twins Beuty</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Nail studio en Tampa, FL. Atencion con cita previa." data-en="Nail studio in Tampa, FL. By appointment only.">Nail studio in Tampa, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>Salon Genevi, 4410 W Hillsborough Ave Suite L, Tampa, FL 33614</p>')
rep('<p><a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace("f0bed7", "bee3f0"),
    '<p><a href="https://booksy.com/en-us/1656935_twinsbeutyllc_nail-salon_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#bee3f0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/twinsbeautyLLC/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @twinsbeautyLLC</a></p>'.replace("f0bed7", "bee3f0"),
    '<p><a href="https://www.instagram.com/twinsbeautyLLC/" target="_blank" rel="noopener" class="hover:text-[#bee3f0]">Instagram · @twinsbeautyLLC</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 TwinsBeutyLLC.</p>')
print("FOOTER done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
