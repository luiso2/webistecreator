import re
import colorsys

h = open("output/lorena-beauty/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Lorena Beauty"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1181951_lorena-beauty_nail-salon_15889_miami"
IG_OLD = "https://www.instagram.com/_lashbloom/"
IG_NEW = "https://www.instagram.com/lorena_beauty/"
IG_HANDLE_OLD = "@_lashbloom"
IG_HANDLE_NEW = "@lorena_beauty"

# ---------- 1. <html lang> + idioma por defecto (data.json language = "en", queda igual al esqueleto) ----------
# El esqueleto light-v2 ya es EN default -> no hace falta tocar <html lang> ni applyLang.

# ---------- 2. HEAD: title/meta/og/favicon ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Nail Salon in North Miami, FL | 5.0 on Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, North Miami FL: manicure, pedicure, acrylics, nail art, lash extensions and brows with a perfect 5.0 across 18 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Nail Salon in North Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure, pedicure, acrylics and nail art. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-15.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-14.jpg" />',
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
    "name": "Lorena Beauty",
    "description": "Nail salon in North Miami, FL: manicure, pedicure, acrylics, nail art, lash extensions, brows and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "1110 NE 213th Ter", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33179", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1181951_lorena-beauty_nail-salon_15889_miami", "https://www.instagram.com/lorena_beauty/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "18", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "07:00", "closes": "08:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "10:30", "closes": "17:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "07:00", "closes": "12:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail, lash and brow services", "itemListElement": [
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Regular Manicure" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Regular Pedicure" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Nails full set" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel mani y gel pedi" } },
      { "@type": "Offer", "price": "95", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Eyelash Extensions clasic full set" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brow lamination" } }
    ] }
  }
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. Booksy URL global + Instagram (misma plataforma, solo cambia handle/URL) ----------
repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_OLD, IG_NEW)
repall(IG_HANDLE_OLD, IG_HANDLE_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LB</span>')  # coincide: Lorena Beauty = LB
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    f'<img src="assets/raw/bk-14.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lorena <span class="text-[color:var(--accent-deep)]">Beauty</span></span>',
)

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="North Miami, FL · Salón de Uñas" data-en="North Miami, FL · Nail Salon">North Miami, FL · Nail Salon</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Belleza hecha a mano, cita tras cita." data-en="Handcrafted beauty, appointment after appointment.">Handcrafted beauty, appointment after appointment.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas, pestañas y cejas," data-en="Nails, lashes and brows,">Nails, lashes and brows,</span><br /><span data-es="hechas para " data-en="made to ">made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicure, pedicura, acrílico, nail art, extensiones de pestañas y cejas hechos por Lorena en North Miami. Un salón de una sola artista, con un 5.0 perfecto en Booksy." data-en="Manicures, pedicures, acrylics, nail art, lash extensions and brows by Lorena in North Miami. A one artist studio with a perfect 5.0 on Booksy.">Manicures, pedicures, acrylics, nail art, lash extensions and brows by Lorena in North Miami. A one artist studio with a perfect 5.0 on Booksy.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 18 reseñas en Booksy" data-en="5.0 · 18 reviews on Booksy">5.0 · 18 reviews on Booksy</span>',
)
rep(
    '            @lorena_beauty\n',
    '            <span data-es="Instagram" data-en="Instagram">Instagram</span>\n',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-15.jpg" alt="Bright yellow sunflower nail art manicure with a real sunflower in frame" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg">Gel mani y gel pedi</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$65 · 1h 10min" data-en="$65 · 1h 10min">$65 · 1h 10min</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="18">18</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Nails <span class="text-shine">&amp;</span> Lashes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicure · Pedicura · Acrílico" data-en="Manicure · Pedicure · Acrylic">Manicure · Pedicure · Acrylic</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">We speak</span> <span class="text-shine" data-es="Español" data-en="Spanish">Spanish</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Warm, personal care</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">North Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1110 NE 213th Ter</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Manicure"),
    ("Hybrid Set", "Pedicure"),
    ("Volume Set", "Acrylic Nails"),
    ("Mega Volume", "Nail Art"),
    ("Bottom Lashes", "Lash Extensions"),
    ("West Palm Beach, FL", "North Miami, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 10. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="French tip manicure with layered rings, elegant closeup" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Pink manicure closeup with hands clasped together, warm candid moment" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una sola artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="belleza sin límites" data-en="beauty without limits">beauty without limits</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    f'data-es="{NAME} es el salón de una sola artista en North Miami: Lorena Rodriguez. Cada cita se piensa contigo, ya sea un manicure clásico, un set de acrílico, extensiones de pestañas o un diseño de cejas." data-en="{NAME} is a one artist studio in North Miami: Lorena Rodriguez. Every appointment is planned around you, whether it is a classic manicure, an acrylic set, lash extensions or a brow design.">{NAME} is a one artist studio in North Miami: Lorena Rodriguez. Every appointment is planned around you, whether it is a classic manicure, an acrylic set, lash extensions or a brow design.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 18 reseñas verificadas en Booksy, y clientas que vuelven cita tras cita por su manicure, pedicura, pestañas o cejas." data-en="The result: a perfect 5.0 across 18 verified reviews on Booksy, and clients who come back appointment after appointment for their manicure, pedicure, lashes or brows.">The result: a perfect 5.0 across 18 verified reviews on Booksy, and clients who come back appointment after appointment for their manicure, pedicure, lashes or brows.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="18">18</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">41+</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Servicios" data-en="Services">Services</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    f'<img src="assets/raw/bk-14.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Lorena · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail &amp; lash artist">Nail &amp; lash artist</span></span>',
)

# ---------- 11. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, detalle" data-en="Your visit, detail">Your visit, detail</span> <span class="text-shine" data-es="por detalle" data-en="by detail">by detail</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy, manicure, pestañas o cejas, con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy, manicure, lashes or brows, with clear price and duration, and confirm instantly.">Pick your service on Booksy, manicure, lashes or brows, with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Elige tu estilo" data-en="Choose your style">Choose your style</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Color, largo y forma para tus uñas, o el efecto que buscas en pestañas y cejas: tú decides el estilo." data-en="Color, length and shape for your nails, or the look you want for lashes and brows: you choose the style.">Color, length and shape for your nails, or the look you want for lashes and brows: you choose the style.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos, pies y rostro al detalle" data-en="Hands, feet &amp; face, detailed">Hands, feet &amp; face, detailed</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cutícula, esmaltado en gel o acrílico, extensiones o cejas: cada paso se hace con calma y cuidado por el detalle." data-en="Filing, cuticle care, gel or acrylic polish, lash extensions or brows: every step done calmly and with attention to detail.">Filing, cuticle care, gel or acrylic polish, lash extensions or brows: every step done calmly and with attention to detail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">You leave ready</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un acabado que dura semanas, tal como cuentan sus reseñas verificadas en Booksy." data-en="You leave with a finish that lasts for weeks, just as her verified reviews on Booksy describe.">You leave with a finish that lasts for weeks, just as her verified reviews on Booksy describe.</p>',
)

