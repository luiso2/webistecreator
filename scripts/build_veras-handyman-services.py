import re
import shutil

SLUG = "veras-handyman-services"
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
# 2. Paleta: gold (pureartistry) -> azul acero (hue-rotate 205, sat*0.85)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#d4a84b", "#5599ca"),
    ("#b8934a", "#5289b0"),
    ("#f0dc9e", "#a4cdea"),
    ("#9a7431", "#396d92"),
    ("#e5c374", "#7cb5dd"),
    ("#e8c476", "#7fb7df"),
    ("#c9a04a", "#5492bf"),
    ("#96742c", "#34698e"),
    ("#e8cf96", "#9cc5e2"),
    ("#f8eed3", "#d6e8f5"),
    ("#bfa060", "#6796b8"),
    ("#ecd9a8", "#adcfe7"),
    ("#f0dcae", "#b3d4eb"),
    ("#e9c3ab", "#b0cee4"),
    ("#6b5222", "#274c66"),
    ("#1c1408", "#09131a"),
    ("#8a744a", "#4f6f85"),
    ("#faf1dc", "#deedf8"),
    ("#c9ab6b", "#72a1c2"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(85,153,202"),
    ("rgba(122,90,30", "rgba(37,83,115"),
    ("rgba(180,140,60", "rgba(69,128,171"),
    ("rgba(232,207,150", "rgba(156,197,226"),
    ("rgba(232,210,160", "rgba(165,201,227"),
    ("rgba(185,138,128", "rgba(132,161,181"),
    ("rgba(110,85,35", "rgba(41,78,104"),
    ("rgba(80,58,18", "rgba(23,53,75"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: sin plataforma de booking -> tel:. Sin FB/IG verificado -> se quita.
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+18138227225"
c = h.count(OLD_BOOK)
assert c > 0, c
h = h.replace(OLD_BOOK, NEW_TEL)
print(f"GLOBALS done ({c} Booksy->tel)")

MAPS_URL = "https://www.google.com/maps/place/Veras+Handyman+Services/@28.0122,-82.2448,10z/data=!3m1!4b1!4m6!3m5!1s0:0x0!8m2!3d28.0122!4d-82.2448?authuser=0&hl=en&entry=ttu"

# "Read all X reviews" quedo apuntando a tel: por el replace global: va al listado real de Google
rep(f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    f'href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 10 reseñas en Google" data-en="Read all 10 reviews on Google">Read all 10 reviews on Google</a>')
print("REVIEWS LINK fixed")

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"

# Quitar el boton secundario de IG del hero (no hay red social verificada)
rep(f'''<a href="{OLD_IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>''', '', n=1)

# Quitar el link @handle de la cabecera de Galeria
rep(f'''<a href="{OLD_IG_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @pure.artistrysk
        </a>''', '', n=1)

# Quitar el boton secundario de IG del CTA final
rep(f'<a href="{OLD_IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>', '', n=1)
print("SOCIAL BUTTONS removed (no verified FB/IG)")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Veras Handyman Services · Handyman in Seffner &amp; Brandon, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Veras Handyman Services, Seffner/Brandon FL: bathroom remodels, water and roof damage repairs and general handyman work. 5.0 stars across 10 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Veras Handyman Services · Handyman in Seffner &amp; Brandon, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Bathroom remodels, water damage repair and general handyman work. 5.0 on Google with 10 reviews. Call for a free estimate." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-4.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-1.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Veras Handyman Services",
    "description": "Handyman service serving Seffner, Brandon and the greater Tampa Bay area: bathroom remodels, water and storm damage repair, and general handyman work.",
    "areaServed": [{ "@type": "City", "name": "Seffner" }, { "@type": "City", "name": "Brandon" }, { "@type": "AdministrativeArea", "name": "Hillsborough County" }],
    "telephone": "+1-813-822-7225",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "10", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bathroom Remodeling" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Water & Storm Damage Repair" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Handyman Repairs" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">VH</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Veras Handyman</span>')

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(215,126,72,0.35)]" />'.replace('rgba(215,126,72', 'rgba(85,153,202'),
    '<img src="assets/raw/gmaps-1.jpg" alt="Veras Handyman Services" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(85,153,202,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Veras <span class="text-[color:var(--accent-deep)]">Handyman</span></span>')

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep(f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Seffner y Brandon, FL · Handyman" data-en="Seffner &amp; Brandon, FL · Handyman">Seffner &amp; Brandon, FL · Handyman</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Un trabajo honesto, bien hecho a la primera." data-en="Honest work, done right the first time.">Honest work, done right the first time.</p>',
    n=2)
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Baños, reparaciones" data-en="Bathroom remodels, repairs">Bathroom remodels, repairs</span><br /><span data-es="y mantenimiento de propiedades, " data-en="and property upkeep, ">and property upkeep, </span><span class="text-shine" data-es="bien hechos" data-en="done right">done right</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Veras Handyman Services hace remodelaciones de baño, reparaciones de daños de agua y techo, y trabajos generales de mantenimiento en Seffner, Brandon y alrededores. El equipo de Ramon y Lin tiene una calificación perfecta de 5.0 en 10 reseñas de Google." data-en="Veras Handyman Services handles bathroom remodels, water and roof damage repairs, and general handyman work across Seffner, Brandon and the surrounding area. The Ramon and Lin team holds a perfect 5.0 rating across 10 Google reviews.">Veras Handyman Services handles bathroom remodels, water and roof damage repairs, and general handyman work across Seffner, Brandon and the surrounding area. The Ramon and Lin team holds a perfect 5.0 rating across 10 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 10 reseñas en Google" data-en="5.0 · 10 reviews on Google">5.0 · 10 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar al (813) 822-7225" data-en="Call (813) 822-7225">Call (813) 822-7225</span>', n=1)
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Reseñas reales en Google" data-en="Real Google reviews">Real Google reviews</span>\n          <span data-es="Presupuesto gratis" data-en="Free estimates">Free estimates</span>\n          <span data-es="Línea directa" data-en="Direct phone line">Direct phone line</span>')
rep('aria-label="Lo que encontrará el cliente"', 'aria-label="What you get"')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-4.jpg" alt="Finished bathroom remodel by Veras Handyman Services in Seffner, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg">Free Estimate</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Seffner y Brandon, FL" data-en="Seffner &amp; Brandon, FL">Seffner &amp; Brandon, FL</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="10">10</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Bathroom <span class="text-shine">&amp;</span> Repairs</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Remodelacion - Daños de agua" data-en="Remodels - Water Damage">Remodels - Water Damage</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl"><span data-es="Abierto" data-en="Open">Open</span> 6</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Dias a la semana, domingo cerrado" data-en="Days a week, closed Sundays">Days a week, closed Sundays</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Seffner</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">&amp; Brandon, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2 widgets, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Bathroom Remodels"),
    ("Loc Retwist", "Water Damage Repair"),
    ("Knotless Braids", "Roof Repairs"),
    ("K-Tip Extensions", "General Handyman"),
    ("Keratin", "Free Estimates"),
    ("Orlando, FL", "Seffner, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (una sola foto real: trabajo en progreso)
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
        <img src="assets/raw/gmaps-5.jpg" alt="Veras Handyman Services crew removing water damaged drywall during a repair job" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un equipo," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="trabajo hecho con cuidado" data-en="work done with care">work done with care</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Veras Handyman Services es un equipo de reparacion y remodelacion que atiende Seffner, Brandon y el area de Tampa Bay: remodelaciones de bano completas, reparacion de daños de agua y techo, y los trabajos generales que una casa necesita, todo coordinado por Ramon y Lin." data-en="Veras Handyman Services is a repair and remodeling team serving Seffner, Brandon and the greater Tampa Bay area: full bathroom remodels, water and roof damage repair, and the general handyman work a home needs, all coordinated directly by Ramon and Lin.">Veras Handyman Services is a repair and remodeling team serving Seffner, Brandon and the greater Tampa Bay area: full bathroom remodels, water and roof damage repair, and the general handyman work a home needs, all coordinated directly by Ramon and Lin.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientes lo confirman: trabajo prolijo, puntual y con buena comunicacion de principio a fin. 5.0 perfecto en 10 reseñas verificadas de Google." data-en="Customers confirm it: tidy, punctual work with clear communication from start to finish. A perfect 5.0 across 10 verified Google reviews.">Customers confirm it: tidy, punctual work with clear communication from start to finish. A perfect 5.0 across 10 verified Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="10">10</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Rápido" data-en="Fast">Fast</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Respuesta rápida" data-en="Quick response">Quick response</p></div>''')
rep('''<p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p>''',
    '''<p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(85,153,202,0.3)]" loading="lazy" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="Veras Handyman Services team" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(85,153,202,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Veras Handyman · <span class="text-[color:var(--ink-40)]" data-es="Baños y reparaciones" data-en="Bathroom &amp; repair specialists">Bathroom &amp; repair specialists</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO -> COMO TRABAJAMOS
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Como trabajamos" data-en="How we work">How we work</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="De la llamada" data-en="From the call">From the call</span> <span class="text-shine" data-es="al trabajo terminado" data-en="to the finished job">to the finished job</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nos cuentas que necesitas arreglar o remodelar y te damos un presupuesto gratis por telefono, sin compromiso." data-en="Tell us what needs fixing or remodeling and we give you a free, no obligation estimate over the phone.">Tell us what needs fixing or remodeling and we give you a free, no obligation estimate over the phone.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Visita al lugar" data-en="On-site visit">On-site visit</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Evaluamos el daño o el alcance del trabajo en persona antes de empezar, para que no haya sorpresas en el precio." data-en="We assess the damage or the scope of the job in person before starting, so there are no surprises in the price.">We assess the damage or the scope of the job in person before starting, so there are no surprises in the price.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="El trabajo se hace" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde una reparacion rapida hasta una remodelacion completa de bano, con limpieza al terminar cada jornada." data-en="From a quick repair to a full bathroom remodel, with cleanup at the end of every work day.">From a quick repair to a full bathroom remodel, with cleanup at the end of every work day.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Revision final" data-en="Final walkthrough">Final walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Revisamos el trabajo juntos antes de irnos. Si algo no te convence, lo corregimos ahi mismo." data-en="We walk through the finished work together before we leave. If something is not right, we fix it on the spot.">We walk through the finished work together before we leave. If something is not right, we fix it on the spot.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Presupuesto gratis en cada trabajo. Sin cargos ocultos." data-en="Free estimate on every job. No hidden fees.">Free estimate on every job. No hidden fees.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Lo que" data-en="What we">What we</span> <span class="text-shine" data-es="hacemos" data-en="do">do</span>')

OLD_SERVICES = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert OLD_SERVICES
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(85,153,202,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad" data-en="Specialty">Specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Remodelacion de baños" data-en="Bathroom Remodeling">Bathroom Remodeling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Baños completos de principio a fin: ducha, piso, vanity y acabados, con atencion al detalle segun las reseñas de nuestros clientes." data-en="Full bathrooms from start to finish: shower, flooring, vanity and finishes, with the attention to detail our customers mention in their reviews.">Full bathrooms from start to finish: shower, flooring, vanity and finishes, with the attention to detail our customers mention in their reviews.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18138227225" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Reparaciones" data-en="Repairs">Repairs</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Daños de agua y techo" data-en="Water &amp; Roof Damage Repair">Water &amp; Roof Damage Repair</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Reparacion de paredes, drywall y techo tras una fuga o un daño de techo, incluyendo trabajo post roofers." data-en="Repair of walls, drywall and ceilings after a leak or roof damage, including post-roofer repair work.">Repair of walls, drywall and ceilings after a leak or roof damage, including post-roofer repair work.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18138227225" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cocinas" data-en="Kitchens">Kitchens</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Instalaciones de cocina" data-en="Kitchen Installs">Kitchen Installs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Electrodomesticos, encimeras y acabados instalados con cuidado, limpios y listos para usar." data-en="Appliances, countertops and finishes installed with care, clean and ready to use.">Appliances, countertops and finishes installed with care, clean and ready to use.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18138227225" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="General" data-en="General">General</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Mantenimiento general" data-en="General Handyman">General Handyman</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Electrico menor, plomeria, carpinteria y todo lo que una casa necesita arreglar." data-en="Minor electrical, plumbing, carpentry and whatever else a house needs fixed.">Minor electrical, plumbing, carpentry and whatever else a house needs fixed.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18138227225" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
'''
h = h[:OLD_SERVICES.start()] + NEW_SERVICES + h[OLD_SERVICES.end():]

OLD_NOTE = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert OLD_NOTE
h = h[:OLD_NOTE.start()] + OLD_NOTE.group(1) + '<span data-es="No ves tu proyecto en la lista? Llama y te damos un presupuesto gratis." data-en="Do not see your project listed? Call and we will give you a free estimate.">Do not see your project listed? Call and we will give you a free estimate.</span>' + OLD_NOTE.group(2) + h[OLD_NOTE.end():]
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (solo 3 fotos reales buenas: 1 ancha + 2 normales)
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="results">results</span>')

OLD_GAL_LINK = re.search(r'<a href="tel:\+18138227225" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">.*?</a>\s*', h, flags=re.S)
if OLD_GAL_LINK:
    h = h[:OLD_GAL_LINK.start()] + h[OLD_GAL_LINK.end():]

OLD_GALLERY = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert OLD_GALLERY
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Baño renovado" data-en="Renovated bathroom">Renovated bathroom</span><img src="assets/raw/gmaps-3.jpg" alt="Baño renovado con ducha de vidrio por Veras Handyman Services" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cocina terminada" data-en="Finished kitchen">Finished kitchen</span><img src="assets/raw/gmaps-2.jpg" alt="Cocina con electrodomesticos instalados por Veras Handyman Services" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Instalacion electrica" data-en="Electrical install">Electrical install</span><img src="assets/raw/gmaps-7.jpg" alt="Instalacion de luz de techo por Veras Handyman Services" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:OLD_GALLERY.start()] + NEW_GALLERY + h[OLD_GALLERY.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="nuestros clientes" data-en="customers say">customers say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 10 reseñas verificadas en Google" data-en="5.0 out of 5 · 10 verified reviews on Google">5.0 out of 5 · 10 verified reviews on Google</span>')

OLD_T1 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>'''
NEW_T1 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Ramon and Lin are an excellent team in handyman services. They remodeled my master bathroom with attention to detail and always considering my preferences and opinion. They are punctual, responsible."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Vanessa</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>'''
rep(OLD_T1, NEW_T1)

OLD_T2 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>'''
NEW_T2 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Super pleased with the work Ramon did for me at my house. Very attentive to details, beautiful work and finishes, punctual, communicates well, cleans up after his jobs, and has very competitive pricing."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Elba Gonzalez</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>'''
rep(OLD_T2, NEW_T2)

OLD_T3 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>'''
NEW_T3 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Reached out to Veras Handyman Services and they were top notch. Quick to respond and easy to work with on a roof damage repair job in Valrico."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Peter Yang</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>'''
rep(OLD_T3, NEW_T3)
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION -> SERVICE AREA (sin direccion exacta, sin mapa: negocio sin local al publico)
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Area de servicio en" data-en="Serving">Serving</span> <span class="text-shine" data-es="Seffner y Brandon" data-en="Seffner &amp; Brandon">Seffner &amp; Brandon</span>')

OLD_LOC_CARDS = re.search(r'<div class="space-y-4">.*?</div>\s*</div>\s*<div class="frame map-frame reveal min-h-\[380px\]".*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert OLD_LOC_CARDS
NEW_LOC = '''<div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Area de servicio" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Seffner, Brandon, Valrico, Plant City y el resto del condado de Hillsborough." data-en="Seffner, Brandon, Valrico, Plant City and the rest of Hillsborough County.">Seffner, Brandon, Valrico, Plant City and the rest of Hillsborough County.</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Llama o escribe" data-en="Call or text">Call or text</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Presupuesto gratis por telefono antes de agendar la visita." data-en="Free estimate over the phone before we schedule a visit.">Free estimate over the phone before we schedule a visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(85,153,202,0.4)]" href="tel:+18138227225" data-es="(813) 822-7225" data-en="(813) 822-7225">(813) 822-7225</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a jueves y sabado, 8am a 6pm. Viernes 8am a 5pm. Domingo cerrado." data-en="Monday to Thursday and Saturday, 8am to 6pm. Friday 8am to 5pm. Closed Sundays.">Monday to Thursday and Saturday, 8am to 6pm. Friday 8am to 5pm. Closed Sundays.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="frame reveal min-h-[380px]" style="transition-delay:180ms">
        <img src="assets/raw/gmaps-1.jpg" alt="Baño terminado por Veras Handyman Services" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>
    </div>
  </section>'''
h = h[:OLD_LOC_CARDS.start()] + NEW_LOC + h[OLD_LOC_CARDS.end():]
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Un arreglo bien hecho" data-en="A repair done right">A repair done right</span> <span class="text-shine" data-es="esta a una llamada" data-en="is one call away">is one call away</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Presupuesto gratis, sin cargos ocultos. Bano, reparacion de daño de agua o ese arreglo pendiente en la casa." data-en="Free estimate, no hidden fees. A bathroom, a water damage repair or that fix you have been putting off.">Free estimate, no hidden fees. A bathroom, a water damage repair or that fix you have been putting off.</p>')
rep('<a href="tel:+18138227225" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="tel:+18138227225" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (813) 822-7225" data-en="Call (813) 822-7225">Call (813) 822-7225</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Veras Handyman</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(234,180,148,0.35)]" loading="lazy" />'.replace('rgba(234,180,148', 'rgba(156,197,226'),
    '<img src="assets/raw/gmaps-1.jpg" alt="Veras Handyman Services" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(156,197,226,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Veras Handyman Services</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Servicio de handyman en Seffner, Brandon y el area de Tampa Bay. Presupuesto gratis por telefono." data-en="Handyman service serving Seffner, Brandon and the greater Tampa Bay area. Free estimates by phone.">Handyman service serving Seffner, Brandon and the greater Tampa Bay area. Free estimates by phone.</p>')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="tel:+18138227225" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'''.replace('#e9c3ab', '#b0cee4'),
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>Seffner &amp; Brandon, FL</p>
        <p><a href="tel:+18138227225" class="hover:text-[#b0cee4]">(813) 822-7225</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="hover:text-[#b0cee4]">Instagram · @pure.artistrysk</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Horario" data-en="Hours">Hours</p>
        <p data-es="Lun-Jue y Sab: 8am-6pm" data-en="Mon-Thu &amp; Sat: 8am-6pm">Mon-Thu &amp; Sat: 8am-6pm</p>
        <p data-es="Viernes: 8am-5pm" data-en="Friday: 8am-5pm">Friday: 8am-5pm</p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Veras Handyman Services.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. BOTON FLOTANTE
# ---------------------------------------------------------------------------
rep('<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span class="book-float-label" data-es="Llamar" data-en="Call now">Call now</span>')
rep('aria-label="Reservar cita online"', 'aria-label="Call Veras Handyman Services"')

open(PATH, "w", encoding="utf-8").write(h)
print("WRITTEN", PATH)
