import colorsys
import re

h = open("output/alvarez-nails-studio-doral/index.html").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


NAME = "Alvarez Nails Studio By Yanetsis"
NAME_SHORT = "Alvarez Nails Studio"
BOOKSY_OLD = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
BOOKSY_NEW = "https://booksy.com/en-us/1699334_alvarez-nails-studio-by-yanetsis_nail-salon_122701_doral"
IG_OLD = "https://www.instagram.com/_lashbloom/"
MAPS_NEW = "https://www.google.com/maps?q=7901+NW+36th+St+suite+102,+Doral,+FL+33166"
MAPS_EMBED = "https://www.google.com/maps?q=25.80958593808094,-80.32555327476233&output=embed"

# ---------- 1. <html lang> + idioma por defecto (ES) ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 2. HEAD: title/meta/og/favicon ----------
rep(
    "<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>",
    f"<title>{NAME} · Salón de Uñas en Doral, FL | 5.0 en Booksy</title>",
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    f'<meta name="description" content="{NAME}, Doral FL: manicura y pedicura en gel, apres gel y luminary nails por Yanetsis Alvarez, con un 5.0 perfecto en 45 reseñas de Booksy. Reserva online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    f'<meta property="og:title" content="{NAME} · Salón de Uñas en Doral, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicura y pedicura en gel, apres gel y luminary nails. 5.0 en Booksy. Reserva online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-5.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-5.jpg" />',
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

NEW_LD = f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "{NAME}",
    "description": "Nail salon in Doral, FL: gel manicures and pedicures, apres gel and luminary nails by Yanetsis Alvarez.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "7901 NW 36th St suite 102", "addressLocality": "Doral", "addressRegion": "FL", "postalCode": "33166", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.80958593808094, "longitude": -80.32555327476233 }},
    "sameAs": ["{BOOKSY_NEW}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "45", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "20:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "19:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      {{ "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Apres gel nails" }} }},
      {{ "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Luminary nails" }} }},
      {{ "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Gel mani" }} }},
      {{ "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Pedicure regular" }} }}
    ] }}
  }}
  </script>"""

rep(OLD_LD, NEW_LD)

# ---------- 4. Booksy URL global ----------
repall(BOOKSY_OLD, BOOKSY_NEW)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">AN</span>')
rep('<span class="pre-word">Lash Bloom</span>', f'<span class="pre-word">{NAME_SHORT}</span>')

# ---------- 6. NAV (sin logo real: monograma de texto) ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm tracking-wide ring-1 ring-[rgba(160,74,114,0.35)] bg-[rgba(160,74,114,0.1)] text-[color:var(--accent-deep)]">AN</span>',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Alvarez <span class="text-[color:var(--accent-deep)]">Nails Studio</span></span>',
)

# ---------- 7. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Doral, FL · Salón de Uñas" data-en="Doral, FL · Nail Salon">Doral, FL · Salón de Uñas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas cuidadas con el detalle que enamora." data-en="Nails cared for with detail that wins you over.">Uñas cuidadas con el detalle que enamora.</p>',
    n=2,
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura y pedicura" data-en="Manicures and pedicures">Manicura y pedicura</span><br /><span data-es="hechas a mano, con " data-en="made by hand, with ">hechas a mano, con </span><span class="text-shine" data-es="amor" data-en="love">amor</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura y pedicura en gel, apres gel y luminary nails, hechas uña por uña por Yanetsis Alvarez en su estudio de Doral. Un 5.0 perfecto en 45 reseñas de Booksy respalda cada set." data-en="Gel manicures and pedicures, apres gel and luminary nails, done nail by nail by Yanetsis Alvarez in her Doral studio. A perfect 5.0 across 45 Booksy reviews backs up every set.">Manicura y pedicura en gel, apres gel y luminary nails, hechas uña por uña por Yanetsis Alvarez en su estudio de Doral. Un 5.0 perfecto en 45 reseñas de Booksy respalda cada set.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 45 reseñas en Booksy" data-en="5.0 · 45 reviews on Booksy">5.0 · 45 reseñas en Booksy</span>',
)

OLD_HERO_IG = (
    '<a href="' + IG_OLD + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "            @_lashbloom\n"
    "          </a>"
)
NEW_HERO_MAPS = (
    '<a href="' + MAPS_NEW + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n'
    '            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>\n'
    '            <span data-es="Cómo llegar" data-en="Get directions">Cómo llegar</span>\n'
    "          </a>"
)
rep(OLD_HERO_IG, NEW_HERO_MAPS)

rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-5.jpg" alt="Manicura francesa en nude con puntas blancas y anillo de diamante, brillo editorial" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>',
    '<p class="font-display text-lg" data-es="Luminary Nails" data-en="Luminary Nails">Luminary Nails</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="$75 · 1h 30min" data-en="$75 · 1h 30min">$75 · 1h 30min</p>',
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="45">45</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Apres</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicura · Pedicura · Luminary" data-en="Manicure · Pedicure · Luminary">Manicura · Pedicura · Luminary</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Se habla" data-en="We speak">Se habla</span> <span class="text-shine" data-es="Español" data-en="Spanish">Español</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención cálida y cercana" data-en="Warm, personal care">Atención cálida y cercana</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Doral, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">7901 NW 36th St</p></div>',
)

# ---------- 9. MARQUEE (6 palabras x4 c/u) ----------
MQ = [
    ("Classic Set", "Gel Mani"),
    ("Hybrid Set", "Apres Gel"),
    ("Volume Set", "Luminary Nails"),
    ("Mega Volume", "Pedicure"),
    ("Bottom Lashes", "Manicura"),
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
    '<img src="assets/raw/bk-6.jpg" alt="Manicura en rosa pálido sólido, acabado limpio y brillante" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Manicura francesa en negro con un diminuto strass, sobre base nude" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">Una artista,</span><br /><span class="text-shine" data-es="uña por uña" data-en="nail by nail">uña por uña</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Alvarez Nails Studio es el espacio de Yanetsis Alvarez en Doral: manicura y pedicura en gel, apres gel y luminary nails, diseñadas uña por uña sobre un lienzo nude, pastel o el color exacto que traes en mente." data-en="Alvarez Nails Studio is Yanetsis Alvarez\'s space in Doral: gel manicures and pedicures, apres gel and luminary nails, designed nail by nail on a nude, pastel canvas or the exact color you have in mind.">Alvarez Nails Studio es el espacio de Yanetsis Alvarez en Doral: manicura y pedicura en gel, apres gel y luminary nails, diseñadas uña por uña sobre un lienzo nude, pastel o el color exacto que traes en mente.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 45 reseñas verificadas en Booksy, donde sus clientas la describen como una excelente profesional que deja las uñas largas, fuertes e impecables semana tras semana." data-en="The result: a perfect 5.0 across 45 verified reviews on Booksy, where clients describe her as an excellent professional whose work leaves nails long, strong and flawless week after week.">El resultado: un 5.0 perfecto en 45 reseñas verificadas en Booksy, donde sus clientas la describen como una excelente profesional que deja las uñas largas, fuertes e impecables semana tras semana.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="45">45</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-xs tracking-wide ring-1 ring-[rgba(160,74,114,0.3)] bg-[rgba(160,74,114,0.1)] text-[color:var(--accent-deep)]">AN</span>\n            <span class="text-sm font-light">Yanetsis · <span class="text-[color:var(--ink-40)]" data-es="Dueña y manicurista" data-en="Owner &amp; nail artist">Dueña y manicurista</span></span>',
)

# ---------- 11. EL METODO / PROCESO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita," data-en="Your visit,">Tu cita,</span> <span class="text-shine" data-es="uña por uña" data-en="nail by nail">uña por uña</span></h2>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges el color, la forma y el efecto que buscas: gel, apres gel o luminary, todo definido antes de empezar." data-en="You choose the color, shape and finish you want: gel, apres gel or luminary, all decided before we start.">Eliges el color, la forma y el efecto que buscas: gel, apres gel o luminary, todo definido antes de empezar.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de diseño" data-en="Design consult">Consulta de diseño</h3>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Preparación y limado" data-en="Prep and filing">Preparación y limado</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cutícula, limado y preparación cuidadosa de la uña para que el gel o el apres se adhieran perfecto y duren semanas." data-en="Cuticle care, filing and careful nail prep so the gel or apres bonds perfectly and lasts for weeks.">Cutícula, limado y preparación cuidadosa de la uña para que el gel o el apres se adhieran perfecto y duren semanas.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación gel o acrílico" data-en="Gel or acrylic application">Aplicación gel o acrílico</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Yanetsis aplica el gel, apres gel o luminary uña por uña, con la precisión que sus clientas repiten en cada reseña." data-en="Yanetsis applies the gel, apres gel or luminary nail by nail, with the precision her clients mention in every review.">Yanetsis aplica el gel, apres gel o luminary uña por uña, con la precisión que sus clientas repiten en cada reseña.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sellado y top coat" data-en="Seal and top coat">Sellado y top coat</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Un top coat sella el color y le da brillo de larga duración, para que salgas con un set impecable." data-en="A top coat seals the color and gives it long-lasting shine, so you leave with a flawless set.">Un top coat sella el color y le da brillo de larga duración, para que salgas con un set impecable.</p>',
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
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extensión resistente" data-en="Sturdy overlay">Extensión resistente</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apres Gel Nails" data-en="Apres Gel Nails">Apres Gel Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gel apres para uñas fuertes, ligeras y de acabado natural en una sola sesión. También con pedicura: Apres gel and regular pies $95 y Apres gel and gel pedicure $105." data-en="Apres gel for sturdy, lightweight nails with a natural finish in one visit. Also with pedicure: Apres gel and regular pies $95 and Apres gel and gel pedicure $105.">Gel apres para uñas fuertes, ligeras y de acabado natural en una sola sesión. También con pedicura: Apres gel and regular pies $95 y Apres gel and gel pedicure $105.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luminary Nails" data-en="Luminary Nails">Luminary Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El acabado luminary, el más pedido del estudio: brillo suave y color uniforme, uña por uña. También con pedicura: Luminary and regular pedicure $100 y Luminary and gel pedicure $110." data-en="The luminary finish, the studio's most requested look: soft shine and even color, nail by nail. Also with pedicure: Luminary and regular pedicure $100 and Luminary and gel pedicure $110.">El acabado luminary, el más pedido del estudio: brillo suave y color uniforme, uña por uña. También con pedicura: Luminary and regular pedicure $100 y Luminary and gel pedicure $110.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicure de todos los días" data-en="Everyday manicure">Manicure de todos los días</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Mani" data-en="Gel Mani">Gel Mani</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure profesional en gel con acabado brillante y de larga duración. También: Manicura regular $25 y Gel mani and pedicure regular $55." data-en="Professional gel manicure with a glossy, long lasting finish. Also: Manicura regular $25 and Gel mani and pedicure regular $55.">Manicure profesional en gel con acabado brillante y de larga duración. También: Manicura regular $25 y Gel mani and pedicure regular $55.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies cuidados" data-en="Feet, taken care of">Pies cuidados</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicure Regular" data-en="Regular Pedicure">Pedicure Regular</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura relajante y completa, con acabado impecable. También: Gel pedicure $35 y Regular mani and pedi $50." data-en="A relaxing, complete pedicure with a flawless finish. Also: Gel pedicure $35 and Regular mani and pedi $50.">Pedicura relajante y completa, con acabado impecable. También: Gel pedicure $35 y Regular mani and pedi $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
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

# ---------- 14. Nota de servicios + bloque de menu completo (13 servicios reales) ----------
FULL_MENU_BLOCK = f"""
      <div class="mt-14">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-8" data-es="Menú completo" data-en="Full menu">Menú completo</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div class="glass glass-hover rounded-2xl p-6 reveal">
            <h4 class="font-display text-lg mb-4" data-es="Manicura" data-en="Manicure">Manicura</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Manicura regular" data-en="Manicura regular">Manicura regular</span><span class="text-[color:var(--ink-40)]">$25</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel mani" data-en="Gel mani">Gel mani</span><span class="text-[color:var(--ink-40)]">$30</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:90ms">
            <h4 class="font-display text-lg mb-4" data-es="Pedicure" data-en="Pedicure">Pedicure</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Pedicure regular" data-en="Pedicure regular">Pedicure regular</span><span class="text-[color:var(--ink-40)]">$30</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel pedicure" data-en="Gel pedicure">Gel pedicure</span><span class="text-[color:var(--ink-40)]">$35</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:150ms">
            <h4 class="font-display text-lg mb-4" data-es="Combos manos y pies" data-en="Hands &amp; feet combos">Combos manos y pies</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Regular mani and pedi" data-en="Regular mani and pedi">Regular mani and pedi</span><span class="text-[color:var(--ink-40)]">$50</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel mani and pedicure regular" data-en="Gel mani and pedicure regular">Gel mani and pedicure regular</span><span class="text-[color:var(--ink-40)]">$55</span></li>
              <li class="flex justify-between gap-3"><span data-es="Gel maní and gel pedí" data-en="Gel maní and gel pedí">Gel maní and gel pedí</span><span class="text-[color:var(--ink-40)]">$65</span></li>
            </ul>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 reveal" style="transition-delay:210ms">
            <h4 class="font-display text-lg mb-4" data-es="Apres &amp; Luminary" data-en="Apres &amp; Luminary">Apres &amp; Luminary</h4>
            <ul class="text-sm text-[color:var(--ink-60)] font-light space-y-2">
              <li class="flex justify-between gap-3"><span data-es="Apres gel nails" data-en="Apres gel nails">Apres gel nails</span><span class="text-[color:var(--ink-40)]">$70</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary nails" data-en="Luminary nails">Luminary nails</span><span class="text-[color:var(--ink-40)]">$75</span></li>
              <li class="flex justify-between gap-3"><span data-es="Apres gel and regular pies" data-en="Apres gel and regular pies">Apres gel and regular pies</span><span class="text-[color:var(--ink-40)]">$95</span></li>
              <li class="flex justify-between gap-3"><span data-es="Apres gel and gel pedicure" data-en="Apres gel and gel pedicure">Apres gel and gel pedicure</span><span class="text-[color:var(--ink-40)]">$105</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary and regular pedicure" data-en="Luminary and regular pedicure">Luminary and regular pedicure</span><span class="text-[color:var(--ink-40)]">$100</span></li>
              <li class="flex justify-between gap-3"><span data-es="Luminary and gel pedicure" data-en="Luminary and gel pedicure">Luminary and gel pedicure</span><span class="text-[color:var(--ink-40)]">$110</span></li>
            </ul>
          </div>
        </div>
        <p class="reveal text-center mt-8">
          <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" data-es="Ver el menú completo y reservar en Booksy" data-en="See the full menu and book on Booksy">Ver el menú completo y reservar en Booksy</a>
        </p>
      </div>"""

rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="13 servicios entre manicura, pedicura, apres gel y luminary nails: menú completo y disponibilidad en tiempo real en Booksy." data-en="13 services across manicure, pedicure, apres gel and luminary nails: full menu and real time availability on Booksy.">13 servicios entre manicura, pedicura, apres gel y luminary nails: menú completo y disponibilidad en tiempo real en Booksy.</span></p>'
    + FULL_MENU_BLOCK,
)

print("PARTE 2 OK (servicios)")

# ---------- 15. GALERIA: eyebrow, H2, boton de accion, grid completo ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas," data-en="Nails,">Uñas,</span> <span class="text-shine" data-es="de cerca" data-en="up close">de cerca</span></h2>',
)
OLD_GAL_SOCIAL = (
    '<a href="' + IG_OLD + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "          @_lashbloom\n"
    "        </a>"
)
NEW_GAL_BOOK = (
    '<a href="' + BOOKSY_NEW + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n'
    '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n'
    '          <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>\n'
    "        </a>"
)
rep(OLD_GAL_SOCIAL, NEW_GAL_BOOK)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

# Nota: solo 7 fotos del dossier tienen resolucion real (bk-3, bk-4, bk-5, bk-6, bk-7, bk-8, bk-9,
# todas >=975x1300px); bk-1 es el retrato/selfie de la dueña (PROHIBIDO en galeria) y bk-2/bk-10..16
# son miniaturas de 100-150px (inservibles para un tile grande, se verian pixeladas). bk-5, bk-6 y
# bk-7 ya se usan en hero/experiencia, asi que la galeria usa las 4 fotos de calidad restantes:
# bk-8 (arte pastel hecho a mano) como tile ancho, y bk-3/bk-4/bk-9 como tiles verticales.
NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño de verano hecho a mano" data-en="Hand-painted summer design">Diseño de verano hecho a mano</span><img src="assets/raw/bk-8.jpg" alt="Diseño de uñas pastel con soles, lunares y olas pintados a mano en azul, rosa, amarillo y blanco" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Coral sólido" data-en="Solid coral">Coral sólido</span><img src="assets/raw/bk-3.jpg" alt="Manicura en coral sólido sobre uñas cuadradas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Verde menta con brillo" data-en="Glossy mint green">Verde menta con brillo</span><img src="assets/raw/bk-4.jpg" alt="Manicura en verde menta brillante sobre uñas almendradas, con anillo dorado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="French en blush" data-en="Blush french">French en blush</span><img src="assets/raw/bk-9.jpg" alt="Manicura francesa en tonos blush con puntas blancas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""

h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end() :]

# ---------- 16. OPINIONES (3 quotes reales verbatim, 45 resenas, 5.0) ----------
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 45 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 45 verified reviews on Booksy">5.0 de 5 · 45 reseñas verificadas en Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Welcoming and clean atmosphere. My nails looked fantastic! I was so pleased with the pedicure that I ended up getting a manicure as well. Great service overall :  highly recommend"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mayda L&hellip;</span> <span class="text-[color:var(--ink-40)]">&middot; Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yanetsi es una excelente profesional. Siempre logra que mis uñas se vean hermosas e impecables tal como me gustan. Gracias a su gran trabajo y los productos que utiliza mis uñas están largas y fuertes y eso hace que se mantengan intactas incluso después de varias semanas. 🥰Amo hacerme las uñas con Yanetsi."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">China</span> <span class="text-[color:var(--ink-40)]">&middot; Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Fabuloso servicio."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ivy I&hellip;</span> <span class="text-[color:var(--ink-40)]">&middot; Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 45 reseñas en Booksy" data-en="Read all 45 reviews on Booksy">Leer las 45 reseñas en Booksy</a>',
)

print("PARTE 3 OK (galeria, opiniones)")

# ---------- 17. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Doral, FL</span></h2>',
)

OLD_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
NEW_LOC_CARDS = (
    '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light">7901 NW 36th St suite 102, Doral, FL 33166</p>\n'
    f'              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="{MAPS_NEW}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(OLD_LOC_CARDS, NEW_LOC_CARDS)

rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
)

OLD_LOC_HOURS = (
    '<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n'
    "            <div>\n"
    '              <p class="font-medium mb-1">Instagram</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>\n'
    '              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + IG_OLD + '" target="_blank" rel="noopener">@_lashbloom</a>\n'
    "            </div>"
)
NEW_LOC_HOURS = (
    '<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>\n'
    "            <div>\n"
    '              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes: 10:00am a 8:00pm. Sábado: 9:00am a 7:00pm." data-en="Monday to Friday: 10:00am to 8:00pm. Saturday: 9:00am to 7:00pm.">Lunes a viernes: 10:00am a 8:00pm. Sábado: 9:00am a 7:00pm.</p>\n'
    f'              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="{BOOKSY_NEW}" target="_blank" rel="noopener" data-es="Ver disponibilidad en Booksy" data-en="See availability on Booksy">Ver disponibilidad en Booksy</a>\n'
    "            </div>"
)
rep(OLD_LOC_HOURS, NEW_LOC_HOURS)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: {NAME}, 7901 NW 36th St suite 102, Doral FL"\n          src="{MAPS_EMBED}"',
)

# ---------- 18. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima manicura" data-en="Your next manicure">Tu próxima manicura</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicure en gel, tu set de luminary o el diseño que ya quieres estrenar con Yanetsis en Doral." data-en="Book online in seconds: your gel manicure, your luminary set, or the design you have been wanting to try with Yanetsis in Doral.">Reserva online en segundos: tu manicure en gel, tu set de luminary o el diseño que ya quieres estrenar con Yanetsis en Doral.</p>',
)
rep(
    '<a href="' + IG_OLD + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="#ubicacion" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Ver ubicación en Doral" data-en="See our Doral location">Ver ubicación en Doral</a>',
)

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', f'<span class="foot-mark" aria-hidden="true">{NAME_SHORT}</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    f'<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-xs tracking-wide ring-1 ring-[rgba(240,190,215,0.35)] bg-[rgba(240,190,215,0.08)] text-[#f0bed7]">AN</span>\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME_SHORT}</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Doral, FL. Atención con cita previa." data-en="Nail salon in Doral, FL. By appointment only.">Salón de uñas en Doral, FL. Atención con cita previa.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>7901 NW 36th St suite 102, Doral, FL 33166</p>',
)

OLD_FOOT_COL3 = (
    '<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">\n'
    '        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n'
    '        <p><a href="' + IG_OLD + '" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>\n'
    "      </div>"
)
NEW_FOOT_COL3 = (
    '<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">\n'
    '        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Horario" data-en="Hours">Horario</p>\n'
    '        <p data-es="Lunes a viernes: 10am a 8pm" data-en="Monday to Friday: 10am to 8pm">Lunes a viernes: 10am a 8pm</p>\n'
    '        <p data-es="Sábado: 9am a 7pm" data-en="Saturday: 9am to 7pm">Sábado: 9am a 7pm</p>\n'
    "      </div>"
)
rep(OLD_FOOT_COL3, NEW_FOOT_COL3)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

print("PARTE 4 OK (ubicacion, cta-final, footer)")

# ---------- 20. Paleta: plum-pink -> lila / lavanda polvo ----------
# Proteger badge dorado de Merktop (bloque CSS completo).
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, "no se encontro el bloque merktop-badge"
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)
assert '#f4eee2' in h  # texto crema neutro del badge, fuera de la paleta del negocio


def hex_to_rgb01(hx):
    return tuple(int(hx[i : i + 2], 16) / 255 for i in (0, 2, 4))


def rgb01_to_hex(rgb):
    return "".join("%02x" % max(0, min(255, round(c * 255))) for c in rgb)


# Delta de matiz calculado del accent-deep real (rosa-magenta) al accent-deep pedido (lila/lavanda).
h1, l1, s1 = colorsys.rgb_to_hls(*hex_to_rgb01("a04a72"))
h2, l2, s2 = colorsys.rgb_to_hls(*hex_to_rgb01("6f5f96"))
DELTA_H = h2 - h1


def hue_shift_hex(hx):
    r, g, b = hex_to_rgb01(hx)
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    hh = (hh + DELTA_H) % 1.0
    return rgb01_to_hex(colorsys.hls_to_rgb(hh, ll, ss))


def hue_shift_rgb(triplet):
    r, g, b = (int(x) / 255 for x in triplet.split(","))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    hh = (hh + DELTA_H) % 1.0
    r2, g2, b2 = colorsys.hls_to_rgb(hh, ll, ss)
    return ",".join(str(round(c * 255)) for c in (r2, g2, b2))


# Anclas exactas pedidas por el negocio (lila/lavanda polvo premium).
FORCED = {"a04a72": "6f5f96", "c47a9c": "9986bc", "f3e0ea": "ece6f5"}

OLD_HEXES = [
    "a04a72", "c47a9c", "5c2140", "f0bed7", "faf2f6", "8a5573", "f3e0ea", "d9a8c2",
    "7d3457", "5f2c48", "33222c", "fbf3f8", "fbeff5", "f8dfeb", "f6f1ea", "f2d5e3",
    "f2cfe0", "efd0e0", "e5c1d4", "dc9dbe", "d3a2bc", "c9789f", "b25a85", "2a1722",
    "1f0f18", "1c0f16",
]

HEX_MAP = []
seen_new = set()
for old in OLD_HEXES:
    new = FORCED.get(old) or hue_shift_hex(old)
    assert new not in [o for o in OLD_HEXES], f"colision new/old: {new}"
    assert new not in seen_new, f"colision new duplicado: {new}"
    seen_new.add(new)
    HEX_MAP.append((old, new))

for old, new in HEX_MAP:
    assert f"#{old}" in h or old.upper() in h, f"hex no encontrado: {old}"
    h = h.replace(old, new)
    h = h.replace(old.upper(), new)

OLD_RGBAS = [
    "160,74,114", "51,34,44", "240,190,215", "70,25,50", "250,242,246",
    "125,52,87", "253,246,250", "40,16,30", "233,205,186", "185,138,128",
]
RGBA_MAP = [(old, hue_shift_rgb(old)) for old in OLD_RGBAS]
for old, new in RGBA_MAP:
    assert old in h, f"rgb no encontrado: {old}"
    h = h.replace(old, new)

# Restaurar el badge dorado protegido.
h = h.replace("@@BADGE@@", badge_block, 1)

print("PARTE 5 OK (paleta lila / lavanda polvo, badge dorado protegido)")

open("output/alvarez-nails-studio-doral/index.html", "w").write(h)
print("DONE: output/alvarez-nails-studio-doral/index.html escrito")
