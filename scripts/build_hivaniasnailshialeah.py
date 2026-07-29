import re

h = open("output/hivanias-nails-hialeah/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Hivania's Nails"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1390898_hivania-s-nails_nail-salon_15886_hialeah"
MAPS_NEW = "https://www.google.com/maps?q=2775+W+Okeechobee+Rd,+Hialeah,+FL+33010"

# ---------- 1. <html lang> + idioma por defecto (ES) ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 2. HEAD: title/meta/og/favicon/theme-color ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Salón de Uñas en Hialeah, FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Hialeah FL: full set de acrílico, soft gel, pedicura y depilación de cejas, con un 5.0 perfecto en 39 reseñas de Booksy. Reserva online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Salón de Uñas en Hialeah, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrílico, soft gel y pedicura. 5.0 en Booksy. Reserva online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-8.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
)
rep('<meta name="theme-color" content="#f6f1ea" />', '<meta name="theme-color" content="#f8f2e6" />')

# ---------- 3. JSON-LD ----------
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

NEW_LD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Hivania's Nails",
    "description": "Salón de uñas en Hialeah, FL: full set de acrílico, soft gel, pedicura y depilación de cejas y bigote por Hivania.",
    "address": { "@type": "PostalAddress", "streetAddress": "2775 W Okeechobee Rd lot 71", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33010", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.846878396288833, "longitude": -80.31209171583333 },
    "sameAs": ["https://booksy.com/en-us/1390898_hivania-s-nails_nail-salon_15886_hialeah"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "39", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Thursday"], "opens": "09:00", "closes": "13:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Thursday", "Friday"], "opens": "14:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday"], "opens": "09:00", "closes": "12:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:30", "closes": "12:15" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "13:30", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set Acrilico" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Soft Gel (Apres)" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Polish Gel (Manicure de gel)" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure gel" } }
    ] }
  }
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. Booksy URL global (no hay Instagram: sin repall de IG) ----------
repall(BOOKSY_OLD, BOOKSY_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">HN</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV (logo real: bk-2.jpg) ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Hivania\'s Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Hivania\'s <span class="text-[color:var(--accent-deep)]">Nails</span></span>',
)

