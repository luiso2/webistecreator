import re, os, shutil

SLUG = "yune-nails"
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

# PALETTE: hue rotation +57.91deg from base pink -> warm terracotta/caramel
PALETTE = [
    ("#faf2f6", "#faf6f2"), ("#f3e0ea", "#f3e8e0"), ("#a04a72", "#a0754a"),
    ("#c47a9c", "#c49f7a"), ("#c9789f", "#c99f78"), ("#5f2c48", "#5f412c"),
    ("#b25a85", "#b2845a"), ("#f2d5e3", "#f2e3d5"), ("#d9a8c2", "#d9bda8"),
    ("#e5c1d4", "#e5d1c1"), ("#7d3457", "#7d5734"), ("#5c2140", "#5c3b21"),
    ("#f0bed7", "#f0d5be"), ("#f8dfeb", "#f8ebdf"), ("#f2cfe0", "#f2e0cf"),
    ("#fbeff5", "#fbf5ef"), ("#efd0e0", "#efded0"), ("#d3a2bc", "#d3b7a2"),
    ("#8a5573", "#8a6a55"), ("#dc9dbe", "#dcb99d"), ("#2a1722", "#2a1e17"),
    ("#1f0f18", "#1f150f"), ("#1c0f16", "#1c150f"), ("#f6f1ea", "#eff6ea"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(160,117,74"),
    ("rgba(125,52,87", "rgba(125,87,52"),
    ("rgba(185,138,128", "rgba(177,185,128"),
    ("rgba(233,205,186", "rgba(216,233,186"),
    ("rgba(240,190,215", "rgba(240,213,190"),
    ("rgba(250,242,246", "rgba(250,246,242"),
    ("rgba(253,246,250", "rgba(253,249,246"),
    ("rgba(40,16,30", "rgba(40,25,16"),
    ("rgba(70,25,50", "rgba(70,43,25"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BK_URL = 'https://booksy.com/en-us/1500785_yune-nails_nail-salon_15886_hialeah'
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BK_URL)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/Yunenails/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@Yunenails')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Yune Nails · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Yune Nails, Hialeah FL: acrylic, Luminary and freehand nail art, plus hair services, with a perfect 5.0 across 87 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Yune Nails · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, Luminary and freehand nail art. 5.0 on Booksy." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-1.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Yune Nails",
    "description": "Nail salon in Hialeah, FL: acrylic, Luminary and freehand nail art, dip manicures and Apres sets.",
    "address": { "@type": "PostalAddress", "streetAddress": "17754 NW 59th Ave, Apto 102", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33015", "addressCountry": "US" },
    "sameAs": ["''' + BK_URL + '''", "https://www.instagram.com/Yunenails/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "87", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "54", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Nails" } },
      { "@type": "Offer", "price": "54", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luminari o Rubber Base" } },
      { "@type": "Offer", "price": "27", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure con Esmaltado en Gel" } },
      { "@type": "Offer", "price": "9", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Disenos a Mano Alzada" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">YN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Yune Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.35)]" />',
    '<img src="assets/raw/bk-1.jpg" alt="Yune Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Yune <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Nail Salon" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Cualquier diseno que imagines, hecho realidad." data-en="Any design you imagine, brought to life.">Any design you imagine, brought to life.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrilico, Luminary y arte" data-en="Acrylic, Luminary and">Acrylic, Luminary and</span><br /><span data-es="a mano alzada, hechos para " data-en="freehand art, made to ">freehand art, made to </span><span class="text-shine" data-es="lucir" data-en="stand out">stand out</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Acrilico, Luminary, dip manicure y Apres, con disenos a mano alzada que traen tu inspiracion a la vida. Yune tambien ofrece alisados organicos e hidratacion capilar en Hialeah." data-en="Acrylic, Luminary, dip manicure and Apres, with freehand designs that bring your inspiration to life. Yune also offers organic straightening and hair hydration in Hialeah.">Acrylic, Luminary, dip manicure and Apres, with freehand designs that bring your inspiration to life. Yune also offers organic straightening and hair hydration in Hialeah.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 87 reseñas en Booksy" data-en="5.0 · 87 reviews on Booksy">5.0 · 87 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Set de unas con pedreria en Yune Nails" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Luminari + Pedicura" data-en="Luminari + Pedicure">Luminari + Pedicura</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$100 · 2h 30min" data-en="$100 · 2h 30min">$100 · 2h 30min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="87">87</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Freehand <span class="text-shine">Art</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Disenos a mano alzada" data-en="Hand-painted designs">Disenos a mano alzada</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Por cita" data-en="By appt">By appt</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atencion uno a uno" data-en="One-on-one care">One-on-one care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">NW 59th Ave</p></div>')

for old, new in [
    ('Classic Set', 'Acrylic'),
    ('Hybrid Set', 'Luminari'),
    ('Volume Set', 'Dip Manicure'),
    ('Mega Volume', 'Apres'),
    ('Bottom Lashes', 'Freehand Art'),
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
    '<img src="assets/raw/bk-13.jpg" alt="Manicura francesa con dije de sol en Yune Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Unas ombre rosa con flores de cerezo en Yune Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="hecho para tu inspiracion" data-en="made for your inspiration">made for your inspiration</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Yune Nails es el estudio de Yunelsi en Hialeah. Sus clientas destacan lo detallada y creativa que es: cualquier inspiracion de diseno que le lleves, ella la trae a la vida en tus unas." data-en="Yune Nails is Yunelsi studio in Hialeah. Her clients highlight how detailed and creative she is: any design inspiration you bring her, she brings it to life on your nails.">Yune Nails es el estudio de Yunelsi en Hialeah. Sus clientas destacan lo detallada y creativa que es: cualquier inspiracion de diseno que le lleves, ella la trae a la vida en tus unas.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 87 resenas verificadas en Booksy, con clientas que dicen que sus unas duran mas de un mes intactas." data-en="The result: a perfect 5.0 across 87 verified Booksy reviews, with clients who say their nails stay intact for over a month.">El resultado: 5.0 perfecto en 87 resenas verificadas en Booksy, con clientas que dicen que sus unas duran mas de un mes intactas.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="87">87</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Yunelsi" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Yunelsi · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, diseno" data-en="Your visit, design">Your visit, design</span> <span class="text-shine" data-es="por diseno" data-en="by design">by design</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tu inspiracion" data-en="Your inspo">Your inspo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Traes tu foto de referencia o ideas, y Yunelsi define el sistema y el diseno para lograrlo." data-en="Bring a reference photo or ideas, and Yunelsi maps out the system and design to make it happen.">Bring a reference photo or ideas, and Yunelsi maps out the system and design to make it happen.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Yunelsi trabaja con detalle, hasta 2h 30min de sesion en los combos mas completos." data-en="Yunelsi works with detail, up to 2h 30min of session for the most complete combos.">Yunelsi works with detail, up to 2h 30min of session for the most complete combos.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el diseno que trajiste hecho realidad, listo para durar mas de un mes." data-en="You leave with the design you brought made real, ready to last over a month.">You leave with the design you brought made real, ready to last over a month.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Yune Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Yune Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Yune Nails on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="sistema" data-en="system">system</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema" data-en="System">System</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Acrylic Nails" data-en="Acrylic Nails">Acrylic Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrilico, base solida para cualquier diseno a mano alzada." data-en="Full acrylic set, a solid base for any freehand design.">Full acrylic set, a solid base for any freehand design.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$54</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,117,74,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luminari + Pedicura" data-en="Luminari + Pedicure">Luminari + Pedicura</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Luminari o base rubber en las manos, mas pedicura podologia completa en la misma cita." data-en="Luminari or rubber base for hands, plus a full podiatric pedicure in the same visit.">Luminari or rubber base for hands, plus a full podiatric pedicure in the same visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Gel" data-en="Gel Manicure">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure con esmaltado en gel o regular, o el combo con pedicura y cabello por $180." data-en="Manicure with gel or regular polish, or the combo with pedicure and hair for $180.">Manicure with gel or regular polish, or the combo with pedicure and hair for $180.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$27</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Diseno a Mano" data-en="Freehand Art">Freehand Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Disenos a mano alzada desde $9, o agrega cejas con tinte henna por $27." data-en="Freehand designs from $9, or add henna brow tinting for $27.">Freehand designs from $9, or add henna brow tinting for $27.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $9" data-en="From $9">From $9</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">5min+</p></div>
            <a href="''' + BK_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: dip manicure, Apres, alisados organicos e hidratacion capilar. Menu completo y disponibilidad en Booksy." data-en="Also available: dip manicure, Apres, organic straightening and hair hydration. Full menu and availability on Booksy.">Also available: dip manicure, Apres, organic straightening and hair hydration. Full menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Diseno" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseno divertido" data-en="Playful design">Diseno divertido</span><img src="assets/raw/bk-10.jpg" alt="Diseno de unas verde divertido en Yune Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Floral rosa" data-en="Pink floral">Floral rosa</span><img src="assets/raw/bk-11.jpg" alt="Unas con diseno floral rosa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Ombre vino" data-en="Wine ombre">Ombre vino</span><img src="assets/raw/bk-12.jpg" alt="Unas con ombre color vino" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Francesa con pedreria" data-en="French with rhinestones">Francesa con pedreria</span><img src="assets/raw/bk-14.jpg" alt="Manicura francesa azul con pedreria" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Verde azulado" data-en="Teal green">Verde azulado</span><img src="assets/raw/bk-15.jpg" alt="Unas en tono verde azulado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Lunares minimalistas" data-en="Minimal polka dots">Lunares minimalistas</span><img src="assets/raw/bk-3.jpg" alt="Unas nude con lunares blancos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 87 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 87 verified reviews on Booksy">5.0 out of 5 · 87 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Beautiful as always"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anjali R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yune is truly talented and makes any design inspo come to life. She is detailed, creative and truly provides you with a great experience."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Alina Maria R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yune, you are the best! Thank you for always doing such an amazing job on my nails. You pay attention to every detail, you're so talented, and you always make me feel welcome."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Danelys</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 87 reseñas en Booksy" data-en="Read all 87 reviews on Booksy">Read all 87 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">17754 NW 59th Ave, Apto 102, Hialeah, FL 33015</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=17754+NW+59th+Ave,+Hialeah,+FL+33015"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,117,74,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,117,74,0.4)]" href="' + BK_URL + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Yunelsi y escribe por DM cualquier duda antes de tu cita." data-en="See Yunelsi\'s latest designs and DM any questions before your appointment.">See Yunelsi\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Yune Nails, 17754 NW 59th Ave, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=17754+NW+59th+Ave,+Hialeah,+FL+33015&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Cualquier diseno que imagines, hecho realidad." data-en="Any design you imagine, brought to life.">Any design you imagine, brought to life.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo diseno" data-en="Your next design">Your next design</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu acrilico, tu Luminari o el diseno a mano que llevas planeando." data-en="Book online in seconds: your acrylic, your Luminari, or the freehand design you have been planning.">Book online in seconds: your acrylic, your Luminari, or the freehand design you have been planning.</p>')
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Yune Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,213,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Yune Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,213,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Yune Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Nail salon in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>17754 NW 59th Ave, Apto 102, Hialeah, FL 33015</p>')
rep('<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f0d5be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BK_URL + '" target="_blank" rel="noopener" class="hover:text-[#f0d5be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/Yunenails/" target="_blank" rel="noopener" class="hover:text-[#f0d5be]">Instagram · @Yunenails</a></p>',
    '<p><a href="https://www.instagram.com/Yunenails/" target="_blank" rel="noopener" class="hover:text-[#f0d5be]">Instagram · @Yunenails</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Yune Nails.</p>')
print("FOOTER done")

# book-float
rep('<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BK_URL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
