import re

h = open("output/wavytroublenails/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Wavy Trouble"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1408434_wavy-trouble_nail-salon_15889_miami"
IG_URL_OLD = "https://www.instagram.com/_lashbloom/"
IG_URL_NEW = "https://www.instagram.com/wavytrouble/"

# ---------- 1. HEAD ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    "<title>Wavy Trouble · Nail Art Studio in North Miami, FL | 5.0 on Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Wavy Trouble, North Miami (Miami, FL): hand-painted nail art, Gel-X and hard gel extensions by Stephanie Rodrigues, a perfect 5.0 across 14 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Wavy Trouble · Nail Art Studio in North Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Hand-painted nail art, Gel-X and hard gel extensions. 5.0 on Booksy. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-6.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-13.jpg" />')

# ---------- 2. JSON-LD ----------
OLD_LD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Lash Bloom LLC",
    "description": "Lash studio in West Palm Beach, FL: classic, hybrid, volume and mega volume eyelash extensions and fills.",
    "address": { "@type": "PostalAddress", "streetAddress": "4580 Cresthaven Blvd", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33415", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach", "https://www.instagram.com/_lashbloom/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "86", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash services", "itemListElement": [
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic full set" } },
      { "@type": "Offer", "price": "145", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hybrid full set" } },
      { "@type": "Offer", "price": "155", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Volume full set" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic 2wk fill" } }
    ] }
  }
  </script>"""

NEW_LD = f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "{NAME}",
    "description": "Nail art studio in North Miami, Miami, FL: hand-painted nail art, Gel-X and hard gel extensions by Stephanie Rodrigues.",
    "address": {{ "@type": "PostalAddress", "addressLocality": "North Miami, Miami", "addressRegion": "FL", "postalCode": "33161", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.89453, "longitude": -80.1826 }},
    "sameAs": ["{BOOKSY_NEW}", "{IG_URL_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "14", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Friday"], "opens": "10:00", "closes": "22:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Nail art services", "itemListElement": [
      {{ "@type": "Offer", "price": "54", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Simple Nail Art" }} }},
      {{ "@type": "Offer", "price": "81", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Apres Gel-X Intermediate Nail Art" }} }},
      {{ "@type": "Offer", "price": "99", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Hard Gel Extension Complex Nail Art" }} }},
      {{ "@type": "Offer", "price": "27", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Removal plus mani" }} }}
    ] }}
  }}
  </script>"""
rep(OLD_LD, NEW_LD)

repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_URL_OLD, IG_URL_NEW)
repall("@_lashbloom", "@wavytrouble")

# ---------- 3. Idioma: ya en default (EN) -> no se toca ----------

# ---------- 4. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">WT</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 5. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    f'<img src="assets/raw/bk-4.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Wavy <span class="text-[color:var(--accent-deep)]">Trouble</span></span>',
)

# ---------- 6. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="North Miami, Miami, FL · Estudio de Nail Art" data-en="North Miami, Miami, FL · Nail Art Studio">North Miami, Miami, FL · Nail Art Studio</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Diseños de uñas con actitud." data-en="Nail art with edge.">Nail art with edge.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Diseños de uñas pintados" data-en="Hand-painted nail art">Hand-painted nail art</span><br /><span data-es="a mano, hechos para " data-en="made to ">made to </span><span class="text-shine" data-es="impresionar" data-en="impress">impress</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Wavy Trouble es el estudio de Stephanie Rodrigues (Steph) en North Miami. Nail art simple, intermedio y complejo sobre gel-x o hard gel, diseños hechos a mano y freestyle sets, con un 5.0 perfecto en 14 reseñas de Booksy." data-en="Wavy Trouble is Stephanie Rodrigues\' (Steph) studio in North Miami. Simple, intermediate and complex nail art on Gel-X or hard gel, hand-painted designs and freestyle sets, with a perfect 5.0 across 14 Booksy reviews.">Wavy Trouble is Stephanie Rodrigues\' (Steph) studio in North Miami. Simple, intermediate and complex nail art on Gel-X or hard gel, hand-painted designs and freestyle sets, with a perfect 5.0 across 14 Booksy reviews.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 14 reseñas en Booksy" data-en="5.0 · 14 reviews on Booksy">5.0 · 14 reviews on Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-6.jpg" alt="Colorful jewel-tone abstract nail art design" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Apres Gel-X Intermediate Nail Art</p>')
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$81 · 2h 30min" data-en="$81 · 2h 30min">$81 · 2h 30min</p>',
)