# ---------- 7. HERO (sin boton de Instagram: reemplazado por boton a Ubicacion) ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salón de Uñas" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Salón de Uñas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas hechas con detalle, uña por uña." data-en="Nails made with detail, nail by nail.">Uñas hechas con detalle, uña por uña.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrílico, soft gel" data-en="Acrylic, soft gel">Acrílico, soft gel</span><br /><span data-es="y nail art hecho a " data-en="and nail art made by ">and nail art made by </span><span class="text-shine" data-es="mano" data-en="hand">hand</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Full set de acrílico, soft gel, pedicura y depilación de cejas y bigote, hechos a mano por Hivania en su salón de Hialeah. Un 5.0 perfecto en 39 reseñas de Booksy, con clientas que la describen como profesional, creativa y detallista." data-en="Full acrylic sets, soft gel, pedicures and brow and lip waxing, done by hand by Hivania in her Hialeah salon. A perfect 5.0 across 39 Booksy reviews, with clients describing her work as professional, creative and detailed." >Full set de acrílico, soft gel, pedicura y depilación de cejas y bigote, hechos a mano por Hivania en su salón de Hialeah. Un 5.0 perfecto en 39 reseñas de Booksy, con clientas que la describen como profesional, creativa y detallista.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 39 reseñas en Booksy" data-en="5.0 · 39 reviews on Booksy">5.0 · 39 reseñas en Booksy</span>',
)
OLD_HERO_BTN2 = (
    '<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "            @_lashbloom\n"
    "          </a>"
)
NEW_HERO_BTN2 = (
    '<a href="#ubicacion" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>\n'
    '            <span data-es="Hialeah, FL" data-en="Hialeah, FL">Hialeah, FL</span>\n'
    "          </a>"
)
rep(OLD_HERO_BTN2, NEW_HERO_BTN2)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-8.jpg" alt="Uñas largas estilo coffin con french blanco, detalle en glitter dorado y anillos dorados" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg">Full Set Acrílico</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$75 · 2h" data-en="$75 · 2h">$75 · 2h</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="39">39</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrílico <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Full Set · Soft Gel · Pedicura" data-en="Full Set · Soft Gel · Pedicure">Full Set · Soft Gel · Pedicura</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">Se habla</span> <span class="text-shine" data-es="Español" data-en="Spanish">Español</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Atención cálida y cercana</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2775 W Okeechobee Rd</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Full Set Acrílico"),
    ("Hybrid Set", "Soft Gel Apres"),
    ("Volume Set", "Manicure Gel"),
    ("Mega Volume", "Pedicure Gel"),
    ("Bottom Lashes", "Nail Art"),
    ("West Palm Beach, FL", "Hialeah, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 10. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Manicure ombré nude a blanco con flor blanca en 3D y pedreria en las puntas" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Manicure con french lila y una una con anillo dorado y pedreria" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">Una artista,</span><br /><span class="text-shine" data-es="detalle que enamora" data-en="detail that wins you over">detalle que enamora</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Hivania\'s Nails es el salón de una sola artista en Hialeah: Hivania. Cada servicio se hace uña por uña, con la paciencia y el ojo minucioso que sus clientas repiten en cada reseña de Booksy." data-en="Hivania\'s Nails is the studio of one nail artist in Hialeah: Hivania. Every service is done nail by nail, with the patience and the sharp eye for detail her clients mention in every Booksy review.">Hivania\'s Nails es el salón de una sola artista en Hialeah: Hivania. Cada servicio se hace uña por uña, con la paciencia y el ojo minucioso que sus clientas repiten en cada reseña de Booksy.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 39 reseñas verificadas en Booksy, donde clientas la describen como profesional, creativa y excelente en su trabajo, cita tras cita." data-en="The result: a perfect 5.0 across 39 verified reviews on Booksy, where clients describe her as professional, creative and excellent at her craft, appointment after appointment.">El resultado: un 5.0 perfecto en 39 reseñas verificadas en Booksy, donde clientas la describen como profesional, creativa y excelente en su trabajo, cita tras cita.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="39">39</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="Hivania\'s Nails" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Hivania · <span class="text-[color:var(--ink-40)]" data-es="Nail artist" data-en="Nail artist">Nail artist</span></span>',
)

# ---------- 11. EL METODO / PROCESO (4 pasos genericos de nail salon) ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita," data-en="Your visit,">Tu cita,</span> <span class="text-shine" data-es="uña por uña" data-en="nail by nail">uña por uña</span></h2>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de diseño" data-en="Design consultation">Design consultation</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges la forma, el largo y el diseño: acrílico, soft gel o un nail art hecho a mano, a tu gusto." data-en="Choose the shape, length and design: acrylic, soft gel or a hand painted nail art, just the way you like it.">Eliges la forma, el largo y el diseño: acrílico, soft gel o un nail art hecho a mano, a tu gusto.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Preparación y limado" data-en="Prep and filing">Prep and filing</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Retiro si hace falta, cutícula, forma y limado: la base pareja que sostiene un buen resultado." data-en="Removal if needed, cuticle care, shape and filing: the even base that holds a great result.">Retiro si hace falta, cutícula, forma y limado: la base pareja que sostiene un buen resultado.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación de gel o acrílico" data-en="Gel or acrylic application">Gel or acrylic application</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Hivania aplica el acrílico, soft gel o dip gel elegido, uña por uña, con calma y precisión." data-en="Hivania applies the chosen acrylic, soft gel or dip gel, nail by nail, calmly and with precision.">Hivania aplica el acrílico, soft gel o dip gel elegido, uña por uña, con calma y precisión.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sellado y top coat" data-en="Seal and top coat">Seal and top coat</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un top coat brillante que sella el diseño y le da la duración que sus clientas destacan en cada reseña." data-en="You leave with a glossy top coat that seals the design and gives it the lasting finish her clients highlight in every review.">Sales con un top coat brillante que sella el diseño y le da la duración que sus clientas destacan en cada reseña.</p>',
)

print("PARTE 1 OK (head, jsonld, preloader, nav, hero, strip, marquee, experiencia, metodo: 4 pasos genericos)")

