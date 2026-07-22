import re
import colorsys

h = open("output/doral-clau-garcia-nails/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Clau Garcia Nails"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/822429_doral-clau-garcia-nails_nail-salon_15889_miami"
IG_OLD = "https://www.instagram.com/_lashbloom/"
IG_NEW = "https://www.instagram.com/claugarcianails/"

# ---------- 1. <html lang> + idioma por defecto (EN) ----------
# el esqueleto light-v2 ya es EN-default (lang="en" y applyLang cae a 'en' salvo navegador 'es'); se deja igual.
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h

# ---------- 2. HEAD: title/meta/og/favicon ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Nail Salon in Doral, Miami, FL | 5.0 on Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Doral FL: manicure, pedicure, dip powder, apres gel and nail art by Claudia García, with a perfect 5.0 across 353 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Nail Salon in Doral, Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure, pedicure, dip powder and nail art. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-3.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />',
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
    "name": "Clau Garcia Nails",
    "description": "Nail salon inside a private salon suite in Doral, Miami, FL: manicure, pedicure, dip powder, apres gel and nail art by Claudia García.",
    "address": { "@type": "PostalAddress", "streetAddress": "11402 NW 41st St #218 (Suite #117)", "addressLocality": "Doral", "addressRegion": "FL", "postalCode": "33178", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.810705, "longitude": -80.383047 },
    "sameAs": ["https://booksy.com/en-us/822429_doral-clau-garcia-nails_nail-salon_15889_miami", "https://www.instagram.com/claugarcianails/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "353", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday"], "opens": "10:00", "closes": "19:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday", "Friday"], "opens": "09:00", "closes": "20:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "07:30", "closes": "19:30" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Regular Polish" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Dip Powder" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luminary Nails Manicure" } },
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Gel Polish" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel Polish & Pedicure Gel Polish" } }
    ] }
  }
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. Booksy URL global + Instagram global ----------
repall(BOOKSY_OLD, BOOKSY_NEW)
repall(IG_OLD, IG_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">CG</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 6. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    f'<img src="assets/raw/bk-1.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Clau <span class="text-[color:var(--accent-deep)]">Garcia</span> Nails</span>',
)
# @_lashbloom leftover en el href del boton de instagram del nav no existe (nav solo tiene Booksy), OK.

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Doral, Miami, FL · Salón de Uñas" data-en="Doral, Miami, FL · Nail Salon">Doral, Miami, FL · Nail Salon</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas que se sienten como tú." data-en="Nails that feel like you.">Nails that feel like you.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas hechas a mano," data-en="Handcrafted nails,">Handcrafted nails,</span><br /><span data-es="hechas para que " data-en="made to " >made to </span><span class="text-shine" data-es="brillen" data-en="shine">shine</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicure, pedicura, dip powder y gel X hechos por Claudia García dentro de un suite privado en Doral. Un 5.0 perfecto en 353 reseñas de Booksy, y clientas que reservan con ella una y otra vez." data-en="Manicure, pedicure, dip powder and gel X by Claudia García, inside a private salon suite in Doral. A perfect 5.0 across 353 Booksy reviews, and clients who book with her again and again.">Manicure, pedicure, dip powder and gel X by Claudia García, inside a private salon suite in Doral. A perfect 5.0 across 353 Booksy reviews, and clients who book with her again and again.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 353 reseñas en Booksy" data-en="5.0 · 353 reviews on Booksy">5.0 · 353 reviews on Booksy</span>',
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
    "            @claugarcianails\n"
    "          </a>"
)
rep(OLD_HERO_BTN2, NEW_HERO_BTN2)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-3.jpg" alt="Manicura arcoíris en azul, coral, amarillo, verde, rosa y morado sobre una mesa de madera" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg">Manicure Dip Powder</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$65 · 1h 30min" data-en="$65 · 1h 30min">$65 · 1h 30min</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="353">353</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicure <span class="text-shine">&amp;</span> Pedicure</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel · Dip Powder · Diseños" data-en="Gel · Dip powder · Designs">Gel · Dip powder · Designs</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">We speak</span> <span class="text-shine" data-es="Español" data-en="Spanish">Spanish</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Warm, personal care</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Doral, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">11402 NW 41st St #218</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Gel Manicure"),
    ("Hybrid Set", "Dip Powder"),
    ("Volume Set", "Apres Gel"),
    ("Mega Volume", "Luminary Nails"),
    ("Bottom Lashes", "Pedicure"),
    ("West Palm Beach, FL", "Doral, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 10. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Collage del proceso de aplicacion de una tip de gel paso a paso" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Dos potes abiertos de dip powder en tonos lavanda y violeta" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una sola artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="diseños infinitos" data-en="endless designs">endless designs</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Clau Garcia Nails es el suite privado de una sola artista de uñas en Doral: Claudia García. Cada set, manicure, pedicura, dip powder o gel X, se hace con calma, un cliente a la vez, dentro de su propio estudio (Suite #117)." data-en="Clau Garcia Nails is the private suite of one licensed nail artist in Doral: Claudia García. Every set, manicure, pedicure, dip powder or gel X, is done with care, one client at a time, inside her own studio (Suite #117).">Clau Garcia Nails is the private suite of one licensed nail artist in Doral: Claudia García. Every set, manicure, pedicure, dip powder or gel X, is done with care, one client at a time, inside her own studio (Suite #117).</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 353 reseñas verificadas en Booksy, uno de los estudios de uñas mejor calificados de Doral, y clientas que describen su trabajo como confiable, creativo y siempre impecable." data-en="The result: a perfect 5.0 across 353 verified reviews on Booksy, one of the highest rated nail studios in Doral, and clients who describe her work as reliable, creative and consistently perfect.">The result: a perfect 5.0 across 353 verified reviews on Booksy, one of the highest rated nail studios in Doral, and clients who describe her work as reliable, creative and consistently perfect.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="353">353</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    f'<img src="assets/raw/bk-1.jpg" alt="{NAME}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Claudia · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>',
)

# ---------- 11. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita," data-en="Your visit,">Your visit,</span> <span class="text-shine" data-es="de principio a fin" data-en="start to finish">start to finish</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio, día y hora en Booksy con precio y duración claros, y confirmas al instante." data-en="Choose your service, day and time on Booksy with clear price and duration, and confirm instantly.">Choose your service, day and time on Booksy with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Elige tu estilo" data-en="Choose your style">Choose your style</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Gel polish, dip powder, apres gel o un diseño hecho a mano: tú eliges el acabado y el color que va contigo." data-en="Gel polish, dip powder, apres gel or a hand painted design: you choose the finish and color that fits you.">Gel polish, dip powder, apres gel or a hand painted design: you choose the finish and color that fits you.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="El trabajo de detalle" data-en="The detail work">The detail work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cutícula y un esmaltado o dip impecable, hecho con calma y un cliente a la vez." data-en="Filing, cuticle care and a flawless polish or dip application, done calmly and one client at a time.">Filing, cuticle care and a flawless polish or dip application, done calmly and one client at a time.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="You leave ready">You leave ready</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu manicure o pedicura lista para durar semanas, tal como cuentan sus 353 reseñas de 5 estrellas." data-en="You walk out with a manicure or pedicure built to last for weeks, just like her 353 five star reviews describe.">You walk out with a manicure or pedicure built to last for weeks, just like her 353 five star reviews describe.</p>',
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
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure de todos los días" data-en="Everyday manicure">Everyday manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure Regular Polish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure clásico con esmalte regular, rápido y bien hecho. También: Manicure Gel Polish $40 y Manicure P/ Caballeros $40." data-en="Classic manicure with regular polish, quick and done right. Also: Manicure Gel Polish $40 and Manicure P/ Caballeros $40.">Classic manicure with regular polish, quick and done right. Also: Manicure Gel Polish $40 and Manicure P/ Caballeros $40.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure Dip Powder</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Dip powder de larga duración, resistente y con acabado perfecto. También: Manicure Apress Gel $75 y Luminary Nails Manicure $60." data-en="Long lasting dip powder manicure, durable with a flawless finish. Also: Manicure Apress Gel $75 and Luminary Nails Manicure $60.">Long lasting dip powder manicure, durable with a flawless finish. Also: Manicure Apress Gel $75 and Luminary Nails Manicure $60.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies cuidados" data-en="Feet, taken care of">Feet, taken care of</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Pedicure Gel Polish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa con esmalte en gel de larga duración. También: Pedicure Regular Polish $40 y Pedicure P/ Caballeros $55." data-en="Full pedicure with long lasting gel polish. Also: Pedicure Regular Polish $40 and Pedicure P/ Caballeros $55.">Full pedicure with long lasting gel polish. Also: Pedicure Regular Polish $40 and Pedicure P/ Caballeros $55.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Combo manos y pies" data-en="Mani + pedi combo">Mani + pedi combo</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Gel Polish &amp; Pedicure Gel Polish" data-en="Manicure Gel Polish &amp; Pedicure Gel Polish">Manicure Gel Polish &amp; Pedicure Gel Polish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo completo de manos y pies en gel. También: Manicure Dip Powder &amp; Pedicure Gel Polish $105 (2h 15min)." data-en="The full hands and feet combo in gel polish. Also: Manicure Dip Powder &amp; Pedicure Gel Polish $105 (2h 15min).">The full hands and feet combo in gel polish. Also: Manicure Dip Powder &amp; Pedicure Gel Polish $105 (2h 15min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
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
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.</p>',
)

# ---------- 14. Nota de servicios + bloque de menu completo (glass-grid) ----------
FULL_MENU_BLOCK = f"""
      <div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-8" data-es="Menú completo" data-en="Full menu">Full menu</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div class="glass glass-hover rounded-2xl p-6 reveal">
            <h4 class="font-display text-lg mb-4" data-es="Manicure" data-en="Manicure">Manicure</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Regular Polish" data-en="Regular Polish">Regular Polish</span><span class="text-[color:var(--ink-40)]">$30</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel Polish" data-en="Gel Polish">Gel Polish</span><span class="text-[color:var(--ink-40)]">$40</span></li>
              <li class="flex justify-between gap-3"><span data-es="Dip Powder" data-en="Dip Powder">Dip Powder</span><span class="text-[color:var(--ink-40)]">$65</span></li>
              <li class="flex justify-between gap-3"><span data-es="Apress Gel" data-en="Apress Gel">Apress Gel</span><span class="text-[color:var(--ink-40)]">$75</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary Nails" data-en="Luminary Nails">Luminary Nails</span><span class="text-[color:var(--ink-40)]">$60</span></li>
              <li class="flex justify-between gap-3"><span data-es="P/ Caballeros" data-en="P/ Caballeros">P/ Caballeros</span><span class="text-[color:var(--ink-40)]">$40</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:90ms">
            <h4 class="font-display text-lg mb-4" data-es="Pedicure" data-en="Pedicure">Pedicure</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Regular Polish" data-en="Regular Polish">Regular Polish</span><span class="text-[color:var(--ink-40)]">$40</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel Polish" data-en="Gel Polish">Gel Polish</span><span class="text-[color:var(--ink-40)]">$45</span></li>
              <li class="flex justify-between gap-3"><span data-es="P/ Caballeros" data-en="P/ Caballeros">P/ Caballeros</span><span class="text-[color:var(--ink-40)]">$55</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:150ms">
            <h4 class="font-display text-lg mb-4" data-es="Combos manos y pies" data-en="Hands &amp; feet combos">Hands &amp; feet combos</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Regular &amp; Regular" data-en="Regular &amp; Regular">Regular &amp; Regular</span><span class="text-[color:var(--ink-40)]">$55</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel &amp; Regular" data-en="Gel &amp; Regular">Gel &amp; Regular</span><span class="text-[color:var(--ink-40)]">$65</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel &amp; Gel" data-en="Gel &amp; Gel">Gel &amp; Gel</span><span class="text-[color:var(--ink-40)]">$80</span></li>
              <li class="flex justify-between gap-3"><span data-es="Dip Powder &amp; Gel" data-en="Dip Powder &amp; Gel">Dip Powder &amp; Gel</span><span class="text-[color:var(--ink-40)]">$105</span></li>
              <li class="flex justify-between gap-3"><span data-es="P/ Caballeros" data-en="P/ Caballeros">P/ Caballeros</span><span class="text-[color:var(--ink-40)]">$85</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:210ms">
            <h4 class="font-display text-lg mb-4" data-es="Extras" data-en="Extras">Extras</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Reparación de Uña" data-en="Nail repair">Nail repair</span><span class="text-[color:var(--ink-40)]">$8</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel Polish P/ Caballeros" data-en="Gel Polish P/ Caballeros">Gel Polish P/ Caballeros</span><span class="text-[color:var(--ink-40)]">$45</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary M&amp;P Regular" data-en="Luminary M&amp;P Regular">Luminary M&amp;P Regular</span><span class="text-[color:var(--ink-40)]">$85</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary M&amp;P Gel" data-en="Luminary M&amp;P Gel">Luminary M&amp;P Gel</span><span class="text-[color:var(--ink-40)]">$95</span></li>
            </ul>
          </div>
        </div>
        <p class="reveal text-center mt-8">
          <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" data-es="Ver el menú completo y reservar en Booksy" data-en="See the full menu and book on Booksy">See the full menu and book on Booksy</a>
        </p>
      </div>"""

# ---------- 14b. Nota de servicios ----------
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Reparación de uña $8 (15min), servicios para caballeros y más: menú completo y disponibilidad en tiempo real en Booksy." data-en="Nail repair $8 (15min), services for men and more: full menu and real time availability on Booksy.">Nail repair $8 (15min), services for men and more: full menu and real time availability on Booksy.</span></p>'
    + FULL_MENU_BLOCK,
)

