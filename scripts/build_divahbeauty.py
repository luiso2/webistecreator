import re

h = open("output/divahbeauty/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "DIVAH Beauty"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1421566_divah-beauty_brows-lashes_15889_miami"
IG_URL_OLD = "https://www.instagram.com/_lashbloom/"
IG_URL_NEW = "https://www.instagram.com/divahbeauty_/"
IG_AT_OLD = "@_lashbloom"
IG_AT_NEW = "@divahbeauty_"

# ---------- 1. HEAD ----------
rep(
    '<meta name="theme-color" content="#f6f1ea" />',
    '<meta name="theme-color" content="#f2faf9" />',
)
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Estudio de Pestañas y Cejas en Miami (Sweetwater), FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Sweetwater Miami FL: extensiones de pestañas clásicas, híbridas y volumen 5D, laminado de cejas y depilación facial con Diana. 5.0 perfecto en Booksy. Reserva en línea." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Pestañas y Cejas en Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Extensiones clásicas, híbridas, volumen 5D y laminado de cejas. 5.0 en Booksy. Reserva en línea." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-13.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

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
    "@type": "BeautySalon",
    "name": "{NAME}",
    "description": "Estudio de pestañas y cejas en Sweetwater, Miami, FL: extensiones clásicas, híbridas y volumen 5D, laminado de cejas y depilación facial.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "9600 SW 8th St, Suite 38", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33174", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.76065252428221, "longitude": -80.35147121136632 }},
    "sameAs": ["{BOOKSY_NEW}", "{IG_URL_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "20", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Friday", "Saturday"], "opens": "08:00", "closes": "20:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "19:00", "closes": "21:30" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Servicios de pestañas y cejas", "itemListElement": [
      {{ "@type": "Offer", "price": "110", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Classic Lash Extension" }} }},
      {{ "@type": "Offer", "price": "120", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Hybrid Lashes" }} }},
      {{ "@type": "Offer", "price": "140", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Volume 5D Full Set" }} }},
      {{ "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Brow Lamination" }} }}
    ] }}
  }}
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 2b. Reemplazo global de URLs/handles (Booksy, IG) ----------
assert h.count(BOOKSY_OLD) == 12, "conteo Booksy inesperado: " + str(h.count(BOOKSY_OLD))
h = h.replace(BOOKSY_OLD, BOOKSY_NEW)
assert h.count(IG_URL_OLD) == 5, "conteo IG url inesperado: " + str(h.count(IG_URL_OLD))
h = h.replace(IG_URL_OLD, IG_URL_NEW)
assert h.count(IG_AT_OLD) == 4, "conteo IG @ inesperado: " + str(h.count(IG_AT_OLD))
h = h.replace(IG_AT_OLD, IG_AT_NEW)

# ---------- 3. Preloader ----------
rep(
    '<span class="pre-mono">LB</span>\n    <span class="pre-word">Lash Bloom</span>',
    f'<span class="pre-mono">DB</span>\n    <span class="pre-word">{NAME}</span>',
)

# ---------- 4. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="DIVAH Beauty" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">DIVAH <span class="text-[color:var(--accent-deep)]">Beauty</span></span>',
)

# ---------- 5. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Sweetwater, Miami, FL · Pestañas y Cejas" data-en="Sweetwater, Miami, FL · Lash &amp; Brow Studio">Sweetwater, Miami, FL · Lash &amp; Brow Studio</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">\n          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>\n        </h1>',
    'data-es="Pestañas y cejas que te hacen sentir divah." data-en="Lashes and brows that make you feel like a diva.">Lashes and brows that make you feel like a diva.</p>\n        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">\n          <span data-es="Extensiones de pestañas" data-en="Lash extensions">Lash extensions</span><br /><span data-es="y cejas, hechas para " data-en="and brows, made to ">and brows, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>\n        </h1>',
    n=1,
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets completos clásicos, híbridos y volumen 5D, laminado de cejas y depilación facial, con Diana como tu artista de confianza en Sweetwater. Perfecto 5.0 en Booksy y clientas que regresan cita tras cita." data-en="Full classic, hybrid and 5D volume sets, brow lamination and facial waxing, with Diana as your trusted lash and brow artist in Sweetwater. A perfect 5.0 on Booksy and clients who keep coming back.">Full classic, hybrid and 5D volume sets, brow lamination and facial waxing, with Diana as your trusted lash and brow artist in Sweetwater. A perfect 5.0 on Booksy and clients who keep coming back.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 20 reseñas en Booksy" data-en="5.0 · 20 reviews on Booksy">5.0 · 20 reviews on Booksy</span>',
)
rep(
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>\n            <svg width="16" height="16"',
    '<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>\n            <svg width="16" height="16"',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-13.jpg" alt="Resultado de extensiones de pestañas volumen en DIVAH Beauty" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="font-display text-lg">Hybrid Lashes</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$120 · 1h 45min" data-en="$120 · 1h 45min">$120 · 1h 45min</p>',
)

