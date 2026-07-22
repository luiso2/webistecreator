import re

h = open("output/saday-beauty-spa-hialeah/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Saday beauty spa"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1653073_saday-beauty-spa_nail-salon_15886_hialeah"
IG_OLD = "https://www.instagram.com/_lashbloom/"
IG_NEW = "https://www.instagram.com/saday_beauty_spa/"

# ---------- 1. <html lang> + idioma por defecto (ES) ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 2. HEAD: title/meta/og/favicon ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Salón de Uñas en Hialeah, FL | 4.7 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Hialeah FL: manicure, pedicura, acrílico, gel y tratamientos spa para manos y pies, con 4.7 en 30 reseñas de Booksy. Reserva online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Salón de Uñas en Hialeah, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure, pedicura, acrílico y gel con un toque spa. 4.7 en Booksy. Reserva online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
)

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
    "name": "Saday beauty spa",
    "description": "Salón de uñas y beauty spa en Hialeah, FL: manicure, pedicura, acrílico, gel y tratamientos spa para manos y pies.",
    "address": { "@type": "PostalAddress", "streetAddress": "555 W 71st St, Apt 104", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33014", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.886794053195946, "longitude": -80.29517000000001 },
    "sameAs": ["https://booksy.com/en-us/1653073_saday-beauty-spa_nail-salon_15886_hialeah", "https://www.instagram.com/saday_beauty_spa/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "30", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "07:00", "closes": "14:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de uñas y spa", "itemListElement": [
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic fill" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure & pedicure" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura spa" } },
      { "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicura y manicura spa" } }
    ] }
  }
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. Booksy URL global + Instagram global ----------
repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_OLD, IG_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">SB</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV (sin logo real: monograma de texto) ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm tracking-wide ring-1 ring-[rgba(160,74,114,0.35)] bg-[rgba(160,74,114,0.1)] text-[color:var(--accent-deep)]">SB</span>',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Saday <span class="text-[color:var(--accent-deep)]">Beauty Spa</span></span>',
)

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Beauty Spa &amp; Uñas" data-en="Hialeah, FL · Beauty Spa &amp; Nails">Hialeah, FL · Beauty Spa &amp; Uñas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Tu ritual de belleza, cerca de casa." data-en="Your beauty ritual, close to home.">Tu ritual de belleza, cerca de casa.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicure, pedicura" data-en="Manicures, pedicures">Manicures, pedicures</span><br /><span data-es="y el detalle de un " data-en="and the detail of a real " >and the detail of a real </span><span class="text-shine" data-es="spa" data-en="spa">spa</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    "data-es=\"Manicure, pedicura, acrílico, gel y tratamientos spa para manos y pies, hechos por Saday en su estudio de Hialeah. Un 4.7 en 30 reseñas de Booksy, con clientas que llevan años confiando solo en ella.\" data-en=\"Manicures, pedicures, acrylic, gel and spa treatments for hands and feet, done by Saday in her Hialeah studio. A 4.7 rating across 30 Booksy reviews, with clients who have trusted her for years.\">Manicure, pedicura, acrílico, gel y tratamientos spa para manos y pies, hechos por Saday en su estudio de Hialeah. Un 4.7 en 30 reseñas de Booksy, con clientas que llevan años confiando solo en ella.</p>",
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.7 · 30 reseñas en Booksy" data-en="4.7 · 30 reviews on Booksy">4.7 · 30 reseñas en Booksy</span>',
)
OLD_HERO_BTN2 = (
    '<a href="' + IG_NEW + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "            @_lashbloom\n"
    "          </a>"
)
NEW_HERO_BTN2 = (
    '<a href="' + IG_NEW + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "            @saday_beauty_spa\n"
    "          </a>"
)
rep(OLD_HERO_BTN2, NEW_HERO_BTN2)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Manicura en borgoña oscuro con diseño de perlas plateadas en la uña acento, uñas almendradas elegantes" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg">Gel Manicure &amp; Pedicure</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$55 · 1h 30min" data-en="$55 · 1h 30min">$55 · 1h 30min</p>',
)

