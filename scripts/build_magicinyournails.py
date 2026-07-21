import re, os, shutil

SLUG = "magicinyournails"
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

PALETTE = [
    ("#faf2f6", "#faf1ec"), ("#f3e0ea", "#f3e3d7"), ("#a04a72", "#8c2f3a"),
    ("#c47a9c", "#c17f5e"), ("#c9789f", "#b8674f"), ("#5f2c48", "#47201c"),
    ("#b25a85", "#a8503a"), ("#f2d5e3", "#f0ded0"), ("#d9a8c2", "#dcb89a"),
    ("#e5c1d4", "#e8cdb0"), ("#7d3457", "#611f22"), ("#5c2140", "#431a19"),
    ("#f0bed7", "#eec9a8"), ("#f8dfeb", "#f5e6d3"), ("#f2cfe0", "#ecd2b0"),
    ("#fbeff5", "#f8ecdd"), ("#efd0e0", "#ecd4b6"), ("#d3a2bc", "#d0a877"),
    ("#8a5573", "#8a5d3a"), ("#dc9dbe", "#d4a26e"), ("#2a1722", "#231512"),
    ("#1f0f18", "#190f0c"), ("#1c0f16", "#170f0b"), ("#f6f1ea", "#f6efe4"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(160,74,114", "rgba(140,47,58"),
    ("rgba(125,52,87", "rgba(97,31,34"),
    ("rgba(185,138,128", "rgba(185,130,100"),
    ("rgba(233,205,186", "rgba(230,190,160"),
    ("rgba(240,190,215", "rgba(238,201,168"),
    ("rgba(250,242,246", "rgba(250,241,236"),
    ("rgba(253,246,250", "rgba(253,245,240"),
    ("rgba(40,16,30", "rgba(33,14,14"),
    ("rgba(70,25,50", "rgba(45,18,11"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

BOOKSY = "https://booksy.com/en-us/1480743_magic-in-your-nails_nail-salon_15886_hialeah"
IG_URL = "https://www.instagram.com/ibis_nails_07/"
IG_HANDLE = "@ibis_nails_07"

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BOOKSY)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', IG_URL)
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', IG_HANDLE)

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Magic In Your Nails · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Magic In Your Nails, Hialeah FL: gel manicures, acrylic, polygel, apres and Russian manicure, with a perfect 5.0 across 78 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Magic In Your Nails · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel, acrylic, polygel and Russian manicures. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-16.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-13.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Magic In Your Nails",
    "description": "Nail salon in Hialeah, FL: gel manicures, acrylic, polygel, apres and Russian manicure sets.",
    "address": { "@type": "PostalAddress", "streetAddress": "429 Hialeah Dr, Suite 8", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33010", "addressCountry": "US" },
    "sameAs": ["''' + BOOKSY + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "78", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel" } },
      { "@type": "Offer", "price": "105", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luminary + Pedi" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Soak Off y Luminary" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura Rusa" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">MN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Magic In Your Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,47,58,0.35)]" />',
    '<img src="assets/raw/bk-13.jpg" alt="Magic In Your Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,47,58,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Magic <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Estudio de Uñas" data-en="Hialeah, FL · Nail Studio">Hialeah, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="La magia esta en el detalle." data-en="The magic is in the detail.">The magic is in the detail.</p>\n        <h1',)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Gel, acrilico, polygel" data-en="Gel, acrylic, polygel">Gel, acrylic, polygel</span><br /><span data-es="y manicura rusa, hechos para " data-en="and Russian manicure, made to ">and Russian manicure, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicuras y pedicuras de gel, acrilico, polygel, apres y rubber base, con nail art y manicura rusa a mano. Ibis, manicurista en Hialeah, atiende un salon privado con parking gratis y cafe de cortesia." data-en="Gel, acrylic, polygel, apres and rubber base manicures and pedicures, with hand-done nail art and Russian manicure. Ibis, manicurist in Hialeah, runs a private salon with free parking and complimentary coffee.">Gel, acrylic, polygel, apres and rubber base manicures and pedicures, with hand-done nail art and Russian manicure. Ibis, manicurist in Hialeah, runs a private salon with free parking and complimentary coffee.</p>')
rep('<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 78 reseñas en Booksy" data-en="5.0 · 78 reviews on Booksy">5.0 · 78 reviews on Booksy</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-16.jpg" alt="Long oval nails in a glossy blush pink finish" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Luminary + Pedi" data-en="Luminary + Pedi">Luminary + Pedi</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$105 · 2h 30min" data-en="$105 · 2h 30min">$105 · 2h 30min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="78">78</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">23 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo con precios" data-en="Full menu, real prices">Full menu, real prices</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Privado" data-en="Private">Private</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Salon con cita previa" data-en="By-appointment salon">By-appointment salon</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Hialeah Dr</p></div>')

for old, new in [
    ('Classic Set', 'Manicure Gel'),
    ('Hybrid Set', 'Acrylic Nails'),
    ('Volume Set', 'Polygel'),
    ('Mega Volume', 'Apres'),
    ('Bottom Lashes', 'Rubber Base'),
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
    '<img src="assets/raw/bk-7.jpg" alt="Rose gold nude manicure, close-up" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Soft pink natural manicure finish" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un salon privado," data-en="A private salon,">A private salon,</span><br /><span class="text-shine" data-es="una manicurista" data-en="one manicurist">one manicurist</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Magic In Your Nails es el salon privado de Ibis Hurtado en Hialeah. Sus clientas describen el lugar como bellamente decorado, lujoso y relajante, con cafe de cortesia y parking gratis incluidos." data-en="Magic In Your Nails is the private salon of Ibis Hurtado in Hialeah. Clients describe it as beautifully decorated, luxurious and relaxing, with complimentary coffee and free parking included.">Magic In Your Nails is the private salon of Ibis Hurtado in Hialeah. Clients describe it as beautifully decorated, luxurious and relaxing, with complimentary coffee and free parking included.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 78 reseñas verificadas en Booksy, y clientas que vuelven cita tras cita por la atencion al detalle de Ibis." data-en="The result: a perfect 5.0 across 78 verified Booksy reviews, and clients who come back appointment after appointment for Ibis attention to detail.">The result: a perfect 5.0 across 78 verified Booksy reviews, and clients who come back appointment after appointment for Ibis attention to detail.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="78">78</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,47,58,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Magic In Your Nails" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,47,58,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Ibis · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Manicurist">Manicurist</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Preparacion" data-en="Prep">Prep</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de uña, largo y el estilo que traigas de referencia definen el resultado final." data-en="Nail shape, length and any reference style you bring define the final result.">Nail shape, length and any reference style you bring define the final result.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Ibis trabaja tu set con calma, de un color solido de 45min a un combo con pedicure de hasta 2h 30min." data-en="Ibis works your set at an unhurried pace, from a 45min solid color to a 2h 30min combo with pedicure.">Ibis works your set at an unhurried pace, from a 45min solid color to a 2h 30min combo with pedicure.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu set terminado y cafe de cortesia si quieres quedarte un momento mas." data-en="You leave with your finished set, complimentary coffee included if you want to stay a moment longer.">You leave with your finished set, complimentary coffee included if you want to stay a moment longer.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Magic In Your Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Magic In Your Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Magic In Your Nails on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clasico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Gel" data-en="Manicure Gel">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura de gel con acabado brillante y de larga duracion, sobre tu uña natural." data-en="Gel manicure with a glossy, long-lasting finish, on your natural nail.">Gel manicure with a glossy, long-lasting finish, on your natural nail.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45 min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(140,47,58,0.4); box-shadow: 0 18px 50px rgba(51,35,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salon" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luminary + Pedi" data-en="Luminary + Pedi">Luminary + Pedi</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de builder gel (Luminary) con pedicura incluida: la experiencia de spa completa." data-en="Full builder gel (Luminary) set with a pedicure included: the complete spa experience.">Full builder gel (Luminary) set with a pedicure included: the complete spa experience.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$105</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30 min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Renovacion" data-en="Refresh">Refresh</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Soak Off y Luminary" data-en="Soak Off &amp; Luminary">Soak Off &amp; Luminary</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Se retira el set anterior y se aplica un Luminary nuevo, uñas frescas de principio a fin." data-en="Your previous set is removed and a fresh Luminary set applied, nails renewed start to finish.">Your previous set is removed and a fresh Luminary set applied, nails renewed start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45 min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tendencia" data-en="Trending">Trending</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Rusa" data-en="Russian Manicure">Russian Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tecnica rusa de precision en la cuticula para un acabado impecable y prolijo." data-en="Precision Russian cuticle technique for an impeccably clean, polished finish.">Precision Russian cuticle technique for an impeccably clean, polished finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30 min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-8" data-es="Menu completo" data-en="Full menu">Full menu</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div class="glass glass-hover rounded-3xl p-6 reveal">
            <h3 class="font-display text-lg mb-4" data-es="Manicura y Pedicura" data-en="Mani &amp; Pedi">Mani &amp; Pedi</h3>
            <div class="text-sm">
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Pedicure Gel</p></div><p class="font-display text-shine shrink-0">$45</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Mani/Pedi</p></div><p class="font-display text-shine shrink-0">$85</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Men's Manicure &amp; Pedicure</p></div><p class="font-display text-shine shrink-0">$85</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Men's Pedicure</p></div><p class="font-display text-shine shrink-0">$45</p></div>
              <div class="flex items-start justify-between gap-3 py-2"><div><p class="text-[color:var(--ink)] font-light">Men's Manicure</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-0.5">45 min</p></div><p class="font-display text-shine shrink-0">$40</p></div>
            </div>
          </div>
          <div class="glass glass-hover rounded-3xl p-6 reveal" style="transition-delay:80ms">
            <h3 class="font-display text-lg mb-4" data-es="Sets de Uñas" data-en="Nail Enhancements">Nail Enhancements</h3>
            <div class="text-sm">
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Acrylic Nails</p></div><p class="font-display text-shine shrink-0">$70</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Luminary (Builder Gel)</p></div><p class="font-display text-shine shrink-0">$60</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Polygel</p></div><p class="font-display text-shine shrink-0">$70</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Apres</p></div><p class="font-display text-shine shrink-0">$70</p></div>
              <div class="flex items-start justify-between gap-3 py-2"><div><p class="text-[color:var(--ink)] font-light">Rubber Base</p></div><p class="font-display text-shine shrink-0">$60</p></div>
            </div>
          </div>
          <div class="glass glass-hover rounded-3xl p-6 reveal" style="transition-delay:160ms">
            <h3 class="font-display text-lg mb-4" data-es="Combos" data-en="Combos">Combos</h3>
            <div class="text-sm">
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Acrilico + Pedi</p></div><p class="font-display text-shine shrink-0">$115</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Apres + Pedi</p></div><p class="font-display text-shine shrink-0">$115</p></div>
              <div class="flex items-start justify-between gap-3 py-2"><div><p class="text-[color:var(--ink)] font-light">Soak Off / Pedicure</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-0.5">1h 15 min</p></div><p class="font-display text-shine shrink-0">$65</p></div>
            </div>
          </div>
          <div class="glass glass-hover rounded-3xl p-6 reveal" style="transition-delay:240ms">
            <h3 class="font-display text-lg mb-4" data-es="Extras y Retoques" data-en="Extras &amp; Touch-Ups">Extras &amp; Touch-Ups</h3>
            <div class="text-sm">
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Nail Repair</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-0.5">10 min</p></div><p class="font-display text-shine shrink-0">$10</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">Soak Off</p></div><p class="font-display text-shine shrink-0">$20</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light" data-es="Removedor de callos" data-en="Callus Removal">Callus Removal</p></div><p class="font-display text-shine shrink-0">$20</p></div>
              <div class="flex items-start justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]"><div><p class="text-[color:var(--ink)] font-light">French</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-0.5">10 min</p></div><p class="font-display text-shine shrink-0">$10</p></div>
              <div class="flex items-start justify-between gap-3 py-2"><div><p class="text-[color:var(--ink)] font-light" data-es="Diseño mano alzada" data-en="Freehand Design">Freehand Design</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-0.5">20 min</p></div><p class="font-display text-shine shrink-0">$15</p></div>
            </div>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: acrilico en 2 dedos $20 y mas nail art a pedido. Menu completo y disponibilidad en Booksy." data-en="Also available: 2-nail acrylic touch-up $20 and more nail art on request. Full menu and availability on Booksy.">Also available: 2-nail acrylic touch-up $20 and more nail art on request. Full menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Arte" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Pearls y anillos" data-en="Pearls &amp; rings">Pearls &amp; rings</span><img src="assets/raw/bk-14.jpg" alt="Nail art with gold rings and pearl embellishments, close-up" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Frances clasico" data-en="Classic french">Classic french</span><img src="assets/raw/bk-11.jpg" alt="Classic almond-shaped french manicure" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Vino profundo" data-en="Deep wine">Deep wine</span><img src="assets/raw/bk-6.jpg" alt="Deep burgundy almost-black glossy manicure" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Naranja vibrante" data-en="Vibrant orange">Vibrant orange</span><img src="assets/raw/bk-3.jpg" alt="Vibrant orange-red gel manicure" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Coffin nude" data-en="Nude coffin">Nude coffin</span><img src="assets/raw/bk-8.jpg" alt="Long nude coffin-shaped acrylic set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Diseño rojo" data-en="Red swirl design">Red swirl design</span><img src="assets/raw/bk-15.jpg" alt="Red nail art with a swirl pattern design" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES (reales, verbatim, Booksy)
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 78 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 78 verified reviews on Booksy">5.0 out of 5 · 78 verified reviews on Booksy</span></p>')
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Buen servicio, mis uñas siempre quedan perfectas"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karla Z.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor en lo que hace"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Darling N.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely the BEST pedicure experience! From the moment I walked in, I felt welcomed &amp; pampered. This private salon is beautifully decorated, luxurious, and incredibly relaxing. Free parking &amp; convenient hours is the icing on the cake."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jewel E.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 78 reseñas en Booksy" data-en="Read all 78 reviews on Booksy">Read all 78 reviews on Booksy</a>')
print("OPINIONES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">429 Hialeah Dr, Suite 8, Hialeah, FL 33010</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=429+Hialeah+Dr,+Hialeah,+FL+33010"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los ultimos disenos de Ibis y escribe por DM cualquier duda antes de tu cita." data-en="See Ibis latest designs and DM any questions before your appointment.">See Ibis latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Magic In Your Nails, 429 Hialeah Dr, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=429+Hialeah+Dr,+Hialeah,+FL+33010&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="La magia esta en el detalle." data-en="The magic is in the detail.">The magic is in the detail.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tus uñas nuevas" data-en="Your new nails">Your new nails</span> <span class="text-shine" data-es="te estan esperando" data-en="are waiting">are waiting</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en Booksy en segundos: tu manicure de gel, tu set de Luminary o esa manicura rusa que quieres probar." data-en="Book on Booksy in seconds: your gel manicure, your Luminary set, or that Russian manicure you have been wanting to try.">Book on Booksy in seconds: your gel manicure, your Luminary set, or that Russian manicure you have been wanting to try.</p>')
rep('<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Magic Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(238,201,168,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Magic In Your Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(238,201,168,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Magic In Your Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de uñas en Hialeah, FL. Atencion con cita previa." data-en="Nail studio in Hialeah, FL. By appointment only.">Nail studio in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>429 Hialeah Dr, Suite 8, Hialeah, FL 33010</p>')
rep('<p><a href="' + BOOKSY + '" target="_blank" rel="noopener" class="hover:text-[#eec9a8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + BOOKSY + '" target="_blank" rel="noopener" class="hover:text-[#eec9a8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#eec9a8]">Instagram · ' + IG_HANDLE + '</a></p>',
    '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#eec9a8]">Instagram · ' + IG_HANDLE + '</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Magic In Your Nails.</p>')
print("FOOTER done")

# book-float
rep('<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="book-float" aria-label="Book on Booksy">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
