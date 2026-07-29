import re
import colorsys

h = open("output/nails-by-brigytte-hialeah/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Nails by Brigytte"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1365947_nails-by-brigytte_nail-salon_15886_hialeah"
IG_OLD = "https://www.instagram.com/_lashbloom/"
IG_NEW = "https://www.instagram.com/nails_by_brigytte/"

# ---------- 1. <html lang> + idioma por defecto (ES) ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 2. HEAD: title/meta/og/favicon ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Salón de Uñas en Hialeah, FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Hialeah FL: manicure en gel, builder gel, extensiones Apres Gel-X y pedicura, con un 5.0 perfecto en 25 reseñas de Booksy. Reserva online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Salón de Uñas en Hialeah, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure en gel, builder gel y pedicura. 5.0 en Booksy. Reserva online." />',
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
    "name": "Nails by Brigytte",
    "description": "Salón de uñas en Hialeah, FL: manicure en gel, builder gel, extensiones Apres Gel-X, pedicura y diseños hechos a mano por Brigytte.",
    "address": { "@type": "PostalAddress", "streetAddress": "3600 W 18th Ave, suite 37", "addressLocality": "Hialeah", "addressRegion": "FL", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.854863855114985, "longitude": -80.31924804345476 },
    "sameAs": ["https://booksy.com/en-us/1365947_nails-by-brigytte_nail-salon_15886_hialeah", "https://www.instagram.com/nails_by_brigytte/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "25", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday"], "opens": "09:00", "closes": "16:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel" } },
      { "@type": "Offer", "price": "54", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder gel" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Gel X con French" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Gel con French" } }
    ] }
  }
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. Booksy URL global + Instagram global ----------
repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_OLD, IG_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NB</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV (usa el logo neon real de la marca: bk-2.jpg) ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Logo de neón redondo de Nails by Brigytte" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails <span class="text-[color:var(--accent-deep)]">by Brigytte</span></span>',
)

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salón de Uñas" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Salón de Uñas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="El detalle que enamora, uña por uña." data-en="The detail that wins you over, nail by nail.">El detalle que enamora, uña por uña.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicure, extensiones" data-en="Manicures, extensions">Manicure, extensiones</span><br /><span data-es="y diseños hechos a " data-en="and designs made by ">y diseños hechos a </span><span class="text-shine" data-es="mano" data-en="hand">mano</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicure en gel, builder gel, extensiones Apres Gel-X y pedicura, hechos a mano por Brigytte en su suite de Hialeah. Un 5.0 perfecto en 25 reseñas de Booksy, con clientas que la acompañan desde hace más de 5 años." data-en="Gel manicures, builder gel, Apres Gel-X extensions and pedicures, hand-done by Brigytte in her Hialeah suite. A perfect 5.0 across 25 Booksy reviews, with clients who have stayed with her for over 5 years.">Manicure en gel, builder gel, extensiones Apres Gel-X y pedicura, hechos a mano por Brigytte en su suite de Hialeah. Un 5.0 perfecto en 25 reseñas de Booksy, con clientas que la acompañan desde hace más de 5 años.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 25 reseñas en Booksy" data-en="5.0 · 25 reviews on Booksy">5.0 · 25 reseñas en Booksy</span>',
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
    "            @nails_by_brigytte\n"
    "          </a>"
)
rep(OLD_HERO_BTN2, NEW_HERO_BTN2)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-6.jpg" alt="Manicura rosa nude con rhinestones dorados y moños 3D iridiscentes" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg">Builder Gel</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$54 · 1h" data-en="$54 · 1h">$54 · 1h</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="25">25</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Builder</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicure · Extensiones · Pedicura" data-en="Manicure · Extensions · Pedicure">Manicure · Extensiones · Pedicura</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">años</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clientas fieles por años</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">3600 W 18th Ave</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Builder Gel"),
    ("Hybrid Set", "Luminary"),
    ("Volume Set", "Apres Gel-X"),
    ("Mega Volume", "Manicure &amp; Pedicure"),
    ("Bottom Lashes", "Diseños de Uñas"),
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
    '<img src="assets/raw/bk-5.jpg" alt="Suite de Nails by Brigytte con letrero neon Hello Gorgeous, silla de pedicura y pared de esmaltes" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Manicura francesa clasica en almendra con anillos dorados de autor" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una manicurista," data-en="One nail artist,">Una manicurista,</span><br /><span class="text-shine" data-es="clientas de toda la vida" data-en="clients for life">clientas de toda la vida</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Nails by Brigytte es el estudio de una sola manicurista en Hialeah: Brigytte. Dueña y única artista de su suite en la 3600 W 18th Ave, atiende con la calma y el detalle que sus clientas mencionan una y otra vez en sus reseñas." data-en="Nails by Brigytte is the studio of one nail artist in Hialeah: Brigytte. Owner and sole artist of her suite on 3600 W 18th Ave, she works with the calm and attention to detail her clients mention again and again in their reviews.">Nails by Brigytte es el estudio de una sola manicurista en Hialeah: Brigytte. Dueña y única artista de su suite en la 3600 W 18th Ave, atiende con la calma y el detalle que sus clientas mencionan una y otra vez en sus reseñas.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 25 reseñas de Booksy, con clientas que llevan más de 5 y hasta 7 años haciéndose las uñas solo con ella, y que describen su lugar como acogedor, con cafecito cubano incluido." data-en="The result: a perfect 5.0 across 25 Booksy reviews, with clients who have been getting their nails done only with her for over 5 and even 7 years, and describe her space as cozy, cafecito cubano included.">El resultado: un 5.0 perfecto en 25 reseñas de Booksy, con clientas que llevan más de 5 y hasta 7 años haciéndose las uñas solo con ella, y que describen su lugar como acogedor, con cafecito cubano incluido.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="25">25</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/bk-13.jpg" alt="Detalle de la marca Nails by Brigytte en un tocador con flores" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Brigytte · <span class="text-[color:var(--ink-40)]" data-es="Dueña y manicurista" data-en="Owner &amp; nail artist">Dueña y manicurista</span></span>',
)