# ---------- 12. SERVICIOS: grid destacado de 4 cards (regex, reemplazo entero) ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="El clásico del salón" data-en="The salon classic">The salon classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Set Acrílico" data-en="Full Set Acrílico">Full Set Acrílico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de uñas acrílicas, en la forma y largo que prefieras. También: Reffill $55 y Reffill con cambio de color $75." data-en="Full acrylic nail set, in the shape and length you prefer. Also: Refill $55 and Refill with color change $75.">Set completo de uñas acrílicas, en la forma y largo que prefieras. También: Reffill $55 y Reffill con cambio de color $75.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Soft Gel (Apres)" data-en="Soft Gel (Apres)">Soft Gel (Apres)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extension en soft gel, ligera y de acabado natural. También: Builder Gel con extensión en moldes $65 y Rubber Base $50." data-en="Soft gel extension, light and natural looking. Also: Builder gel with mold extension $65 and Rubber Base $50.">Extension en soft gel, ligera y de acabado natural. También: Builder Gel con extensión en moldes $65 y Rubber Base $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure de todos los días" data-en="Everyday manicure">Everyday manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Polish Gel" data-en="Polish Gel">Polish Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure de gel con acabado brillante y larga duración. También: Manicure con esmalte regular $20 y Rubber Base $50." data-en="Gel manicure with a glossy, long lasting finish. Also: Regular polish manicure $20 and Rubber Base $50.">Manicure de gel con acabado brillante y larga duración. También: Manicure con esmalte regular $20 y Rubber Base $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies cuidados" data-en="Feet, taken care of">Feet, taken care of</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicure Gel" data-en="Pedicure Gel">Pedicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa con esmalte en gel de larga duración. También: Pedicure regular $25." data-en="Complete pedicure with long lasting gel polish. Also: Regular pedicure $25.">Pedicura completa con esmalte en gel de larga duración. También: Pedicure regular $25.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end() :]

# ---------- 13. Eyebrow/H2/subtitulo de servicios ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">service</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)

# ---------- 14. Nota de servicios + bloque de menu completo (14 servicios reales) ----------
FULL_MENU_BLOCK = f"""
      <div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-8" data-es="Menú completo" data-en="Full menu">Menú completo</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div class="glass glass-hover rounded-2xl p-6 reveal">
            <h4 class="font-display text-lg mb-4" data-es="Manos" data-en="Hands">Manos</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Polish Gel (Manicure de gel)" data-en="Polish Gel (Manicure de gel)">Polish Gel (Manicure de gel)</span><span class="text-[color:var(--ink-40)]">$35</span></li>
              <li class="flex justify-between gap-3"><span data-es="Manicure con esmalte regular" data-en="Manicure con esmalte regular">Manicure con esmalte regular</span><span class="text-[color:var(--ink-40)]">$20</span></li>
              <li class="flex justify-between gap-3"><span data-es="Rubber Base" data-en="Rubber Base">Rubber Base</span><span class="text-[color:var(--ink-40)]">$50</span></li>
              <li class="flex justify-between gap-3"><span data-es="Hybrid Dip Gel" data-en="Hybrid Dip Gel">Hybrid Dip Gel</span><span class="text-[color:var(--ink-40)]">$50</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:90ms">
            <h4 class="font-display text-lg mb-4" data-es="Acrílico y extensiones" data-en="Acrylic &amp; extensions">Acrylic &amp; extensions</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Full Set Acrílico" data-en="Full Set Acrílico">Full Set Acrílico</span><span class="text-[color:var(--ink-40)]">$75</span></li>
              <li class="flex justify-between gap-3"><span data-es="Reffill Acrílico" data-en="Reffill Acrílico">Reffill Acrílico</span><span class="text-[color:var(--ink-40)]">$55</span></li>
              <li class="flex justify-between gap-3"><span data-es="Reffil cambio de color de acrílico" data-en="Reffil cambio de color de acrílico">Reffil cambio de color de acrílico</span><span class="text-[color:var(--ink-40)]">$75</span></li>
              <li class="flex justify-between gap-3"><span data-es="Retiro de uñas acrílicas" data-en="Retiro de uñas acrílicas">Retiro de uñas acrílicas</span><span class="text-[color:var(--ink-40)]">$15</span></li>
              <li class="flex justify-between gap-3"><span data-es="Builder Gel con Extensión en Moldes" data-en="Builder Gel con Extensión en Moldes">Builder Gel con Extensión en Moldes</span><span class="text-[color:var(--ink-40)]">$65</span></li>
              <li class="flex justify-between gap-3"><span data-es="Soft Gel (Apres)" data-en="Soft Gel (Apres)">Soft Gel (Apres)</span><span class="text-[color:var(--ink-40)]">$60</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:150ms">
            <h4 class="font-display text-lg mb-4" data-es="Pies" data-en="Feet">Pies</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Pedicure regular" data-en="Pedicure regular">Pedicure regular</span><span class="text-[color:var(--ink-40)]">$25</span></li>
              <li class="flex justify-between gap-3"><span data-es="Pedicure gel" data-en="Pedicure gel">Pedicure gel</span><span class="text-[color:var(--ink-40)]">$35</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:210ms">
            <h4 class="font-display text-lg mb-4" data-es="Depilación" data-en="Waxing">Depilación</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Depilación de Bigote (Upper Lip Wash)" data-en="Depilación de Bigote (Upper Lip Wash)">Depilación de Bigote (Upper Lip Wash)</span><span class="text-[color:var(--ink-40)]">$10</span></li>
              <li class="flex justify-between gap-3"><span data-es="Depilación de Ceja (Eyebrow Wax)" data-en="Depilación de Ceja (Eyebrow Wax)">Depilación de Ceja (Eyebrow Wax)</span><span class="text-[color:var(--ink-40)]">$10</span></li>
            </ul>
          </div>
        </div>
        <p class="reveal text-center mt-8">
          <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" data-es="Ver el menú completo y reservar en Booksy" data-en="See the full menu and book on Booksy">Ver el menú completo y reservar en Booksy</a>
        </p>
      </div>"""

rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="14 servicios entre manos, pies, extensiones y depilación: menú completo y disponibilidad en tiempo real en Booksy." data-en="14 services across hands, feet, extensions and waxing: full menu and real time availability on Booksy.">14 servicios entre manos, pies, extensiones y depilación: menú completo y disponibilidad en tiempo real en Booksy.</span></p>'
    + FULL_MENU_BLOCK,
)

print("PARTE 2 OK (servicios)")

# ---------- 15. GALERIA: eyebrow, H2, boton social (sin IG: boton a Booksy), grid completo ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas," data-en="Nails,">Uñas,</span> <span class="text-shine" data-es="de cerca" data-en="up close">up close</span></h2>',
)
OLD_GAL_SOCIAL = (
    '<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "          @_lashbloom\n"
    "        </a>"
)
NEW_GAL_SOCIAL = (
    f'<a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n'
    '          <span data-es="Ver en Booksy" data-en="See on Booksy">Ver en Booksy</span>\n'
    "        </a>"
)
rep(OLD_GAL_SOCIAL, NEW_GAL_SOCIAL)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Nail art floral en tonos lila y amarillo" data-en="Floral nail art in lilac and yellow">Floral nail art in lilac and yellow</span><img src="assets/raw/bk-6.jpg" alt="Unas en lila y amarillo pastel con diseno floral cromado en dorado y rosa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="French amarillo con flores doradas" data-en="Yellow french with gold flowers">Yellow french with gold flowers</span><img src="assets/raw/bk-3.jpg" alt="Unas amarillas con diseno floral de perlas doradas sobre base transparente" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Ombré blanco con líneas doradas" data-en="White ombre with gold linework">White ombre with gold linework</span><img src="assets/raw/bk-4.jpg" alt="Unas transparentes con marmoleado blanco, glitter y lineas doradas estilo chrome" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Ombré lila sobre fondo suave" data-en="Lilac ombre on a soft backdrop">Lilac ombre on a soft backdrop</span><img src="assets/raw/bk-9.jpg" alt="Unas en degradado lila y nude sobre un fondo peludo claro" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Lila sobre denim" data-en="Lilac against denim">Lilac against denim</span><img src="assets/raw/bk-14.jpg" alt="Manicure en tono lila fotografiada sobre tela de mezclilla" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Chrome amarillo" data-en="Yellow chrome">Yellow chrome</span><img src="assets/raw/bk-15.jpg" alt="Unas en amarillo con acabado chrome brillante" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

