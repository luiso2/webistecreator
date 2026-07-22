import re, os, shutil

SLUG = "belleciia-nails"
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

# PALETTE: hue rotation +30deg from base pink (a04a72 -> a04d4a, red-terracotta/rosewood)
PALETTE = [
    ("#faf2f6", "#faf3f2"), ("#f3e0ea", "#f3e1e0"), ("#a04a72", "#a04d4a"),
    ("#c47a9c", "#c47d7a"), ("#c9789f", "#c97b78"), ("#5f2c48", "#5f2e2c"),
    ("#b25a85", "#b25c5a"), ("#f2d5e3", "#f2d6d5"), ("#d9a8c2", "#d9aaa8"),
    ("#e5c1d4", "#e5c2c1"), ("#7d3457", "#7d3634"), ("#5c2140", "#5c2321"),
    ("#f0bed7", "#f0c0be"), ("#f8dfeb", "#f8e0df"), ("#f2cfe0", "#f2d0cf"),
    ("#fbeff5", "#fbf0ef"), ("#efd0e0", "#efd1d0"), ("#d3a2bc", "#d3a4a2"),
    ("#8a5573", "#8a5755"), ("#dc9dbe", "#dc9f9d"), ("#2a1722", "#2a1817"),
    ("#1f0f18", "#1f1010"), ("#1c0f16", "#1c1010"), ("#f6f1ea", "#f6f3ea"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(160,77,74"),
    ("rgba(125,52,87", "rgba(125,54,52"),
    ("rgba(185,138,128", "rgba(185,141,138"),
    ("rgba(233,205,186", "rgba(233,208,205"),
    ("rgba(240,190,215", "rgba(240,192,190"),
    ("rgba(250,242,246", "rgba(250,243,242"),
    ("rgba(253,246,250", "rgba(253,247,246"),
    ("rgba(40,16,30", "rgba(40,17,16"),
    ("rgba(70,25,50", "rgba(70,26,25"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/glambeautyroom_bydaymi/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@glambeautyroom_bydaymi')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Belleciia Nails · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Belleciia Nails, Hialeah FL: acrylic, polygel and Luminary nail systems plus gel pedicures, with a perfect 5.0 across 272 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Belleciia Nails · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, polygel and Luminary sets. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-2.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Belleciia Nails",
    "description": "Nail salon in Hialeah, FL: acrylic, polygel and Luminary nail systems, gel manicures and pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "6782 W 22nd Ln", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33016", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah", "https://www.instagram.com/glambeautyroom_bydaymi/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "272", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set Acrylic" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set Pink and White" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luminary Nails System" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure and Pedicure" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">BN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Belleciia Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.35)]" />',
    '<img src="assets/raw/bk-1.jpg" alt="Belleciia Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Belleciia <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Nail Salon" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Manos hermosas, hechas con detalle." data-en="Beautiful hands, made with detail.">Beautiful hands, made with detail.</p>\n        <h1',)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Sets de acrilico, polygel" data-en="Acrylic, polygel and">Acrylic, polygel and</span><br /><span data-es="y Luminary, hechos para " data-en="Luminary sets, made to ">Luminary sets, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Acrilico, polygel, Luminary y Pink and White, mas pedicura en gel y disenos, todo con Daimy en un salon donde muchas clientas llevan mas de 8 anos regresando." data-en="Acrylic, polygel, Luminary and Pink and White sets, plus gel pedicures and nail art, all with Daimy in a salon where many clients have kept coming back for over 8 years.">Acrylic, polygel, Luminary and Pink and White sets, plus gel pedicures and nail art, all with Daimy in a salon where many clients have kept coming back for over 8 years.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 272 reseñas en Booksy" data-en="5.0 · 272 reviews on Booksy">5.0 · 272 reviews on Booksy</span>
        </div>
''')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Manicura francesa terminada en Belleciia Nails" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Pink &amp; White Set</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$100 · 1h 45min" data-en="$100 · 1h 45min">$100 · 1h 45min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="272">272</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Polygel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+8 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W 22nd Ln</p></div>')

for old, new in [
    ('Classic Set', 'Polygel'),
    ('Hybrid Set', 'Rubber Base'),
    ('Volume Set', 'Luminary System'),
    ('Mega Volume', 'Pink &amp; White'),
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
    '<img src="assets/raw/bk-13.jpg" alt="Set de unas nude en Belleciia Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Diseno floral pastel en Belleciia Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un salon," data-en="One salon,">One salon,</span><br /><span class="text-shine" data-es="ocho anos de confianza" data-en="eight years of trust">eight years of trust</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Belleciia Nails es el salon de Daimy Del Corral en Hialeah. Sus clientas la describen como dedicada y atenta, con manicuristas que llevan hasta 8 anos regresando por su trabajo prolijo en acrilico, polygel y Luminary." data-en="Belleciia Nails is Daimy Del Corral studio in Hialeah. Her clients describe her as dedicated and attentive, with regulars who have kept coming back for up to 8 years for her precise work in acrylic, polygel and Luminary.">Belleciia Nails is Daimy Del Corral studio in Hialeah. Her clients describe her as dedicated and attentive, with regulars who have kept coming back for up to 8 years for her precise work in acrylic, polygel and Luminary.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 272 resenas verificadas en Booksy, y clientas que aseguran que Daimy es su manicurista de cabecera desde hace anos." data-en="The result: a perfect 5.0 across 272 verified Booksy reviews, and clients who say Daimy has been their go-to manicurist for years.">The result: a perfect 5.0 across 272 verified Booksy reviews, and clients who say Daimy has been their go-to manicurist for years.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="272">272</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-12.jpg" alt="Daimy Del Corral" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Daimy · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, un set" data-en="Your visit, one set">Your visit, one set</span> <span class="text-shine" data-es="hecho con detalle" data-en="made with detail">made with detail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set on Booksy with clear price and duration, and confirm instantly.">Pick your set on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y sistema" data-en="Shape and system">Shape and system</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elegimos la forma de la una y el sistema: acrilico, polygel o Luminary, segun lo que buscas." data-en="We choose the nail shape and the system: acrylic, polygel or Luminary, based on what you want.">We choose the nail shape and the system: acrylic, polygel or Luminary, based on what you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Daimy trabaja con calma y precision, hasta 1h 45min de aplicacion segun el set que elijas." data-en="Daimy works calmly and precisely, up to 1h 45min of application depending on the set you choose.">Daimy works calmly and precisely, up to 1h 45min of application depending on the set you choose.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu set terminado y el toque de nail art que hayas elegido, listo para durar." data-en="You leave with your finished set and the nail art touch you chose, ready to last.">You leave with your finished set and the nail art touch you chose, ready to last.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Belleciia Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Belleciia Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Belleciia Nails on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="set" data-en="set">set</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clasico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Set Acrylic" data-en="Full Set Acrylic">Full Set Acrylic</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrilico, base solida y duradera. Version XL extra larga disponible por $90." data-en="Full acrylic set, a solid and long-lasting base. XL extra long version available for $90.">Full acrylic set, a solid and long-lasting base. XL extra long version available for $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,77,74,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salon" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pink &amp; White" data-en="Pink &amp; White">Pink &amp; White</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El set Pink and White sin diseno, el clasico limpio y elegante que nunca pasa de moda." data-en="The Pink and White set with no art, the clean, elegant classic that never goes out of style.">The Pink and White set with no art, the clean, elegant classic that never goes out of style.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema premium" data-en="Premium system">Premium system</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luminary System" data-en="Luminary System">Luminary System</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema Luminary de Belleciia Nails, tambien disponible con pedicura en gel incluida por $90." data-en="Belleciia Nails Luminary system, also available bundled with a gel pedicure for $90.">Belleciia Nails Luminary system, also available bundled with a gel pedicure for $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 10min</p></div>
            <a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Extras">Extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Mani + Pedi" data-en="Gel Mani + Pedi">Gel Mani + Pedi</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura y pedicura en gel regular, o agrega diseno desde $10 y diamantes desde $15." data-en="Regular gel manicure and pedicure, or add nail art from $10 and rhinestones from $15.">Regular gel manicure and pedicure, or add nail art from $10 and rhinestones from $15.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: polygel, rubber base, overlay, reparaciones y clases personalizadas. Menu completo de 22 servicios y disponibilidad en Booksy." data-en="Also available: polygel, rubber base, overlay, repairs and personalized classes. Full 22-service menu and availability on Booksy.">Also available: polygel, rubber base, overlay, repairs and personalized classes. Full 22-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail work">nail work</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseno floral amarillo" data-en="Yellow floral design">Yellow floral design</span><img src="assets/raw/bk-2.jpg" alt="Unas con diseno floral amarillo en Belleciia Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Azul profundo" data-en="Deep blue">Deep blue</span><img src="assets/raw/bk-3.jpg" alt="Set de unas azul profundo" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Nude con joyeria" data-en="Nude with jewelry">Nude with jewelry</span><img src="assets/raw/bk-4.jpg" alt="Unas nude con anillos dorados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Acento festivo" data-en="Festive accent">Festive accent</span><img src="assets/raw/bk-5.jpg" alt="Unas nude con acento rojo festivo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Brillo dorado" data-en="Gold shimmer">Gold shimmer</span><img src="assets/raw/bk-7.jpg" alt="Unas con acento de brillo dorado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Contorno francés" data-en="French outline">French outline</span><img src="assets/raw/bk-8.jpg" alt="Manicura francesa con contorno negro" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES (reales, con autor)
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 272 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 272 verified reviews on Booksy">5.0 out of 5 · 272 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent service I loved it"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Samantha C…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Daimy has ben my nail artist for over 8 years now, she is professional and gets the job done in a timely manner. My nails are always healthy and beautiful :) I strongly recommend her!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rosangela R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent service and excellent work! Daimy has been my manicurist for 8 years. I recommend her 100%."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">dayanmi d…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 272 reseñas en Booksy" data-en="Read all 272 reviews on Booksy">Read all 272 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">6782 W 22nd Ln, Hialeah, FL 33016</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=6782+W+22nd+Ln,+Hialeah,+FL+33016"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,77,74,0.4)]" href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,77,74,0.4)]" href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los sets mas recientes de Daimy y escribe por DM cualquier duda antes de tu cita." data-en="See Daimy\'s latest sets and DM any questions before your appointment.">See Daimy\'s latest sets and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Belleciia Nails, 6782 W 22nd Ln, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=6782+W+22nd+Ln,+Hialeah,+FL+33016&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Manos hermosas, hechas con detalle." data-en="Beautiful hands, made with detail.">Beautiful hands, made with detail.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu acrilico, tu polygel, tu Luminary o el Pink and White que ya te toca." data-en="Book online in seconds: your acrylic, your polygel, your Luminary, or the Pink and White set you are due for.">Book online in seconds: your acrylic, your polygel, your Luminary, or the Pink and White set you are due for.</p>')
rep('<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Belleciia Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,192,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Belleciia Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,192,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Belleciia Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Hialeah, FL. Atencion con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Nail salon in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>6782 W 22nd Ln, Hialeah, FL 33016</p>')
rep('<p><a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="hover:text-[#f0c0be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="hover:text-[#f0c0be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/glambeautyroom_bydaymi/" target="_blank" rel="noopener" class="hover:text-[#f0c0be]">Instagram · @glambeautyroom_bydaymi</a></p>',
    '<p><a href="https://www.instagram.com/glambeautyroom_bydaymi/" target="_blank" rel="noopener" class="hover:text-[#f0c0be]">Instagram · @glambeautyroom_bydaymi</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Belleciia Nails.</p>')
print("FOOTER done")

# book-float
rep('<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://booksy.com/en-us/166337_belleciia-nails_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
