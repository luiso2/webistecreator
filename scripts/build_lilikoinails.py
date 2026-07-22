import re

h = open("output/lilikoinails/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Lilikoi Nail Salon"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/797812_lilikoi-nail-salon-unas-miami_nail-salon_15889_miami"
IG_URL_OLD = "https://www.instagram.com/_lashbloom/"
IG_URL_NEW = "https://www.instagram.com/lilikoi_nail_studio/"
IG_AT_OLD = "@_lashbloom"
IG_AT_NEW = "@lilikoi_nail_studio"

# ---------- 1. HEAD ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Nail Salon in Miami, FL | 5.0 on Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Miami FL: manicure, Russian manicure, combi gel, apres and nail art with a perfect 5.0 across 75 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Nail Salon in Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure, Russian manicure, combi gel and nail art. 5.0 on Booksy. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-7.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-7.jpg" />')

# ---------- 2. JSON-LD ----------
m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, "no se encontro JSON-LD"

NEW_LD = f"""<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "{NAME}",
    "description": "Nail salon in Miami, FL: classic manicure, Russian manicure, combi gel, apres and hand painted nail art.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "8762 W Flagler St, Suite 1", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33174", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.7693191, "longitude": -80.338485 }},
    "sameAs": ["{BOOKSY_NEW}", "{IG_URL_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "75", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Friday"], "opens": "10:00", "closes": "18:30" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Thursday"], "opens": "10:00", "closes": "19:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "13:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      {{ "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Manicure Luminary" }} }},
      {{ "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Russian Manicure" }} }},
      {{ "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Combi Gel Manicure" }} }},
      {{ "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Apres" }} }},
      {{ "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Classic (Regular) Pedicure" }} }},
      {{ "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Combi Gel Pedicure" }} }},
      {{ "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Designed/Decoration" }} }},
      {{ "@type": "Offer", "price": "10", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Manicure Una Uña" }} }}
    ] }}
  }}
  </script>"""

h = h[: m.start()] + NEW_LD + h[m.end():]

repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_URL_OLD, IG_URL_NEW)
repall(IG_AT_OLD, IG_AT_NEW)

# ---------- 3. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LN</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 4. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,146,160,0.35)]" />',
    f'<img src="assets/raw/bk-14.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,146,160,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lilikoi <span class="text-[color:var(--accent-deep)]">Nail Salon</span></span>',
)

# ---------- 5. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Salón de Uñas" data-en="Miami, FL · Nail Salon">Miami, FL · Salón de Uñas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Un toque tropical en cada uña." data-en="A tropical touch on every nail.">Un toque tropical en cada uña.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicure de precisión," data-en="Precision manicures,">Manicure de precisión,</span><br /><span data-es="pedicura y nail art, para " data-en="pedicure and nail art, made to ">pedicura y nail art, para </span><span class="text-shine" data-es="brillar" data-en="shine">brillar</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicure clásica, manicure rusa, combi gel, apres y nail art hechos a mano por Lilibet Ruiz Páez en su salón de la calle Flagler en Miami. Un 5.0 perfecto en 75 reseñas verificadas en Booksy." data-en="Classic manicures, Russian manicure, combi gel, apres and hand painted nail art by Lilibet Ruiz Páez at her salon on Flagler Street in Miami. A perfect 5.0 across 75 verified Booksy reviews.">Classic manicures, Russian manicure, combi gel, apres and hand painted nail art by Lilibet Ruiz Páez at her salon on Flagler Street in Miami. A perfect 5.0 across 75 verified Booksy reviews.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 75 reseñas en Booksy" data-en="5.0 · 75 reviews on Booksy">5.0 · 75 reseñas en Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-7.jpg" alt="Manicure ombré negro y plata en uñas stiletto" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Russian Manicure</p>')
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$80" data-en="$80">$80</p>',
)

# ---------- 6. STRIP ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="75">75</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicure <span class="text-shine">&amp;</span> Pedicura</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicios completos" data-en="Full services">Servicios completos</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Manicure <span class="text-shine" data-es="Rusa" data-en="Russian">Rusa</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Técnica de precisión" data-en="Precision technique">Técnica de precisión</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">8762 W Flagler St</p></div>',
)