# ---------- 12. SERVICIOS: 4 cards destacadas + menu completo agrupado (regex, reemplazo entero) ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure y pedicura" data-en="Manicure &amp; pedicure">Manicure &amp; pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel mani y gel pedi</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure y pedicura en gel de larga duración, en una sola cita. También: Regular Manicure $40, Gel mani $40 y Gel mani y reg pedi $50." data-en="Long lasting gel manicure and pedicure, in one visit. Also available: Regular Manicure $40, Gel mani $40 and Gel mani y reg pedi $50.">Long lasting gel manicure and pedicure, in one visit. Also available: Regular Manicure $40, Gel mani $40 and Gel mani y reg pedi $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 10min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Nails full set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrílico, la base perfecta para cualquier diseño. También: Poligel $50, Apres $60 y Refill $45." data-en="Full acrylic set, the perfect base for any design. Also available: Poligel $50, Apres $60 and Refill $45.">Full acrylic set, the perfect base for any design. Also available: Poligel $50, Apres $60 and Refill $45.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Regular Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa para pies suaves y cuidados. También: Gel Pedicure $45, Refill gel pedi $85 y Refill reg pedi $80." data-en="Full pedicure for soft, cared for feet. Also available: Gel Pedicure $45, Refill gel pedi $85 and Refill reg pedi $80.">Full pedicure for soft, cared for feet. Also available: Gel Pedicure $45, Refill gel pedi $85 and Refill reg pedi $80.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pestañas y cejas" data-en="Lashes &amp; brows">Lashes &amp; brows</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Eyelash Extensions classic full set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de extensiones clásicas. También: Diseño de cejas con wax y henna $55 y Brow lamination $50." data-en="Full classic lash extension set. Also available: Diseño de cejas con wax y henna $55 and Brow lamination $50.">Full classic lash extension set. Also available: Diseño de cejas con wax y henna $55 and Brow lamination $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$95</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>

      <!-- MENU COMPLETO, agrupado por categoria -->
      <div class="mt-8">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-6" data-es="El menú completo" data-en="The full menu">The full menu</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div class="glass glass-hover rounded-2xl p-6 reveal">
            <h4 class="font-display text-lg mb-4" data-es="Manicure y pedicura" data-en="Manicure &amp; pedicure">Manicure &amp; pedicure</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Regular Manicure</span><span class="whitespace-nowrap">$40</span></li>
              <li class="flex justify-between gap-3"><span>Gel Pedicure</span><span class="whitespace-nowrap">$45</span></li>
              <li class="flex justify-between gap-3"><span>Luminary</span><span class="whitespace-nowrap">$45</span></li>
              <li class="flex justify-between gap-3"><span>Refill reg pedi y wax</span><span class="whitespace-nowrap">$85</span></li>
            </ul>
            <p class="text-xs text-[color:var(--ink-40)] mt-4" data-es="y 7 más en Booksy" data-en="+7 more on Booksy">+7 more on Booksy</p>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:80ms">
            <h4 class="font-display text-lg mb-4" data-es="Acrílico y esmaltado" data-en="Acrylic &amp; enhancements">Acrylic &amp; enhancements</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Apres</span><span class="whitespace-nowrap">$60</span></li>
              <li class="flex justify-between gap-3"><span>Poligel</span><span class="whitespace-nowrap">$50</span></li>
              <li class="flex justify-between gap-3"><span>Refill</span><span class="whitespace-nowrap">$45</span></li>
            </ul>
            <p class="text-xs text-[color:var(--ink-40)] mt-4" data-es="y 2 más en Booksy" data-en="+2 more on Booksy">+2 more on Booksy</p>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:140ms">
            <h4 class="font-display text-lg mb-4" data-es="Extensiones de pestañas" data-en="Lash extensions">Lash extensions</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Eyelah hybrid full set</span><span class="whitespace-nowrap">$120</span></li>
              <li class="flex justify-between gap-3"><span>Eyelash Extensions volume full set</span><span class="whitespace-nowrap">$160</span></li>
              <li class="flex justify-between gap-3"><span>Refill Classic set 2 weeks</span><span class="whitespace-nowrap">$70</span></li>
            </ul>
            <p class="text-xs text-[color:var(--ink-40)] mt-4" data-es="y 9 más en Booksy" data-en="+9 more on Booksy">+9 more on Booksy</p>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:200ms">
            <h4 class="font-display text-lg mb-4" data-es="Cejas y depilación con cera" data-en="Brows &amp; waxing">Brows &amp; waxing</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Eyebrow Waxing</span><span class="whitespace-nowrap">$15</span></li>
              <li class="flex justify-between gap-3"><span>Eyebrows lamination, waxing &amp; tinting</span><span class="whitespace-nowrap">$100</span></li>
              <li class="flex justify-between gap-3"><span>Ombre brows</span><span class="whitespace-nowrap">$300</span></li>
              <li class="flex justify-between gap-3"><span>Full face</span><span class="whitespace-nowrap">$60</span></li>
            </ul>
            <p class="text-xs text-[color:var(--ink-40)] mt-4" data-es="y 4 más en Booksy" data-en="+4 more on Booksy">+4 more on Booksy</p>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:260ms">
            <h4 class="font-display text-lg mb-4" data-es="Depilación y labios" data-en="Hair removal &amp; lips">Hair removal &amp; lips</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span>Brazilian hair removal</span><span class="whitespace-nowrap">$60</span></li>
              <li class="flex justify-between gap-3"><span>Leg Hair Removal</span><span class="whitespace-nowrap">$80</span></li>
              <li class="flex justify-between gap-3"><span>Lips blush</span><span class="whitespace-nowrap">$150</span></li>
            </ul>
            <p class="text-xs text-[color:var(--ink-40)] mt-4" data-es="y 2 más en Booksy" data-en="+2 more on Booksy">+2 more on Booksy</p>
          </div>
        </div>
        <div class="text-center mt-8 reveal">
          <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2" data-es="Ver los 41 servicios en Booksy" data-en="See all 41 services on Booksy">See all 41 services on Booksy</a>
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
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.</p>',
)