print("PARTE 1 OK (head, jsonld, preloader, nav, hero)")

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="30">30</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicure <span class="text-shine">&amp;</span> Pedicure</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Acrílico · Gel · Spa" data-en="Acrylic · Gel · Spa">Acrílico · Gel · Spa</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">Se habla</span> <span class="text-shine" data-es="Español" data-en="Spanish">Español</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Atención cálida y cercana</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">555 W 71st St</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Manicure"),
    ("Hybrid Set", "Pedicura"),
    ("Volume Set", "Acrílico"),
    ("Mega Volume", "Gel"),
    ("Bottom Lashes", "Spa"),
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
    '<img src="assets/raw/bk-8.jpg" alt="Mano en remojo dentro de un bowl con agua tibia color coral, tratamiento de spa" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Manicura nude con delicados detalles de cristal en forma de flor" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un spa" data-en="A spa">A spa</span><br /><span class="text-shine" data-es="hecho a mano, uña por uña" data-en="made by hand, nail by nail">made by hand, nail by nail</span></h2>',
)
rep(
    "data-es=\"Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad.\" data-en=\"Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.\">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>",
    "data-es=\"Saday beauty spa es el estudio de Saday en Hialeah: manicure, pedicura, acrílico y gel con la calidez y el detalle que solo un spa de barrio puede dar. Cada cita se vive como un ritual, no solo un servicio.\" data-en=\"Saday beauty spa is Saday's studio in Hialeah: manicures, pedicures, acrylic and gel with the warmth and detail only a neighborhood spa can give. Every appointment feels like a ritual, not just a service.\">Saday beauty spa es el estudio de Saday en Hialeah: manicure, pedicura, acrílico y gel con la calidez y el detalle que solo un spa de barrio puede dar. Cada cita se vive como un ritual, no solo un servicio.</p>",
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 4.7 en 30 reseñas verificadas en Booksy, donde sus clientas la describen como profesional, detallista y alguien a quien vuelven cita tras cita." data-en="The result: a 4.7 rating across 30 verified reviews on Booksy, where clients describe her as professional, detail oriented, and someone they keep coming back to, appointment after appointment.">El resultado: un 4.7 en 30 reseñas verificadas en Booksy, donde sus clientas la describen como profesional, detallista y alguien a quien vuelven cita tras cita.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="30">30</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-xs tracking-wide ring-1 ring-[rgba(160,74,114,0.3)] bg-[rgba(160,74,114,0.1)] text-[color:var(--accent-deep)]">SB</span>\n            <span class="text-sm font-light">Saday · <span class="text-[color:var(--ink-40)]" data-es="Dueña y nail artist" data-en="Owner &amp; nail artist">Owner &amp; nail artist</span></span>',
)

print("PARTE 2 OK (strip, marquee, experiencia)")

# ---------- 11. EL METODO / PROCESO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita en" data-en="Your visit in">Your visit in</span> <span class="text-shine" data-es="4 pasos" data-en="4 steps">4 steps</span></h2>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de diseño" data-en="Design consultation">Design consultation</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges el servicio, el color y el diseño que quieres, y Saday te asesora según la forma de tus uñas." data-en="You choose the service, color and design you want, and Saday advises you based on your nail shape.">You choose the service, color and design you want, and Saday advises you based on your nail shape.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Preparación y limado" data-en="Prep and filing">Prep and filing</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cutícula, forma y limado profesional para dejar la base perfecta antes de cualquier aplicación." data-en="Cuticle care, shaping and professional filing to leave the perfect base before any application.">Cuticle care, shaping and professional filing to leave the perfect base before any application.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación gel o acrílico" data-en="Gel or acrylic application">Gel or acrylic application</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Gel, acrílico, extensiones o el color que elegiste, aplicado con calma y precisión, uña por uña." data-en="Gel, acrylic, extensions or the color you chose, applied calmly and precisely, nail by nail.">Gel, acrylic, extensions or the color you chose, applied calmly and precisely, nail by nail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sellado y top coat" data-en="Sealing and top coat">Sealing and top coat</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Un top coat brillante y de larga duración para que tu manicure o pedicura se vea perfecta por semanas." data-en="A glossy, long lasting top coat so your manicure or pedicure looks flawless for weeks.">A glossy, long lasting top coat so your manicure or pedicure looks flawless for weeks.</p>',
)

