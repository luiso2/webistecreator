import re

h = open("output/lizt-nails-miami/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Lizt Nails Miami"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1483661_lizt-nails-miami_nail-salon_15889_miami"
IG_OLD = "https://www.instagram.com/_lashbloom/"
IG_NEW = "https://www.instagram.com/lizt_nails_miami/"
HANDLE_OLD = "@_lashbloom"
HANDLE_NEW = "@lizt_nails_miami"
FB_NEW = "https://facebook.com/profile.php?id=61575994346288"

# ---------- 1. <html lang> + idioma por defecto ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 2. HEAD: title/meta/og/favicon ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Salón de Uñas en Miami, FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Miami FL: manicure, pedicura, acrílico y diseños de uñas con un 5.0 perfecto en 58 reseñas de Booksy. Reserva en línea." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Salón de Uñas en Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure, pedicura y acrílico. 5.0 en Booksy. Reserva en línea." />',
)
# og:image ya apunta a assets/raw/bk-6.jpg, coincide con nuestra foto hero: sin cambios de ruta.
rep(
    '<meta name="theme-color" content="#f6f1ea" />',
    '<meta name="theme-color" content="#fdf1ec" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-9.jpg" />',
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
    "name": "Lizt Nails Miami",
    "description": "Salón de uñas en Miami, FL: manicure, pedicura, acrílico, rubber base y diseños de uñas hechos por Liz.",
    "address": { "@type": "PostalAddress", "streetAddress": "11031 NW 7th St, Apto 203", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33172", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.776470, "longitude": -80.374540 },
    "sameAs": ["https://booksy.com/en-us/1483661_lizt-nails-miami_nail-salon_15889_miami", "https://www.instagram.com/lizt_nails_miami/", "https://facebook.com/profile.php?id=61575994346288"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "58", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure regular" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel manicure & Spa pedicure" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Full Set" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Rubber base" } }
    ] }
  }
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. URLs globales: Booksy, Instagram, handle ----------
repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_OLD, IG_NEW)
repall(HANDLE_OLD, HANDLE_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LN</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    f'<img src="assets/raw/bk-9.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lizt <span class="text-[color:var(--accent-deep)]">Nails Miami</span></span>',
)

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Salón de Uñas" data-en="Miami, FL · Nail Salon">Miami, FL · Nail Salon</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas hechas con amor, en el corazón de Miami." data-en="Nails made with love, in the heart of Miami.">Nails made with love, in the heart of Miami.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas de salón," data-en="Salon nails,">Salon nails,</span><br /><span data-es="hechas para " data-en="made to ">made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicure, pedicura, acrílico, rubber base y diseños de uñas hechos a mano por Liz en Miami. Una artista, mucho cariño por el detalle, y un 5.0 perfecto en Booksy." data-en="Manicures, pedicures, acrylics, rubber base and hand painted nail art by Liz in Miami. One artist, real attention to detail, and a perfect 5.0 on Booksy.">Manicures, pedicures, acrylics, rubber base and hand painted nail art by Liz in Miami. One artist, real attention to detail, and a perfect 5.0 on Booksy.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 58 reseñas en Booksy" data-en="5.0 · 58 reviews on Booksy">5.0 · 58 reviews on Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-6.jpg" alt="Manicura con diseño floral 3D en rosa nude, flores blancas y perlas doradas" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg">Acrylic Full Set</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$65 · 2h" data-en="$65 · 2h">$65 · 2h</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="58">58</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicure <span class="text-shine">&amp;</span> Acrílico</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel · Rubber Base · Nail Art" data-en="Gel · Rubber Base · Nail Art">Gel · Rubber Base · Nail Art</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">We speak</span> <span class="text-shine" data-es="Español" data-en="Spanish">Spanish</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Warm, personal care</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">11031 NW 7th St</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Gel Manicure"),
    ("Hybrid Set", "Spa Pedicure"),
    ("Volume Set", "Acrylic Set"),
    ("Mega Volume", "Rubber Base"),
    ("Bottom Lashes", "Nail Art"),
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
    '<img src="assets/raw/bk-9.jpg" alt="Manicura clásica en francés blanco, uñas limpias y naturales" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Manicura elegante en tono vino oscuro sobre fondo de piel blanca" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una sola artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="con mucho amor por el detalle" data-en="with real love for detail">with real love for detail</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Lizt Nails Miami es el salón de una sola artista: Liz, una mujer emprendedora que atiende cada cita ella misma. Cada set se piensa contigo, uña por uña, ya sea un manicure clásico, un acrílico con diseño o una pedicura spa completa." data-en="Lizt Nails Miami is the studio of one artist: Liz, an entrepreneurial woman who takes every appointment herself. Every set is planned with you, nail by nail, whether it is a classic manicure, a designed acrylic set or a full spa pedicure.">Lizt Nails Miami is the studio of one artist: Liz, an entrepreneurial woman who takes every appointment herself. Every set is planned with you, nail by nail, whether it is a classic manicure, a designed acrylic set or a full spa pedicure.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 58 reseñas verificadas en Booksy, y clientas que aseguran que sus uñas nunca lucieron mejor." data-en="The result: a perfect 5.0 across 58 verified reviews on Booksy, and clients who say their nails have never looked better.">The result: a perfect 5.0 across 58 verified reviews on Booksy, and clients who say their nails have never looked better.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="58">58</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