# ---------- 11. EL METODO / PROCESO (4 pasos genericos de nail salon) ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita," data-en="Your visit,">Tu cita,</span> <span class="text-shine" data-es="uña por uña" data-en="nail by nail">uña por uña</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio, día y hora en Booksy con precio y duración claros, y confirmas al instante." data-en="Choose your service, day and time on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio, día y hora en Booksy con precio y duración claros, y confirmas al instante.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de diseño" data-en="Design consultation">Consulta de diseño</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma, largo y estilo: gel, builder gel, acrílico o un diseño hecho a mano, todo conversado antes de empezar." data-en="Shape, length and style: gel, builder gel, acrylic or a hand-painted design, all discussed before starting.">Forma, largo y estilo: gel, builder gel, acrílico o un diseño hecho a mano, todo conversado antes de empezar.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Preparación y limado" data-en="Prep &amp; filing">Preparación y limado</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cutícula, forma y limado: la base pareja que necesita todo buen gel o acrílico para durar semanas." data-en="Cuticle, shape and filing: the even base every good gel or acrylic set needs to last for weeks.">Cutícula, forma y limado: la base pareja que necesita todo buen gel o acrílico para durar semanas.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sellado y top coat" data-en="Sealing &amp; top coat">Sellado y top coat</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un top coat brillante que sella el diseño, tal como cuentan sus clientas: uñas que duran más de un mes." data-en="You leave with a glossy top coat that seals the design, just like her clients say: nails that last more than a month.">Sales con un top coat brillante que sella el diseño, tal como cuentan sus clientas: uñas que duran más de un mes.</p>',
)
# 3er paso (aplicacion gel/acrilico): titulo del div queda "The zen part" original ya reemplazado arriba con Preparacion.
# Insertamos el paso de aplicacion como bloque propio via anchor del step-num 03.
rep(
    '<p class="step-num text-5xl mb-5">03</p>\n          <h3 class="font-display text-xl mb-3" data-es="Preparación y limado" data-en="Prep &amp; filing">Preparación y limado</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cutícula, forma y limado: la base pareja que necesita todo buen gel o acrílico para durar semanas." data-en="Cuticle, shape and filing: the even base every good gel or acrylic set needs to last for weeks.">Cutícula, forma y limado: la base pareja que necesita todo buen gel o acrílico para durar semanas.</p>',
    '<p class="step-num text-5xl mb-5">03</p>\n          <h3 class="font-display text-xl mb-3" data-es="Aplicación de gel o acrílico" data-en="Gel or acrylic application">Aplicación de gel o acrílico</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Builder gel, luminary, apres o acrílico, aplicado uña por uña con la calma que sus clientas repiten en cada reseña." data-en="Builder gel, luminary, apres or acrylic, applied nail by nail with the calm her clients mention in every review.">Builder gel, luminary, apres o acrílico, aplicado uña por uña con la calma que sus clientas repiten en cada reseña.</p>',
)