# ---------- 6. STRIP ----------
rep(
    '<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="20">20</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
)
rep(
    '<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p>',
    '<p class="font-display text-2xl">Lashes <span class="text-shine">&amp;</span> Brows</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl text-shine">16</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicios en el menú" data-en="Services on the menu">Services on the menu</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Sweetwater, Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">9600 SW 8th St</p></div>',
)

# ---------- 7. MARQUEE (x2, 4 marquee-word usos por palabra) ----------
MARQUEE_WORDS = [
    ("Classic Set", "Classic Lashes"),
    ("Hybrid Set", "Hybrid Lashes"),
    ("Volume Set", "Soft Bloom YY"),
    ("Mega Volume", "Volume 5D"),
    ("Bottom Lashes", "Brow Lamination"),
    ("West Palm Beach, FL", "Sweetwater, Miami, FL"),
]
for old, new in MARQUEE_WORDS:
    old_tag = f'<span class="marquee-word">{old}</span>'
    new_tag = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_tag) == 4, f"marquee '{old}': conteo {h.count(old_tag)}"
    h = h.replace(old_tag, new_tag)

# ---------- 8. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Detalle de laminado de cejas en DIVAH Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Detalle de extensiones de pestañas aplicadas en DIVAH Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    'data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="La experiencia" data-en="The experience">La experiencia</p>',
)
rep(
    '<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio íntimo" data-en="An intimate studio">An intimate studio</span><br /><span class="text-shine" data-es="hecho para consentirte" data-en="made to pamper you">made to pamper you</span>',
)
rep(
    "data-es=\"Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad.\" data-en=\"Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.\">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>",
    "data-es=\"DIVAH Beauty es el estudio de Diana, en el suite 38 de la 9600 SW 8th St en Sweetwater. Sus clientas la describen como profesional, rápida y eficiente, en un ambiente limpio y agradable, con parking accesible.\" data-en=\"DIVAH Beauty is Diana's studio, at suite 38 on 9600 SW 8th St in Sweetwater. Her clients describe her as professional, quick and efficient, in a clean, pleasant space with accessible parking.\">DIVAH Beauty is Diana's studio, at suite 38 on 9600 SW 8th St in Sweetwater. Her clients describe her as professional, quick and efficient, in a clean, pleasant space with accessible parking.</p>",
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 20 reseñas verificadas en Booksy, y clientas que llevan años volviendo solo con Diana para sus cejas y pestañas." data-en="The result: a perfect 5.0 across 20 verified Booksy reviews, and clients who have kept coming back to Diana for years for their brows and lashes.">The result: a perfect 5.0 across 20 verified Booksy reviews, and clients who have kept coming back to Diana for years for their brows and lashes.</p>',
)
rep(
    '<p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<p class="font-display text-xl text-shine"><span data-count="20">20</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="DIVAH Beauty" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Diana · <span class="text-[color:var(--ink-40)]" data-es="Artista de pestañas y cejas" data-en="Lash &amp; brow artist">Lash &amp; brow artist</span></span>',
)

# ---------- 9. EL METODO ----------
rep(
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
)
rep(
    '<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio de pestañas o cejas en Booksy, con precio y duración claros, y confirmas al instante." data-en="Pick your lash or brow service on Booksy with clear price and duration, and confirm instantly.">Pick your lash or brow service on Booksy with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Diseño a tu medida" data-en="Your custom design">Your custom design</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Diana evalúa la forma de tu ojo o ceja natural para definir el estilo clásico, híbrido, volumen o laminado que más te favorece." data-en="Diana looks at your natural eye or brow shape to define the classic, hybrid, volume or lamination style that suits you best.">Diana looks at your natural eye or brow shape to define the classic, hybrid, volume or lamination style that suits you best.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Tiempo con Diana" data-en="Time with Diana">Time with Diana</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas y Diana aplica pestaña por pestaña o perfila tus cejas con calma, en un ambiente limpio y relajante." data-en="You lie back while Diana works lash by lash or shapes your brows at an unhurried pace, in a clean, relaxing space.">You lie back while Diana works lash by lash or shapes your brows at an unhurried pace, in a clean, relaxing space.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Tu plan de retoque" data-en="Your touch-up plan">Your touch-up plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno o retoque agendado para mantener la mirada perfecta semana tras semana." data-en="You leave with your fill or touch-up booked to keep your look perfect week after week.">You leave with your fill or touch-up booked to keep your look perfect week after week.</p>',
)

