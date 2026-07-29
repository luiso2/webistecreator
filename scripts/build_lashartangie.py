import re

h = open("output/lash-art-by-angie-miami/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "The Lash Art by Angie"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1787126_the-lash-art-by-angie_brows-lashes_15889_miami"
IG_URL_OLD = "https://www.instagram.com/_lashbloom/"
IG_URL_NEW = "https://www.instagram.com/lashart_angie/"
IG_AT_OLD = "@_lashbloom"
IG_AT_NEW = "@lashart_angie"

# ---------- 1. HEAD ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Lash Studio in Miami, FL | 5.0 on Booksy</title>",
)
rep('<meta name="theme-color" content="#f6f1ea" />', '<meta name="theme-color" content="#f2f5ee" />')
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Miami FL: classic, hybrid, volume and wet set lash extensions plus lash lifts and brow lamination, with a perfect 5.0 across 24 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Lash Studio in Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Classic, hybrid, volume and wet set lashes. 5.0 on Booksy. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-4.jpg" />')
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
    "@type": "HealthAndBeautyBusiness",
    "name": "{NAME}",
    "description": "Lash studio in Miami, FL: classic, hybrid, volume and wet set eyelash extensions, lash lifts, brow lamination and threading.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "15140 SW 72nd St, Suite 9", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33193", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.6985028, "longitude": -80.4373558 }},
    "sameAs": ["{BOOKSY_NEW}", "{IG_URL_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "24", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "07:00", "closes": "18:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday"], "opens": "07:00", "closes": "17:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:00", "closes": "16:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Lash services", "itemListElement": [
      {{ "@type": "Offer", "price": "110", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Classic full set" }} }},
      {{ "@type": "Offer", "price": "140", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Hybrid full set" }} }},
      {{ "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Volume full set" }} }},
      {{ "@type": "Offer", "price": "110", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Lash Lift Koreano + Tinting" }} }}
    ] }}
  }}
  </script>"""
rep(OLD_LD, NEW_LD)

repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_URL_OLD, IG_URL_NEW)
repall(IG_AT_OLD, IG_AT_NEW)

# ---------- 3. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LA</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 4. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    f'<img src="assets/raw/bk-13.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash Art <span class="text-[color:var(--accent-deep)]">by Angie</span></span>',
)

# ---------- 5. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Estudio de Pestañas" data-en="Miami, FL · Lash Studio">Miami, FL · Lash Studio</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="El arte de tu mirada." data-en="The art of your gaze.">The art of your gaze.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y wet set, hechas para " data-en="and wet set lashes, made to ">and wet set lashes, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    f'data-es="Sets completos clásicos, híbridos, volumen y wet set, además de lash lift y laminado de cejas, hechos a mano por Angela Noguera en Miami. Un 5.0 perfecto en 24 reseñas de Booksy, y clientas que dicen que su trabajo siempre queda impecable." data-en="Full classic, hybrid, volume and wet set lashes, plus lash lifts and brow lamination, done by hand by Angela Noguera in Miami. A perfect 5.0 across 24 Booksy reviews, and clients who say her work is always flawless.">Full classic, hybrid, volume and wet set lashes, plus lash lifts and brow lamination, done by hand by Angela Noguera in Miami. A perfect 5.0 across 24 Booksy reviews, and clients who say her work is always flawless.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 24 reseñas en Booksy" data-en="5.0 · 24 reviews on Booksy">5.0 · 24 reviews on Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-4.jpg" alt="Closeup of full volume lash extensions on an open eye" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Hybrid Full Set</p>')
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$140 · 1h 45min" data-en="$140 · 1h 45min">$140 · 1h 45min</p>',
)

# ---------- 6. STRIP ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="24">24</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Lashes <span class="text-shine">&amp;</span> Brows</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets · Lash lift · Laminado" data-en="Sets · Lash lift · Lamination">Sets · Lash lift · Lamination</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">We speak</span> <span class="text-shine" data-es="Español" data-en="Spanish">Spanish</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Warm, personal care</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">15140 SW 72nd St</p></div>',
)

# ---------- 7. MARQUEE ----------
MQ = [
    ("Classic Set", "Classic Set"),
    ("Hybrid Set", "Hybrid Set"),
    ("Volume Set", "Volume Set"),
    ("Mega Volume", "Wet Set"),
    ("Bottom Lashes", "Lash Lift"),
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
    '<img src="assets/raw/bk-1.jpg" alt="Closeup of natural-effect lash extensions" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Client smiling after a brow and lash appointment" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="atencion al detalle" data-en="obsessed with detail">obsessed with detail</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    f'data-es="{NAME} es el estudio de Angela Noguera en Miami. Cada set se disena sobre tu ojo, pestana por pestana, con la atencion al detalle que sus clientas describen una y otra vez en sus resenas." data-en="{NAME} is Angela Noguera\'s studio in Miami. Every set is designed around your eye, lash by lash, with the attention to detail her clients describe again and again in their reviews.">{NAME} is Angela Noguera\'s studio in Miami. Every set is designed around your eye, lash by lash, with the attention to detail her clients describe again and again in their reviews.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 24 reseñas verificadas en Booksy, y clientas que dicen sentirse especiales cada vez que se sientan en su silla." data-en="The result: a perfect 5.0 across 24 verified reviews on Booksy, and clients who say they feel special every time they sit in her chair.">The result: a perfect 5.0 across 24 verified reviews on Booksy, and clients who say they feel special every time they sit in her chair.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="24">24</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    f'<img src="assets/raw/bk-13.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Angela Noguera · <span class="text-[color:var(--ink-40)]" data-es="Artista de pestañas" data-en="Lash artist">Lash artist</span></span>',
)

# ---------- 9. EL METODO ----------
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu set, lash lift o servicio de cejas en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set, lash lift or brow service on Booksy with clear price and duration, and confirm instantly.">Pick your set, lash lift or brow service on Booksy with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido, volumen o wet set." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid, volume or wet set design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid, volume or wet set design comes from.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación tranquila" data-en="Unhurried application">Unhurried application</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Angie hace lo suyo: hasta 1h 45min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Angie does her thing: up to 1h 45min of unhurried, lash-by-lash application.">You lie back, close your eyes and Angie does her thing: up to 1h 45min of unhurried, lash-by-lash application.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu proximo relleno agendado y tus pestanas o cejas listas para durar semanas." data-en="You leave with your next fill booked and your lashes or brows ready to last for weeks.">You leave with your next fill booked and your lashes or brows ready to last for weeks.</p>',
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
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto natural" data-en="Natural effect">Natural effect</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Classic Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una extension por pestana natural para un efecto limpio de todos los dias. Relleno clasico $70." data-en="One extension per natural lash for a clean, everyday effect. Classic refill $70.">One extension per natural lash for a clean, everyday effect. Classic refill $70.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$110</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Hybrid Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La mezcla perfecta entre clasico y volumen, con textura wispy. Relleno hibrido $80." data-en="The perfect mix of classic and volume, with wispy texture. Hybrid refill $80.">The perfect mix of classic and volume, with wispy texture. Hybrid refill $80.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$140</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Maximo impacto" data-en="Maximum impact">Maximum impact</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Volume Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Abanicos hechos a mano para densidad total. Tambien: Wet Set Full Set $130. Relleno volumen $90." data-en="Handmade fans for full density. Also: Wet Set Full Set $130. Volume refill $90.">Handmade fans for full density. Also: Wet Set Full Set $130. Volume refill $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$150</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas y pestanas" data-en="Brows &amp; lashes">Brows &amp; lashes</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Lash Lift Koreano + Tinting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Levantamiento coreano con tinte para pestanas naturales con mas curva. Tambien: Brow Lamination $80 y Henna Brows $25." data-en="Korean-style lash lift with tint for natural lashes with more curl. Also: Brow Lamination $80 and Henna Brows $25.">Korean-style lash lift with tint for natural lashes with more curl. Also: Brow Lamination $80 and Henna Brows $25.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$110</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end():]

rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.</p>',
)

rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: Lash Lift tradicional $80 · Eyebrow waxing/threading $25 · Lip wax $15. Precios exactos y disponibilidad en tiempo real en Booksy." data-en="Also on the menu: Traditional lash lift $80 · Eyebrow waxing/threading $25 · Lip wax $15. Exact prices and real time availability on Booksy.">Also on the menu: Traditional lash lift $80 · Eyebrow waxing/threading $25 · Lip wax $15. Exact prices and real time availability on Booksy.</span></p>',
)

# ---------- 13. GALERIA ----------
OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Mirada terminada" data-en="Finished look">Finished look</span><img src="assets/raw/bk-9.jpg" alt="Portrait with full lash extensions and defined brows" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Volumen natural" data-en="Natural volume">Natural volume</span><img src="assets/raw/bk-3.jpg" alt="Closeup of volume lash extensions on an open eye" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Perfil de cejas" data-en="Brow profile">Brow profile</span><img src="assets/raw/bk-7.jpg" alt="Side profile closeup of shaped brows and lashes" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Detalle macro" data-en="Macro detail">Macro detail</span><img src="assets/raw/bk-8.jpg" alt="Macro detail of lash extensions with a mirror reflection" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 15. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 24 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 24 verified reviews on Booksy">5.0 out of 5 · 24 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Angie is wonderful! She always makes me feel special and I love how my eyelashes look." (Translated from Spanish)</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Vivian T…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"It was a divine experience, Angela is very professional, for me she exceeded all expectations." (Translated from Spanish)</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yudiesky G…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Angela is the best! She's so sweet, pays amazing attention to detail, and her lash work is always flawless. She also does eyebrow threading and she's amazing at it!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Katia P…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 24 reseñas en Booksy" data-en="Read all 24 reviews on Booksy">Read all 24 reviews on Booksy</a>',
)

# ---------- 16. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami, FL</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">15140 SW 72nd St, Suite 9, Miami, FL 33193</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=15140+SW+72nd+St,+Miami,+FL+33193" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto martes a jueves de 7:00 am a 6:00 pm, viernes de 7:00 am a 5:00 pm, y sábado de 8:00 am a 4:00 pm." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Tuesday through Thursday 7:00 am to 6:00 pm, Friday 7:00 am to 5:00 pm, and Saturday 8:00 am to 4:00 pm.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Tuesday through Thursday 7:00 am to 6:00 pm, Friday 7:00 am to 5:00 pm, and Saturday 8:00 am to 4:00 pm.</p>',
)

rep(
    'data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los sets más recientes de Angie y escribe por DM cualquier duda antes de tu cita." data-en="See Angie\'s latest sets and DM any questions before your appointment.">See Angie\'s latest sets and DM any questions before your appointment.</p>',
)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Map: {NAME}, 15140 SW 72nd St, Miami FL"\n          src="https://www.google.com/maps?q=15140+SW+72nd+St,+Miami,+FL+33193&output=embed"',
)

# ---------- 17. CTA FINAL ----------
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu set clásico, híbrido, volumen o wet set, o el lash lift que ya te toca." data-en="Book online in seconds: your classic, hybrid, volume or wet set, or the lash lift you are due for.">Book online in seconds: your classic, hybrid, volume or wet set, or the lash lift you are due for.</p>',
)

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-13.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de pestañas en Miami, FL. Atención con cita previa." data-en="Lash studio in Miami, FL. By appointment only.">Lash studio in Miami, FL. By appointment only.</p>',
)
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>15140 SW 72nd St, Suite 9, Miami, FL 33193</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 19. Paleta: plum-pink -> sage green ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

HEX_MAP = {
    "a04a72": "5c7a5e",  # accent-deep
    "c47a9c": "8faa8a",  # accent-mid
    "f3e0ea": "e6ede0",  # bg-2 / accent-soft
    "faf2f6": "f2f5ee",  # bg
    "f0bed7": "c8d9c2",  # dark-band text-shine/stars/hover accent
    "8a5573": "5f7a5e",  # dark-band btn-3d shadow (medium)
    "d9a8c2": "c0d3ba",  # orb-b light tint
    "7d3457": "3f5940",  # btn-3d gradient dark stop / scroll-progress start
    "5f2c48": "334833",  # text-shine dark stop / step-num dark stop
    "33222c": "23291f",  # ink
    "fbf3f8": "f4f7ef",  # tile-cap text
    "fbeff5": "eef3e8",  # dark-band btn-3d top stop
    "f8dfeb": "dde8d5",  # dark-band text-shine 2nd stop
    "f2d5e3": "d7e3d0",  # orb-a light tint
    "f2cfe0": "d3e0cb",  # dark-band text-shine last stop
    "efd0e0": "d8e4d0",  # dark-band btn-3d mid stop
    "e5c1d4": "cddbc5",  # orb-c light tint
    "dc9dbe": "b6cbab",  # scroll-progress last stop
    "d3a2bc": "b8cab0",  # dark-band btn-3d bottom stop
    "c9789f": "9db494",  # text-shine 2nd stop
    "b25a85": "7f9a7c",  # text-shine last stop
    "5c2140": "2f4230",  # btn-3d / book-float shadow border (light theme)
    "2a1722": "18201a",  # cta-final dark-band background gradient (start)
    "1f0f18": "121a13",  # cta-final dark-band background gradient (end)
    "1c0f16": "111a12",  # footer dark-band background
}
for old, new in HEX_MAP.items():
    assert old in h, f"paleta: no se encontro hex #{old}"
    h = h.replace(f"#{old}", f"#{new}")

RGB_TRIPLE_MAP = [
    ((160, 74, 114), (92, 122, 94)),
    ((70, 25, 50), (47, 66, 48)),
    ((51, 34, 44), (35, 41, 31)),
    ((125, 52, 87), (63, 89, 64)),
    ((240, 190, 215), (200, 217, 194)),
    ((233, 205, 186), (208, 219, 196)),
    ((185, 138, 128), (140, 165, 138)),
    ((253, 246, 250), (247, 250, 244)),
    ((250, 242, 246), (243, 247, 238)),
    ((40, 16, 30), (24, 32, 26)),
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

open("output/lash-art-by-angie-miami/index.html", "w").write(h)
print("BUILD OK: lash-art-by-angie-miami")