print("PARTE 1 OK (head, jsonld, preloader, nav, hero, strip, marquee, experiencia, metodo)")

# ---------- 12. SERVICIOS: grid destacado de 4 cards (regex, reemplazo entero) ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure de todos los días" data-en="Everyday manicure">Manicure de todos los días</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Gel" data-en="Manicure Gel">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure profesional en gel con acabado brillante y de larga duración. También: Manicure Gel con French $45 y Rubber Base Nails $45." data-en="Professional gel manicure with a glossy, long lasting finish. Also: Manicure Gel con French $45 and Rubber Base Nails $45.">Manicure profesional en gel con acabado brillante y de larga duración. También: Manicure Gel con French $45 y Rubber Base Nails $45.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Builder Gel" data-en="Builder Gel">Builder Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio más pedido de la casa: gel resistente moldeado uña por uña con acabado natural y duradero. También: Builder gel con French $70 y Builder gel with extension $68." data-en="The studio's most requested service: a sturdy gel shaped nail by nail with a natural, long lasting finish. Also: Builder gel con French $70 and Builder gel with extension $68.">El servicio más pedido de la casa: gel resistente moldeado uña por uña con acabado natural y duradero. También: Builder gel con French $70 y Builder gel with extension $68.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$54</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extensión con estilo" data-en="Extension with style">Extensión con estilo</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apres Gel X con French" data-en="Apres Gel X con French">Apres Gel X con French</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tips Apres prediseñadas con punta francesa impecable en una sola sesión. También: Apres Gel-X sin diseño $59." data-en="Pre-designed Apres tips with an impeccable french tip in one visit. Also: Apres Gel-X without design $59.">Tips Apres prediseñadas con punta francesa impecable en una sola sesión. También: Apres Gel-X sin diseño $59.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies con acabado french" data-en="Feet with a french finish">Pies con acabado french</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicure Gel con French" data-en="Pedicure Gel con French">Pedicure Gel con French</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa en gel con punta francesa impecable. También: Pedicure Gel polish $45 y Pedicure Regular polish $35." data-en="A complete gel pedicure with an impeccable french tip. Also: Pedicure Gel polish $45 and Pedicure Regular polish $35.">Pedicura completa en gel con punta francesa impecable. También: Pedicure Gel polish $45 y Pedicure Regular polish $35.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end() :]

# ---------- 13. Eyebrow/H2/subtitulo de servicios ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)