# ---------- 7. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="14">14</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Nail Art <span class="text-shine">&amp;</span> Extensions</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel-X · Hard Gel · Diseños" data-en="Gel-X · Hard Gel · Nail art">Gel-X · Hard Gel · Nail art</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Solo una" data-en="Just one">Just one</span> <span class="text-shine" data-es="artista" data-en="artist">artist</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cada diseño hecho por Steph" data-en="Every design made by Steph">Every design made by Steph</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">North Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Miami, FL 33161</p></div>',
)

# ---------- 8. MARQUEE (x4 cada palabra) ----------
MQ = [
    ("Classic Set", "Nail Art"),
    ("Hybrid Set", "Gel-X"),
    ("Volume Set", "Hard Gel"),
    ("Mega Volume", "Freestyle Set"),
    ("Bottom Lashes", "Removal + Mani"),
    ("West Palm Beach, FL", "North Miami, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 9. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Pink French-tip manicure with a clean, glossy finish" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Delicate hand-painted swan nail art detail" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una sola artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="uñas sin límites" data-en="nail art without limits">nail art without limits</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Wavy Trouble es el estudio de Stephanie Rodrigues, conocida como Steph, en North Miami. Cada cita se piensa contigo: nail art simple, intermedio o complejo, sobre gel-x o hard gel, con diseños hechos a mano a partir de las fotos de inspiración que le muestres." data-en="Wavy Trouble is Stephanie Rodrigues\' studio, known to her clients as Steph, in North Miami. Every visit is planned around you: simple, intermediate or complex nail art, on Gel-X or hard gel, with hand-painted designs built from the inspo pictures you bring her.">Wavy Trouble is Stephanie Rodrigues\' studio, known to her clients as Steph, in North Miami. Every visit is planned around you: simple, intermediate or complex nail art, on Gel-X or hard gel, with hand-painted designs built from the inspo pictures you bring her.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 14 reseñas verificadas en Booksy, y clientas que dicen que la atención al detalle de Steph es incomparable." data-en="The result: a perfect 5.0 across 14 verified reviews on Booksy, and clients who say Steph\'s attention to detail is unmatched.">The result: a perfect 5.0 across 14 verified reviews on Booksy, and clients who say Steph\'s attention to detail is unmatched.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="14">14</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>''',
    f'''<img src="assets/raw/bk-4.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Stephanie Rodrigues · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail artist">Nail artist</span></span>''',
)

# ---------- 10. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, diseño" data-en="Your visit, design">Your visit, design</span> <span class="text-shine" data-es="por diseño" data-en="by design">by design</span></h2>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Elige tu diseño" data-en="Choose your design">Choose your design</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nail art simple, intermedio o complejo, en gel-x o hard gel, pintado a mano según las fotos de inspiración que muestres." data-en="Simple, intermediate or complex nail art, on Gel-X or hard gel, hand-painted to match the inspo pictures you show her.">Simple, intermediate or complex nail art, on Gel-X or hard gel, hand-painted to match the inspo pictures you show her.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva en Booksy" data-en="Book on Booksy">Book on Booksy</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="La cita" data-en="The appointment">The appointment</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Aplicación de gel-x o hard gel y luego tu diseño pintado a mano, detalle por detalle." data-en="Gel-X or hard gel extension application, then your design hand-painted, detail by detail.">Gel-X or hard gel extension application, then your design hand-painted, detail by detail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">You leave ready</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set nuevo que combina exactamente con las fotos de inspiración que le mostraste." data-en="You leave with a new set that matches the inspo photos you showed her.">You leave with a new set that matches the inspo photos you showed her.</p>',
)

