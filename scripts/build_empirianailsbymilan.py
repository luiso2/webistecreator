import re

h = open("output/empirianailsbymilan/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Empirianails by Milan"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1220912_empirianails-by-milan_nail-salon_15889_miami"
IG_URL_OLD = "https://www.instagram.com/_lashbloom/"
IG_URL_NEW = "https://www.instagram.com/empirianails_by_milan/"
MAPS_Q = "25.7327,-80.30536"

# ---------- 1. HEAD ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    "<title>Empirianails by Milan · Salón de Uñas en Miami, FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Empirianails by Milan, Westchester, Miami FL: manicure gel, nivelación y manicure rusa, sistema híbrido, poli gel y pedicura con Iris Jenny Milan Valerino. 5.0 perfecto en 17 reseñas de Booksy." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Empirianails by Milan · Salón de Uñas en Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure gel, nivelación, rusa, híbrido y pedicura. 5.0 en Booksy. Reserva en línea." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-1.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

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
    "description": "Nail salon en Westchester, Miami, FL: manicure gel, nivelación y manicure rusa, sistema híbrido, poli gel y pedicura con Iris Jenny Milan Valerino.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "6840 SW 40th St, 39", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33155", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.7327, "longitude": -80.30536 }},
    "sameAs": ["{BOOKSY_NEW}", "{IG_URL_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "17", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "19:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "10:30", "closes": "19:30" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      {{ "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Gel Manicure" }} }},
      {{ "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Leveling and Russian Manicure (Long)" }} }},
      {{ "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Hybrid System or Poli Gel (Medium Nails)" }} }},
      {{ "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Gel Pedicure" }} }}
    ] }}
  }}
  </script>"""
rep(OLD_LD, NEW_LD)

repall(BOOKSY_OLD, BOOKSY_NEW)

# ---------- 3. Idioma: default ES ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 4. Paleta (amatista/ciruela) ----------
PALETTE = [
    ("#a04a72", "#7c4b95"), ("#5c2140", "#422152"), ("#f0bed7", "#dab9eb"), ("#faf2f6", "#f3ebf7"),
    ("#c47a9c", "#a677bd"), ("#8a5573", "#725481"), ("#f3e0ea", "#e8daef"), ("#d9a8c2", "#c3a4d3"),
    ("#7d3457", "#5e3472"), ("#5f2c48", "#472b56"), ("#33222c", "#281f2c"), ("#fbf3f8", "#f4ecf8"),
    ("#fbeff5", "#f3e8f8"), ("#f8dfeb", "#ebd8f5"), ("#f6f1ea", "#ede4f2"), ("#f4eee2", "#e9dcf0"),
    ("#f2d5e3", "#e4cfee"), ("#f2cfe0", "#e2c9ee"), ("#efd0e0", "#e0caeb"), ("#e5c1d4", "#d4bce0"),
    ("#dc9dbe", "#c299d6"), ("#d3a2bc", "#bd9ecd"), ("#c9789f", "#a875c2"), ("#b25a85", "#8f58aa"),
    ("#2a1722", "#1e1423"), ("#1f0f18", "#140c18"), ("#1c0f16", "#120c15"),
]
for old, new in PALETTE:
    repall(old, new)

# rgba() triples que corresponden a hex de la lista (accent-deep, ink, accent-mid oscuro)
RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(124,75,149"),
    ("rgba(51,34,44", "rgba(40,31,44"),
    ("rgba(240,190,215", "rgba(218,185,235"),
    ("rgba(250,242,246", "rgba(243,235,247"),
    ("rgba(125,52,87", "rgba(94,52,114"),
]
for old, new in RGBA_PALETTE:
    repall(old, new)

assert "#D4A84B" in h, "el badge merktop debe seguir dorado"

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">EM</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(124,75,149,0.35)]" />',
    f'<img src="assets/raw/bk-1.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(124,75,149,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Empirianails <span class="text-[color:var(--accent-deep)]">by Milan</span></span>',
)

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Westchester, Miami, FL · Salón de Uñas" data-en="Westchester, Miami, FL · Nail Salon">Westchester, Miami, FL · Salón de Uñas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas cuidadas al detalle." data-en="Nails cared for, down to the last detail.">Uñas cuidadas al detalle.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicure, pedicura y" data-en="Manicure, pedicure and">Manicure, pedicure and</span><br /><span data-es="diseños hechos para " data-en="nail designs made to ">nail designs made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Empirianails by Milan es el estudio de Iris Jenny Milan Valerino en Westchester, Miami. Manicure gel, nivelación y manicure rusa, sistema híbrido, poli gel y pedicura, con un 5.0 perfecto en 17 reseñas de Booksy." data-en="Empirianails by Milan is Iris Jenny Milan Valerino\'s studio in Westchester, Miami. Gel manicure, leveling and Russian manicure, hybrid system, poli gel and pedicure, with a perfect 5.0 across 17 Booksy reviews.">Empirianails by Milan is Iris Jenny Milan Valerino\'s studio in Westchester, Miami. Gel manicure, leveling and Russian manicure, hybrid system, poli gel and pedicure, with a perfect 5.0 across 17 Booksy reviews.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 17 reseñas en Booksy" data-en="5.0 · 17 reviews on Booksy">5.0 · 17 reseñas en Booksy</span>',
)
rep(
    '''<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
    f'''<a href="{IG_URL_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @empirianails_by_milan
          </a>''',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Manicura roja glossy sobre fondo neutro" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Leveling and Russian Manicure (Long)</p>')
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$90 · 2h 10min" data-en="$90 · 2h 10min">$90 · 2h 10min</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="17">17</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Rusa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Nivelación · Poli Gel" data-en="Leveling · Poli gel">Nivelación · Poli Gel</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Solo" data-en="Just">Just</span> <span class="text-shine">Iris</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Una artista, tu cita" data-en="One artist, your appointment">Una artista, tu cita</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Westchester, Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">6840 SW 40th St</p></div>',
)

# ---------- 9. MARQUEE (x4 cada palabra) ----------
MQ = [
    ("Classic Set", "Gel Manicure"),
    ("Hybrid Set", "Russian Manicure"),
    ("Volume Set", "Poli Gel"),
    ("Mega Volume", "Gel Pedicure"),
    ("Bottom Lashes", "Acrylic Set"),
    ("West Palm Beach, FL", "Miami, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 10. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Manicura nude glossy, brillo natural" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Manicura gris perlada con brillo y anillo de diamante" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="hecho a mano" data-en="made by hand">made by hand</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Empirianails by Milan es el estudio de una sola artista: Iris Jenny Milan Valerino, en Westchester, Miami. Cada cita se piensa contigo: manicure gel, nivelación y manicure rusa, sistema híbrido o poli gel, y pedicura, con el mismo cuidado al detalle en cada visita." data-en="Empirianails by Milan is the studio of one artist: Iris Jenny Milan Valerino, in Westchester, Miami. Every visit is planned around you: gel manicure, leveling and Russian manicure, hybrid system or poli gel, and pedicure, with the same attention to detail every time.">Empirianails by Milan is the studio of one artist: Iris Jenny Milan Valerino, in Westchester, Miami. Every visit is planned around you: gel manicure, leveling and Russian manicure, hybrid system or poli gel, and pedicure, with the same attention to detail every time.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 17 reseñas verificadas en Booksy, y clientas que dicen que Iris es dulce, detallista y que sus uñas nunca se han visto mejor." data-en="The result: a perfect 5.0 across 17 verified reviews on Booksy, and clients who say Iris is sweet, detail-oriented, and that their nails have never looked better.">The result: a perfect 5.0 across 17 verified reviews on Booksy, and clients who say Iris is sweet, detail-oriented, and that their nails have never looked better.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="17">17</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(124,75,149,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>''',
    f'''<img src="assets/raw/bk-2.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(124,75,149,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Iris Jenny Milan Valerino · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail artist">Nail artist</span></span>''',
)

# ---------- 11. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy, con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy, with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy, con precio y duración claros, y confirmas al instante.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Preparación experta" data-en="Expert prep">Expert prep</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cutícula y la base perfecta antes de cualquier gel, nivelación o manicure rusa." data-en="Filing, cuticle care and the perfect base before any gel, leveling or Russian manicure.">Filing, cuticle care and the perfect base before any gel, leveling or Russian manicure.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación al detalle" data-en="Careful application">Careful application</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Iris trabaja con calma y precisión: gel, nivelación, rusa, híbrido o poli gel, uña por uña." data-en="Iris works calmly and precisely: gel, leveling, Russian, hybrid or poli gel, nail by nail.">Iris works calmly and precisely: gel, leveling, Russian, hybrid or poli gel, nail by nail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">You leave ready</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un acabado impecable, listo para lucir hasta tu próxima cita." data-en="You leave with a flawless finish, ready to last until your next visit.">You leave with a flawless finish, ready to last until your next visit.</p>',
)

# ---------- 12. SERVICIOS ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cuidado esencial" data-en="Everyday care">Cuidado esencial</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure con gel de larga duración: forma, cutícula y esmaltado impecable. También: Acrylic Full Set (Short Nails) $60 (1h 20min)." data-en="A long-lasting gel manicure: shaping, cuticle care and a flawless polish. Also: Acrylic Full Set (Short Nails) $60 (1h 20min).">A long-lasting gel manicure: shaping, cuticle care and a flawless polish. Also: Acrylic Full Set (Short Nails) $60 (1h 20min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 10min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(124,75,149,0.4); box-shadow: 0 18px 50px rgba(40,31,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Leveling and Russian Manicure (Long)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Nivelación y manicure rusa en uñas largas, con un acabado impecable y de larga duración. También disponible en Medium $70 (1h 45min) y Short $65." data-en="Leveling and Russian manicure on long nails, with a flawless, long-lasting finish. Also available in Medium $70 (1h 45min) and Short $65.">Leveling and Russian manicure on long nails, with a flawless, long-lasting finish. Also available in Medium $70 (1h 45min) and Short $65.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 10min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema híbrido" data-en="Hybrid system">Sistema híbrido</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Hybrid System or Poli Gel (Medium Nails)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sistema híbrido o poli gel en uñas medianas: resistente y con un acabado natural. También disponible en Long $90 (2h 10min) y Short $65." data-en="Hybrid system or poli gel on medium nails: strong, with a natural finish. Also available in Long $90 (2h 10min) and Short $65.">Hybrid system or poli gel on medium nails: strong, with a natural finish. Also available in Long $90 (2h 10min) and Short $65.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicura</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura en gel de larga duración, con limado y cuidado completo de principio a fin. También: Men's Pedicure $50 (1h 30min)." data-en="A long-lasting gel pedicure, with filing and complete care from start to finish. Also: Men's Pedicure $50 (1h 30min).">A long-lasting gel pedicure, with filing and complete care from start to finish. Also: Men's Pedicure $50 (1h 30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 20min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end():]

rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)

# ---------- 13. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: Men\'s Manicure $35 (1h) · Regular Pedicure $40 (1h 10min) · Clean Pedicure $30 (45min). Precios y disponibilidad exactos en Booksy." data-en="Also on the menu: Men\'s Manicure $35 (1h) · Regular Pedicure $40 (1h 10min) · Clean Pedicure $30 (45min). Exact prices and availability on Booksy.">También en el menú: Men\'s Manicure $35 (1h) · Regular Pedicure $40 (1h 10min) · Clean Pedicure $30 (45min). Precios y disponibilidad exactos en Booksy.</span></p>',
)

# ---------- 14. GALERIA ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>',
)

rep(
    '''<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>''',
    f'''<a href="{IG_URL_NEW}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @empirianails_by_milan
        </a>''',
)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Ciruela intenso sobre seda" data-en="Deep plum on silk">Deep plum on silk</span><img src="assets/raw/bk-3.jpg" alt="Manicura en tono ciruela intenso sobre seda" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Francesa con brillo y corazones" data-en="Glittery French with hearts">Glittery French with hearts</span><img src="assets/raw/bk-16.jpg" alt="Uñas francesa con brillo rosa y diseño de corazones junto a una columna decorativa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Francesa en azul" data-en="Blue French tips">Blue French tips</span><img src="assets/raw/bk-12.jpg" alt="Manicura francesa azul con un pequeño detalle de uña" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Lila glossy con anillo" data-en="Glossy lilac with a ring">Glossy lilac with a ring</span><img src="assets/raw/bk-10.jpg" alt="Manicura lila glossy con un anillo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Francesa clásica" data-en="Classic French">Classic French</span><img src="assets/raw/bk-11.jpg" alt="Manicura francesa clásica en uñas ovaladas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Nude con corazones" data-en="Nude with hearts">Nude with hearts</span><img src="assets/raw/bk-4.jpg" alt="Manicura nude con delicados corazones blancos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 15. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 17 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 17 verified reviews on Booksy">5.0 de 5 · 17 reseñas verificadas en Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"It was my first time having this work done, so i dont have anything to compare it to. I loved the results, and she was very pleasant."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Morayma R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Just had my first appointment, best my nails have ever looked! Iris is so sweet, and makes sure every nail is crafted to perfection. 10/10 service ❤️"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Julie R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She is great and detailed"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Vanessa O…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 17 reseñas en Booksy" data-en="Read all 17 reviews on Booksy">Leer las 17 reseñas en Booksy</a>',
)

# ---------- 16. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Westchester, Miami</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(124,75,149,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">6840 SW 40th St, 39, Miami, FL 33155</p>\n'
    f'              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(124,75,149,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
)

OLD_LOC_SOCIAL = (
    '<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">\n'
    '            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    '            <div>\n'
    '              <p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(124,75,149,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>\n'
    '            </div>\n'
    '          </div>'
)
NEW_LOC_HOURS = (
    '<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">\n'
    '            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>\n'
    '            <div>\n'
    '              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes a viernes de 10:00 am a 7:00 pm. Sábados y domingos de 10:30 am a 7:30 pm." data-en="Tuesday to Friday, 10:00 am to 7:00 pm. Saturdays and Sundays, 10:30 am to 7:30 pm.">Martes a viernes de 10:00 am a 7:00 pm. Sábados y domingos de 10:30 am a 7:30 pm.</p>\n'
    '            </div>\n'
    '          </div>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_HOURS)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: {NAME}, 6840 SW 40th St, Miami FL"\n          src="https://www.google.com/maps?q={MAPS_Q}&output=embed"',
)

# ---------- 17. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tus uñas nuevas" data-en="Your next manicure">Your next manicure</span> <span class="text-shine" data-es="te están esperando" data-en="is waiting">te están esperando</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure, nivelación, sistema híbrido o pedicura con Iris en Westchester, Miami." data-en="Book online in seconds: your manicure, leveling, hybrid system or pedicure with Iris in Westchester, Miami.">Reserva online en segundos: tu manicure, nivelación, sistema híbrido o pedicura con Iris en Westchester, Miami.</p>',
)
rep(
    '''<a href="https://booksy.com/en-us/1220912_empirianails-by-milan_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    f'''<a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="{IG_URL_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
)

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(218,185,235,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-1.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(218,185,235,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami, FL. Atención con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Salón de uñas en Miami, FL. Atención con cita previa.</p>',
)
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>6840 SW 40th St, 39, Miami, FL 33155</p>')

rep(
    '<p><a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="hover:text-[#dab9eb]">Instagram · @_lashbloom</a></p>',
    f'<p><a href="{IG_URL_NEW}" target="_blank" rel="noopener" class="hover:text-[#dab9eb]">Instagram · @empirianails_by_milan</a></p>',
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 19. Verificacion final de restos del esqueleto anterior ----------
for leftover in ["Lash Bloom", "Yesi", "West Palm Beach", "Cresthaven", "519855", "lash",
                  "pestañas", "_lashbloom", "logo.jpg", "hero-1.jpg", "about-2.jpg"]:
    assert leftover not in h, "LEFTOVER: " + leftover

assert h.count("—") == 0, "em-dash prohibido"

open("output/empirianailsbymilan/index.html", "w").write(h)
print("BUILD OK: empirianailsbymilan")
