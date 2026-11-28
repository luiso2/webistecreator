import re
import shutil

SLUG = "bre-solutions-ocala"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/dark-v2/index.html", PATH)
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
# 2. Paleta: gold (pureartistry) -> burnt-orange/rust (logo real de BRE Solutions)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#d4a84b", "#d77e48"),
    ("#b8934a", "#bb7347"),
    ("#f0dc9e", "#f2bc9c"),
    ("#9a7431", "#9d582e"),
    ("#e5c374", "#e89e71"),
    ("#e8c476", "#eba073"),
    ("#c9a04a", "#cc7947"),
    ("#96742c", "#995329"),
    ("#e8cf96", "#eab494"),
    ("#f8eed3", "#f9e1d2"),
    ("#bfa060", "#c1835e"),
    ("#ecd9a8", "#eec1a6"),
    ("#f0dcae", "#f2c6ac"),
    ("#e9c3ab", "#ebc2a9"),
    ("#6b5222", "#6d3d20"),
    ("#1c1408", "#1c0f07"),
    ("#8a744a", "#8c6248"),
    ("#faf1dc", "#fbe7db"),
    ("#c9ab6b", "#cb8e69"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(215,126,72"),
    ("rgba(122,90,30", "rgba(124,64,28"),
    ("rgba(180,140,60", "rgba(183,105,57"),
    ("rgba(232,207,150", "rgba(234,180,148"),
    ("rgba(232,210,160", "rgba(234,187,158"),
    ("rgba(185,138,128", "rgba(186,149,127"),
    ("rgba(110,85,35", "rgba(112,63,33"),
    ("rgba(80,58,18", "rgba(82,41,16"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: sin plataforma de booking -> tel: + Facebook (no hay IG)
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+13522085428"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_FB_URL = "https://www.facebook.com/bresolutions"
c = h.count(OLD_IG_URL)
assert c == 6, c
h = h.replace(OLD_IG_URL, NEW_FB_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_FB_HANDLE = "facebook.com/bresolutions"
c = h.count(OLD_IG_HANDLE)
assert c == 4, c
h = h.replace(OLD_IG_HANDLE, NEW_FB_HANDLE)
print("GLOBALS done")

MAPS_URL = "https://www.google.com/maps/place/B.R.E.+Solutions+LLC/@29.114755,-82.400191,10z/data=!3m1!4b1!4m6!3m5!1s0x88e62d0945eab715:0x86230580fb0353d6!8m2!3d29.114755!4d-82.400191!16s%2Fg%2F11h6nkfxmd?authuser=0&hl=en&entry=ttu"

# Reparar el "Read all X reviews" (quedo apuntando a tel: por el replace global): va al listado real de Google
rep(f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    f'href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 33 reseñas en Google" data-en="Read all 33 reviews on Google">Read all 33 reviews on Google</a>')
print("REVIEWS LINK fixed")

# Facebook icon (outline, estilo Lucide/Feather) en vez del icono de Instagram, en los 4 lugares
OLD_IG_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>'
NEW_FB_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>'
rep_all(OLD_IG_ICON, NEW_FB_ICON, expect=2)
print("FB ICON done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>B.R.E. Solutions LLC · Handyman &amp; Property Maintenance in Ocala, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="B.R.E. Solutions LLC, Ocala FL: handyman repairs, lawn care, exterior painting, holiday lighting and rental turnovers for homeowners, landlords and Airbnb hosts. 5.0 stars across 33 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="B.R.E. Solutions LLC · Property Maintenance in Ocala, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Handyman repairs, lawn care, painting and rental turnovers in Ocala, FL. 5.0 on Google with 33 reviews. Call for a free estimate." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/logo.png" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/png" href="assets/logo.png" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "B.R.E. Solutions LLC",
    "description": "Property maintenance company serving Ocala, Marion County and Citrus County, FL: handyman repairs, lawn care, exterior painting, holiday light installation and turnover services for homeowners, landlords and Airbnb hosts.",
    "areaServed": [{ "@type": "City", "name": "Ocala" }, { "@type": "AdministrativeArea", "name": "Citrus County" }],
    "telephone": "+1-352-208-5428",
    "sameAs": ["''' + NEW_FB_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "33", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Property maintenance services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Handyman Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Rental & Airbnb Turnovers" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Lawn Care & Exterior Painting" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Holiday Light Installation" } }
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
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">BRE</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">BRE Solutions</span>')

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(215,126,72,0.35)]" />',
    '<img src="assets/logo.png" alt="B.R.E. Solutions LLC" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(215,126,72,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">BRE <span class="text-[color:var(--accent-deep)]">Solutions</span></span>')

rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Ocala, FL · Mantenimiento de Propiedades" data-en="Ocala, FL · Property Maintenance">Ocala, FL · Property Maintenance</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Mantenimiento de propiedades, bien hecho." data-en="Property maintenance, done right.">Property maintenance, done right.</p>',
    n=2)
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Reparaciones, jardinería" data-en="Handyman repairs, lawn care">Handyman repairs, lawn care</span><br /><span data-es="y mantenimiento de propiedades, " data-en="and property upkeep, ">and property upkeep, </span><span class="text-shine" data-es="bien hecho" data-en="done right">done right</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="B.R.E. Solutions se encarga de las reparaciones, el cuidado del césped, la pintura exterior y el trabajo de temporada que mantienen en buen estado una casa o propiedad de alquiler, de confianza para propietarios, arrendadores y anfitriones de Airbnb en Ocala y el condado de Citrus, con una calificación perfecta de 5.0 en Google." data-en="B.R.E. Solutions handles the handyman repairs, lawn care, exterior painting and seasonal work that keep a home or rental property in shape, trusted by homeowners, landlords and Airbnb hosts across Ocala and Citrus County, with a perfect 5.0 rating on Google.">B.R.E. Solutions handles the handyman repairs, lawn care, exterior painting and seasonal work that keep a home or rental property in shape, trusted by homeowners, landlords and Airbnb hosts across Ocala and Citrus County, with a perfect 5.0 rating on Google.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 33 reseñas en Google" data-en="5.0 · 33 reviews on Google">5.0 · 33 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar al (352) 208-5428" data-en="Call (352) 208-5428">Call (352) 208-5428</span>', n=1)
# (el boton secundario del hero ya quedo en FB_URL + NEW_FB_ICON + handle por los replaces globales del paso 3)
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Reseñas reales en Google" data-en="Real Google reviews">Real Google reviews</span>\n          <span data-es="Presupuesto gratis" data-en="Free estimates">Free estimates</span>\n          <span data-es="Línea directa" data-en="Direct phone line">Direct phone line</span>')
rep('aria-label="Lo que encontrará el cliente"', 'aria-label="What you get"')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/logo.png" alt="B.R.E. Solutions LLC logo" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg">Property Maintenance</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Presupuesto gratis · Ocala, FL" data-en="Free estimate · Ocala, FL">Free estimate · Ocala, FL</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="33">33</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Handyman <span class="text-shine">&amp;</span> Lawn Care</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Pintura · Luces navideñas" data-en="Painting · Holiday Lights">Painting · Holiday Lights</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl"><span data-es="Abierto" data-en="Open">Open</span> <span class="text-shine">7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Los 7 días, 8am a 5pm" data-en="7 days a week, 8am-5pm">7 days a week, 8am-5pm</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Ocala, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">&amp; Citrus County</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Handyman Repairs"),
    ("Loc Retwist", "Lawn Care"),
    ("Knotless Braids", "Exterior Painting"),
    ("K-Tip Extensions", "Holiday Lighting"),
    ("Keratin", "Rental Turnovers"),
    ("Orlando, FL", "Ocala, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (solo 1 foto real disponible: una sola imagen, no grid de 2)
# ---------------------------------------------------------------------------
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="frame zoomable aspect-[4/5] img-reveal">
        <img src="assets/logo.png" alt="B.R.E. Solutions LLC logo" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un equipo," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="todas las reparaciones cubiertas" data-en="all the repairs covered">all the repairs covered</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="B.R.E. Solutions es un equipo de mantenimiento de propiedades que atiende Ocala y el condado de Citrus: reparaciones de todo tipo, cuidado del césped, pintura exterior y trabajos de temporada como la instalación de luces navideñas, todo a cargo de un mismo equipo al que propietarios, arrendadores y anfitriones de Airbnb pueden llamar directamente." data-en="B.R.E. Solutions is a property maintenance team serving Ocala and Citrus County: handyman repairs, lawn care, exterior painting and seasonal work like holiday light installation, all handled by one crew that homeowners, landlords and Airbnb hosts can call directly.">B.R.E. Solutions is a property maintenance team serving Ocala and Citrus County: handyman repairs, lawn care, exterior painting and seasonal work like holiday light installation, all handled by one crew that homeowners, landlords and Airbnb hosts can call directly.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="El resultado: una calificación perfecta de 5.0 en 33 reseñas de Google, con propietarios y administradores de propiedades que destacan lo confiable, detallista y fácil de tratar que es el equipo, visita tras visita." data-en="The result: a perfect 5.0 rating across 33 Google reviews, with landlords and property managers specifically praising how reliable, detail oriented and easy to work with the team is, visit after visit.">The result: a perfect 5.0 rating across 33 Google reviews, with landlords and property managers specifically praising how reliable, detail oriented and easy to work with the team is, visit after visit.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="33">33</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Abierto todos los días" data-en="Open every day">Open every day</p></div>''')
rep('Booksy</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="33"',
    'Google</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="33"')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(215,126,72,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo.png" alt="B.R.E. Solutions LLC" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(215,126,72,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">BRE Solutions · <span class="text-[color:var(--ink-40)]" data-es="Equipo de mantenimiento" data-en="Property Maintenance Team">Property Maintenance Team</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Cómo trabajamos" data-en="How we work">How we work</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así trabajamos" data-en="How we">How we</span> <span class="text-shine" data-es="resolvemos cada trabajo" data-en="get it done">get it done</span></h2>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llama o escríbenos" data-en="Call or message us">Call or message us</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama, envía un mensaje de texto o escríbenos por Facebook y cuéntanos qué necesitas: una reparación, cuidado del césped, pintura o un turnover de alquiler." data-en="Call, text or message us on Facebook and tell us what needs doing: a repair, lawn care, painting or a rental turnover.">Call, text or message us on Facebook and tell us what needs doing: a repair, lawn care, painting or a rental turnover.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Revisamos el trabajo, en persona o por teléfono, y te damos un precio claro y honesto antes de empezar." data-en="We take a look, in person or over the phone, and give you a clear, honest price before any work starts.">We take a look, in person or over the phone, and give you a clear, honest price before any work starts.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Se hace el trabajo" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nuestro equipo llega y resuelve el trabajo, desde una reparación rápida hasta pintar el exterior completo o instalar luces navideñas, con la misma atención al detalle que mencionan nuestras reseñas." data-en="Our crew shows up and handles the job, from a quick repair to a full exterior paint job or a holiday light install, with the same attention to detail our reviews mention.">Our crew shows up and handles the job, from a quick repair to a full exterior paint job or a holiday light install, with the same attention to detail our reviews mention.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Revisión final" data-en="Walkthrough &amp; follow up">Walkthrough &amp; follow up</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Revisamos la propiedad contigo antes de dar el trabajo por terminado, y seguimos a una llamada de distancia para el siguiente trabajo, sobre todo si manejas varias propiedades." data-en="We walk the property with you before calling it done, and we are one call away for the next job, especially if you manage multiple properties.">We walk the property with you before calling it done, and we are one call away for the next job, especially if you manage multiple properties.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; solo nombres, sin precios inventados)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Servicios para" data-en="Services for">Services for</span> <span class="text-shine">your property</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Cada trabajo se cotiza después de revisar la propiedad. Llama o escríbenos por Facebook para un presupuesto gratis, sin compromiso." data-en="Every job is quoted after a quick look at the property. Call or message us on Facebook for a free, no-obligation estimate.">Every job is quoted after a quick look at the property. Call or message us on Facebook for a free, no-obligation estimate.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más solicitado" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Handyman Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Reparaciones generales y trabajos pequeños en la casa o la propiedad de alquiler, resueltos rápido y bien hechos desde la primera vez." data-en="General repairs and small jobs around the house or rental, handled quick and done right the first time.">General repairs and small jobs around the house or rental, handled quick and done right the first time.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(215,126,72,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad" data-en="Specialty">Specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Rental &amp; Airbnb Turnovers" data-en="Rental &amp; Airbnb Turnovers">Rental &amp; Airbnb Turnovers</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cuidado del césped, mantenimiento y entregas rápidas para propietarios y anfitriones de Airbnb en Ocala y el condado de Citrus que necesitan un equipo de confianza entre huéspedes o inquilinos." data-en="Lawn care, maintenance and quick turnarounds for landlords and Airbnb hosts in Ocala and Citrus County who need a crew they can count on between guests or tenants.">Lawn care, maintenance and quick turnarounds for landlords and Airbnb hosts in Ocala and Citrus County who need a crew they can count on between guests or tenants.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Imagen exterior" data-en="Curb appeal">Curb appeal</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lawn Care &amp; Exterior Painting" data-en="Lawn Care &amp; Exterior Painting">Lawn Care &amp; Exterior Painting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Mantenimiento regular del césped más pintura exterior que dura, con precio justo y un acabado limpio." data-en="Regular lawn maintenance plus exterior painting that holds up, priced fair and finished clean.">Regular lawn maintenance plus exterior painting that holds up, priced fair and finished clean.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="De temporada" data-en="Seasonal">Seasonal</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Holiday Light Installation" data-en="Holiday Light Installation">Holiday Light Installation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Instalación de luces navideñas de principio a fin, para que lo único que tengas que hacer sea disfrutarlas." data-en="Christmas light installation handled start to finish, so the only thing you do is enjoy it.">Christmas light installation handled start to finish, so the only thing you do is enjoy it.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Mantenimiento" data-en="Handyman">Handyman</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Reparaciones generales" data-en="General repairs">General repairs</li>
            <li class="flex items-center gap-2" data-es="Arreglos pequeños en casa" data-en="Small home fixes">Small home fixes</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Exterior" data-en="Outdoor">Outdoor</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Cuidado del césped" data-en="Lawn care">Lawn care</li>
            <li class="flex items-center gap-2" data-es="Pintura exterior" data-en="Exterior painting">Exterior painting</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Propiedades" data-en="Property Care">Property Care</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Turnovers de alquiler y Airbnb" data-en="Rental &amp; Airbnb turnovers">Rental &amp; Airbnb turnovers</li>
            <li class="flex items-center gap-2" data-es="Instalación de luces navideñas" data-en="Holiday light installation">Holiday light installation</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="El precio depende del trabajo y la propiedad. Llama al (352) 208-5428 o escríbenos por Facebook para un presupuesto exacto." data-en="Pricing depends on the job and the property. Call (352) 208-5428 or message us on Facebook for an exact quote.">Pricing depends on the job and the property. Call (352) 208-5428 or message us on Facebook for an exact quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA: se omite por completo (solo 1 foto real disponible, es el logo)
# ---------------------------------------------------------------------------
galeria_re = re.compile(r'\s*<!-- GALERIA -->\s*<section id="galeria">.*?</section>\n', flags=re.S)
# El comentario real no tiene ese id en una sola linea; usar regex sobre el bloque completo de la seccion
galeria_re = re.compile(r'  <!-- GALERIA -->\n  <section id="galeria".*?</section>\n\n', flags=re.S)
gm = galeria_re.search(h)
assert gm, "galeria section not found"
h = h[:gm.start()] + h[gm.end():]
print("GALERIA omitida (solo 1 foto real disponible)")

# ---------------------------------------------------------------------------
# 14. OPINIONES (3 reseñas reales verbatim de Google)
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="los clientes" data-en="customers say">customers say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 33 reseñas verificadas en Google" data-en="5.0 out of 5 · 33 verified reviews on Google">5.0 out of 5 · 33 verified reviews on Google</span>')
rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"BRE Solutions did a Christmas light installation job for me and I&#39;m extremely happy with the results. Great service and work!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Isabel Lalonde</span> <span class="text-[color:var(--ink-40)]" data-es="· Reseña de Google" data-en="· Google review">· Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"BRE Solutions provides lawn care and handyman services for my Airbnb properties in Citrus County. I have been using them for several months now and they always get the job done. I appreciate their attention to detail and flexibility."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Paul Burgos</span> <span class="text-[color:var(--ink-40)]" data-es="· Reseña de Google" data-en="· Google review">· Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We recently hired this team to paint the exterior of our home, and we couldn&#39;t be more pleased with the results. Their pricing was very competitive and fair, and the quality of the work was top-notch. They were professional throughout the entire process and did a fantastic job. Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Zachary Avant</span> <span class="text-[color:var(--ink-40)]" data-es="· Reseña de Google" data-en="· Google review">· Google review</span></figcaption>
        </figure>''')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION -> AREA DE SERVICIO (sin direccion fija, sin mapa; una sola columna)