# ---------- 10. SERVICIOS ----------
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)
# Card 1: Classic
rep(
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto natural" data-en="Natural effect">Natural effect</p>\n          <h3 class="font-display text-2xl leading-snug mb-3">Classic Full Set</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una extensión por pestaña natural: el efecto limpio y elegante de todos los días. Rellenos de 2 semanas $70 y de 3 semanas $80." data-en="One extension per natural lash: the clean, elegant everyday effect. 2-week fills $70 and 3-week fills $80.">One extension per natural lash: the clean, elegant everyday effect. 2-week fills $70 and 3-week fills $80.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$130</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto natural" data-en="Natural effect">Natural effect</p>\n          <h3 class="font-display text-2xl leading-snug mb-3">Classic Lash Extension</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una extensión por pestaña natural: el efecto limpio y elegante de todos los días. Relleno clásico desde $60." data-en="One extension per natural lash: the clean, elegant everyday effect. Classic refill from $60.">One extension per natural lash: the clean, elegant everyday effect. Classic refill from $60.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$110</p></div>',
)
# Card 2: Hybrid (destacada)
rep(
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>\n          <h3 class="font-display text-2xl leading-snug mb-3">Hybrid Full Set</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La mezcla perfecta entre clásico y volumen: textura wispy con cuerpo. Rellenos de 2 semanas $80 y de 3 semanas $90." data-en="The perfect mix of classic and volume: wispy texture with body. 2-week fills $80 and 3-week fills $90.">The perfect mix of classic and volume: wispy texture with body. 2-week fills $80 and 3-week fills $90.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$145</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 50min</p></div>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>\n          <h3 class="font-display text-2xl leading-snug mb-3">Hybrid Lashes</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La mezcla perfecta entre clásico y volumen: textura wispy con cuerpo, también disponible como Soft Bloom YY." data-en="The perfect mix of classic and volume: wispy texture with body, also available as the Soft Bloom YY set.">The perfect mix of classic and volume: wispy texture with body, also available as the Soft Bloom YY set.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$120</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>',
)
# Card 3: Volume
rep(
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Maximo impacto" data-en="Maximum impact">Maximum impact</p>\n          <h3 class="font-display text-2xl leading-snug mb-3">Volume &amp; Mega</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Abanicos hechos a mano para densidad total: Volume full set $155 y rellenos volume $90-$105 o mega volume $100." data-en="Handmade fans for full density: Volume full set $155 with volume fills $90-$105 or mega volume fills $100.">Handmade fans for full density: Volume full set $155 with volume fills $90-$105 or mega volume fills $100.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$155</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 50min</p></div>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Maximo impacto" data-en="Maximum impact">Maximum impact</p>\n          <h3 class="font-display text-2xl leading-snug mb-3">Volume 5D Full Set</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Abanicos 5D hechos a mano para densidad total. Relleno volume 5D desde $70. También disponible el Light Volume por $130." data-en="Handmade 5D fans for full density. Volume 5D refill from $70. Light Volume also available for $130.">Handmade 5D fans for full density. Volume 5D refill from $70. Light Volume also available for $130.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$140</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>',
)
# Card 4: Brows/Extras
rep(
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especiales" data-en="Specials">Specials</p>\n          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Special &amp; Extras" data-en="Special &amp; Extras">Special &amp; Extras</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El especial classic/hybrid/volume por $120, y bottom lashes por $25 para completar la mirada." data-en="The classic/hybrid/volume special at $120, plus bottom lashes for $25 to complete the look.">The classic/hybrid/volume special at $120, plus bottom lashes for $25 to complete the look.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$120</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 40min</p></div>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas" data-en="Brows">Brows</p>\n          <h3 class="font-display text-2xl leading-snug mb-3">Brow Lamination</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas peinadas y definidas por semanas. También ofrecemos brow design wax por $20 y depilación facial desde $10." data-en="Brushed-up, defined brows for weeks. Brow design wax also available for $20, plus facial waxing from $10.">Brushed-up, defined brows for weeks. Brow design wax also available for $20, plus facial waxing from $10.</p>\n          <div class="mt-auto">\n            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>',
)
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="16 servicios en el menú, incluyendo rellenos, lash removal y depilación facial. Menú completo y disponibilidad en Booksy." data-en="16 services on the menu, including refills, lash removal and facial waxing. Full menu and availability on Booksy.">16 services on the menu, including refills, lash removal and facial waxing. Full menu and availability on Booksy.</span></p>',
)