# ---------- 16. OPINIONES (3 quotes reales verbatim de Booksy, 39 resenas, 5.0) ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 39 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 39 verified reviews on Booksy">5.0 de 5 · 39 reseñas verificadas en Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente en su trabajo. Muy profesional y creativa"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Cliente verificada</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente servicio y calidad."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karla P.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encanta su trabajo"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Daisy C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 39 reseñas en Booksy" data-en="Read all 39 reviews on Booksy">Leer las 39 reseñas en Booksy</a>',
)

print("PARTE 3 OK (galeria, opiniones)")

# ---------- 17. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah, FL</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">2775 W Okeechobee Rd lot 71, Hialeah, FL 33010</p>\n'
    f'              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="{MAPS_NEW}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes, martes y jueves 9am a 1pm y 2pm a 6pm." data-en="By appointment via Booksy: pick the service, day and time, confirmation is instant. Monday, Tuesday and Thursday 9am to 1pm and 2pm to 6pm.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes, martes y jueves 9am a 1pm y 2pm a 6pm.</p>',
)

# Tercer card: reemplazamos Instagram (no existe) por Horario completo, con datos reales.
OLD_LOC_SOCIAL = (
    '<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    '            <div>\n'
    '              <p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>\n'
    '            </div>'
)
NEW_LOC_SOCIAL = (
    '<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>\n'
    '            <div>\n'
    '              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lun, mar y jue: 9am a 1pm y 2pm a 6pm. Vie: 9am a 12:30pm y 2pm a 6pm. Sáb: 8:30am a 12:15pm y 1:30pm a 5pm. Cerrado miércoles y domingo." data-en="Mon, Tue and Thu: 9am to 1pm and 2pm to 6pm. Fri: 9am to 12:30pm and 2pm to 6pm. Sat: 8:30am to 12:15pm and 1:30pm to 5pm. Closed Wednesday and Sunday.">Lun, mar y jue: 9am a 1pm y 2pm a 6pm. Vie: 9am a 12:30pm y 2pm a 6pm. Sáb: 8:30am a 12:15pm y 1:30pm a 5pm. Cerrado miércoles y domingo.</p>\n'
    f'              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="{BOOKSY_NEW}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n'
    '            </div>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_SOCIAL)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Hivania\'s Nails, 2775 W Okeechobee Rd, Hialeah FL"\n          src="https://www.google.com/maps?q=25.846878396288833,-80.31209171583333&output=embed"',
)

print("PARTE 4a OK (ubicacion)")

# ---------- 18. CTA FINAL (sin Instagram: segundo boton apunta a Como llegar) ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo set" data-en="Your next set">Tu próximo set</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu full set de acrílico, tu soft gel o el diseño que ya quieres estrenar con Hivania en Hialeah." data-en="Book online in seconds: your acrylic full set, your soft gel, or the design you have been wanting to try with Hivania in Hialeah.">Reserva online en segundos: tu full set de acrílico, tu soft gel o el diseño que ya quieres estrenar con Hivania en Hialeah.</p>',
)
rep(
    '<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    f'<a href="{MAPS_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-2.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Salón de uñas en Hialeah, FL. Atención con cita previa.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>2775 W Okeechobee Rd, Hialeah, FL 33010</p>',
)
# La columna "Síguenos" (Instagram) se reemplaza por "Horario" (no hay Instagram).
OLD_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>'
)
NEW_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Horario" data-en="Hours">Horario</p>\n'
    '        <p data-es="Lun, mar, jue: 9am-1pm y 2pm-6pm" data-en="Mon, Tue, Thu: 9am-1pm and 2pm-6pm">Lun, mar, jue: 9am-1pm y 2pm-6pm</p>\n'
    '        <p data-es="Vie: 9am-12:30pm y 2pm-6pm · Sáb: 8:30am-12:15pm y 1:30pm-5pm" data-en="Fri: 9am-12:30pm and 2pm-6pm · Sat: 8:30am-12:15pm and 1:30pm-5pm">Vie: 9am-12:30pm y 2pm-6pm · Sáb: 8:30am-12:15pm y 1:30pm-5pm</p>'
)
rep(OLD_FOOT_SOCIAL, NEW_FOOT_SOCIAL)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

