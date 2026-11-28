import re
import shutil

SLUG = "mr-and-mrs-handy-services-llc"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/light-v2/index.html", PATH)
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:200]
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    c = h.count(a)
    assert c > 0, "NO ANCHOR: " + a[:200]
    if expect is not None:
        assert c == expect, f"count {c} != expected {expect} for " + a[:80]
    h = h.replace(a, b)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (Lash Bloom) -> borgona/vino (negocio real: sin marca visual
#    propia mas alla del letrero rojo/blanco de su trailer, asi que se deriva un
#    vino profundo clasico, premium, sobre la misma base clara).
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#7a3d4f"),
    ("#5c2140", "#4a2f3b"),
    ("#f0bed7", "#e3b8c2"),
    ("#c47a9c", "#a3697c"),
    ("#8a5573", "#724a57"),
    ("#d9a8c2", "#cf9eae"),
    ("#7d3457", "#5c2d3d"),
    ("#5f2c48", "#46222f"),
    ("#fbf3f8", "#faf3f4"),
    ("#fbeff5", "#f6ecec"),
    ("#f8dfeb", "#efd9dc"),
    ("#f2d5e3", "#e8d2d8"),
    ("#f2cfe0", "#ecd3d8"),
    ("#efd0e0", "#e6d2d6"),
    ("#e5c1d4", "#d9c0c6"),
    ("#dc9dbe", "#c98fa0"),
    ("#d3a2bc", "#b98998"),
    ("#c9789f", "#a66577"),
    ("#b25a85", "#8f4d64"),
    ("#2a1722", "#2a1a1e"),
    ("#1f0f18", "#1f1215"),
    ("#1c0f16", "#1c1214"),
    ("#f3e0ea", "#f1e4e6"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(122,61,79"),
    ("rgba(240,190,215", "rgba(227,184,194"),
    ("rgba(125,52,87", "rgba(92,45,61"),
    ("rgba(185,138,128", "rgba(150,95,88"),
    ("rgba(233,205,186", "rgba(225,195,188"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: sin booking online, sin FB/IG publico -> todo a tel:
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+13219484890"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, NEW_TEL)
print("GLOBALS (booksy->tel) done")

MAPS_URL = "https://www.google.com/maps/place/Mr.+%26+Mrs.+Handy+Services+LLC/data=!4m7!3m6!1s0xa9b044fdb3f31bf1:0x4585f617da075537!8m2!3d28.664613!4d-81.5872639!16s%2Fg%2F11rhwl1jfg!19sChIJ8Rvzs_1EsKkRN1UH2hf2hUU?authuser=0&hl=en&g_ep=EgoyMDI2MTEyMy4wIJJjKgBIAVAD&rclk=1"

# "Read all X reviews" -> va al listado real de Google, no a tel:
rep(f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    f'href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 47 reseñas en Google" data-en="Read all 47 reviews on Google">Read all 47 reviews on Google</a>')
print("REVIEWS LINK fixed")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Mr. &amp; Mrs. Handy Services LLC · Handyman in Kissimmee &amp; Central FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Mr. &amp; Mrs. Handy Services LLC, serving Kissimmee and Central Florida: drywall repair, interior painting, fixture and door installs, and rental property turnovers. 5.0 stars across 47 Google reviews. Free estimates." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Mr. &amp; Mrs. Handy Services LLC · Handyman in Kissimmee, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Drywall, painting, installs and property turnovers. 5.0 on Google with 47 reviews. Call for a free estimate." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-5.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Mr. & Mrs. Handy Services LLC",
    "description": "Handyman and property maintenance team serving Kissimmee and Central Florida: drywall repair and texture matching, interior painting, light fixture and ceiling fan installation, door and cabinetry installs, and turnover work for landlords and property managers.",
    "areaServed": [{ "@type": "City", "name": "Kissimmee" }, { "@type": "AdministrativeArea", "name": "Central Florida" }],
    "telephone": "+1-321-948-4890",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "47", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Drywall Repair & Texture Matching" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Interior Painting" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Fixture, Fan & Door Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Rental & Property Manager Turnovers" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (ya es el default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">M&amp;M</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Mr &amp; Mrs Handy</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(122,61,79,0.35)]" />',
    '<img src="assets/raw/logo.jpg" alt="Mr. & Mrs. Handy Services trailer" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(122,61,79,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Mr &amp; Mrs <span class="text-[color:var(--accent-deep)]">Handy</span></span>')

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Kissimmee, FL · Handyman Services" data-en="Kissimmee, FL · Handyman Services">Kissimmee, FL · Handyman Services</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="El trabajo bien hecho, sin sorpresas." data-en="The job done right, no surprises.">The job done right, no surprises.</p>',
    n=2)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Reparaciones, pintura y" data-en="Repairs, painting and">Repairs, painting and</span><br /><span data-es="mantenimiento de propiedades, " data-en="property upkeep, ">property upkeep, </span><span class="text-shine" data-es="bien hecho" data-en="done right">done right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Hugo y Jackie forman el equipo detras de Mr. &amp; Mrs. Handy Services: reparaciones de drywall, pintura interior, instalacion de puertas, lamparas y ventiladores, y el mantenimiento de propiedades de alquiler que propietarios y administradores necesitan, con presupuesto gratis y una calificacion perfecta de 5.0 en Google." data-en="Hugo and Jackie are the team behind Mr. & Mrs. Handy Services: drywall repair, interior painting, door, light fixture and ceiling fan installs, and the rental property upkeep that landlords and property managers rely on, with free estimates and a perfect 5.0 rating on Google.">Hugo and Jackie are the team behind Mr. & Mrs. Handy Services: drywall repair, interior painting, door, light fixture and ceiling fan installs, and the rental property upkeep that landlords and property managers rely on, with free estimates and a perfect 5.0 rating on Google.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 47 reseñas en Google" data-en="5.0 · 47 reviews on Google">5.0 · 47 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar al (321) 948-4890" data-en="Call (321) 948-4890">Call (321) 948-4890</span>', n=1)
# Quitar el boton secundario de Instagram del hero (no hay IG/FB publico)
rep('''
          <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>
''', '', n=1)
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-5.jpg" alt="Remodelacion de bano terminada por Mr. and Mrs. Handy Services" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg" data-es="Presupuesto Gratis" data-en="Free Estimates">Free Estimates</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Kissimmee y Centro de Florida" data-en="Kissimmee & Central FL">Kissimmee &amp; Central FL</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="47">47</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Drywall <span class="text-shine">&amp;</span> Paint</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Reparacion y textura" data-en="Repair & texture match">Repair &amp; texture match</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span data-es="Presupuesto" data-en="Free">Free</span> <span class="text-shine" data-es="gratis" data-en="estimate">estimate</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sin compromiso" data-en="No obligation">No obligation</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Kissimmee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="y Centro de Florida" data-en="& Central Florida">&amp; Central Florida</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Drywall Repair"),
    ("Hybrid Set", "Interior Painting"),
    ("Volume Set", "Fixture Installs"),
    ("Mega Volume", "Door Installs"),
    ("Bottom Lashes", "Property Turnovers"),
    ("West Palm Beach, FL", "Kissimmee, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-2.jpg" alt="Hugo y Jackie instalando una lampara de techo en escalera" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-4.jpg" alt="Camioneta y trailer de Mr. and Mrs. Handy Services en un vecindario de Kissimmee" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un equipo," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="todas las reparaciones cubiertas" data-en="every repair covered">every repair covered</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Mr. &amp; Mrs. Handy Services es el equipo de Hugo y Jackie, quienes atienden Kissimmee y el centro de Florida: drywall, pintura interior, instalacion de puertas, lamparas, ventiladores de techo y gabinetes, ademas del trabajo de mantenimiento que propietarios y administradores de propiedades de alquiler necesitan en cada cambio de inquilino." data-en="Mr. & Mrs. Handy Services is the two person team of Hugo and Jackie, serving Kissimmee and Central Florida: drywall, interior painting, door, light fixture, ceiling fan and cabinetry installs, plus the turnover upkeep that landlords and property managers need between tenants.">Mr. & Mrs. Handy Services is the two person team of Hugo and Jackie, serving Kissimmee and Central Florida: drywall, interior painting, door, light fixture, ceiling fan and cabinetry installs, plus the turnover upkeep that landlords and property managers need between tenants.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: una calificacion perfecta de 5.0 en 47 reseñas de Google, con clientes que destacan lo confiables, detallistas y faciles de tratar que son, y administradores de propiedades que trabajan con ellos en multiples direcciones a la vez." data-en="The result: a perfect 5.0 rating across 47 Google reviews, with clients praising how reliable, detail oriented and easy to work with they are, and property managers who trust them across multiple addresses at once.">The result: a perfect 5.0 rating across 47 Google reviews, with clients praising how reliable, detail oriented and easy to work with they are, and property managers who trust them across multiple addresses at once.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="47">47</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Equipo familiar" data-en="Family team">Family team</p></div>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(122,61,79,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>''',
    '''<img src="assets/raw/logo.jpg" alt="Mr. & Mrs. Handy Services" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(122,61,79,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Hugo &amp; Jackie · <span class="text-[color:var(--ink-40)]" data-es="Equipo familiar" data-en="Family owned team">Family owned team</span></span>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO -> COMO TRABAJAMOS
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Como trabajamos" data-en="How we work">How we work</p>', n=1)
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="De la llamada" data-en="From your call">From your call</span> <span class="text-shine" data-es="al trabajo terminado" data-en="to the finished job">to the finished job</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nos cuentas que necesitas arreglar, instalar o pintar, y coordinamos una visita para ver el trabajo." data-en="Tell us what needs fixing, installing or painting, and we set up a visit to see the job.">Tell us what needs fixing, installing or painting, and we set up a visit to see the job.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Evaluamos el trabajo y te damos un precio claro antes de empezar, sin sorpresas en la factura." data-en="We look at the job and give you a clear price before starting, no surprises on the bill.">We look at the job and give you a clear price before starting, no surprises on the bill.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Hugo y Jackie trabajan" data-en="Hugo & Jackie get to work">Hugo &amp; Jackie get to work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Drywall, pintura, instalaciones o mantenimiento, hecho con cuidado y limpiando despues de cada visita." data-en="Drywall, paint, installs or upkeep, done with care and cleaned up after every visit.">Drywall, paint, installs or upkeep, done with care and cleaned up after every visit.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Trabajo terminado" data-en="Job done right">Job done right</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Si eres propietario o administrador de propiedades, te seguimos atendiendo visita tras visita." data-en="If you are a landlord or property manager, we keep showing up visit after visit.">If you are a landlord or property manager, we keep showing up visit after visit.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (variante adaptada: sin precios fijos, "se cotiza" / free estimate)
# ---------------------------------------------------------------------------
rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que" data-en="What we">What we</span> <span class="text-shine" data-es="hacemos" data-en="handle">handle</span></h2>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Presupuesto gratis en cada visita. Llama o escribe para contarnos el trabajo." data-en="Free estimate on every visit. Call or text to describe the job.">Free estimate on every visit. Call or text to describe the job.</p>')

SERVICES_BLOCK_OLD = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert SERVICES_BLOCK_OLD
SERVICES_BLOCK_NEW = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Reparacion" data-en="Repair">Repair</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Drywall y Pintura" data-en="Drywall & Paint">Drywall &amp; Paint</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Reparacion y emparejado de textura, pintura de puertas, paredes de acento y gabinetes de cocina." data-en="Drywall repair and texture matching, plus painting doors, accent walls and kitchen cabinets.">Drywall repair and texture matching, plus painting doors, accent walls and kitchen cabinets.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-xl text-shine" data-es="Se cotiza" data-en="Free quote">Free quote</p></div>
            <a href="tel:+13219484890" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(122,61,79,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Instalaciones" data-en="Installations">Installations</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Lamparas, ventiladores de techo, puertas y gabinetes, instalados y nivelados correctamente." data-en="Light fixtures, ceiling fans, doors and cabinetry, installed and leveled the right way.">Light fixtures, ceiling fans, doors and cabinetry, installed and leveled the right way.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-xl text-shine" data-es="Se cotiza" data-en="Free quote">Free quote</p></div>
            <a href="tel:+13219484890" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Exteriores" data-en="Outdoor">Outdoor</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Mejoras del hogar" data-en="Home Upgrades">Home Upgrades</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cocinas exteriores, barras caseras, reemplazo de weatherstripping y remocion de chatarra de garaje." data-en="Outdoor kitchens, home bar installs, weatherstripping replacement and garage junk removal.">Outdoor kitchens, home bar installs, weatherstripping replacement and garage junk removal.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-xl text-shine" data-es="Se cotiza" data-en="Free quote">Free quote</p></div>
            <a href="tel:+13219484890" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Propietarios" data-en="Landlords">Landlords</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Mantenimiento de Alquileres" data-en="Rental Turnovers">Rental Turnovers</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trabajo recurrente para propietarios y administradores de propiedades en multiples direcciones." data-en="Recurring work for landlords and property managers across multiple addresses.">Recurring work for landlords and property managers across multiple addresses.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-xl text-shine" data-es="Se cotiza" data-en="Free quote">Free quote</p></div>
            <a href="tel:+13219484890" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>\n      '''
h = h[:SERVICES_BLOCK_OLD.start()] + SERVICES_BLOCK_NEW + h[SERVICES_BLOCK_OLD.end():]

NOTE_OLD = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert NOTE_OLD
h = h[:NOTE_OLD.start()] + NOTE_OLD.group(1) + '<span data-es="Antecedentes verificados. Presupuesto gratis antes de cada trabajo." data-en="Background checked. Free estimate before every job.">Background checked. Free estimate before every job.</span>' + NOTE_OLD.group(2) + h[NOTE_OLD.end():]
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="work">work</span></h2>')
GALLERY_HEADER_LINK_OLD = re.search(r'<a href="https://www\.instagram\.com/_lashbloom/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">.*?</a>\s*\n', h, flags=re.S)
assert GALLERY_HEADER_LINK_OLD
h = h[:GALLERY_HEADER_LINK_OLD.start()] + h[GALLERY_HEADER_LINK_OLD.end():]

GALLERY_GRID_OLD = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert GALLERY_GRID_OLD
GALLERY_GRID_NEW = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Instalacion de cocina exterior" data-en="Outdoor kitchen install">Outdoor kitchen install</span><img src="assets/raw/gmaps-7.jpg" alt="Cocina exterior de acero inoxidable instalada por Mr. and Mrs. Handy Services" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Antes y despues" data-en="Before & after">Before &amp; after</span><img src="assets/raw/gmaps-3.jpg" alt="Antes y despues de instalar un ventilador de techo" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Barra casera instalada" data-en="Home bar installed">Home bar installed</span><img src="assets/raw/gmaps-6.jpg" alt="Instalacion de barra casera de 8 piezas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Marco de ventana y fregadero" data-en="Window trim & sink">Window trim &amp; sink</span><img src="assets/raw/gmaps-1.jpg" alt="Marco de ventana nuevo sobre fregadero de cocina" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Puerta instalada" data-en="Custom door install">Custom door install</span><img src="assets/raw/gmaps-8.jpg" alt="Puerta interior instalada a medida" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Remodelacion de cocina" data-en="Kitchen remodel">Kitchen remodel</span><img src="assets/raw/gmaps-9.jpg" alt="Cocina remodelada con gabinetes y mesones nuevos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:GALLERY_GRID_OLD.start()] + GALLERY_GRID_NEW + h[GALLERY_GRID_OLD.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES (3 reseñas reales verbatim de Google)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What our">What our</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span></h2>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 47 reseñas verificadas en Google" data-en="5.0 out of 5 · 47 verified reviews on Google">5.0 out of 5 · 47 verified reviews on Google</span>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Highly recommend Mr. &amp; Mrs. Handy Services! If you want your project done right, these are the people you want to use. They do NOT cut corners and your project will be done correctly."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Jody Stancliff</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The most reliable and responsive handyman team you will ever find. I have worked with Hugo and Jackie on multiple properties as a property manager. Drywall patches, paint, weatherstripping, light fixtures, anything I need."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Ashley Mitchell</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mr and Mrs Handyman have done several repairs and installations in our home. They are always responsive, communicative and do excellent work. Their pricing is fair and if they cannot do a job they refer fellow contractors they trust."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Miami Shop Girl</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION -> SERVICE AREA (sin direccion fija, sin mapa: negocio movil)
# ---------------------------------------------------------------------------
UBICACION_OLD = re.search(r'<!-- UBICACION -->.*?</section>', h, flags=re.S)
assert UBICACION_OLD
UBICACION_NEW = '''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-4xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-14">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Area de servicio" data-en="Service area">Service area</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Atendemos" data-en="Serving">Serving</span> <span class="text-shine">Kissimmee &amp; Central FL</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 gap-5">
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Donde trabajamos" data-en="Where we work">Where we work</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Negocio movil: vamos a tu casa o propiedad en Kissimmee y el centro de Florida. Sin local al que visitar." data-en="We come to you: a mobile team serving homes and rental properties around Kissimmee and Central Florida. No shop to visit.">We come to you: a mobile team serving homes and rental properties around Kissimmee and Central Florida. No shop to visit.</p>
          </div>
        </div>
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Llama o escribe" data-en="Call or text">Call or text</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Presupuesto gratis por telefono. Respondemos rapido, los 7 dias de la semana." data-en="Free estimates by phone. We respond fast, seven days a week.">Free estimates by phone. We respond fast, seven days a week.</p>
            <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(122,61,79,0.4)]" href="tel:+13219484890">(321) 948-4890</a>
          </div>
        </div>
      </div>
    </div>
  </section>'''
h = h[:UBICACION_OLD.start()] + UBICACION_NEW + h[UBICACION_OLD.end():]
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu presupuesto gratis" data-en="Your free estimate">Your free estimate</span> <span class="text-shine" data-es="esta a una llamada" data-en="is one call away">is one call away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Drywall, pintura, instalaciones o mantenimiento de alquileres en Kissimmee y el centro de Florida. Presupuesto gratis, sin compromiso." data-en="Drywall, painting, installs or rental turnovers across Kissimmee and Central Florida. Free estimate, no obligation.">Drywall, painting, installs or rental turnovers across Kissimmee and Central Florida. Free estimate, no obligation.</p>')
rep('''<a href="tel:+13219484890" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="tel:+13219484890" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (321) 948-4890" data-en="Call (321) 948-4890">Call (321) 948-4890</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Mr &amp; Mrs Handy</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(227,184,194,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<img src="assets/raw/logo.jpg" alt="Mr. & Mrs. Handy Services" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(227,184,194,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Mr &amp; Mrs Handy</span>''')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Equipo de handyman movil atendiendo Kissimmee y el centro de Florida." data-en="Mobile handyman team serving Kissimmee and Central Florida.">Mobile handyman team serving Kissimmee and Central Florida.</p>')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="tel:+13219484890" target="_blank" rel="noopener" class="hover:text-[#e3b8c2]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p><a href="tel:+13219484890" class="hover:text-[#e3b8c2]">(321) 948-4890</a></p>
        <p data-es="Kissimmee y centro de Florida" data-en="Kissimmee & Central Florida">Kissimmee &amp; Central Florida</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="hover:text-[#e3b8c2]">Instagram · @_lashbloom</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Horario" data-en="Hours">Hours</p>
        <p data-es="Lunes a sabado, 8am a 6pm" data-en="Monday to Saturday, 8am to 6pm">Monday to Saturday, 8am to 6pm</p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Mr. &amp; Mrs. Handy Services LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante
# ---------------------------------------------------------------------------
rep('<a href="tel:+13219484890" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+13219484890" class="book-float" aria-label="Llamar ahora">')
print("FLOAT done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("WROTE", PATH, len(h), "bytes")