print("PARTE 3 OK (metodo)")

# ---------- 12. SERVICIOS: grid destacado de 4 cards (regex, reemplazo entero) ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uñas fuertes y duraderas" data-en="Strong, long lasting nails">Strong, long lasting nails</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Fill</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Relleno de acrílico para mantener tus uñas fuertes y con la forma perfecta entre sets. También: Nail Extensions apress $60 y Gel extensions $65." data-en="Acrylic fill to keep your nails strong and perfectly shaped between full sets. Also: Nail Extensions apress $60 and Gel extensions $65.">Relleno de acrílico para mantener tus uñas fuertes y con la forma perfecta entre sets. También: Nail Extensions apress $60 y Gel extensions $65.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del spa" data-en="Spa favorite">Spa favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Manicure &amp; Pedicure" data-en="Gel Manicure &amp; Pedicure">Gel Manicure &amp; Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo más pedido: manicure y pedicura en gel con acabado brillante y de larga duración, manos y pies el mismo día. También: Manicure gel $35 y Pedicure $30." data-en="The most requested combo: gel manicure and pedicure with a glossy, long lasting finish, hands and feet the same day. Also: Manicure gel $35 and Pedicure $30.">El combo más pedido: manicure y pedicura en gel con acabado brillante y de larga duración, manos y pies el mismo día. También: Manicure gel $35 y Pedicure $30.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="El ritual de la casa" data-en="The house ritual">The house ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Spa" data-en="Manicura Spa">Manicura Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El tratamiento que le da nombre al spa: manicure relajante con remojo e hidratación profunda para tus manos. También: Parafina many $10." data-en="The treatment the spa is named after: a relaxing manicure with soak and deep hydration for your hands. Also: Parafina many $10.">El tratamiento que le da nombre al spa: manicure relajante con remojo e hidratación profunda para tus manos. También: Parafina many $10.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Ritual completo" data-en="Full ritual">Full ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicura y Manicura Spa" data-en="Pedicura y Manicura Spa">Pedicura y Manicura Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El ritual spa completo para manos y pies en una sola cita, con remojo, exfoliación e hidratación. También: Pedicura spa con gel $90." data-en="The complete spa ritual for hands and feet in one visit, with soak, exfoliation and hydration. Also: Pedicura spa con gel $90.">El ritual spa completo para manos y pies en una sola cita, con remojo, exfoliación e hidratación. También: Pedicura spa con gel $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$150</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end() :]

# ---------- 13. subtitulo de servicios ----------
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)

print("PARTE 4 OK (servicios destacados)")