print("PARTE 4b OK (cta-final, footer)")

# ---------- 20. Paleta: plum-pink -> miel / latte dorado ----------
# Proteger badge dorado de Merktop (bloque CSS completo) ANTES de tocar la paleta dorada.
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)
# La unica referencia de color de marca Merktop fuera del bloque CSS protegido es el texto
# "Powered by Merktop" del footer (#f4eee2, crema neutro): se deja intacta.
assert '#f4eee2' in h

HEX_MAP = [
    ("faf2f6", "faf6ef"),  # bg base
    ("f3e0ea", "f2e6d3"),  # bg-2 / accent-soft
    ("33222c", "2e2419"),  # ink
    ("a04a72", "a8763e"),  # accent-deep
    ("c47a9c", "c9975c"),  # accent-mid
    ("c9789f", "d9ad72"),  # shimmer stop claro-medio
    ("5f2c48", "6b4423"),  # shimmer stop oscuro / step-num stop2
    ("b25a85", "c48a4a"),  # shimmer stop final
    ("f2d5e3", "f2e0c2"),  # orb-a
    ("d9a8c2", "e0c090"),  # orb-b / dark-band text-shine stop3
    ("e5c1d4", "e8cda0"),  # orb-c
    ("7d3457", "8a5a2e"),  # btn-3d gradiente oscuro / scroll-progress stop1
    ("5c2140", "5c3a1a"),  # boton 3d, "suela" oscura
    ("f0bed7", "f0d9a8"),  # dark-band text-shine stop1 / stars claro
    ("f8dfeb", "f6e6cf"),  # dark-band text-shine stop2
    ("f2cfe0", "f0dcb8"),  # dark-band text-shine stop4
    ("fbeff5", "f9f1e0"),  # dark-band btn-3d stop claro
    ("efd0e0", "e8caa0"),  # dark-band btn-3d stop medio
    ("d3a2bc", "caa06e"),  # dark-band btn-3d stop oscuro
    ("8a5573", "8a6a3a"),  # dark-band btn-3d sombra solida
    ("dc9dbe", "dcb37a"),  # scroll-progress stop claro
    ("fbf3f8", "faf3e6"),  # tile-cap texto casi blanco
    ("2a1722", "2a2015"),  # cta-final gradiente inicio
    ("1f0f18", "1c150d"),  # cta-final gradiente fin
    ("1c0f16", "1a130c"),  # footer bg
]
for old, new in HEX_MAP:
    assert f"#{old}" in h or old.upper() in h, f"hex no encontrado: {old}"
    h = h.replace(old, new)
    h = h.replace(old.upper(), new)

RGBA_MAP = [
    ("253,246,250", "253,248,240"),  # surface rgb
    ("51,34,44", "46,36,25"),  # ink rgb
    ("160,74,114", "168,118,62"),  # accent-deep rgb
    ("250,242,246", "250,246,239"),  # bg rgb (dark-band ink-60/40, nav.scrolled bg)
    ("233,205,186", "224,196,144"),  # dark-band accent-ghost
    ("240,190,215", "240,217,168"),  # f0bed7 rgb
    ("185,138,128", "200,158,110"),  # orb-b dark-band
    ("125,52,87", "138,90,46"),  # dark-band btn-3d sombra (7d3457 rgb)
    ("70,25,50", "90,58,26"),  # btn-3d inset oscuro
    ("40,16,30", "36,26,16"),  # tile-cap gradiente oscuro
]
for old, new in RGBA_MAP:
    assert old in h, f"rgb no encontrado: {old}"
    h = h.replace(old, new)

# Restaurar el badge dorado protegido (intacto, sin mezclar con la paleta miel del negocio).
h = h.replace("@@BADGE@@", badge_block, 1)

print("PARTE 5 OK (paleta miel / latte dorado, badge dorado protegido)")

open("output/hivanias-nails-hialeah/index.html", "w").write(h)
print("DONE: output/hivanias-nails-hialeah/index.html escrito")