# ---------- 14. Nota de servicios + bloque de menu completo (32 servicios reales, 4 categorias) ----------
FULL_MENU_BLOCK = f"""
      <div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-8" data-es="Menú completo" data-en="Full menu">Menú completo</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div class="glass glass-hover rounded-2xl p-6 reveal">
            <h4 class="font-display text-lg mb-4" data-es="Manicure" data-en="Manicure">Manicure</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Manicure Gel" data-en="Manicure Gel">Manicure Gel</span><span class="text-[color:var(--ink-40)]">$35</span></li>
              <li class="flex justify-between gap-3"><span data-es="Manicure Gel con French" data-en="Manicure Gel con French">Manicure Gel con French</span><span class="text-[color:var(--ink-40)]">$45</span></li>
              <li class="flex justify-between gap-3"><span data-es="Rubber Base Nails" data-en="Rubber Base Nails">Rubber Base Nails</span><span class="text-[color:var(--ink-40)]">$45</span></li>
              <li class="flex justify-between gap-3"><span data-es="Rubber Base con French" data-en="Rubber Base con French">Rubber Base con French</span><span class="text-[color:var(--ink-40)]">$60</span></li>
              <li class="flex justify-between gap-3"><span data-es="Fix 1 nail" data-en="Fix 1 nail">Fix 1 nail</span><span class="text-[color:var(--ink-40)]">$5</span></li>
              <li class="flex justify-between gap-3"><span data-es="Retirar Apres, Acrílico, builder, luminary" data-en="Retirar Apres, Acrílico, builder, luminary">Retirar Apres, Acrílico, builder, luminary</span><span class="text-[color:var(--ink-40)]">$15</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:90ms">
            <h4 class="font-display text-lg mb-4" data-es="Extensiones" data-en="Extensions">Extensiones</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Builder gel" data-en="Builder gel">Builder gel</span><span class="text-[color:var(--ink-40)]">$54</span></li>
              <li class="flex justify-between gap-3"><span data-es="Builder gel con French" data-en="Builder gel con French">Builder gel con French</span><span class="text-[color:var(--ink-40)]">$70</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary" data-en="Luminary">Luminary</span><span class="text-[color:var(--ink-40)]">$54</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary con French" data-en="Luminary con French">Luminary con French</span><span class="text-[color:var(--ink-40)]">$70</span></li>
              <li class="flex justify-between gap-3"><span data-es="Apres Gel-X" data-en="Apres Gel-X">Apres Gel-X</span><span class="text-[color:var(--ink-40)]">$59</span></li>
              <li class="flex justify-between gap-3"><span data-es="Apres Gel X con French" data-en="Apres Gel X con French">Apres Gel X con French</span><span class="text-[color:var(--ink-40)]">$75</span></li>
              <li class="flex justify-between gap-3"><span data-es="Builder gel with extension" data-en="Builder gel with extension">Builder gel with extension</span><span class="text-[color:var(--ink-40)]">$68</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:150ms">
            <h4 class="font-display text-lg mb-4" data-es="Pedicure y combos" data-en="Pedicure &amp; combos">Pedicure y combos</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Pedicure Regular polish" data-en="Pedicure Regular polish">Pedicure Regular polish</span><span class="text-[color:var(--ink-40)]">$35</span></li>
              <li class="flex justify-between gap-3"><span data-es="Pedicure Gel polish" data-en="Pedicure Gel polish">Pedicure Gel polish</span><span class="text-[color:var(--ink-40)]">$45</span></li>
              <li class="flex justify-between gap-3"><span data-es="Pedicure Gel con French" data-en="Pedicure Gel con French">Pedicure Gel con French</span><span class="text-[color:var(--ink-40)]">$50</span></li>
              <li class="flex justify-between gap-3"><span data-es="Manicure gel/pedi reg" data-en="Manicure gel/pedi reg">Manicure gel/pedi reg</span><span class="text-[color:var(--ink-40)]">$60</span></li>
              <li class="flex justify-between gap-3"><span data-es="Manicure gel/pedi gel" data-en="Manicure gel/pedi gel">Manicure gel/pedi gel</span><span class="text-[color:var(--ink-40)]">$70</span></li>
              <li class="flex justify-between gap-3"><span data-es="Builder Gel &amp; gel Pedi" data-en="Builder Gel &amp; gel Pedi">Builder Gel &amp; gel Pedi</span><span class="text-[color:var(--ink-40)]">$100</span></li>
              <li class="flex justify-between gap-3"><span data-es="Builder Gel &amp; reg Pedi" data-en="Builder Gel &amp; reg Pedi">Builder Gel &amp; reg Pedi</span><span class="text-[color:var(--ink-40)]">$90</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary &amp; Gel pedi" data-en="Luminary &amp; Gel pedi">Luminary &amp; Gel pedi</span><span class="text-[color:var(--ink-40)]">$100</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary &amp; Reg Pedi" data-en="Luminary &amp; Reg Pedi">Luminary &amp; Reg Pedi</span><span class="text-[color:var(--ink-40)]">$90</span></li>
              <li class="flex justify-between gap-3"><span data-es="Apres Extension &amp; gel pedi" data-en="Apres Extension &amp; gel pedi">Apres Extension &amp; gel pedi</span><span class="text-[color:var(--ink-40)]">$110</span></li>
              <li class="flex justify-between gap-3"><span data-es="Apres Extension &amp; Reg Pedi" data-en="Apres Extension &amp; Reg Pedi">Apres Extension &amp; Reg Pedi</span><span class="text-[color:var(--ink-40)]">$100</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:210ms">
            <h4 class="font-display text-lg mb-4" data-es="Diseño y cejas" data-en="Design &amp; brows">Diseño y cejas</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Diseño ombre nails" data-en="Diseño ombre nails">Diseño ombre nails</span><span class="text-[color:var(--ink-40)]">$10</span></li>
              <li class="flex justify-between gap-3"><span data-es="Diseño efecto chrome" data-en="Diseño efecto chrome">Diseño efecto chrome</span><span class="text-[color:var(--ink-40)]">$5</span></li>
              <li class="flex justify-between gap-3"><span data-es="Diseño de French manicure" data-en="Diseño de French manicure">Diseño de French manicure</span><span class="text-[color:var(--ink-40)]">$10</span></li>
              <li class="flex justify-between gap-3"><span data-es="Diseños en varias uñas" data-en="Diseños en varias uñas">Diseños en varias uñas</span><span class="text-[color:var(--ink-40)]">$20</span></li>
              <li class="flex justify-between gap-3"><span data-es="Depilación de cejas" data-en="Eyebrow waxing">Depilación de cejas</span><span class="text-[color:var(--ink-40)]">$15</span></li>
              <li class="flex justify-between gap-3"><span data-es="Depilación de cejas, labio y mentón" data-en="Brows, lip &amp; chin waxing">Depilación de cejas, labio y mentón</span><span class="text-[color:var(--ink-40)]">$25</span></li>
              <li class="flex justify-between gap-3"><span data-es="Wax cejas y labio superior" data-en="Brow &amp; lip wax">Wax cejas y labio superior</span><span class="text-[color:var(--ink-40)]">$20</span></li>
              <li class="flex justify-between gap-3"><span data-es="Depilación de cejas y tinte" data-en="Brow waxing &amp; tint">Depilación de cejas y tinte</span><span class="text-[color:var(--ink-40)]">$25</span></li>
            </ul>
          </div>
        </div>
        <p class="reveal text-center mt-8">
          <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" data-es="Ver el menú completo y reservar en Booksy" data-en="See the full menu and book on Booksy">Ver el menú completo y reservar en Booksy</a>
        </p>
      </div>"""

rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También servicios de cejas: depilación, wax y tinte. Menú completo y disponibilidad en tiempo real en Booksy." data-en="Brow services too: waxing, threading and tint. Full menu and real time availability on Booksy.">También servicios de cejas: depilación, wax y tinte. Menú completo y disponibilidad en tiempo real en Booksy.</span></p>'
    + FULL_MENU_BLOCK,
)

print("PARTE 2 OK (servicios)")

# ---------- 15. GALERIA: eyebrow, H2, link social, grid completo ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas," data-en="Nails,">Uñas,</span> <span class="text-shine" data-es="de cerca" data-en="up close">de cerca</span></h2>',
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
    "          @nails_by_brigytte\n"
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño sirena, conchas y estrellas" data-en="Mermaid shells and starfish">Mermaid shells and starfish</span><img src="assets/raw/bk-11.jpg" alt="Manicura nude con punta francesa en glitter azul plateado y dijes de conchas y estrellas de mar" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Azul eléctrico" data-en="Electric blue">Electric blue</span><img src="assets/raw/bk-12.jpg" alt="Manicura solida en azul electrico brillante sobre unas cuadradas" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Animal print con flores 3D" data-en="Cow print with 3D flowers">Cow print with 3D flowers</span><img src="assets/raw/bk-8.jpg" alt="Manicura nude con puntas estilo animal print y flores 3D en coral, azul y blanco" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Moño 3D y fresitas" data-en="3D bow and strawberries">3D bow and strawberries</span><img src="assets/raw/bk-9.jpg" alt="Manicura nude con moño 3D iridiscente, strass plateado y dijes de fresas pintadas a mano" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Blanco con strass dorado" data-en="White with gold studs">White with gold studs</span><img src="assets/raw/bk-7.jpg" alt="Manicura solida en blanco con pequenos strass dorados sobre unas almendradas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Corazones rojos y strass" data-en="Red hearts and rhinestones">Red hearts and rhinestones</span><img src="assets/raw/bk-3.jpg" alt="Manicura blanca con corazones rojos pintados a mano y strass transparentes" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