print("PARTE 2 OK (servicios)")

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
    "          @claugarcianails\n"
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Manicura arcoíris" data-en="Rainbow manicure">Rainbow manicure</span><img src="assets/raw/bk-3.jpg" alt="Manicura arcoíris en azul, coral, amarillo, verde, rosa y morado sobre una mesa de madera" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rojo brillante" data-en="Deep red shimmer">Deep red shimmer</span><img src="assets/raw/bk-13.jpg" alt="Manicura corta y redondeada en rojo vino brillante, manos cruzadas" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Azul marino brillante" data-en="Navy blue gloss">Navy blue gloss</span><img src="assets/raw/bk-14.jpg" alt="Manicura brillante en azul marino sobre uñas en forma almendrada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Almendra espresso" data-en="Espresso almond">Espresso almond</span><img src="assets/raw/bk-15.jpg" alt="Manicura almendrada en marron espresso profundo con un anillo de corazon" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Violeta brillante" data-en="Violet shimmer">Violet shimmer</span><img src="assets/raw/bk-16.jpg" alt="Manicura cuadrada en esmalte violeta con brillo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Colección Luminary Nails" data-en="Luminary Nails collection">Luminary Nails collection</span><img src="assets/raw/bk-7.jpg" alt="Fila de frascos de esmalte en gel de Luminary Nail Systems" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