# El chip "1:1 · Atencion personal" ya calza perfecto (salon de una sola artista): sin cambios.
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    f'<img src="assets/raw/bk-9.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Liz · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>',
)

# ---------- 11. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio, manicure, pedicura o acrílico, con precio y duración claros en Booksy, y confirmas al instante." data-en="Pick your service, manicure, pedicure or acrylic, with clear price and duration on Booksy, and confirm instantly.">Pick your service, manicure, pedicure or acrylic, with clear price and duration on Booksy, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Elige tu diseño" data-en="Choose your design">Choose your design</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma, largo y color: clásico, francés, ruso o un diseño hecho a mano, tú decides el estilo." data-en="Shape, length and color: classic, French, Russian or a hand painted design, you choose the style.">Shape, length and color: classic, French, Russian or a hand painted design, you choose the style.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos y pies al detalle" data-en="Hands &amp; feet, detailed">Hands &amp; feet, detailed</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cutícula, esmaltado en gel, rubber base o acrílico: cada paso se hace con calma y con cariño por el detalle." data-en="Filing, cuticle care, gel, rubber base or acrylic polish: every step done calmly and with real attention to detail.">Filing, cuticle care, gel, rubber base or acrylic polish: every step done calmly and with real attention to detail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">You leave ready</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu manicure o pedicura terminada, lista para durar semanas, tal como cuentan sus reseñas en Booksy." data-en="You leave with your manicure or pedicure finished, ready to last for weeks, just as her Booksy reviews describe.">You leave with your manicure or pedicure finished, ready to last for weeks, just as her Booksy reviews describe.</p>',
)

# ---------- 12. SERVICIOS: grid completo (regex, reemplazo entero) ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure" data-en="Manicure">Manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure con esmaltado en gel de larga duración. También disponible: manicure regular $20 (30min) y manicura rusa $30 (30min)." data-en="Manicure with long lasting gel polish. Also available: regular manicure $20 (30min) and Russian manicure $30 (30min).">Manicure with long lasting gel polish. Also available: regular manicure $20 (30min) and Russian manicure $30 (30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrílico, el lienzo perfecto para cualquier diseño (el precio varía según el largo). También: acrylic refill $50." data-en="Full acrylic set, the perfect canvas for any design (price varies by length). Also: acrylic refill $50.">Full acrylic set, the perfect canvas for any design (price varies by length). Also: acrylic refill $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Spa pedicure (gel color)" data-en="Spa pedicure (gel color)">Spa pedicure (gel color)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura spa completa con esmaltado en gel. También: Lizt signature foot spa (gel color) $50." data-en="Full spa pedicure with gel polish. Also: Lizt signature foot spa (gel color) $50.">Full spa pedicure with gel polish. Also: Lizt signature foot spa (gel color) $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Combos y extras" data-en="Combos &amp; extras">Combos &amp; extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel manicure &amp; Spa pedicure" data-en="Gel manicure &amp; Spa pedicure">Gel manicure &amp; Spa pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo de manos y pies en una sola cita. También: gel manicure &amp; gel pedicure $50, rubber base $40 (1h), rubber base &amp; spa pedicure $55 (1h40) y luminary system $60 (1h)." data-en="The hands and feet combo in one visit. Also: gel manicure &amp; gel pedicure $50, rubber base $40 (1h), rubber base &amp; spa pedicure $55 (1h40) and luminary system $60 (1h).">The hands and feet combo in one visit. Also: gel manicure &amp; gel pedicure $50, rubber base $40 (1h), rubber base &amp; spa pedicure $55 (1h40) and luminary system $60 (1h).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end() :]