# ---------------------------------------------------------------------------
old_ubicacion_re = re.compile(r'  <!-- UBICACION -->\n  <section id="ubicacion".*?</section>\n\n', flags=re.S)
um = old_ubicacion_re.search(h)
assert um, "ubicacion section not found"

NEW_UBICACION = '''  <!-- AREA DE SERVICIO -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-4xl mx-auto px-5 sm:px-8">
      <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5 text-center" data-es="Área de servicio" data-en="Service area">Service area</p>
      <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9 text-center" style="transition-delay:80ms"><span data-es="Atendemos" data-en="Serving">Serving</span> <span class="text-shine">Ocala &amp; Citrus County</span></h2>
      <div class="space-y-4">
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Área de servicio" data-en="Service Area">Service Area</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="B.R.E. Solutions trabaja en Ocala, el condado de Marion y el condado de Citrus, Florida, atendiendo cada trabajo en la propiedad, no desde un local." data-en="B.R.E. Solutions works across Ocala, Marion County and Citrus County, Florida, handling every job at the property, not from a storefront.">B.R.E. Solutions works across Ocala, Marion County and Citrus County, Florida, handling every job at the property, not from a storefront.</p>
          </div>
        </div>
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Abierto todos los días de 8 AM a 5 PM. Llama o envía un mensaje de texto para coordinar una visita." data-en="Open every day from 8 AM to 5 PM. Call or text to set up a time that works for your property.">Open every day from 8 AM to 5 PM. Call or text to set up a time that works for your property.</p>
            <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(215,126,72,0.4)]" href="''' + NEW_TEL + '''" data-es="Llamar al (352) 208-5428" data-en="Call (352) 208-5428">Call (352) 208-5428</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
          ''' + NEW_FB_ICON.replace('width="15" height="15"', 'width="20" height="20"') + '''
          <div>
            <p class="font-medium mb-1">Facebook</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira el trabajo del equipo y escríbenos directamente por Facebook." data-en="See more of what the team does and message us directly on Facebook.">See more of what the team does and message us directly on Facebook.</p>
            <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(215,126,72,0.4)]" href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener">facebook.com/bresolutions</a>
          </div>
        </div>
      </div>
    </div>
  </section>

'''
h = h[:um.start()] + NEW_UBICACION + h[um.end():]
print("UBICACION done (area de servicio, sin mapa ni direccion fija)")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
# (la frase del script ya quedo traducida en ambos lugares por el rep n=2 del paso HERO)
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo trabajo" data-en="Your next job">Your next job</span> <span class="text-shine" data-es="nos espera" data-en="is waiting">is waiting</span></h2>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Llama o escríbenos hoy: una reparación, una visita de cuidado del césped, un trabajo de pintura exterior o tu próximo turnover de alquiler, estamos listos cuando tú lo estés." data-en="Call or message us today: a repair, a lawn care visit, an exterior paint job or your next rental turnover, we are ready when you are.">Call or message us today: a repair, a lawn care visit, an exterior paint job or your next rental turnover, we are ready when you are.</p>')
rep(f'''<a href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="{NEW_FB_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    f'''<a href="{NEW_TEL}" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (352) 208-5428" data-en="Call (352) 208-5428">Call (352) 208-5428</a>
        <a href="{NEW_FB_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Escríbenos por Facebook" data-en="Message us on Facebook">Message us on Facebook</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">BRE Solutions</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(234,180,148,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo.png" alt="B.R.E. Solutions LLC" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(234,180,148,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">BRE Solutions</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Mantenimiento de propiedades en Ocala, el condado de Marion y el condado de Citrus, FL. Reparaciones, cuidado del césped, pintura y turnovers de alquiler." data-en="Property maintenance serving Ocala, Marion County and Citrus County, FL. Handyman repairs, lawn care, painting and rental turnovers.">Property maintenance serving Ocala, Marion County and Citrus County, FL. Handyman repairs, lawn care, painting and rental turnovers.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#ebc2a9]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p data-es="Ocala, FL y el condado de Citrus" data-en="Ocala, FL &amp; Citrus County">Ocala, FL &amp; Citrus County</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#ebc2a9]" data-es="Llamar al (352) 208-5428" data-en="Call (352) 208-5428">Call (352) 208-5428</a></p>''')
rep('<p><a href="' + NEW_FB_URL + '" target="_blank" rel="noopener" class="hover:text-[#ebc2a9]">Instagram · facebook.com/bresolutions</a></p>',
    '<p><a href="' + NEW_FB_URL + '" target="_blank" rel="noopener" class="hover:text-[#ebc2a9]">Facebook · bresolutions</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 B.R.E. Solutions LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep(f'<a href="{NEW_TEL}" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    f'<a href="{NEW_TEL}" class="book-float" aria-label="Call B.R.E. Solutions LLC">')
rep('<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span class="book-float-label" data-es="Llamar ahora" data-en="Call now">Call now</span>')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 19. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace(f'href="{NEW_TEL}" target="_blank" rel="noopener"', f'href="{NEW_TEL}"')
print("CLEANUP tel links done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", PATH)
