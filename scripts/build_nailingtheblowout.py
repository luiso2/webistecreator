import re, os, shutil

SLUG = "nailingtheblowout"
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

assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
              'https://nailingtheblowout.glossgenius.com')
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/nailing_the_blowout/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@nailing_the_blowout')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Nailing the Blowout · Nail Studio in Miami Lakes, FL | Book Online</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nailing the Blowout by Jazmin, Miami Lakes FL: gel and structured manicures, nail art, pedicures. Real menu, real photos. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nailing the Blowout · Nail Studio in Miami Lakes, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel manicures, nail art and pedicures, one client at a time. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-13.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-12.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nailing the Blowout",
    "description": "Nail studio in Miami Lakes, FL: gel manicures, structured/luminary manicures, nail art and pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "7221 Miami Lakeway South", "addressLocality": "Miami Lakes", "addressRegion": "FL", "postalCode": "33014", "addressCountry": "US" },
    "telephone": "+17864790555",
    "sameAs": ["https://nailingtheblowout.glossgenius.com", "https://www.instagram.com/nailing_the_blowout/"],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Structured/Luminary Manicure" } },
      { "@type": "Offer", "price": "10", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hand Paraffin Wax" } },
      { "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Personalized Charcuterie Board" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nailing the Blowout</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.35)]" />',
    '<img src="assets/raw/bk-12.jpg" alt="Nailing the Blowout" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nailing the <span class="text-[color:var(--accent-deep)]">Blowout</span></span>')
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="nav-link" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
print("NAV done")

# HERO
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami Lakes, FL · Estudio de Uñas" data-en="Miami Lakes, FL · Nail Studio">Miami Lakes, FL · Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Se trata de la experiencia." data-en="It is all about the experience.">It is all about the experience.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura gel, arte en uñas" data-en="Gel manicures, nail art">Gel manicures, nail art</span><br /><span data-es="y pedicura hechas con " data-en="and pedicures made with ">and pedicures made with </span><span class="text-shine" data-es="elegancia" data-en="elegance">elegance</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura de gel y estructurada, arte en uñas por niveles, pedicura gel y volcano detox, en un beauty bar en Miami Lakes hecho para consentirte. Walk-ins y niños bienvenidos, citas preferidas." data-en="Gel and structured manicures, tiered nail art, gel and volcano detox pedicures, in a beauty bar in Miami Lakes made to pamper you. Walk-ins and kids welcome, appointments preferred.">Gel and structured manicures, tiered nail art, gel and volcano detox pedicures, in a beauty bar in Miami Lakes made to pamper you. Walk-ins and kids welcome, appointments preferred.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar cita" data-en="Book online">Book online</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-13.jpg" alt="Metallic silver chrome nail manicure, close-up" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Manicura Estructurada" data-en="Structured Manicure">Structured Manicure</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$65 · 1h 20min" data-en="$65 · 1h 20min">$65 · 1h 20min</p>')

# STRIP
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl">Nails <span class="text-shine">&amp;</span> Care</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo, precios reales" data-en="Full menu, real prices">Full menu, real prices</p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">5 <span class="text-shine" data-es="niveles" data-en="tiers">tiers</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Diseños por nivel" data-en="Nail art by tier">Nail art by tier</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="5ta visita" data-en="5th visit">5th visit</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="50% de descuento de lealtad" data-en="50% loyalty discount">50% loyalty discount</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Lakes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Miami Lakeway South</p></div>')