# ---------- 14. Nota de servicios + bloque de menu completo (6 categorias, 34 servicios reales) ----------
FULL_MENU_BLOCK = f"""
      <div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-8" data-es="Menú completo" data-en="Full menu">Full menu</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div class="glass glass-hover rounded-2xl p-6 reveal">
            <h4 class="font-display text-lg mb-4" data-es="Manos" data-en="Hands">Hands</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Manicure</span><span class="text-[color:var(--ink-40)]">$20</span></li>
              <li class="flex justify-between gap-3"><span>Manicure gel</span><span class="text-[color:var(--ink-40)]">$35</span></li>
              <li class="flex justify-between gap-3"><span>Manicura spa</span><span class="text-[color:var(--ink-40)]">$70</span></li>
              <li class="flex justify-between gap-3"><span>Parafina many</span><span class="text-[color:var(--ink-40)]">$10</span></li>
              <li class="flex justify-between gap-3"><span>Nail repair</span><span class="text-[color:var(--ink-40)]">$5</span></li>
              <li class="flex justify-between gap-3"><span data-es="Manicure y pedicura para caballeros" data-en="Manicure and pedicure for men">Manicure y pedicura para caballeros</span><span class="text-[color:var(--ink-40)]">$45</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:90ms">
            <h4 class="font-display text-lg mb-4" data-es="Pies" data-en="Feet">Feet</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Pedicure</span><span class="text-[color:var(--ink-40)]">$30</span></li>
              <li class="flex justify-between gap-3"><span>Gel pedicure</span><span class="text-[color:var(--ink-40)]">$40</span></li>
              <li class="flex justify-between gap-3"><span>Parafina pedicura</span><span class="text-[color:var(--ink-40)]">$15</span></li>
              <li class="flex justify-between gap-3"><span data-es="Pedicura spa con gel" data-en="Pedicura spa con gel">Pedicura spa con gel</span><span class="text-[color:var(--ink-40)]">$90</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:150ms">
            <h4 class="font-display text-lg mb-4" data-es="Extensiones y diseño" data-en="Extensions &amp; design">Extensions &amp; design</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Acrylic fill</span><span class="text-[color:var(--ink-40)]">$50</span></li>
              <li class="flex justify-between gap-3"><span>Gel extensions</span><span class="text-[color:var(--ink-40)]">$65</span></li>
              <li class="flex justify-between gap-3"><span>Nail Extensions apress</span><span class="text-[color:var(--ink-40)]">$60</span></li>
              <li class="flex justify-between gap-3"><span>Nail designs</span><span class="text-[color:var(--ink-40)]">$10</span></li>
              <li class="flex justify-between gap-3"><span>French</span><span class="text-[color:var(--ink-40)]">$10</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:210ms">
            <h4 class="font-display text-lg mb-4" data-es="Combos manos y pies" data-en="Hands &amp; feet combos">Hands &amp; feet combos</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Gel Manicure &amp; pedicure</span><span class="text-[color:var(--ink-40)]">$55</span></li>
              <li class="flex justify-between gap-3"><span>Pedicura y manicura spa</span><span class="text-[color:var(--ink-40)]">$150</span></li>
              <li class="flex justify-between gap-3"><span data-es="Acrílico refill &amp; pedicura" data-en="Acrylic refill &amp; pedicure">Acrílico refill &amp; pedicura</span><span class="text-[color:var(--ink-40)]">$85</span></li>
              <li class="flex justify-between gap-3"><span data-es="Acrílico refill &amp; gel pedicura" data-en="Acrylic refill &amp; gel pedicure">Acrílico refill &amp; gel pedicura</span><span class="text-[color:var(--ink-40)]">$95</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel manos y gel pies" data-en="Gel hands &amp; gel feet">Gel manos y gel pies</span><span class="text-[color:var(--ink-40)]">$70</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:270ms">
            <h4 class="font-display text-lg mb-4" data-es="Cabello" data-en="Hair">Hair</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Secado cabello corto" data-en="Short hair blowout">Secado cabello corto</span><span class="text-[color:var(--ink-40)]">$50</span></li>
              <li class="flex justify-between gap-3"><span data-es="Secado de cabello largo" data-en="Long hair blowout">Secado de cabello largo</span><span class="text-[color:var(--ink-40)]">$70</span></li>
              <li class="flex justify-between gap-3"><span data-es="Corte y secado" data-en="Cut &amp; blowout">Corte y secado</span><span class="text-[color:var(--ink-40)]">$85</span></li>
              <li class="flex justify-between gap-3"><span data-es="Mascarilla hidratante" data-en="Hydrating mask">Hydrating mask</span><span class="text-[color:var(--ink-40)]">$85</span></li>
              <li class="flex justify-between gap-3"><span data-es="Tinte de raíz y secado" data-en="Root touch-up &amp; blowout">Tinte raíz y secado</span><span class="text-[color:var(--ink-40)]">$90</span></li>
              <li class="flex justify-between gap-3"><span data-es="Tinte de raíz" data-en="Root touch-up">Tinte raíz</span><span class="text-[color:var(--ink-40)]">$40</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:330ms">
            <h4 class="font-display text-lg mb-4" data-es="Cejas, pestañas y maquillaje" data-en="Brows, Lifts &amp; Makeup">Brows, Lifts &amp; Makeup</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Lifting de pestañas" data-en="Lift treatment">Ayelashes lifting</span><span class="text-[color:var(--ink-40)]">$70</span></li>
              <li class="flex justify-between gap-3"><span data-es="Diseño de cejas (shading)" data-en="Eyebrow shading">Eyebrow shading</span><span class="text-[color:var(--ink-40)]">$350</span></li>
              <li class="flex justify-between gap-3"><span data-es="Depilación de cejas" data-en="Eyebrow waxing">Eyebrow waxing</span><span class="text-[color:var(--ink-40)]">$15</span></li>
              <li class="flex justify-between gap-3"><span>Bigote</span><span class="text-[color:var(--ink-40)]">$15</span></li>
              <li class="flex justify-between gap-3"><span data-es="Cejas con henna" data-en="Eyebrows with henna">Eyebrows with henna</span><span class="text-[color:var(--ink-40)]">$40</span></li>
              <li class="flex justify-between gap-3"><span data-es="Pigmentación de labios" data-en="Lip pigmentation">Lip pigmentation</span><span class="text-[color:var(--ink-40)]">$250</span></li>
              <li class="flex justify-between gap-3"><span data-es="Maquillaje" data-en="Makeup">Makeup</span><span class="text-[color:var(--ink-40)]">$150</span></li>
              <li class="flex justify-between gap-3"><span data-es="Maquillaje de novia" data-en="Wedding makeup">Wedding Makeup</span><span class="text-[color:var(--ink-40)]">$250</span></li>
            </ul>
          </div>
        </div>
        <p class="reveal text-center mt-8">
          <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" data-es="Ver el menú completo y reservar en Booksy" data-en="See the full menu and book on Booksy">Ver el menú completo y reservar en Booksy</a>
        </p>
      </div>"""