# ---------- 13. GALERIA ----------
rep(
    '<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Miradas" data-en="Real">Miradas</span> <span class="text-shine" data-es="reales" data-en="results">reales</span>',
)
rep(
    '<div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Clienta feliz, set nuevo" data-en="Fresh set, happy client">Fresh set, happy client</span><img src="assets/raw/bk-6.jpg" alt="Clienta sonriendo con su set de pestañas nuevo en Lash Bloom" class="blur-up w-full h-full object-cover" /></div>',
    '<div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Resultado de pestañas" data-en="Lash result">Resultado de pestañas</span><img src="assets/raw/bk-11.jpg" alt="Resultado de extensiones de pestañas en DIVAH Beauty" class="blur-up w-full h-full object-cover" /></div>',
)
rep(
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Volumen wispy" data-en="Wispy volume">Wispy volume</span><img src="assets/raw/bk-12.jpg" alt="Closeup de pestanas de volumen wispy" class="blur-up w-full h-full object-cover" /></div>',
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Volumen dramático" data-en="Dramatic volume">Volumen dramático</span><img src="assets/raw/bk-6.jpg" alt="Closeup de pestanas de volumen dramatico" class="blur-up w-full h-full object-cover" /></div>',
)
rep(
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cejas + pestañas" data-en="Brows + lashes">Brows + lashes</span><img src="assets/raw/gallery-7.jpg" alt="Ceja perfilada con pestanas de volumen" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cejas + pestañas" data-en="Brows + lashes">Cejas + pestañas</span><img src="assets/raw/bk-7.jpg" alt="Ceja y pestanas combinadas en DIVAH Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
)
rep(
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Resultado natural" data-en="Natural result">Natural result</span><img src="assets/raw/gallery-2.jpg" alt="Clienta con resultado natural de pestanas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Laminado de cejas" data-en="Brow lamination">Laminado de cejas</span><img src="assets/raw/bk-14.jpg" alt="Resultado de laminado de cejas en DIVAH Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
)
rep(
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Set clásico" data-en="Classic set">Classic set</span><img src="assets/raw/bk-10.jpg" alt="Set clasico de pestanas en camilla rosa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Mirada natural" data-en="Natural look">Mirada natural</span><img src="assets/raw/bk-3.jpg" alt="Mirada natural con extensiones de pestanas en DIVAH Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
)
rep(
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Híbrido con brillo" data-en="Glowy hybrid">Glowy hybrid</span><img src="assets/raw/bk-3.jpg" alt="Clienta con set hibrido de pestanas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Detalle de aplicación" data-en="Application detail">Detalle de aplicación</span><img src="assets/raw/bk-15.jpg" alt="Detalle de aplicacion de pestanas y cejas en DIVAH Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
)

# ---------- 15. OPINIONES ----------
rep(
    'data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    'data-es="5.0 de 5 · 20 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 20 verified reviews on Booksy">5.0 out of 5 · 20 verified reviews on Booksy</span>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encantó la experiencia me dejaron hermosísima amé mis cejitas 🥰🥰 y la atención 10 de 10 😘😘😘"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Abigail B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Gracias Dianita por dejarme siempre hermosas y cuidadas mis pestañitas y cejas !!!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Diannelis P.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Recomendada! Desde que estoy en Miami solo me hago las cejas aquí 🙏🏼 excelente servicio"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Karitzamar B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
)
rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 20 reseñas en Booksy" data-en="Read all 20 reviews on Booksy">Read all 20 reviews on Booksy</a>',
)

# ---------- 16. UBICACION ----------
rep(
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Sweetwater</span>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">9600 SW 8th St, Suite 38, Miami, FL 33174</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=9600+SW+8th+St,+Suite+38,+Miami,+FL+33174" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
)
rep(
    'data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los sets más recientes de Diana y escribe por DM cualquier duda antes de tu cita." data-en="See Diana\'s latest sets and DM any questions before your appointment.">See Diana\'s latest sets and DM any questions before your appointment.</p>',
)
rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: {NAME}, 9600 SW 8th St, Suite 38, Miami FL"\n          src="https://www.google.com/maps?q=9600+SW+8th+St,+Suite+38,+Miami,+FL+33174&output=embed"',
)