# ---------- 17. OPINIONES ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 353 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 353 verified reviews on Booksy">5.0 out of 5 · 353 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing as always"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karla T…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Claudia is incredibly talented, pays so much attention to detail, and made sure my nails came out perfect. She’s patient, professional, and creates such a comfortable, welcoming atmosphere. If you’re looking for someone who is reliable, creative, and consistently delivers amazing results, she’s definitely the one to book with."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jade R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Adrianna U…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 353 reseñas en Booksy" data-en="Read all 353 reviews on Booksy">Read all 353 reviews on Booksy</a>',
)

print("PARTE 3 OK (galeria, opiniones)")

# ---------- 18. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Doral, FL</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">11402 NW 41st St #218 (Suite #117), Doral, Miami, FL 33178</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=11402+NW+41st+St+%23218,+Doral,+FL+33178" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes a miércoles 10am a 7:30pm, jueves y viernes 9am a 8:30pm, y sábados 7:30am a 7:30pm." data-en="By appointment via Booksy: pick the service, day and time, confirmation is instant. Monday to Wednesday 10am to 7:30pm, Thursday and Friday 9am to 8:30pm, and Saturday 7:30am to 7:30pm.">By appointment via Booksy: pick the service, day and time, confirmation is instant. Monday to Wednesday 10am to 7:30pm, Thursday and Friday 9am to 8:30pm, and Saturday 7:30am to 7:30pm.</p>',
)