rep(
    'data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span>',
    'data-es="Manicure y pedicura para caballeros, tratamientos de cabello, cejas, pestañas y maquillaje: menú completo y disponibilidad en tiempo real en Booksy." data-en="Manicure and pedicure for men, hair treatments, brow and lift services, and makeup: full menu and real time availability on Booksy.">Manicure y pedicura para caballeros, tratamientos de cabello, cejas, pestañas y maquillaje: menú completo y disponibilidad en tiempo real en Booksy.</span>'
    + FULL_MENU_BLOCK,
)

print("PARTE 5 OK (menu completo)")

# ---------- 15. GALERIA: eyebrow, H2, link social, grid completo ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas," data-en="Nails,">Nails,</span> <span class="text-shine" data-es="de cerca" data-en="up close">up close</span></h2>',
)
OLD_GAL_SOCIAL = (
    '<a href="' + IG_NEW + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "          @_lashbloom\n"
    "        </a>"
)
NEW_GAL_SOCIAL = (
    '<a href="' + IG_NEW + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "          @saday_beauty_spa\n"
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño con detalle de perlas" data-en="Pearl detail nail art">Pearl detail nail art</span><img src="assets/raw/bk-16.jpg" alt="Manicura en borgoña oscuro con diseño de perlas plateadas en la uña acento, uñas almendradas" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="French en borgoña con flor dorada" data-en="Burgundy french with gold flower">Burgundy french with gold flower</span><img src="assets/raw/bk-11.jpg" alt="Manicura francesa con borde en borgoña oscuro y un diseño floral dorado en la uña acento" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Copo de nieve en marrón" data-en="Snowflake in brown">Snowflake in brown</span><img src="assets/raw/bk-12.jpg" alt="Manicura en tono marrón con brillo y un copo de nieve pintado a mano en la uña acento" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="French neón verde" data-en="Neon green french">Neon green french</span><img src="assets/raw/bk-15.jpg" alt="Manicura french con línea neón verde sobre base nude en uñas cuadradas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Efecto mármol" data-en="Marble effect">Marble effect</span><img src="assets/raw/bk-13.jpg" alt="Manicura con efecto mármol en blanco y gris sobre uñas almendradas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Pedicura impecable" data-en="Flawless pedicure">Flawless pedicure</span><img src="assets/raw/bk-6.jpg" alt="Pedicura en tono blanco nude, pies recién arreglados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

print("PARTE 6 OK (galeria)")

# ---------- 16. OPINIONES (3 quotes reales verbatim, 30 resenas, 4.7) ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.7 de 5 · 30 reseñas verificadas en Booksy" data-en="4.7 out of 5 · 30 verified reviews on Booksy">4.7 de 5 · 30 reseñas verificadas en Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Encantada con Saday Beauty spa , trato excelente y todo los procedimientos que allí realizan son increíbles con buen precio !! Saquen su cita chicas no se van a arrepentir !!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lisbeidi T…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor muy profesional y siempre salgo complacida"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Martha P…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"súper especial me encanta su trabajo es única la quiero mucho es la mejor en lo q hase"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mabel de l…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 30 reseñas en Booksy" data-en="Read all 30 reviews on Booksy">Leer las 30 reseñas en Booksy</a>',
)

