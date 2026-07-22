import re

h = open("output/solynailsmiami/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Soly Nails Miami"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1665100_soly-nails-miami_nail-salon_15889_miami"
IG_URL_OLD = "https://www.instagram.com/_lashbloom/"
IG_URL_NEW = "https://www.instagram.com/solynailsmiami/"
IG_AT_OLD = "@_lashbloom"
IG_AT_NEW = "@solynailsmiami"

# ---------- 1. HEAD ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Salón de Uñas en Miami, FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Miami FL: full set acrílico, builder gel, manicure en gel y nail art personalizado, con un 5.0 perfecto en 42 reseñas en Booksy. Reserva online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Salón de Uñas en Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Full set acrílico, builder gel y nail art personalizado. 5.0 en Booksy. Reserva online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-13.jpg" />')
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
    "description": "Salón de uñas y belleza en Miami, FL: full set acrílico, builder gel, manicure en gel, nail art, cejas y tratamientos de mirada.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "19377 NE 10th Ave", "addressLocality": "North Miami Beach", "addressRegion": "FL", "postalCode": "33179", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.95315562762389, "longitude": -80.18030874431133 }},
    "sameAs": ["{BOOKSY_NEW}", "{IG_URL_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "42", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "11:00", "closes": "19:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      {{ "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Full Set Acrylic" }} }},
      {{ "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Builder Gel Refill" }} }},
      {{ "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Gel Manicure" }} }},
      {{ "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Complex Nail Art" }} }},
      {{ "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "French" }} }},
      {{ "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Regular Pedicure" }} }}
    ] }}
  }}
  </script>"""
rep(OLD_LD, NEW_LD)

repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_URL_OLD, IG_URL_NEW)
repall(IG_AT_OLD, IG_AT_NEW)

# ---------- 3. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">SN</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 4. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(103,74,160,0.35)]" />',
    f'<img src="assets/raw/bk-4.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(103,74,160,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Soly <span class="text-[color:var(--accent-deep)]">Nails Miami</span></span>',
)

# ---------- 5. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Salón de Uñas" data-en="Miami, FL · Nail Salon">Miami, FL · Salón de Uñas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas hechas para brillar." data-en="Nails made to shine.">Uñas hechas para brillar.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Full set acrílico y builder gel" data-en="Full set acrylic and builder gel">Full set acrílico y builder gel</span><br /><span data-es="con nail art hecho para " data-en="with nail art made to ">con nail art hecho para </span><span class="text-shine" data-es="durar" data-en="last">durar</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    f'data-es="Full set acrílico, builder gel, manicure en gel y nail art personalizado, hechos a mano por Soly en su salón de Miami, FL. Un 5.0 perfecto en 42 reseñas de Booksy, y clientas que solo confían sus uñas a ella." data-en="Acrylic full sets, builder gel, gel manicures and personalized nail art, done by hand by Soly at her salon in Miami, FL. A perfect 5.0 across 42 Booksy reviews, and clients who trust their nails to no one else.">Acrylic full sets, builder gel, gel manicures and personalized nail art, done by hand by Soly at her salon in Miami, FL. A perfect 5.0 across 42 Booksy reviews, and clients who trust their nails to no one else.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 42 reseñas en Booksy" data-en="5.0 · 42 reviews on Booksy">5.0 · 42 reseñas en Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-13.jpg" alt="Nail art de ojo turco azul, diseño destacado de Soly Nails Miami" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Full Set Acrylic</p>')
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$70" data-en="$70">$70</p>',
)

# ---------- 6. STRIP ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="42">42</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrílico <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Full set · Nail art" data-en="Full sets · Nail art">Full set · Nail art</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span class="text-shine" data-es="Favorita" data-en="Favorite">Favorita</span> <span data-es="de sus clientas" data-en="among clients">de sus clientas</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Así la describen en Booksy" data-en="That is how clients describe her on Booksy">Así la describen en Booksy</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">North Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">19377 NE 10th Ave</p></div>',
)

# ---------- 7. MARQUEE ----------
MQ = [
    ("Classic Set", "Full Set Acrylic"),
    ("Hybrid Set", "Builder Gel"),
    ("Volume Set", "Gel Manicure"),
    ("Mega Volume", "Nail Art"),
    ("Bottom Lashes", "Regular Pedicure"),
    ("West Palm Beach, FL", "Miami, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 8. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-12.jpg" alt="French blanco floral hecho en Soly Nails Miami" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Pedicura nude con flor 3D hecha en Soly Nails Miami" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un salón de barrio," data-en="A neighborhood salon,">Un salón de barrio,</span><br /><span class="text-shine" data-es="pensado para ti" data-en="made just for you">pensado para ti</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    f'data-es="{NAME} es el salón de Soly N. en North Miami Beach. Cada cita se piensa contigo: full set acrílico, builder gel, manicure en gel o un nail art hecho a mano, ella se toma el tiempo para que quede exactamente como lo imaginaste." data-en="{NAME} is Soly N.\'s salon in North Miami Beach. Every visit is planned around you: acrylic full set, builder gel, gel manicure or hand-painted nail art, she takes her time to get it exactly the way you imagined.">{NAME} is Soly N.\'s salon in North Miami Beach. Every visit is planned around you: acrylic full set, builder gel, gel manicure or hand-painted nail art, she takes her time to get it exactly the way you imagined.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 42 reseñas verificadas en Booksy, y clientas que la describen como su manicurista favorita, con una actitud tan buena como su trabajo." data-en="The result: a perfect 5.0 across 42 verified reviews on Booksy, and clients who call her their favorite nail tech, with an attitude as great as her work.">The result: a perfect 5.0 across 42 verified reviews on Booksy, and clients who call her their favorite nail tech, with an attitude as great as her work.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="42">42</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(103,74,160,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    f'<img src="assets/raw/bk-4.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(103,74,160,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Soly N. · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail artist">Artista de uñas</span></span>',
)

# ---------- 9. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, uña" data-en="Your visit, nail">Tu cita, uña</span> <span class="text-shine" data-es="por uña" data-en="by nail">por uña</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy, ya sea full set acrílico, manicure en gel o nail art, con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy, whether a full acrylic set, gel manicure or nail art, with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy, ya sea full set acrílico, manicure en gel o nail art, con precio y duración claros, y confirmas al instante.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Elige tu estilo" data-en="Choose your style">Elige tu estilo</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma, largo y color: acrílico, builder gel, gel manicure o un diseño de nail art pintado a mano, tú decides el estilo." data-en="Shape, length and color: acrylic, builder gel, gel manicure or a hand-painted nail art design, you choose the style.">Forma, largo y color: acrílico, builder gel, gel manicure o un diseño de nail art pintado a mano, tú decides el estilo.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos al detalle" data-en="Hands, detailed">Manos al detalle</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cuidado de cutícula y aplicación en acrílico, gel o builder gel, cada paso con calma y atención al detalle." data-en="Filing, cuticle care and acrylic, gel or builder gel application, every step done calmly and with attention to detail.">Limado, cuidado de cutícula y aplicación en acrílico, gel o builder gel, cada paso con calma y atención al detalle.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">Sales lista</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus uñas listas, tal como cuentan sus reseñas: un trabajo excelente y con muy buena actitud." data-en="You leave with your nails finished, just as her reviews describe: excellent work with a great attitude.">Sales con tus uñas listas, tal como cuentan sus reseñas: un trabajo excelente y con muy buena actitud.</p>',
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
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Refill" data-en="Refill">Refill</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Builder Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Relleno de builder gel sobre uña natural: un acabado fuerte, prolijo y con brillo duradero." data-en="Builder gel refill over your natural nail: a strong, polished finish with long-lasting shine.">Relleno de builder gel sobre uña natural: un acabado fuerte, prolijo y con brillo duradero.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(103,74,160,0.4); box-shadow: 0 18px 50px rgba(38,34,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Favorito del salón</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Set Acrylic</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El set completo en acrílico, la base preferida en Soly Nails Miami para un acabado resistente y bien definido." data-en="The full acrylic set, the go-to base at Soly Nails Miami for a strong, well-defined finish.">El set completo en acrílico, la base preferida en Soly Nails Miami para un acabado resistente y bien definido.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure" data-en="Manicure">Manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure en gel con acabado brillante, parejo y de larga duración." data-en="Gel manicure with a glossy, even, long-lasting finish.">Manicure en gel con acabado brillante, parejo y de larga duración.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Nail Art" data-en="Nail Art">Nail Art</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Complex Nail Art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseños de nail art elaborados y hechos a mano, a tu gusto y con el detalle que pidas." data-en="Elaborate, hand-painted nail art designs made exactly to your taste.">Diseños de nail art elaborados y hechos a mano, a tu gusto y con el detalle que pidas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end():]

rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="diseño" data-en="design">diseño</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)

# ---------- 12. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: French $15 · Chrome / Effects $10 · Regular Pedicure $35 · Lash Lift $55 (50min) · Brow Lamination $55 (50min) · Removal (Acrílico/Gel/Soft Gel) $15. Además de uñas, en Soly Nails Miami también trabajan cejas y mirada. Precios exactos y disponibilidad en tiempo real en Booksy." data-en="Also on the menu: French $15 · Chrome / Effects $10 · Regular Pedicure $35 · Lash Lift $55 (50min) · Brow Lamination $55 (50min) · Removal (Acrylic/Gel/Soft Gel) $15. Beyond nails, Soly Nails Miami also does brows and eye treatments. Exact prices and real time availability on Booksy.">También en el menú: French $15 · Chrome / Effects $10 · Regular Pedicure $35 · Lash Lift $55 (50min) · Brow Lamination $55 (50min) · Removal (Acrílico/Gel/Soft Gel) $15. Además de uñas, en Soly Nails Miami también trabajan cejas y mirada. Precios exactos y disponibilidad en tiempo real en Booksy.</span></p>',
)

# ---------- 13. GALERIA ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Uñas</span> <span class="text-shine" data-es="reales" data-en="nails">reales</span></h2>',
)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="French con nail art negro" data-en="Black nail art french">French con nail art negro</span><img src="assets/raw/bk-10.jpg" alt="French con nail art negro hecho en Soly Nails Miami" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rojo con gema" data-en="Red with gem">Rojo con gema</span><img src="assets/raw/bk-4.jpg" alt="Nail art rojo con gema" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Blanco y rosa" data-en="White &amp; pink">Blanco y rosa</span><img src="assets/raw/bk-5.jpg" alt="Nail art blanco y rosa con gema" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="French floral pastel" data-en="Pastel floral french">French floral pastel</span><img src="assets/raw/bk-7.jpg" alt="French floral en tonos pastel" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Vino floral" data-en="Wine floral">Vino floral</span><img src="assets/raw/bk-14.jpg" alt="Nail art vino con detalle floral" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="French en V" data-en="V-cut french">French en V</span><img src="assets/raw/bk-15.jpg" alt="French en V" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 15. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 42 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 42 verified reviews on Booksy">5.0 de 5 · 42 reseñas verificadas en Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Espectacular, mi manicurista favorita."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">josnelbys b…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Trabaja excelente, además de la buena actitud que tiene."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Catalina c…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very skilled nail tech."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mariana Y…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 42 reseñas en Booksy" data-en="Read all 42 reviews on Booksy">Leer las 42 reseñas en Booksy</a>',
)

# ---------- 16. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">North Miami Beach</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(103,74,160,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">19377 NE 10th Ave, North Miami Beach, FL 33179</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(103,74,160,0.4)]" href="https://www.google.com/maps?q=19377+NE+10th+Ave,+North+Miami+Beach,+FL+33179" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto de martes a sábado, de 11:00 am a 7:00 pm." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Tuesday through Saturday, 11:00 am to 7:00 pm.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto de martes a sábado, de 11:00 am a 7:00 pm.</p>',
)

rep(
    'data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los diseños más recientes de Soly y escribe por DM cualquier duda antes de tu cita." data-en="See Soly\'s latest designs and DM any questions before your appointment.">Mira los diseños más recientes de Soly y escribe por DM cualquier duda antes de tu cita.</p>',
)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: {NAME}, 19377 NE 10th Ave, North Miami Beach FL"\n          src="https://www.google.com/maps?q=19377+NE+10th+Ave,+North+Miami+Beach,+FL+33179&output=embed"',
)

# ---------- 17. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tus uñas nuevas" data-en="Your next manicure">Tus uñas nuevas</span> <span class="text-shine" data-es="te están esperando" data-en="is waiting">te están esperando</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu full set acrílico, tu builder gel o el nail art que ya quieres probar." data-en="Book online in seconds: your acrylic full set, your builder gel refill, or the nail art you have been wanting to try.">Reserva online en segundos: tu full set acrílico, tu builder gel o el nail art que ya quieres probar.</p>',
)

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(205,190,240,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-4.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(205,190,240,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami, FL. Atención con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Salón de uñas en Miami, FL. Atención con cita previa.</p>',
)
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>19377 NE 10th Ave, North Miami Beach, FL 33179</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 19. Idioma: ES por defecto ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep(
    "applyLang(lang === 'es' ? 'es' : 'en');",
    "applyLang(lang === 'en' ? 'en' : 'es');",
)

open("output/solynailsmiami/index.html", "w").write(h)
print("BUILD OK: solynailsmiami")