OLD_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@_lashbloom</a>'
)
NEW_LOC_SOCIAL = (
    '<p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos más recientes de Claudia y escribe por DM cualquier duda antes de tu cita." data-en="See Claudia\'s latest work and DM any questions before your appointment.">See Claudia\'s latest work and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_NEW + '" target="_blank" rel="noopener">@claugarcianails</a>'
)
rep(OLD_LOC_SOCIAL, NEW_LOC_SOCIAL)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Clau Garcia Nails, 11402 NW 41st St #218, Doral FL"\n          src="https://www.google.com/maps?q=25.810705,-80.383047&output=embed"',
)

# ---------- 19. CTA FINAL ----------
# (la linea "Lashes that bloom with you." ya se reemplazo en HERO con n=2, cubre hero + cta-final)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure, pedicura, dip powder o el diseño que ya quieres estrenar con Claudia en Doral." data-en="Book online in seconds: your manicure, pedicure, dip powder or the design you have been wanting to try with Claudia in Doral.">Book online in seconds: your manicure, pedicure, dip powder or the design you have been wanting to try with Claudia in Doral.</p>',
)
# (el boton "Seguir en Instagram" del CTA final ya apunta a IG_NEW via el repall global)

# ---------- 20. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<img src="assets/raw/bk-1.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Doral, Miami, FL. Atención con cita previa." data-en="Nail salon in Doral, Miami, FL. By appointment only.">Nail salon in Doral, Miami, FL. By appointment only.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>11402 NW 41st St #218, Doral, FL 33178</p>',
)
OLD_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>'
)
NEW_FOOT_SOCIAL = (
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_NEW + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @claugarcianails</a></p>'
)
rep(OLD_FOOT_SOCIAL, NEW_FOOT_SOCIAL)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