print("PARTE 7 OK (opiniones)")

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
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">555 W 71st St, Apt 104, Hialeah, FL 33014</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=555+W+71st+St,+Apt+104,+Hialeah,+FL+33014" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes a viernes 9am a 5:30pm, y sábados 7am a 2pm." data-en="By appointment via Booksy: pick the service, day and time, confirmation is instant. Monday to Friday 9am to 5:30pm, and Saturday 7am to 2pm.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes a viernes 9am a 5:30pm, y sábados 7am a 2pm.</p>',
)

OLD_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@_lashbloom</a>'
)
NEW_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos más recientes de Saday y escribe por DM cualquier duda antes de tu cita." data-en="See Saday\'s latest work and DM any questions before your appointment.">Mira los trabajos más recientes de Saday y escribe por DM cualquier duda antes de tu cita.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@saday_beauty_spa</a>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_SOCIAL)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Saday beauty spa, 555 W 71st St, Hialeah FL"\n          src="https://www.google.com/maps?q=25.886794053195946,-80.29517000000001&output=embed"',
)

print("PARTE 8 OK (ubicacion)")

# ---------- 18. CTA FINAL ----------
# (la linea "Tu ritual de belleza, cerca de casa." ya se reemplazo en HERO con n=2, cubre hero + cta-final)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting for you">te está esperando</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    "data-es=\"Reserva online en segundos: tu manicure, tu pedicura spa o el diseño que ya quieres estrenar con Saday en Hialeah.\" data-en=\"Book online in seconds: your manicure, your spa pedicure, or the design you have been wanting to try with Saday in Hialeah.\">Reserva online en segundos: tu manicure, tu pedicura spa o el diseño que ya quieres estrenar con Saday en Hialeah.</p>",
)
# (el boton "Seguir en Instagram" del CTA final ya apunta a IG_NEW via el repall global)

print("PARTE 9 OK (cta final)")

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-xs tracking-wide ring-1 ring-[rgba(240,190,215,0.35)] bg-[rgba(240,190,215,0.08)] text-[#f0bed7]">SB</span>\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas y beauty spa en Hialeah, FL. Atención con cita previa." data-en="Nail salon and beauty spa in Hialeah, FL. By appointment only.">Salón de uñas y beauty spa en Hialeah, FL. Atención con cita previa.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>555 W 71st St, Apt 104, Hialeah, FL 33014</p>',
)
OLD_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>'
)
NEW_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @saday_beauty_spa</a></p>'
)
rep(OLD_FOOT_SOCIAL, NEW_FOOT_SOCIAL)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