# ---------- 7. MARQUEE ----------
MQ = [
    ("Classic Set", "Manicure Luminary"),
    ("Hybrid Set", "Russian Manicure"),
    ("Volume Set", "Combi Gel"),
    ("Mega Volume", "Apres"),
    ("Bottom Lashes", "Nail Art"),
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
    '<img src="assets/raw/bk-1.jpg" alt="Vista real del interior del salón Lilikoi Nail Salon" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Manicure en uñas azul marino almendra con acabado elegante" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un salón cercano" data-en="A neighborhood salon">Un salón cercano</span><br /><span class="text-shine" data-es="hecho para cuidarte" data-en="made to pamper you">hecho para cuidarte</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    f'data-es="{NAME} es el salón de Lilibet Ruiz Páez en la calle Flagler de Miami. Cada cita se piensa contigo: manicure clásica, manicure rusa, combi gel, apres o un diseño de nail art hecho a mano, con calma y atención al detalle." data-en="{NAME} is Lilibet Ruiz Páez\'s salon on Flagler Street in Miami. Every visit is planned around you: classic manicure, Russian manicure, combi gel, apres or a hand painted nail art design, done calmly and with attention to detail.">{NAME} is Lilibet Ruiz Páez\'s salon on Flagler Street in Miami. Every visit is planned around you: classic manicure, Russian manicure, combi gel, apres or a hand painted nail art design, done calmly and with attention to detail.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 75 reseñas verificadas en Booksy, y clientas que describen su trabajo como impecable y profesional." data-en="The result: a perfect 5.0 across 75 verified reviews on Booksy, and clients who describe her work as flawless and professional.">The result: a perfect 5.0 across 75 verified reviews on Booksy, and clients who describe her work as flawless and professional.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="75">75</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,146,160,0.3)]" loading="lazy" />',
    f'<img src="assets/raw/bk-14.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,146,160,0.3)]" loading="lazy" />',
)
rep(
    '<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Lilibet Ruiz Páez · <span class="text-[color:var(--ink-40)]" data-es="Especialista en uñas" data-en="Nail specialist">Especialista en uñas</span></span>',
)

# ---------- 9. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, uña" data-en="Your visit, nail">Tu cita, uña</span> <span class="text-shine" data-es="por uña" data-en="by nail">por uña</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy, manicure, pedicura o nail art, con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy, manicure, pedicure or nail art, with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy, manicure, pedicura o nail art, con precio y duración claros, y confirmas al instante.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Elige tu estilo" data-en="Choose your style">Elige tu estilo</h3>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma, largo y color: manicure clásica, manicure rusa, combi gel o un diseño de nail art, tú decides el estilo." data-en="Shape, length and color: classic manicure, Russian manicure, combi gel or a nail art design, you choose the style.">Forma, largo y color: manicure clásica, manicure rusa, combi gel o un diseño de nail art, tú decides el estilo.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos al detalle" data-en="Hands, detailed">Manos al detalle</h3>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cuidado de cutícula y la técnica que elegiste, aplicada con calma y precisión, uña por uña." data-en="Filing, cuticle care and the technique you picked, applied calmly and with precision, nail by nail.">Limado, cuidado de cutícula y la técnica que elegiste, aplicada con calma y precisión, uña por uña.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">Sales lista</h3>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus uñas listas, tal como cuentan sus reseñas: un acabado impecable y profesional." data-en="You leave with your nails done, just as her reviews describe: a flawless, professional finish.">Sales con tus uñas listas, tal como cuentan sus reseñas: un acabado impecable y profesional.</p>',
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
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure Luminary</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema luminary en tus manos, con acabado brillante y resistente que dura semanas." data-en="The luminary system on your hands, with a glossy, long-lasting finish that lasts for weeks.">El sistema luminary en tus manos, con acabado brillante y resistente que dura semanas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(74,146,160,0.4); box-shadow: 0 18px 50px rgba(34,50,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Favorito del salón</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Russian Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La técnica de precisión más pedida: cutícula perfecta y un acabado impecable que dura más." data-en="The most requested precision technique: perfect cuticle work and a flawless finish that lasts longer.">La técnica de precisión más pedida: cutícula perfecta y un acabado impecable que dura más.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Gel" data-en="Gel">Gel</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Combi Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure combinada con esmaltado en gel: color intenso y brillo que se mantiene." data-en="Manicure combined with gel polish: intense color and shine that lasts.">Manicure combinada con esmaltado en gel: color intenso y brillo que se mantiene.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extensión" data-en="Extension">Extensión</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Apres</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensión en gel-x de apariencia natural, ligera y con gran resistencia día a día." data-en="A gel-x extension with a natural look, lightweight and highly resistant for everyday wear.">Extensión en gel-x de apariencia natural, ligera y con gran resistencia día a día.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end():]

rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)