# ---------- 17. CTA FINAL ----------
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    'data-es="Pestañas y cejas que te hacen sentir divah." data-en="Lashes and brows that make you feel like a diva.">Lashes and brows that make you feel like a diva.</p>\n      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu nueva mirada" data-en="Your new look">Your new look</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen 5D, tu laminado de cejas, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or 5D volume set, your brow lamination, or the fill you are due for.">Book online in seconds: your classic, hybrid or 5D volume set, your brow lamination, or the fill you are due for.</p>',
)

# ---------- 18. FOOTER ----------
rep(
    '<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    f'<span class="foot-mark" aria-hidden="true">{NAME}</span>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-2.jpg" alt="DIVAH Beauty" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de pestañas y cejas en Sweetwater, Miami, FL. Atención con cita previa." data-en="Lash &amp; brow studio in Sweetwater, Miami, FL. By appointment only.">Lash &amp; brow studio in Sweetwater, Miami, FL. By appointment only.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>9600 SW 8th St, Suite 38, Miami, FL 33174</p>',
)
rep(
    '<p><a href="https://www.instagram.com/divahbeauty_/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @divahbeauty_</a></p>',
    '<p><a href="https://www.instagram.com/divahbeauty_/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @divahbeauty_</a></p>',
)
rep(
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>',
)

# ---------- 19. Paleta: plum-pink -> teal esmeralda (rotacion de matiz, luminancia/saturacion preservadas) ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

HEX_MAP = {
    "a04a72": "4aa09a",  # accent-deep
    "c47a9c": "7ac4bf",  # accent-mid
    "f3e0ea": "e0f3f2",  # bg-2 / accent-soft
    "faf2f6": "f2faf9",  # bg
    "f0bed7": "bef0ed",  # dark-band text-shine/stars/hover accent
    "8a5573": "558a86",  # dark-band btn-3d shadow (medium)
    "d9a8c2": "a8d9d6",  # orb-b light tint
    "7d3457": "347d78",  # btn-3d gradient dark stop / scroll-progress start
    "5f2c48": "2c5f5c",  # text-shine dark stop / step-num dark stop
    "33222c": "223332",  # ink
    "fbf3f8": "f3fbfa",  # tile-cap text
    "fbeff5": "effbfa",  # dark-band btn-3d top stop
    "f8dfeb": "dff8f6",  # dark-band text-shine 2nd stop
    "f2d5e3": "d5f2f0",  # orb-a light tint
    "f2cfe0": "cff2f0",  # dark-band text-shine last stop
    "efd0e0": "d0efed",  # dark-band btn-3d mid stop
    "e5c1d4": "c1e5e3",  # orb-c light tint
    "dc9dbe": "9ddcd8",  # scroll-progress last stop
    "d3a2bc": "a2d3d0",  # dark-band btn-3d bottom stop
    "c9789f": "78c9c4",  # text-shine 2nd stop
    "b25a85": "5ab2ac",  # text-shine last stop
    "5c2140": "215c58",  # btn-3d / book-float shadow border (light theme)
    "2a1722": "172a29",  # cta-final dark-band bg start
    "1f0f18": "0f1f1e",  # cta-final dark-band bg end
    "1c0f16": "0f1c1b",  # footer dark-band bg
    "f4eee2": "f0f9f8",  # footer credit text (light teal-white tint)
}
for old, new in HEX_MAP.items():
    assert old in h, f"paleta: no se encontro hex #{old}"
    h = h.replace(f"#{old}", f"#{new}")

RGB_TRIPLE_MAP = [
    ((160, 74, 114), (74, 160, 154)),
    ((70, 25, 50), (25, 70, 67)),
    ((51, 34, 44), (34, 51, 50)),
    ((125, 52, 87), (52, 125, 120)),
    ((240, 190, 215), (190, 240, 237)),
    ((233, 205, 186), (186, 233, 230)),
    ((185, 138, 128), (128, 185, 181)),
    ((253, 246, 250), (246, 253, 253)),
    ((250, 242, 246), (242, 250, 249)),
    ((40, 16, 30), (16, 40, 38)),
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

# ---------- 20. Idioma principal: ES ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep(
    "let lang = localStorage.getItem('lang') || (navigator.language || 'es').slice(0, 2);\n    applyLang(lang === 'es' ? 'es' : 'en');",
    "let lang = localStorage.getItem('lang') || (navigator.language || 'es').slice(0, 2);\n    applyLang(lang === 'en' ? 'en' : 'es');",
)

open("output/divahbeauty/index.html", "w").write(h)
print("BUILD OK: divahbeauty")