# ---------- 16. OPINIONES (3 quotes reales verbatim, 25 resenas, 5.0) ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 25 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 25 verified reviews on Booksy">5.0 de 5 · 25 reseñas verificadas en Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor manicurista, he sido su clienta por más de 5 años y cada vez amo más su trabajo, mis uñas siempre duran más de 1 mes. Excelente trabajo."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jessi C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor manicurista, mis uñas duran más de un mes y llevo haciéndomelas con Brigytte por más de 7 años. El lugar es bien acogedor, el cafecito cubano nunca falta, la atención es excepcional y las uñas las mejores de todas."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jessi C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I always have a great experience with Brigytte. She is always on time and super quick. My nails are always very neat and her salon is super clean and cute!! Siempre tengo una buena experiencia con Brigytte. Es muy puntual y rápida. Mis uñas siempre salen muy detalladas y me encanta el ambiente de su salón!! 💕💕"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anonymous</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 25 reseñas en Booksy" data-en="Read all 25 reviews on Booksy">Leer las 25 reseñas en Booksy</a>',
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
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">3600 W 18th Ave, suite 37, Hialeah, FL</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=3600+W+18th+Ave,+Suite+37,+Hialeah,+FL" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes de 9am a 4pm, y martes a viernes de 9am a 6pm." data-en="By appointment via Booksy: pick the service, day and time, confirmation is instant. Monday 9am to 4pm, and Tuesday to Friday 9am to 6pm.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes de 9am a 4pm, y martes a viernes de 9am a 6pm.</p>',
)

OLD_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@_lashbloom</a>'
)
NEW_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los diseños más recientes de Brigytte y escribe por DM cualquier duda antes de tu cita." data-en="See Brigytte\'s latest designs and DM any questions before your appointment.">Mira los diseños más recientes de Brigytte y escribe por DM cualquier duda antes de tu cita.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@nails_by_brigytte</a>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_SOCIAL)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Nails by Brigytte, 3600 W 18th Ave, suite 37, Hialeah FL"\n          src="https://www.google.com/maps?q=25.854863855114985,-80.31924804345476&output=embed"',
)

# ---------- 18. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima manicura" data-en="Your next manicure">Tu próxima manicura</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure, tu builder gel o el diseño que ya quieres estrenar con Brigytte en Hialeah." data-en="Book online in seconds: your manicure, your builder gel set, or the design you have been wanting to try with Brigytte in Hialeah.">Reserva online en segundos: tu manicure, tu builder gel o el diseño que ya quieres estrenar con Brigytte en Hialeah.</p>',
)

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-2.jpg" alt="Logo de neón redondo de Nails by Brigytte" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Salón de uñas en Hialeah, FL. Atención con cita previa.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>3600 W 18th Ave, suite 37, Hialeah, FL</p>',
)
OLD_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>'
)
NEW_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @nails_by_brigytte</a></p>'
)
rep(OLD_FOOT_SOCIAL, NEW_FOOT_SOCIAL)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

print("PARTE 4 OK (ubicacion, cta-final, footer)")

# ---------- 20. Paleta: plum-pink -> rosa polvo premium (a8536e/c47f95/f2dde3) ----------
# Proteger badge dorado de Merktop (bloque CSS completo).
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)
# La unica referencia de color de marca Merktop fuera del bloque CSS protegido es el texto
# "Powered by Merktop" del footer (#f4eee2, crema neutro): se deja intacta.
assert '#f4eee2' in h


def hex_to_rgb(hx):
    hx = hx.lstrip('#')
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return ''.join(f'{max(0, min(255, round(c))):02x}' for c in rgb)


# Derivamos el shift (hue/sat/light) a partir del cambio de accent-deep real
# a04a72 (plum-pink original) -> a8536e (rosa polvo premium pedido) y lo
# aplicamos proporcionalmente a TODOS los tonos derivados del esqueleto.
_old_deep = hex_to_rgb('a04a72')
_new_deep = hex_to_rgb('a8536e')
_oh, _ol, _os = colorsys.rgb_to_hls(*(c / 255 for c in _old_deep))
_nh, _nl, _ns = colorsys.rgb_to_hls(*(c / 255 for c in _new_deep))
HUE_DELTA = _nh - _oh
SAT_SCALE = (_ns / _os) if _os > 0 else 1.0
LIGHT_SCALE = (_nl / _ol) if _ol > 0 else 1.0