# ---------- 14. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="41 servicios en total, con precios exactos y disponibilidad en tiempo real en Booksy." data-en="41 services in total, with exact prices and real time availability on Booksy.">41 services in total, with exact prices and real time availability on Booksy.</span></p>',
)

# ---------- 15. GALERIA: eyebrow, H2, link social, grid completo ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>',
)
rep(
    '          @lorena_beauty\n',
    '          <span data-es="Instagram" data-en="Instagram">Instagram</span>\n',
)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño de girasol, look distintivo" data-en="Sunflower design, our signature look">Sunflower design, our signature look</span><img src="assets/raw/bk-15.jpg" alt="Bright yellow sunflower nail art manicure closeup with a real sunflower" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Amarillo y lila" data-en="Yellow &amp; lilac two-tone">Yellow &amp; lilac two-tone</span><img src="assets/raw/bk-13.jpg" alt="Two-tone yellow and lilac manicure closeup" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Rosa al aire libre" data-en="Pink, outdoor light">Pink, outdoor light</span><img src="assets/raw/bk-6.jpg" alt="Pink manicure closeup in natural outdoor garden light" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Borgoña clásico" data-en="Classic burgundy">Classic burgundy</span><img src="assets/raw/bk-14.jpg" alt="Burgundy manicure closeup in outdoor garden light" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Francés con anillos" data-en="French tip with rings">French tip with rings</span><img src="assets/raw/bk-3.jpg" alt="French tip manicure with layered rings, elegant closeup" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Francés simple" data-en="Clean simple French">Clean simple French</span><img src="assets/raw/bk-9.jpg" alt="Clean simple French tip manicure outdoors" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