# ---------- 13. Subtitulo y nota de servicios ----------
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata.</p>',
)
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Precios exactos y disponibilidad en tiempo real en Booksy. El precio del acrílico varía según el largo." data-en="Exact prices and real time availability on Booksy. Acrylic pricing varies by length.">Exact prices and real time availability on Booksy. Acrylic pricing varies by length.</span></p>',
)

# ---------- 14. GALERIA: eyebrow/H2 + grid completo (regex, reemplazo entero) ----------
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño floral 3D en rosa nude" data-en="3D floral design in nude pink">3D floral design in nude pink</span><img src="assets/raw/bk-6.jpg" alt="Manicura con flores blancas en 3D y perlas doradas sobre base rosa nude" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Vino tinto con anillos dorados" data-en="Burgundy set with gold rings">Burgundy set with gold rings</span><img src="assets/raw/bk-14.jpg" alt="Manicura en tono vino oscuro con detalles de leopardo y anillos dorados" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Lavanda mate" data-en="Matte lavender">Matte lavender</span><img src="assets/raw/bk-4.jpg" alt="Manicura mate en color lavanda con pulsera dorada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Diseño floral en azul" data-en="Blue floral detail">Blue floral detail</span><img src="assets/raw/bk-8.jpg" alt="Uñas acrílicas largas con diseño floral azul, mármol y piedras" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Francés con anillos" data-en="French tips with rings">French tips with rings</span><img src="assets/raw/bk-15.jpg" alt="Manicura francesa en blanco y nude con anillos dorados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Rojo clásico" data-en="Classic red">Classic red</span><img src="assets/raw/bk-3.jpg" alt="Manicura roja clásica en forma almendrada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

# ---------- 15. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 58 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 58 verified reviews on Booksy">5.0 out of 5 · 58 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mis uñas pasaron de 0 a 100 desde que empecé a atenderme con Liz💅🏻✨ Ya tengo casi un año con ella y lo único de lo que me arrepiento es de no haberla encontrado antes. Siempre me las deja hermosas, cuidadas y, lo mejor de todo… naturales👀"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Veronica</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mis uñas 💅 han dado un cambio espectacular, como nunca,me encantannnnnn🥰🥰🥰🥰"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Zadis R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"AMEEEE mis uñas 💕 excelente trabajo salí con uñas que no me imaginé 💕"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Nathasha R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 58 reseñas en Booksy" data-en="Read all 58 reviews on Booksy">Read all 58 reviews on Booksy</a>',
)

# ---------- 16. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami, FL</span></h2>',
)

OLD_LOC_ADDR = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_ADDR = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">11031 NW 7th St, Apto 203, Miami, FL 33172</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=11031+NW+7th+St,+Miami,+FL+33172" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_ADDR, NEW_LOC_ADDR)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto de lunes a viernes de 9:00 am a 7:00 pm y sábados de 7:30 am a 6:00 pm." data-en="By appointment via Booksy: pick the service, day and time, confirmation is instant. Open Monday to Friday 9:00 am to 7:00 pm and Saturdays 7:30 am to 6:00 pm.">By appointment via Booksy: pick the service, day and time, confirmation is instant. Open Monday to Friday 9:00 am to 7:00 pm and Saturdays 7:30 am to 6:00 pm.</p>',
)

OLD_LOC_IG = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">' + HANDLE_NEW + "</a>"
)
NEW_LOC_IG = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos más recientes de Liz y escribe por DM cualquier duda antes de tu cita." data-en="See Liz\'s latest work and DM any questions before your appointment.">See Liz\'s latest work and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">' + HANDLE_NEW + "</a>"
)
rep(OLD_LOC_IG, NEW_LOC_IG)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: {NAME}, 11031 NW 7th St, Miami FL"\n          src="https://www.google.com/maps?q=11031+NW+7th+St,+Miami,+FL+33172&output=embed"',
)