def shift_hex(old_hex):
    r, g, b = hex_to_rgb(old_hex)
    hh, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hh = (hh + HUE_DELTA) % 1.0
    ss = max(0.0, min(1.0, ss * SAT_SCALE))
    ll = max(0.0, min(1.0, ll * LIGHT_SCALE))
    r2, g2, b2 = colorsys.hls_to_rgb(hh, ll, ss)
    return rgb_to_hex((r2 * 255, g2 * 255, b2 * 255))


def shift_rgb_tuple(old_tuple):
    r, g, b = old_tuple
    hh, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hh = (hh + HUE_DELTA) % 1.0
    ss = max(0.0, min(1.0, ss * SAT_SCALE))
    ll = max(0.0, min(1.0, ll * LIGHT_SCALE))
    r2, g2, b2 = colorsys.hls_to_rgb(hh, ll, ss)
    return tuple(round(c * 255) for c in (r2, g2, b2))


HEX_LIST = [
    'a04a72', 'c47a9c', '5c2140', 'f0bed7', 'faf2f6', '8a5573', 'f3e0ea',
    'd9a8c2', '7d3457', '5f2c48', '33222c', 'fbf3f8', 'fbeff5', 'f8dfeb',
    'f6f1ea', 'f2d5e3', 'f2cfe0', 'efd0e0', 'e5c1d4', 'dc9dbe', 'd3a2bc',
    'c9789f', 'b25a85', '2a1722', '1f0f18', '1c0f16',
]
SHIFTED = {}
for old in HEX_LIST:
    new = shift_hex(old)
    SHIFTED[old] = new
    assert f"#{old}" in h or old.upper() in h, f"hex no encontrado: {old}"
    h = h.replace(f"#{old}", f"#{new}")
    h = h.replace(f"#{old.upper()}", f"#{new}")

# El shift HSL clampea a blanco puro / casi-blanco los tonos ya muy claros
# (bg y bg-2/accent-soft): forzamos estos dos a la crema rosa polvo pedida
# en vez de dejar el clamp accidental.
BG_FORCE = {"faf2f6": "faf3f4", "f3e0ea": "f2dde3"}
for old_key, forced_new in BG_FORCE.items():
    computed = SHIFTED[old_key]
    if f"#{computed}" in h:
        h = h.replace(f"#{computed}", f"#{forced_new}")
    if f"#{computed.upper()}" in h:
        h = h.replace(f"#{computed.upper()}", f"#{forced_new}")

RGBA_LIST = [
    (160, 74, 114), (51, 34, 44), (240, 190, 215), (70, 25, 50),
    (250, 242, 246), (125, 52, 87), (253, 246, 250), (40, 16, 30),
    (233, 205, 186), (185, 138, 128),
]
# Igual que con los hex casi-blancos: forzamos manualmente los rgb que el
# shift HSL clampea a blanco puro, para no perder la crema rosa polvo.
RGB_FORCE = {(250, 242, 246): (250, 243, 244), (253, 246, 250): (253, 244, 247)}
for old_t in RGBA_LIST:
    old_s = ','.join(str(v) for v in old_t)
    new_t = RGB_FORCE.get(old_t) or shift_rgb_tuple(old_t)
    new_s = ','.join(str(v) for v in new_t)
    assert old_s in h, f"rgb no encontrado: {old_s}"
    h = h.replace(old_s, new_s)

# Forzamos que las 3 variables de acento clave queden EXACTAS al brief
# (accent-deep/mid/soft), sin depender de redondeos del shift HSL.
rep('--accent-deep: ' + '#' + shift_hex('a04a72') + ';', '--accent-deep: #a8536e;')
rep('--accent-mid: ' + '#' + shift_hex('c47a9c') + ';', '--accent-mid: #c47f95;')

# Restaurar el badge dorado protegido.
h = h.replace("@@BADGE@@", badge_block, 1)

print("PARTE 5 OK (paleta rosa polvo premium, badge dorado protegido)")

open("output/nails-by-brigytte-hialeah/index.html", "w").write(h)
print("DONE: output/nails-by-brigytte-hialeah/index.html escrito")