print("PARTE 4 OK (ubicacion, cta-final, footer)")

# ---------- 21. Paleta: plum-pink -> indigo-denim ----------
# Proteger badge dorado de Merktop.
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# Los dos tonos con hex EXACTO pedido por la tarea (accent-deep / accent-mid), y su rgb
# equivalente para las rgba() que traen 160,74,114 (rgb literal de #a04a72).
assert h.count("a04a72") == 7, f"a04a72 count = {h.count('a04a72')}"
assert h.count("c47a9c") == 4, f"c47a9c count = {h.count('c47a9c')}"
assert h.count("160,74,114") == 22, f"160,74,114 count = {h.count('160,74,114')}"  # 21 del esqueleto + 1 del link nuevo en el menu completo
h = h.replace("a04a72", "3e5c8a")
h = h.replace("c47a9c", "6f8fc4")
h = h.replace("160,74,114", "62,92,138")

# Proteger los dos hex exactos y su rgb para que la rotacion de matiz generica (que cubre
# el resto de la familia plum-pink: sombras, dark-band, fondos, ink, etc.) no los vuelva a mover.
h = h.replace("3e5c8a", "TOKACCENTDEEPHEX")
h = h.replace("6f8fc4", "TOKACCENTMIDHEX")
h = h.replace("62,92,138", "TOKACCENTDEEPRGB")

HUE_SHIFT = 244.6  # grados: plum-pink (~332) -> indigo-denim (~216), calibrado sobre a04a72->3e5c8a y c47a9c->6f8fc4


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

# Restaurar los tonos exactos protegidos y el badge dorado.
h = h.replace("TOKACCENTDEEPHEX", "3e5c8a")
h = h.replace("TOKACCENTMIDHEX", "6f8fc4")
h = h.replace("TOKACCENTDEEPRGB", "62,92,138")
h = h.replace("@@BADGE@@", badge_block, 1)

print("PARTE 5 OK (paleta indigo-denim, badge dorado protegido)")

open("output/doral-clau-garcia-nails/index.html", "w").write(h)
print("DONE: output/doral-clau-garcia-nails/index.html escrito")