# ---------- 11. SERVICIOS ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Nail art del día a día" data-en="Everyday nail art">Everyday nail art</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Simple Nail Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseños simples sobre tus uñas naturales o extensiones, perfectos para el día a día. También: 1 color Gel Manicure $45." data-en="Simple designs on natural nails or extensions, perfect for every day. Also: 1 color Gel Manicure $45.">Simple designs on natural nails or extensions, perfect for every day. Also: 1 color Gel Manicure $45.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$54</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,103,74,0.4); box-shadow: 0 18px 50px rgba(51,40,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Apres Gel-X Intermediate Nail Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensión gel-x con nail art de complejidad intermedia, el balance perfecto entre diseño y duración. También: Apres Gel-X Freestyle Set $90." data-en="Gel-X extension with intermediate-complexity nail art, the perfect balance of design and wear time. Also: Apres Gel-X Freestyle Set $90.">Gel-X extension with intermediate-complexity nail art, the perfect balance of design and wear time. Also: Apres Gel-X Freestyle Set $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$81</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Máximo detalle" data-en="Maximum detail">Maximum detail</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Hard Gel Extension Complex Nail Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensión en hard gel con nail art complejo, para el diseño más elaborado del menú. También: Gel Pedicure $45." data-en="Hard gel extension with complex nail art, the most elaborate design on the menu. Also: Gel Pedicure $45.">Hard gel extension with complex nail art, the most elaborate design on the menu. Also: Gel Pedicure $45.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$99</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h 10min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mantenimiento" data-en="Maintenance">Maintenance</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Removal + Mani</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Retiro de tu set anterior y manicure, para dejar tus manos listas para tu próximo diseño." data-en="Removal of your previous set plus a manicure, to get your hands ready for your next design.">Removal of your previous set plus a manicure, to get your hands ready for your next design.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$27</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end():]

rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine">nail art</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.</p>',
)

# ---------- 12. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: Gel Pedicure $45 · 1 color Gel Manicure $45 · Apres Gel-X Freestyle Set $90. Precios y disponibilidad exactos en Booksy." data-en="Also on the menu: Gel Pedicure $45 · 1 color Gel Manicure $45 · Apres Gel-X Freestyle Set $90. Exact prices and availability on Booksy.">Also on the menu: Gel Pedicure $45 · 1 color Gel Manicure $45 · Apres Gel-X Freestyle Set $90. Exact prices and availability on Booksy.</span></p>',
)

# ---------- 13. GALERIA ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Diseños" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nail art">nail art</span></h2>',
)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Calaveras y murciélagos" data-en="Skulls &amp; bats nail art">Skulls &amp; bats nail art</span><img src="assets/raw/bk-13.jpg" alt="Halloween-style nail art with colorful skulls and bats on a dark background" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rayas verdes y naranjas" data-en="Green &amp; orange stripes">Green &amp; orange stripes</span><img src="assets/raw/bk-3.jpg" alt="Green and orange striped nail art design" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Mármol con glitter azul y rosa" data-en="Blue &amp; pink glitter marble">Blue &amp; pink glitter marble</span><img src="assets/raw/bk-7.jpg" alt="Blue and pink glitter marbled nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Personaje pintado a mano" data-en="Hand-painted cartoon art">Hand-painted cartoon art</span><img src="assets/raw/bk-8.jpg" alt="Hand-painted cartoon character nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Murciélagos rosa y negro" data-en="Pink &amp; black bats">Pink &amp; black bats</span><img src="assets/raw/bk-12.jpg" alt="Pink and black Halloween bat nail art design" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Colmillos de vampiro en rojo" data-en="Red vampire teeth">Red vampire teeth</span><img src="assets/raw/bk-16.jpg" alt="Red vampire-teeth Halloween nail art design" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 14. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 14 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 14 verified reviews on Booksy">5.0 out of 5 · 14 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"So incredibly talented :’3 please book with Steph!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Daniela C…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always amazing 🩷"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Valerie S…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Ate down"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily C…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 14 reseñas en Booksy" data-en="Read all 14 reviews on Booksy">Read all 14 reviews on Booksy</a>',
)

# ---------- 15. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">North Miami</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">North Miami, Miami, FL 33161</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,103,74,0.4)]" href="https://www.google.com/maps?q=25.89453,-80.1826" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
)

OLD_LOC_SOCIAL = (
    '<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">\n'
    '            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    '            <div>\n'
    '              <p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    f'              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="{IG_URL_NEW}" target="_blank" rel="noopener">@wavytrouble</a>\n'
    '            </div>\n'
    '          </div>'
)
# nota: en este punto del script ya corrieron los repall globales de IG_URL e @_lashbloom (seccion 2),
# por eso este bloque ancla ya con href/handle NUEVOS; "Yesi" todavia no se toco aqui (se reemplaza
# igual porque toda la tarjeta se sustituye por la de Horario).
NEW_LOC_HOURS = (
    '<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">\n'
    '            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>\n'
    '            <div>\n'
    '              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes, martes, miércoles y viernes de 10:00 am a 10:00 pm." data-en="Monday, Tuesday, Wednesday and Friday, 10:00 am to 10:00 pm.">Monday, Tuesday, Wednesday and Friday, 10:00 am to 10:00 pm.</p>\n'
    '            </div>\n'
    '          </div>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_HOURS)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: {NAME}, North Miami, Miami FL"\n          src="https://www.google.com/maps?q=25.89453,-80.1826&output=embed"',
)

