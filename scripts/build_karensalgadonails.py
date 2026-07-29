import re

h = open("output/karen-salgado-nails/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Nails by Karen"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/898761_nails-by-karen_nail-salon_15886_hialeah"
IG_URL_OLD = "https://www.instagram.com/_lashbloom/"
IG_URL_NEW = "https://www.instagram.com/nail_by_karen_salgado/"
IG_AT_OLD = "@_lashbloom"
IG_AT_NEW = "@nail_by_karen_salgado"

# ---------- 1. HEAD ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Nail Salon in Miami Lakes, FL | 5.0 on Booksy</title>",
)
rep('<meta name="theme-color" content="#f6f1ea" />', '<meta name="theme-color" content="#faf6ec" />')
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Miami Lakes FL: dip, gel, Apres and Polygel manicures, spa pedicures and nail art with a perfect 5.0 across 38 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Nail Salon in Miami Lakes, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Dip, gel, Apres and Polygel nails. 5.0 on Booksy. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-9.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-6.jpg" />')

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
    "description": "Nail salon in Miami Lakes, FL: dip, gel, Apres and Polygel manicures, spa pedicures and nail art.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "15485 Eagle Nest Ln, Suite 100", "addressLocality": "Miami Lakes", "addressRegion": "FL", "postalCode": "33014", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.88979, "longitude": -80.30859 }},
    "sameAs": ["{BOOKSY_NEW}", "{IG_URL_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "38", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday"], "opens": "09:30", "closes": "19:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday", "Friday"], "opens": "09:00", "closes": "19:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:15", "closes": "16:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      {{ "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Regular Manicure" }} }},
      {{ "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Dip Manicure" }} }},
      {{ "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Apres" }} }},
      {{ "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Luminary Nails and Spa Pedicure" }} }},
      {{ "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Regular Pedicure" }} }},
      {{ "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Polygel" }} }}
    ] }}
  }}
  </script>"""
rep(OLD_LD, NEW_LD)

repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_URL_OLD, IG_URL_NEW)
repall(IG_AT_OLD, IG_AT_NEW)

# ---------- 3. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NK</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 4. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    f'<img src="assets/raw/bk-6.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails by <span class="text-[color:var(--accent-deep)]">Karen</span></span>',
)

# ---------- 5. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami Lakes, FL · Salón de Uñas" data-en="Miami Lakes, FL · Nail Salon">Miami Lakes, FL · Nail Salon</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas hechas a tu manera." data-en="Nails, done your way.">Nails, done your way.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Dip, gel, Apres" data-en="Dip, gel, Apres">Dip, gel, Apres</span><br /><span data-es="y Polygel, hechos para " data-en="and Polygel, made to ">and Polygel, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    f'data-es="Manicure y pedicura en dip, gel, Apres y Polygel, hechas a mano por Karen Salgado en su suite privado de Miami Lakes. Un 5.0 perfecto en 38 reseñas de Booksy, y clientas que solo confían sus uñas a ella." data-en="Dip, gel, Apres and Polygel manicures and pedicures, done by hand by Karen Salgado in her private suite in Miami Lakes. A perfect 5.0 across 38 Booksy reviews, and clients who trust their nails to no one else.">Dip, gel, Apres and Polygel manicures and pedicures, done by hand by Karen Salgado in her private suite in Miami Lakes. A perfect 5.0 across 38 Booksy reviews, and clients who trust their nails to no one else.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 38 reseñas en Booksy" data-en="5.0 · 38 reviews on Booksy">5.0 · 38 reviews on Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-9.jpg" alt="Dark chrome ombre manicure on almond-shaped nails" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Luminary Nails + Spa Pedicure</p>')
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$130 · 2h 45min" data-en="$130 · 2h 45min">$130 · 2h 45min</p>',
)

# ---------- 6. STRIP ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="38">38</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Dip <span class="text-shine">&amp;</span> Polygel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicure · Pedicura" data-en="Manicure · Pedicure">Manicure · Pedicure</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">We speak</span> <span class="text-shine" data-es="Español" data-en="Spanish">Spanish</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Warm, personal care</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami Lakes, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">15485 Eagle Nest Ln</p></div>',
)

# ---------- 7. MARQUEE ----------
MQ = [
    ("Classic Set", "Dip Manicure"),
    ("Hybrid Set", "Gel Manicure"),
    ("Volume Set", "Apres"),
    ("Mega Volume", "Polygel"),
    ("Bottom Lashes", "Spa Pedicure"),
    ("West Palm Beach, FL", "Miami Lakes, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 8. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Marbled chrome nail art closeup" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Glossy bronze ombre manicure on coffin-shaped nails" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite privado," data-en="A private suite,">A private suite,</span><br /><span class="text-shine" data-es="pensado para ti" data-en="made just for you">made just for you</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    f'data-es="{NAME} es el suite privado de Karen Salgado en Miami Lakes. Cada cita se piensa contigo: dip, gel, Apres, Polygel o un diseño hecho a mano, ella se toma el tiempo para que quede exactamente como quieres." data-en="{NAME} is Karen Salgado\'s private suite in Miami Lakes. Every visit is planned around you: dip, gel, Apres, Polygel or a hand-painted design, she takes her time to get it exactly right.">{NAME} is Karen Salgado\'s private suite in Miami Lakes. Every visit is planned around you: dip, gel, Apres, Polygel or a hand-painted design, she takes her time to get it exactly right.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 38 reseñas verificadas en Booksy, y clientas que dicen que Karen cuida cada detalle hasta que sus uñas quedan impecables." data-en="The result: a perfect 5.0 across 38 verified reviews on Booksy, and clients who say Karen is careful and tedious about every detail until your nails look flawless.">The result: a perfect 5.0 across 38 verified reviews on Booksy, and clients who say Karen is careful and tedious about every detail until your nails look flawless.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="38">38</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    f'<img src="assets/raw/bk-6.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Karen Salgado · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail artist">Nail artist</span></span>',
)

# ---------- 9. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy, ya sea manicure, pedicura o extensión, con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy, whether manicure, pedicure or extension, with clear price and duration, and confirm instantly.">Pick your service on Booksy, whether manicure, pedicure or extension, with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Elige tu acabado" data-en="Choose your finish">Choose your finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma, largo y color: dip, gel, Apres, Polygel o un diseño pintado a mano, tú decides el estilo." data-en="Shape, length and color: dip, gel, Apres, Polygel or a hand-painted design, you choose the style.">Shape, length and color: dip, gel, Apres, Polygel or a hand-painted design, you choose the style.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos y pies al detalle" data-en="Hands &amp; feet, detailed">Hands &amp; feet, detailed</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cuidado de cutícula y aplicación en dip, gel o Polygel, cada paso con calma y atención al detalle." data-en="Filing, cuticle care and dip, gel or Polygel application, every step done calmly and with attention to detail.">Filing, cuticle care and dip, gel or Polygel application, every step done calmly and with attention to detail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">You leave ready</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu manicure o pedicura lista, tal como cuentan sus reseñas: impecable y con acabado profesional." data-en="You leave with your manicure or pedicure finished, just as her reviews describe: flawless, with a professional finish.">You leave with your manicure or pedicure finished, just as her reviews describe: flawless, with a professional finish.</p>',
)

# ---------- 10. SERVICIOS ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure" data-en="Manicure">Manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Dip Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure en polvo dip con acabado duradero y brillo natural. También: Regular Manicure $20, Gel Manicure $40 y Dip Full Manicure $60." data-en="Dip powder manicure with a long-lasting, naturally glossy finish. Also available: Regular Manicure $20, Gel Manicure $40 and Dip Full Manicure $60.">Dip powder manicure with a long-lasting, naturally glossy finish. Also available: Regular Manicure $20, Gel Manicure $40 and Dip Full Manicure $60.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Luminary Nails + Spa Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo completo: sistema luminary en manos y una pedicura spa relajante en un solo turno. También: Luminary Nail System sola $65." data-en="The full combo: the luminary nail system on your hands and a relaxing spa pedicure in one visit. Also: Luminary Nail System alone $65.">The full combo: the luminary nail system on your hands and a relaxing spa pedicure in one visit. Also: Luminary Nail System alone $65.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$130</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Regular Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura clasica con limado, cuidado de cuticula y esmaltado. También: Gel Pedicure $50 (1h) y Spa Pedicura $60." data-en="A classic pedicure with shaping, cuticle care and polish. Also available: Gel Pedicure $50 (1h) and Spa Pedicure $60.">A classic pedicure with shaping, cuticle care and polish. Also available: Gel Pedicure $50 (1h) and Spa Pedicure $60.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extensiones" data-en="Extensions">Extensions</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Polygel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extension en Polygel de apariencia natural y gran resistencia. También: Polygel con Extension $80 (1h45) y Apres $70 (1h30)." data-en="A strong, natural-looking Polygel extension. Also: Polygel with Extension $80 (1h45) and Apres $70 (1h30).">A strong, natural-looking Polygel extension. Also: Polygel with Extension $80 (1h45) and Apres $70 (1h30).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end():]

rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="acabado" data-en="finish">finish</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.</p>',
)

# ---------- 12. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: Chrome $10 · Cat Eyes $10 · fix a nail $7 · Manicura y pedicura para hombres desde $25. Precios exactos y disponibilidad en tiempo real en Booksy." data-en="Also on the menu: Chrome $10 · Cat Eyes $10 · nail fix $7 · Men\'s manicure and pedicure from $25. Exact prices and real time availability on Booksy.">Also on the menu: Chrome $10 · Cat Eyes $10 · nail fix $7 · Men\'s manicure and pedicure from $25. Exact prices and real time availability on Booksy.</span></p>',
)

# ---------- 13. GALERIA ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>',
)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Vista de estudio" data-en="Studio detail">Studio detail</span><img src="assets/raw/bk-7.jpg" alt="Nail art closeup on a rustic wood surface" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rosa con anillo" data-en="Pink set with ring">Pink set with ring</span><img src="assets/raw/bk-4.jpg" alt="Pink gel manicure on almond-shaped nails with a gold ring" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Nude clásico" data-en="Classic nude">Classic nude</span><img src="assets/raw/bk-5.jpg" alt="Nude manicure on short square nails" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 15. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 38 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 38 verified reviews on Booksy">5.0 out of 5 · 38 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Beautiful work!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lisvette R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I love it !!! 😍"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anays C…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Karen is the best nail tech in Miami lakes!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sheyla B…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 38 reseñas en Booksy" data-en="Read all 38 reviews on Booksy">Read all 38 reviews on Booksy</a>',
)

# ---------- 16. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami Lakes, FL</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">15485 Eagle Nest Ln, Suite 100, Miami Lakes, FL 33014</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=15485+Eagle+Nest+Ln,+Miami+Lakes,+FL+33014" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto martes y miércoles de 9:30 am a 7:00 pm, jueves y viernes de 9:00 am a 7:00 pm, y sábado de 8:15 am a 4:00 pm." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Tuesday and Wednesday 9:30 am to 7:00 pm, Thursday and Friday 9:00 am to 7:00 pm, and Saturday 8:15 am to 4:00 pm.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Tuesday and Wednesday 9:30 am to 7:00 pm, Thursday and Friday 9:00 am to 7:00 pm, and Saturday 8:15 am to 4:00 pm.</p>',
)

rep(
    'data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los diseños más recientes de Karen y escribe por DM cualquier duda antes de tu cita." data-en="See Karen\'s latest designs and DM any questions before your appointment.">See Karen\'s latest designs and DM any questions before your appointment.</p>',
)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Map: {NAME}, 15485 Eagle Nest Ln, Miami Lakes FL"\n          src="https://www.google.com/maps?q=15485+Eagle+Nest+Ln,+Miami+Lakes,+FL+33014&output=embed"',
)

# ---------- 17. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tus uñas nuevas" data-en="Your next manicure">Your next manicure</span> <span class="text-shine" data-es="te están esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu dip, gel, Apres o Polygel, o la pedicura spa que ya te toca." data-en="Book online in seconds: your dip, gel, Apres or Polygel set, or the spa pedicure you are due for.">Book online in seconds: your dip, gel, Apres or Polygel set, or the spa pedicure you are due for.</p>',
)

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-6.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami Lakes, FL. Atención con cita previa." data-en="Nail salon in Miami Lakes, FL. By appointment only.">Nail salon in Miami Lakes, FL. By appointment only.</p>',
)
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>15485 Eagle Nest Ln, Suite 100, Miami Lakes, FL 33014</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 19. Paleta: plum-pink -> warm bronze/champagne gold ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

HEX_MAP = {
    "a04a72": "9c7a3a",  # accent-deep
    "c47a9c": "c9a662",  # accent-mid
    "f3e0ea": "f2ead6",  # bg-2 / accent-soft
    "faf2f6": "faf6ec",  # bg
    "f0bed7": "e8d19f",  # dark-band text-shine/stars/hover accent
    "8a5573": "8a7143",  # dark-band btn-3d shadow (medium)
    "d9a8c2": "d9c495",  # orb-b light tint
    "7d3457": "6b5225",  # btn-3d gradient dark stop / scroll-progress start
    "5f2c48": "574321",  # text-shine dark stop / step-num dark stop
    "33222c": "2c2418",  # ink
    "fbf3f8": "faf6ea",  # tile-cap text
    "fbeff5": "f5eedd",  # dark-band btn-3d top stop
    "f8dfeb": "eee0bd",  # dark-band text-shine 2nd stop
    "f2d5e3": "ecdcb0",  # orb-a light tint
    "f2cfe0": "ecdba9",  # dark-band text-shine last stop
    "efd0e0": "e8d8ab",  # dark-band btn-3d mid stop
    "e5c1d4": "e0d0a0",  # orb-c light tint
    "dc9dbe": "d1b57e",  # scroll-progress last stop
    "d3a2bc": "cbb283",  # dark-band btn-3d bottom stop
    "c9789f": "bb9c5c",  # text-shine 2nd stop
    "b25a85": "9f7f42",  # text-shine last stop
    "5c2140": "4a3a1a",  # btn-3d / book-float shadow border (light theme)
    "2a1722": "1e1810",  # cta-final dark-band background gradient (start)
    "1f0f18": "15110b",  # cta-final dark-band background gradient (end)
    "1c0f16": "14100a",  # footer dark-band background
}
for old, new in HEX_MAP.items():
    assert old in h, f"paleta: no se encontro hex #{old}"
    h = h.replace(f"#{old}", f"#{new}")

RGB_TRIPLE_MAP = [
    ((160, 74, 114), (156, 122, 58)),
    ((70, 25, 50), (74, 58, 26)),
    ((51, 34, 44), (44, 36, 24)),
    ((125, 52, 87), (107, 82, 37)),
    ((240, 190, 215), (232, 209, 159)),
    ((233, 205, 186), (224, 200, 150)),
    ((185, 138, 128), (168, 140, 90)),
    ((253, 246, 250), (250, 248, 238)),
    ((250, 242, 246), (250, 246, 236)),
    ((40, 16, 30), (30, 24, 16)),
]
for (ro, go, bo), (rn, gn, bn) in RGB_TRIPLE_MAP:
    pattern = re.compile(r"rgba?\(\s*%d\s*,\s*%d\s*,\s*%d\s*(,\s*[\d.]+\s*)?\)" % (ro, go, bo))
    assert pattern.search(h), f"paleta: no se encontro rgb({ro},{go},{bo})"

    def _mk(rn=rn, gn=gn, bn=bn):
        def _repl(mo):
            alpha = mo.group(1)
            if alpha is not None:
                return "rgba(%d,%d,%d%s)" % (rn, gn, bn, alpha)
            return "rgb(%d,%d,%d)" % (rn, gn, bn)
        return _repl

    h = pattern.sub(_mk(), h)

h = h.replace("@@BADGE@@", badge_block, 1)

open("output/karen-salgado-nails/index.html", "w").write(h)
print("BUILD OK: karen-salgado-nails")
