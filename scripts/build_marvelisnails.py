import re
import colorsys

h = open("output/marvelisnails/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Marvelis’ Nails"  # Marvelis' Nails (apostrofe curvo, igual al data.json)
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1475947_marvelis-nails_nail-salon_15886_hialeah"
FB_OLD = "https://www.instagram.com/_lashbloom/"
FB_NEW = "https://www.facebook.com/MarvelisDeulofeu/"
FB_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M22 12.06C22 6.48 17.52 2 11.94 2 6.35 2 1.87 6.48 1.87 12.06c0 5.02 3.66 9.19 8.44 9.94v-7.03H7.9v-2.91h2.41V9.97c0-2.38 1.42-3.7 3.6-3.7 1.04 0 2.13.19 2.13.19v2.34h-1.2c-1.18 0-1.55.74-1.55 1.5v1.8h2.64l-.42 2.91h-2.22V22c4.78-.75 8.44-4.92 8.44-9.94Z"/></svg>'

# ---------- 1. <html lang> + idioma por defecto ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 2. HEAD: title/meta/og/favicon ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Salón de Uñas en Hialeah, FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Hialeah FL: manicure, pedicura, acrílico, gel X y diseños de uñas con un 5.0 perfecto en 95 reseñas de Booksy. Reserva en línea." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Salón de Uñas en Hialeah, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure, pedicura y acrílico. 5.0 en Booksy. Reserva en línea." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-8.jpg" />',
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
    "name": "Marvelis’ Nails",
    "description": "Salón de uñas en Hialeah, FL: manicure, pedicura, acrílico, gel X y diseños de uñas.",
    "address": { "@type": "PostalAddress", "streetAddress": "267 E 49th St #3", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33013", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1475947_marvelis-nails_nail-salon_15886_hialeah", "https://www.facebook.com/MarvelisDeulofeu/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "95", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "32", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel manicure" } },
      { "@type": "Offer", "price": "54", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic full set" } },
      { "@type": "Offer", "price": "27", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Basic pedicure" } },
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure and pedicure básico" } }
    ] }
  }
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. Booksy URL global (13 usos) + Instagram->Facebook (icono + href, caso por caso) ----------
repall(BOOKSY_OLD, BOOKSY_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">MN</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    f'<img src="assets/raw/bk-8.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Marvelis’ <span class="text-[color:var(--accent-deep)]">Nails</span></span>',
)

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salón de Uñas" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas que cuentan tu historia." data-en="Nails that tell your story.">Nails that tell your story.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas hermosas," data-en="Beautiful nails,">Beautiful nails,</span><br /><span data-es="hechas para " data-en="made to ">made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    f'data-es="Manicure, pedicura, acrílico, gel X y diseños de uñas hechos por Marvelis en Hialeah. Un salón de una sola artista, con clientas que confian en su trabajo desde hace años y un 5.0 perfecto en Booksy." data-en="Manicures, pedicures, acrylics, gel X and nail art by Marvelis in Hialeah. A one artist studio trusted by regulars for years, with a perfect 5.0 on Booksy.">Manicures, pedicures, acrylics, gel X and nail art by Marvelis in Hialeah. A one artist studio trusted by regulars for years, with a perfect 5.0 on Booksy.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 95 reseñas en Booksy" data-en="5.0 · 95 reviews on Booksy">5.0 · 95 reviews on Booksy</span>',
)
OLD_HERO_BTN2 = (
    '<a href="' + FB_OLD + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "            @_lashbloom\n"
    "          </a>"
)
NEW_HERO_BTN2 = (
    '<a href="' + FB_NEW + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    "            " + FB_ICON + "\n"
    '            <span data-es="Facebook" data-en="Facebook">Facebook</span>\n'
    "          </a>"
)
rep(OLD_HERO_BTN2, NEW_HERO_BTN2)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Uñas almendra en degradado rojo a nude con brillo dorado, sobre fondo de perlas" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg">Acrylic full set</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$54 · 2h" data-en="$54 · 2h">$54 · 2h</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="95">95</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicure <span class="text-shine">&amp;</span> Acrylics</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel · Acrílico · Diseños" data-en="Gel · Acrylic · Nail art">Gel · Acrylic · Nail art</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Se habla <span class="text-shine" data-es="Español" data-en="Spanish">Spanish</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Warm, personal care</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">267 E 49th St #3</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Gel Manicure"),
    ("Hybrid Set", "Acrylic Full Set"),
    ("Volume Set", "Basic Pedicure"),
    ("Mega Volume", "Russian Manicure"),
    ("Bottom Lashes", "Nail Designs"),
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
    '<img src="assets/raw/bk-9.jpg" alt="Manicura corta en rosa envejecido con línea blanca estilo francés" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="Uñas cuadradas nude con línea blanca fina estilo francés y un pequeño strass" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una sola artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="mil diseños distintos" data-en="a thousand designs">a thousand designs</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    f'data-es="{NAME} es el salón de una sola artista en Hialeah: Marvelis. Cada set se piensa contigo, uña por uña, ya sea un gel manicure clásico, un acrílico con diseño o una pedicura completa." data-en="{NAME} is a one artist studio in Hialeah: Marvelis. Every set is planned with you, nail by nail, whether it is a classic gel manicure, a designed acrylic set or a full pedicure.">{NAME} is a one artist studio in Hialeah: Marvelis. Every set is planned with you, nail by nail, whether it is a classic gel manicure, a designed acrylic set or a full pedicure.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 95 reseñas verificadas en Booksy, y una clientela que vuelve una y otra vez por su manicure, pedicura o set de acrílico." data-en="The result: a perfect 5.0 across 95 verified reviews on Booksy, and clients who come back again and again for their manicure, pedicure or acrylic set.">The result: a perfect 5.0 across 95 verified reviews on Booksy, and clients who come back again and again for their manicure, pedicure or acrylic set.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="95">95</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Nail Art</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Diseños a mano" data-en="Hand painted">Hand painted</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    f'<img src="assets/raw/bk-8.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Marvelis · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>',
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
    '<h3 class="font-display text-xl mb-3" data-es="Manos y pies al detalle" data-en="Hands &amp; feet, detailed">Hands &amp; feet, detailed</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cuticula, esmaltado en gel o acrílico: cada paso se hace con calma y cuidado por el detalle." data-en="Filing, cuticle care, gel or acrylic polish: every step done calmly and with attention to detail.">Filing, cuticle care, gel or acrylic polish: every step done calmly and with attention to detail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">You leave ready</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu manicure o pedicura terminada, lista para durar semanas, tal como cuentan las reseñas." data-en="You leave with your manicure or pedicure finished, ready to last for weeks, just as her reviews describe.">You leave with your manicure or pedicure finished, ready to last for weeks, just as her reviews describe.</p>',
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
          <h3 class="font-display text-2xl leading-snug mb-3">Gel manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure con esmaltado en gel de larga duración. También disponible: basic manicure $23, French manicure $9 y Russian manicure $36." data-en="Manicure with long lasting gel polish. Also available: basic manicure $23, French manicure $9 and Russian manicure $36.">Manicure with long lasting gel polish. Also available: basic manicure $23, French manicure $9 and Russian manicure $36.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$32</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic full set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrílico, la base perfecta para cualquier diseño. También: acrylic overlay $45 y acrylic removal $18." data-en="Full acrylic set, the perfect base for any design. Also: acrylic overlay $45 and acrylic removal $18.">Full acrylic set, the perfect base for any design. Also: acrylic overlay $45 and acrylic removal $18.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$54</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Basic pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa para pies suaves y cuidados. También: kids pedicure $23, callus removal $14 y paraffin treatment $9." data-en="Full pedicure for soft, cared for feet. Also: kids pedicure $23, callus removal $14 and paraffin treatment $9.">Full pedicure for soft, cared for feet. Also: kids pedicure $23, callus removal $14 and paraffin treatment $9.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$27</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Combos y extras" data-en="Combos &amp; extras">Combos &amp; extras</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure and pedicure básico" data-en="Manicure and pedicure básico">Manicure and pedicure básico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo de manos y pies en una sola cita. También: nail designs $9 y gel x $59 para un acabado sin límites." data-en="The hands and feet combo in one visit. Also: nail designs $9 and gel x $59 for a limitless finish.">The hands and feet combo in one visit. Also: nail designs $9 and gel x $59 for a limitless finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      """

h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end() :]

# ---------- 13. Eyebrow/H2/subtitulo de servicios ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="estilo" data-en="style">style</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.</p>',
)

# ---------- 14. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Más de 25 servicios, con precios exactos y disponibilidad en tiempo real en Booksy." data-en="More than 25 services, with exact prices and real time availability on Booksy.">More than 25 services, with exact prices and real time availability on Booksy.</span></p>',
)

# ---------- 15. GALERIA: eyebrow, H2, link social, grid completo ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>',
)
OLD_GAL_SOCIAL = (
    '<a href="' + FB_OLD + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "          @_lashbloom\n"
    "        </a>"
)
NEW_GAL_SOCIAL = (
    '<a href="' + FB_NEW + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    "          " + FB_ICON + "\n"
    '          <span data-es="Facebook" data-en="Facebook">Facebook</span>\n'
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño coffin con lazo 3D" data-en="Coffin set with a 3D bow">Coffin set with a 3D bow</span><img src="assets/raw/bk-15.jpg" alt="Uñas coffin largas en francés rosa y blanco con un lazo 3D y una perla" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Diseño floral en rojo" data-en="Red floral design">Red floral design</span><img src="assets/raw/bk-13.jpg" alt="Uñas almendra en rojo vino con diseño floral blanco y strass" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalles dorados" data-en="Golden line art">Golden line art</span><img src="assets/raw/bk-11.jpg" alt="Uñas almendra nude con lineas doradas y una uña acento amarilla" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Francés con flor de perlas" data-en="French with a pearl flower">French with a pearl flower</span><img src="assets/raw/bk-4.jpg" alt="Uñas cuadradas en francés blanco con un diseño floral delicado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Verde oliva" data-en="Olive green">Olive green</span><img src="assets/raw/bk-12.jpg" alt="Uñas cortas en verde oliva con una uña acento con hojas doradas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Pedicura con flores" data-en="Floral pedicure">Floral pedicure</span><img src="assets/raw/bk-6.jpg" alt="Pedicura en francés blanco con flores y strass" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

# ---------- 16. MARQUEE reverse (mismas 6 palabras, ya cubierto arriba con count==4) ----------
# (el bucle MQ de la parte 1 ya cubrio las 4 apariciones de cada palabra en ambos marquees)

# ---------- 17. OPINIONES ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
)
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 95 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 95 verified reviews on Booksy">5.0 out of 5 · 95 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Su trabajo es hermoso y duradero, siempre te voy a eleguir Marvelis. Este es mi trabajo 1 mes"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maria D…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encantó mi manicura! El servicio fue excelente, el personal fue muy amable y atento, y el resultado quedó impecable. Se nota el cuidado por los detalles y la calidad del trabajo. Sin duda volveré y lo recomiendo al 100 %."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lukas D…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"🤍"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ana J…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 95 reseñas en Booksy" data-en="Read all 95 reviews on Booksy">Read all 95 reviews on Booksy</a>',
)

# ---------- 18. UBICACION ----------
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
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">267 E 49th St #3, Hialeah, FL 33013</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=267+E+49th+St+%233,+Hialeah,+FL+33013" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto los 7 días, de 9:00 am a 7:00 pm." data-en="By appointment via Booksy: pick the service, day and time, confirmation is instant. Open 7 days a week, 9:00 am to 7:00 pm.">By appointment via Booksy: pick the service, day and time, confirmation is instant. Open 7 days a week, 9:00 am to 7:00 pm.</p>',
)

OLD_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + FB_OLD + '" target="_blank" rel="noopener">@_lashbloom</a>'
)
NEW_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Facebook</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos más recientes de Marvelis y escribe cualquier duda antes de tu cita." data-en="See Marvelis\' latest work and reach out with any questions before your appointment.">See Marvelis\' latest work and reach out with any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + FB_NEW + '" target="_blank" rel="noopener">Facebook · Marvelis Deulofeu</a>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_SOCIAL)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Marvelis’ Nails, 267 E 49th St #3, Hialeah FL"\n          src="https://www.google.com/maps?q=267+E+49th+St+%233,+Hialeah,+FL+33013&output=embed"',
)

# ---------- 19. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu manicure nuevo" data-en="Your next manicure">Your next manicure</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure, pedicura, acrílico o el diseño que ya quieres estrenar." data-en="Book online in seconds: your manicure, pedicure, acrylic set or the design you have been wanting to try.">Book online in seconds: your manicure, pedicure, acrylic set or the design you have been wanting to try.</p>',
)
rep(
    'data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="'
    + FB_OLD
    + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="'
    + FB_NEW
    + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Facebook" data-en="Follow on Facebook">Seguir en Facebook</a>',
)

# ---------- 20. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-8.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Nail salon in Hialeah, FL. By appointment only.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>267 E 49th St #3, Hialeah, FL 33013</p>',
)
OLD_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + FB_OLD + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>'
)
NEW_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + FB_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Facebook · Marvelis Deulofeu</a></p>'
)
rep(OLD_FOOT_SOCIAL, NEW_FOOT_SOCIAL)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 21. Paleta: rotacion de matiz uniforme (plum-pink -> terracota-rosa calido) ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

HUE_SHIFT = 42  # grados: plum-pink (~332) -> terracota-rosa calido (~14)


def shift_hex(hexcode):
    r = int(hexcode[0:2], 16) / 255.0
    g = int(hexcode[2:4], 16) / 255.0
    b = int(hexcode[4:6], 16) / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return "%02x%02x%02x" % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def shift_rgb_tuple(rr, gg, bb):
    r, g, b = rr / 255.0, gg / 255.0, bb / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def repl_hex(mo):
    return "#" + shift_hex(mo.group(1))


def repl_rgba(mo):
    rr, gg, bb = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
    alpha = mo.group(4)
    nr, ng, nb = shift_rgb_tuple(rr, gg, bb)
    if alpha is not None:
        return "rgba(%d,%d,%d,%s)" % (nr, ng, nb, alpha)
    return "rgb(%d,%d,%d)" % (nr, ng, nb)


h = re.sub(r"#([0-9a-fA-F]{6})\b", repl_hex, h)
h = re.sub(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)", repl_rgba, h)

h = h.replace("@@BADGE@@", badge_block, 1)

open("output/marvelisnails/index.html", "w").write(h)
print("PARTE 3 OK (opiniones, ubicacion, cta-final, footer, paleta)")