# ---------- 16. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu próximo nail art simple, intermedio o complejo, con Steph en North Miami." data-en="Book online in seconds: your next simple, intermediate or complex nail art set, with Steph in North Miami.">Book online in seconds: your next simple, intermediate or complex nail art set, with Steph in North Miami.</p>',
)

# ---------- 17. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-4.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de nail art en North Miami, Miami, FL. Atención con cita previa." data-en="Nail art studio in North Miami, Miami, FL. By appointment only.">Nail art studio in North Miami, Miami, FL. By appointment only.</p>',
)
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>North Miami, Miami, FL 33161</p>')
# nota: "Instagram · @_lashbloom" ya quedo en "Instagram · @wavytrouble" por el repall global de la seccion 2.
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 18. Paleta: swap global de hex (terracota/rust) ----------
PALETTE = [
    ("#a04a72", "#a0674a"),
    ("#5c2140", "#5c3521"),
    ("#f0bed7", "#f0cfbe"),
    ("#faf2f6", "#faf5f2"),
    ("#c47a9c", "#c4937a"),
    ("#8a5573", "#8a6755"),
    ("#f3e0ea", "#f3e6e0"),
    ("#d9a8c2", "#d9b8a8"),
    ("#7d3457", "#7d4c34"),
    ("#5f2c48", "#5f3d2c"),
    ("#33222c", "#332822"),
    ("#fbf3f8", "#fbf6f3"),
    ("#fbeff5", "#fbf3ef"),
    ("#f8dfeb", "#f8e7df"),
    ("#f6f1ea", "#f6eeea"),
    ("#f4eee2", "#f4e8e2"),
    ("#f2d5e3", "#f2dfd5"),
    ("#f2cfe0", "#f2dbcf"),
    ("#efd0e0", "#efdad0"),
    ("#e5c1d4", "#e5cdc1"),
    ("#dc9dbe", "#dcb29d"),
    ("#d3a2bc", "#d3b2a2"),
    ("#c9789f", "#c99378"),
    ("#b25a85", "#b2775a"),
    ("#2a1722", "#2a1d17"),
    ("#1f0f18", "#1f140f"),
    ("#1c0f16", "#1c130f"),
]
# #D4A84B (merktop badge gold dot) queda protegido: NO esta en la lista, no se toca.
assert "#D4A84B" in h, "el badge dorado debe seguir presente"
for old, new in PALETTE:
    repall(old, new)
assert "#D4A84B" in h, "el badge dorado se alteró (no deberia)"

# rgbas decimales de los tonos de acento/ink que tambien aparecen literal en el markup
RGBA_DECIMAL = [
    ("160,74,114", "160,103,74"),   # a04a72 -> a0674a (accent-deep)
    ("51,34,44", "51,40,34"),       # 33222c -> 332822 (ink)
    ("240,190,215", "240,207,190"), # f0bed7 -> f0cfbe (dark-band accent)
    ("250,242,246", "250,245,242"), # faf2f6 -> faf5f2 (bg)
    ("125,52,87", "125,76,52"),     # 7d3457 -> 7d4c34 (btn-3d shadow)
    ("244,238,226", "244,232,226"), # f4eee2 -> f4e8e2 (badge text color rgb)
]
for old, new in RGBA_DECIMAL:
    repall(old, new)
# rgba del badge dorado (212,168,75) queda protegido: no esta en la lista, no se toca.
assert "212,168,75" in h, "el rgba del badge dorado se alteró (no deberia)"

# ---------- 19. Verificacion final de restos del esqueleto anterior ----------
for leftover in ["Lash Bloom", "Yesi", "West Palm Beach", "Cresthaven", "519855",
                  "pestañas", "_lashbloom", "lash-bloom", "logo.jpg", "hero-1.jpg", "about-2.jpg"]:
    assert leftover not in h, "LEFTOVER: " + leftover

open("output/wavytroublenails/index.html", "w").write(h)
print("BUILD OK: wavytroublenails")