for old, new in [
    ('Classic Set', 'Gel Manicure'),
    ('Hybrid Set', 'Structured Mani'),
    ('Volume Set', 'Gel Pedicure'),
    ('Mega Volume', 'Volcano Detox'),
    ('Bottom Lashes', 'Nail Art'),
    ('West Palm Beach, FL', 'Miami Lakes, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# EXPERIENCIA
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Hand paraffin wax treatment in a warm bowl" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Charcuterie board served during a nail appointment" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un beauty bar," data-en="A beauty bar,">A beauty bar,</span><br /><span class="text-shine" data-es="hecho para consentirte" data-en="made to pamper you">made to pamper you</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Nailing the Blowout es el beauty bar de Jazmin en Miami Lakes, hecho alrededor de la experiencia completa: manicura, pedicura y arte en uñas con un toque de consentimiento, como el charcuterie board en tu cita." data-en="Nailing the Blowout is Jazmin\'s beauty bar in Miami Lakes, built around the full experience: manicures, pedicures and nail art with a pampering touch, like the charcuterie board during your visit.">Nailing the Blowout is Jazmin\'s beauty bar in Miami Lakes, built around the full experience: manicures, pedicures and nail art with a pampering touch, like the charcuterie board during your visit.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Cada clienta recibe una tarjeta de lealtad que se sella en cada visita: en tu quinta visita recibes 50% de descuento en el total, como agradecimiento. Walk-ins y niños bienvenidos." data-en="Every client gets a loyalty card stamped at each visit: on your 5th visit you get 50% off your total, as a thank you. Walk-ins and kids welcome.">Every client gets a loyalty card stamped at each visit: on your 5th visit you get 50% off your total, as a thank you. Walk-ins and kids welcome.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Uñas" data-en="Nails">Nails</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Especialidad" data-en="Specialty">Specialty</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="5ta" data-en="5th">5th</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Visita, 50% off" data-en="Visit, 50% off">Visit, 50% off</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Miami Lakes" data-en="Miami Lakes">Miami Lakes</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Ubicación" data-en="Location">Location</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-12.jpg" alt="Nailing the Blowout" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,117,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Jazmin · <span class="text-[color:var(--ink-40)]" data-es="Fundadora" data-en="Founder">Founder</span></span>')
print("EXPERIENCIA done")

# METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu manicura, pedicura o nivel de arte con precio y duración claros, y confirmas al instante." data-en="Pick your manicure, pedicure or art tier with clear price and duration, and confirm instantly.">Pick your manicure, pedicure or art tier with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consiéntete" data-en="Get pampered">Get pampered</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llegas y te reciben con un charcuterie board personalizado mientras eliges tu diseño y add-ons." data-en="You arrive and are welcomed with a personalized charcuterie board while you pick your design and add-ons.">You arrive and are welcomed with a personalized charcuterie board while you pick your design and add-ons.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De una manicura gel de 50 minutos a una pedicura volcano detox: cada servicio recibe su tiempo completo." data-en="From a 50-minute gel manicure to a volcano detox pedicure: every service gets its full time.">From a 50-minute gel manicure to a volcano detox pedicure: every service gets its full time.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Tarjeta sellada" data-en="Loyalty stamped">Loyalty stamped</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu tarjeta de lealtad sellada, un paso mas cerca del 50% de descuento en tu quinta visita." data-en="You leave with your loyalty card stamped, one step closer to 50% off on your 5th visit.">You leave with your loyalty card stamped, one step closer to 50% off on your 5th visit.</p>''')
print("METODO done")

# SERVICIOS
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nailing the Blowout. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nailing the Blowout. Booking confirms instantly.">Prices and durations as published by Nailing the Blowout. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicura" data-en="Manicure">Manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Gel" data-en="Gel Manicure">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura de gel clasica con acabado de larga duracion." data-en="Classic gel manicure with a long-lasting finish.">Classic gel manicure with a long-lasting finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">50min</p></div>
            <a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,117,74,0.4); box-shadow: 0 18px 50px rgba(51,35,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicura" data-en="Manicure">Manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Estructurada" data-en="Structured Manicure">Structured Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura estructurada/luminary para reforzar la uña natural con un acabado impecable." data-en="Structured/luminary manicure to reinforce the natural nail with a flawless finish.">Structured/luminary manicure to reinforce the natural nail with a flawless finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 20min</p></div>
            <a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel y Volcano Detox" data-en="Gel &amp; Volcano Detox">Gel &amp; Volcano Detox</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura de gel desde $50, o el volcano detox por $70 para un mimo mas profundo." data-en="Gel pedicure from $50, or the volcano detox at $70 for a deeper pampering.">Gel pedicure from $50, or the volcano detox at $70 for a deeper pampering.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $50" data-en="From $50">From $50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h+</p></div>
            <a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Arte" data-en="Art">Art</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Diseños por Nivel" data-en="Tiered Nail Art">Tiered Nail Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Desde 1 diseño ($5) hasta 5 uñas con diseño ($25), mas chrome, french y cat eye desde $12." data-en="From 1 nail design ($5) to 5 nails with design ($25), plus chrome, french and cat eye from $12.">From 1 nail design ($5) to 5 nails with design ($25), plus chrome, french and cat eye from $12.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $5" data-en="From $5">From $5</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">10min+</p></div>
            <a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: manicura princesa (4-11 anos), charcuterie board personalizado, masajes de pies y piernas, y reparacion de poly gel. Menu completo y disponibilidad en el sitio de reservas." data-en="Also available: princess manicure (ages 4-11), personalized charcuterie board, foot and leg massage add-ons, and poly gel repair. Full menu and availability on the booking site.">Also available: princess manicure (ages 4-11), personalized charcuterie board, foot and leg massage add-ons, and poly gel repair. Full menu and availability on the booking site.</span></p>')
print("SERVICIOS done")

# GALERIA
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Detalles" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="details">details</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Pedicura relajante" data-en="Relaxing pedicure">Relaxing pedicure</span><img src="assets/raw/bk-3.jpg" alt="Pedicure bowl treatment, feet soaking" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cromo metalico" data-en="Metallic chrome">Metallic chrome</span><img src="assets/raw/bk-13.jpg" alt="Metallic silver chrome manicure, close-up" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Rojo clasico" data-en="Classic red">Classic red</span><img src="assets/raw/bk-14.jpg" alt="Classic red almond nail set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Decal decorativo" data-en="Nail art decal">Nail art decal</span><img src="assets/raw/bk-15.jpg" alt="Nude manicure with a decorative decal on one nail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Diseño con acentos" data-en="Accent design">Accent design</span><img src="assets/raw/bk-16.jpg" alt="Neutral manicure with a gold swirl accent design" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Manicura princesa" data-en="Princess manicure">Princess manicure</span><img src="assets/raw/bk-11.jpg" alt="Young child receiving a princess manicure" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# OPINIONES -> ESPECIALIDADES
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="El beauty bar" data-en="The beauty bar">The beauty bar</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Por qué" data-en="Why">Why</span> <span class="text-shine" data-es="Nailing the Blowout" data-en="Nailing the Blowout">Nailing the Blowout</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Manicura, pedicura y arte en uñas, hechos alrededor de la experiencia completa." data-en="Manicures, pedicures and nail art, built around the full experience.">Manicures, pedicures and nail art, built around the full experience.</p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_WHY = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="font-display text-2xl text-shine mb-3" data-es="Toda la experiencia" data-en="The full experience">The full experience</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Un charcuterie board personalizado te recibe mientras te consientes con manicura, pedicura o arte en uñas." data-en="A personalized charcuterie board welcomes you while you get pampered with manicures, pedicures or nail art.">A personalized charcuterie board welcomes you while you get pampered with manicures, pedicures or nail art.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Lealtad que se nota" data-en="Loyalty that shows">Loyalty that shows</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tarjeta de lealtad sellada en cada visita: 50% de descuento en tu quinta visita, como agradecimiento." data-en="Loyalty card stamped at every visit: 50% off on your 5th visit, as a thank you.">Loyalty card stamped at every visit: 50% off on your 5th visit, as a thank you.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Para toda la familia" data-en="For the whole family">For the whole family</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Walk-ins y niños bienvenidos, con manicura princesa para las mas pequeñas, de 4 a 11 años." data-en="Walk-ins and kids welcome, with a princess manicure for the little ones, ages 4 to 11.">Walk-ins and kids welcome, with a princess manicure for the little ones, ages 4 to 11.</p>
        </div>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_WHY + h[reviews_grid.end():]

rep('<a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver el menu completo y reservar" data-en="See the full menu and book">See the full menu and book</a>')
print("ESPECIALIDADES done")

# UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Lakes</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">7221 Miami Lakeway South, Miami Lakes, FL 33014</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=7221+Miami+Lakeway+South,+Miami+Lakes,+FL+33014"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa en linea (walk-ins bienvenidos): eliges servicio, dia y hora, y la confirmacion es inmediata." data-en="By appointment online (walk-ins welcome): pick the service, day and time, and the confirmation is instant.">By appointment online (walk-ins welcome): pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,117,74,0.4)]" href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,117,74,0.4)]" href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los sets mas recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest sets and DM any questions before your appointment.">See the latest sets and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Nailing the Blowout, 7221 Miami Lakeway South, Miami Lakes FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=7221+Miami+Lakeway+South,+Miami+Lakes,+FL+33014&output=embed"')
print("UBICACION done")

# CTA FINAL
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Se trata de la experiencia." data-en="It is all about the experience.">It is all about the experience.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proxima cita" data-en="Your next visit">Your next visit</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu manicura, tu pedicura, o ese diseño que llevas planeando." data-en="Book online in seconds: your manicure, your pedicure, or that design you have been planning.">Book online in seconds: your manicure, your pedicure, or that design you have been planning.</p>')
rep('<a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')
print("CTA FINAL done")

# FOOTER
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Nailing the Blowout</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,213,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-12.jpg" alt="Nailing the Blowout" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,213,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Nailing the Blowout</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Beauty bar en Miami Lakes, FL. Walk-ins y citas bienvenidos." data-en="Beauty bar in Miami Lakes, FL. Walk-ins and appointments welcome.">Beauty bar in Miami Lakes, FL. Walk-ins and appointments welcome.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>7221 Miami Lakeway South, Miami Lakes, FL 33014</p>')
rep('<p><a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#f0d5be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#f0d5be]" data-es="Reservas en linea" data-en="Online booking">Online booking</a></p>')
rep('<p><a href="https://www.instagram.com/nailing_the_blowout/" target="_blank" rel="noopener" class="hover:text-[#f0d5be]">Instagram · @nailing_the_blowout</a></p>',
    '<p><a href="https://www.instagram.com/nailing_the_blowout/" target="_blank" rel="noopener" class="hover:text-[#f0d5be]">Instagram · @nailing_the_blowout</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nailing the Blowout.</p>')
print("FOOTER done")

# book-float
rep('<a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://nailingtheblowout.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