# ---------- 17. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima manicura" data-en="Your next manicure">Your next manicure</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure, pedicura, acrílico o el diseño que ya quieres estrenar." data-en="Book online in seconds: your manicure, pedicure, acrylic set or the design you have been wanting to try.">Book online in seconds: your manicure, pedicure, acrylic set or the design you have been wanting to try.</p>',
)

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-9.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami, FL. Atención con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Nail salon in Miami, FL. By appointment only.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>11031 NW 7th St, Miami, FL 33172</p>',
)
OLD_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · ' + HANDLE_NEW + "</a></p>"
)
NEW_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · ' + HANDLE_NEW + '</a></p>\n'
    '        <p><a href="' + FB_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Facebook</a></p>'
)
rep(OLD_FOOT_SOCIAL, NEW_FOOT_SOCIAL)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 19. PALETA: plum-pink -> peach-coral calido ----------
# accent-deep #a04a72 -> #d97a5a · accent-mid #c47a9c -> #eda183
# El dorado del merktop-badge (#D4A84B y rgba(212,168,75,...)) y los neutrales
# (blanco/negro puros, y el fondo oscuro del badge) NO se tocan.
HEX_PAIRS = [
    ("#a04a72", "#d97a5a"),  # accent-deep
    ("#c47a9c", "#eda183"),  # accent-mid
    ("#5c2140", "#7a3823"),  # btn-3d / book-float sombra oscura
    ("#f0bed7", "#f3c9a8"),  # dark-band rosa claro -> durazno claro
    ("#faf2f6", "#fdf1ec"),  # bg / dark-band ink blanco calido
    ("#8a5573", "#a3653f"),  # dark-band btn-3d sombra media
    ("#f3e0ea", "#f8ddd0"),  # bg-2 / accent-soft
    ("#d9a8c2", "#e3a688"),  # orb-b / dark-band text-shine medio
    ("#7d3457", "#a8492f"),  # btn-3d oscuro / scroll-progress inicio
    ("#5f2c48", "#8a3f2a"),  # text-shine oscuro / step-num oscuro
    ("#33222c", "#332420"),  # ink / dark-band btn-3d color
    ("#fbf3f8", "#fdf1ea"),  # tile-cap color texto
    ("#fbeff5", "#fdf1e8"),  # dark-band btn-3d gradiente inicio
    ("#f8dfeb", "#fbe8d8"),  # dark-band text-shine 30%
    ("#f2d5e3", "#f7d9c4"),  # orb-a
    ("#f2cfe0", "#f6d9bd"),  # dark-band text-shine 100%
    ("#efd0e0", "#f5ddc9"),  # dark-band btn-3d gradiente 48%
    ("#e5c1d4", "#edc7ab"),  # orb-c
    ("#dc9dbe", "#f2b48f"),  # scroll-progress fin
    ("#d3a2bc", "#dba98c"),  # dark-band btn-3d gradiente 100%
    ("#c9789f", "#f2b48f"),  # text-shine 30%
    ("#b25a85", "#e2926a"),  # text-shine 100%
    ("#2a1722", "#241712"),  # CTA final bg inicio
    ("#1f0f18", "#180f0b"),  # CTA final bg fin
    ("#1c0f16", "#1a100b"),  # footer bg
]
for old, new in HEX_PAIRS:
    assert old in h, f"paleta: no se encontro {old}"
    h = h.replace(old, new)

# Tripletas rgb dentro de rgba(...): el reemplazo cubre TODOS los alphas de una vez.
RGB_TRIPLES = [
    ("160,74,114", "217,122,90"),   # accent-deep rgb
    ("51,34,44", "51,36,32"),       # ink rgb (giro calido)
    ("70,25,50", "90,40,20"),       # btn-3d sombra oscura
    ("240,190,215", "243,201,168"), # dark-band durazno claro
    ("125,52,87", "163,101,63"),    # dark-band btn-3d sombra media
    ("233,205,186", "237,161,131"), # dark-band accent-ghost
    ("185,138,128", "227,166,136"), # dark-band orb-b
    ("253,246,250", "253,244,238"), # surface
    ("250,242,246", "253,241,236"), # nav-scrolled / dark-band ink
    ("40,16,30", "40,20,14"),       # tile-cap gradiente oscuro
]
for old, new in RGB_TRIPLES:
    assert old in h, f"paleta rgb: no se encontro {old}"
    h = h.replace(old, new)

# Verificacion: el dorado del badge Merktop sigue intacto.
assert "#D4A84B" in h, "se perdio el dorado del merktop-badge"
assert "rgba(212,168,75," in h, "se perdio el rgba dorado del merktop-badge"

open("output/lizt-nails-miami/index.html", "w").write(h)
print("BUILD OK: lizt-nails-miami")