# ---------- 16. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 18 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 18 verified reviews on Booksy">5.0 out of 5 · 18 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Muy bellas que trabaja las manos y pies. Es bien rápida.  Hoy fue mi appointment y quedé complacida con un arreglo precioso y fino. . Gracias Lorena!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emisney R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She is the best love it"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">María S…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"🩷🩷"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lexy S…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 18 reseñas en Booksy" data-en="Read all 18 reviews on Booksy">Read all 18 reviews on Booksy</a>',
)

# ---------- 17. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">North Miami</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">1110 NE 213th Ter, Miami, FL 33179</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=1110+NE+213th+Ter,+Miami,+FL+33179" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto de lunes a sábado." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Monday through Saturday.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Monday through Saturday.</p>',
)

OLD_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@lorena_beauty</a>'
)
NEW_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los diseños más recientes de Lorena y escribe por DM cualquier duda antes de tu cita." data-en="See Lorena\'s latest designs and DM any questions before your appointment.">See Lorena\'s latest designs and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@lorena_beauty</a>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_SOCIAL)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Lorena Beauty, 1110 NE 213th Ter, Miami FL"\n          src="https://www.google.com/maps?q=1110+NE+213th+Ter,+Miami,+FL+33179&output=embed"',
)

# ---------- 18. CTA FINAL ----------
# (la linea script "Lashes that bloom with you." ya se cubrio con n=2 en la seccion HERO)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure, pedicura, acrílico, pestañas o el diseño de cejas que ya quieres estrenar." data-en="Book online in seconds: your manicure, pedicure, acrylic set, lashes or the brow design you have been wanting to try.">Book online in seconds: your manicure, pedicure, acrylic set, lashes or the brow design you have been wanting to try.</p>',
)
rep(
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
)

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-14.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en North Miami, FL. Atención con cita previa." data-en="Nail salon in North Miami, FL. By appointment only.">Nail salon in North Miami, FL. By appointment only.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>1110 NE 213th Ter, Miami, FL 33179</p>',
)
OLD_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @lorena_beauty</a></p>'
)
rep(OLD_FOOT_SOCIAL, OLD_FOOT_SOCIAL)  # ya reemplazado por repall global; se deja como verificacion de anclas
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ---------- 20. Paleta: rotacion de matiz -> mauve-rose empolvado, pin exacto de accent-deep/mid ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

HUE_SHIFT = 11
SAT_MUL = 0.82


def shift_hex(hexcode):
    r = int(hexcode[0:2], 16) / 255.0
    g = int(hexcode[2:4], 16) / 255.0
    b = int(hexcode[4:6], 16) / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    s = max(0.0, min(1.0, s * SAT_MUL))
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return "%02x%02x%02x" % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def shift_rgb_tuple(rr, gg, bb):
    r, g, b = rr / 255.0, gg / 255.0, bb / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    s = max(0.0, min(1.0, s * SAT_MUL))
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

# Pin exacto de los 2 tonos con nombre pedidos por la tarea: accent-deep #9c5468, accent-mid #bc8494
auto_deep = shift_hex("a04a72")   # lo que produjo el shift automatico para el tono base
auto_mid = shift_hex("c47a9c")
deep_rgb = shift_rgb_tuple(160, 74, 114)
mid_rgb = shift_rgb_tuple(196, 122, 156)

def maybe_repall(a, b):
    global h
    if a in h:
        h = h.replace(a, b)


maybe_repall("#" + auto_deep, "#9c5468")
maybe_repall("#" + auto_mid, "#bc8494")
maybe_repall("rgb(%d,%d,%d)" % deep_rgb, "rgb(156,84,104)")
maybe_repall("%d,%d,%d" % deep_rgb, "156,84,104")
maybe_repall("%d,%d,%d" % mid_rgb, "188,132,148")

open("output/lorena-beauty/index.html", "w").write(h)
print("BUILD OK: lorena-beauty")