print("PARTE 10 OK (footer)")

# ---------- 20. Paleta: plum-pink -> borgoña / vino profundo ----------
# Proteger badge dorado de Merktop (bloque CSS completo).
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)
assert '#f4eee2' in h

HEX_MAP = [
    ("a04a72", "7a2340"),  # accent-deep
    ("c47a9c", "a83a5c"),  # accent-mid
    ("5c2140", "4d1a2e"),  # boton 3d, "suela" oscura
    ("f0bed7", "eab9c5"),  # dark-band text-shine / stars claro
    ("faf2f6", "faf3f1"),  # bg base / ink sobre dark-band
    ("8a5573", "8a3d52"),  # dark-band btn-3d sombra solida
    ("f3e0ea", "f2dde3"),  # bg-2 / accent-soft
    ("d9a8c2", "d9a3ae"),  # orb-b / dark-band shine
    ("7d3457", "6b2140"),  # btn-3d gradiente oscuro / scroll-progress
    ("5f2c48", "592038"),  # shimmer oscuro / step-num
    ("33222c", "2c1a20"),  # ink
    ("fbf3f8", "fdf4f2"),  # tile-cap texto casi blanco
    ("fbeff5", "fdf1ee"),  # dark-band btn-3d stop claro
    ("f8dfeb", "f6e2e6"),  # dark-band shine stop 2
    ("f6f1ea", "f8f0ee"),  # theme-color meta
    ("f2d5e3", "f2d9de"),  # orb-a
    ("f2cfe0", "f0d3d9"),  # dark-band shine stop 3
    ("efd0e0", "eed4d8"),  # dark-band btn-3d stop medio
    ("e5c1d4", "e3c3ca"),  # orb-c
    ("dc9dbe", "d9a0ac"),  # scroll-progress stop claro
    ("d3a2bc", "d1a3ac"),  # dark-band btn-3d stop oscuro
    ("c9789f", "c96a80"),  # shimmer stop claro-medio
    ("b25a85", "a8455f"),  # shimmer stop final
    ("2a1722", "2a1319"),  # cta-final gradiente inicio
    ("1f0f18", "1c0e12"),  # cta-final gradiente fin
    ("1c0f16", "1a0e11"),  # footer bg
]
for old, new in HEX_MAP:
    assert f"#{old}" in h or old.upper() in h, f"hex no encontrado: {old}"
    h = h.replace(old, new)
    h = h.replace(old.upper(), new)

RGBA_MAP = [
    ("160,74,114", "122,35,64"),   # accent-deep rgb
    ("51,34,44", "44,26,32"),      # ink rgb
    ("240,190,215", "234,185,197"),  # f0bed7 rgb
    ("70,25,50", "77,26,46"),      # btn-3d inset oscuro
    ("250,242,246", "250,243,241"),  # bg rgb (ink-60/40 en dark-band)
    ("125,52,87", "107,33,64"),    # dark-band btn-3d sombra (7d3457 rgb)
    ("253,246,250", "253,244,242"),  # surface rgb
    ("40,16,30", "44,26,32"),      # tile-cap gradiente oscuro
    ("233,205,186", "226,199,201"),  # dark-band accent-ghost
    ("185,138,128", "198,148,155"),  # orb-b dark-band
]
for old, new in RGBA_MAP:
    assert old in h, f"rgb no encontrado: {old}"
    h = h.replace(old, new)

# Restaurar el badge dorado protegido.
h = h.replace("@@BADGE@@", badge_block, 1)

print("PARTE 11 OK (paleta borgoña / vino profundo, badge dorado protegido)")

open("output/saday-beauty-spa-hialeah/index.html", "w").write(h)
print("DONE: output/saday-beauty-spa-hialeah/index.html escrito")