# ---------- 11. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: Pedicura clásica $40 (30min) · Combi Gel Pedicure $50 · Diseño/Decoración $15 (20min) · Manicure de una uña $10 (15min). Precios exactos y disponibilidad en tiempo real en Booksy." data-en="Also on the menu: Classic Pedicure $40 (30min), Combi Gel Pedicure $50, Design/Decoration $15 (20min), Single nail manicure $10 (15min). Exact prices and real time availability on Booksy.">También en el menú: Pedicura clásica $40 (30min) · Combi Gel Pedicure $50 · Diseño/Decoración $15 (20min) · Manicure de una uña $10 (15min). Precios exactos y disponibilidad en tiempo real en Booksy.</span></p>',
)

# ---------- 12. GALERIA ----------
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Ombré negro y plata" data-en="Black and silver ombre">Ombré negro y plata</span><img src="assets/raw/bk-7.jpg" alt="Manicure ombré negro y plata en uñas stiletto" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Nude brillante" data-en="Glossy nude">Nude brillante</span><img src="assets/raw/bk-3.jpg" alt="Manicure nude con acabado brillante" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Nail art con gema" data-en="Nail art with gem">Nail art con gema</span><img src="assets/raw/bk-8.jpg" alt="Nail art color vino con gema decorativa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Nude clásico" data-en="Classic nude">Nude clásico</span><img src="assets/raw/bk-11.jpg" alt="Manicure nude clásico en uñas cortas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Nude natural" data-en="Natural nude">Nude natural</span><img src="assets/raw/bk-12.jpg" alt="Manicure nude con acabado natural" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="French en V" data-en="V-tip french">French en V</span><img src="assets/raw/bk-15.jpg" alt="Diseño french nude en V sobre uñas almendradas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 13. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 75 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 75 verified reviews on Booksy">5.0 de 5 · 75 reseñas verificadas en Booksy</span>',
)

OLD_REVIEWS = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10 reveal">)',
    h,
    flags=re.S,
)
assert OLD_REVIEWS, "no se encontro grid de opiniones"

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor experiencia y atención que he recibido en mucho tiempo. Un excelente servicio y profesionalidad."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yenisel F…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very professional!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maria S…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Muy bien, me gusto."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Miry M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""

h = h[: OLD_REVIEWS.start()] + NEW_REVIEWS + h[OLD_REVIEWS.end():]

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 75 reseñas en Booksy" data-en="Read all 75 reviews on Booksy">Leer las 75 reseñas en Booksy</a>',
)

# ---------- 14. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Miami, FL</span></h2>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">8762 W Flagler St, Suite 1, Miami, FL 33174</p>',
)
rep(
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,146,160,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,146,160,0.4)]" href="https://www.google.com/maps?q=8762+W+Flagler+St,+Miami,+FL+33174" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto lunes, martes y viernes de 10:00 am a 6:30 pm, miércoles y jueves de 10:00 am a 7:00 pm, y sábado de 10:00 am a 1:00 pm." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Monday, Tuesday and Friday 10:00 am to 6:30 pm, Wednesday and Thursday 10:00 am to 7:00 pm, and Saturday 10:00 am to 1:00 pm.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto lunes, martes y viernes de 10:00 am a 6:30 pm, miércoles y jueves de 10:00 am a 7:00 pm, y sábado de 10:00 am a 1:00 pm.</p>',
)
rep(
    'data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los diseños más recientes de Lilibet y escribe por DM cualquier duda antes de tu cita." data-en="See Lilibet\'s latest designs and DM any questions before your appointment.">Mira los diseños más recientes de Lilibet y escribe por DM cualquier duda antes de tu cita.</p>',
)
rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: {NAME}, 8762 W Flagler St, Miami FL"\n          src="https://www.google.com/maps?q=8762+W+Flagler+St,+Miami,+FL+33174&output=embed"',
)

# ---------- 15. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tus uñas nuevas" data-en="Your new nails">Tus uñas nuevas</span> <span class="text-shine" data-es="te están esperando" data-en="are waiting">te están esperando</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure clásica, rusa, combi gel o el nail art que ya te toca." data-en="Book online in seconds: your classic, Russian or combi gel manicure, or the nail art you are due for.">Reserva online en segundos: tu manicure clásica, rusa, combi gel o el nail art que ya te toca.</p>',
)

# ---------- 16. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,233,240,0.35)]" loading="lazy" />',
    f'<img src="assets/raw/bk-14.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />',
)
rep(
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami, FL. Atención con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Salón de uñas en Miami, FL. Atención con cita previa.</p>',
)
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>8762 W Flagler St, Suite 1, Miami, FL 33174</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 17. Idioma ES por defecto ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

open("output/lilikoinails/index.html", "w").write(h)
print("BUILD OK: lilikoinails")
