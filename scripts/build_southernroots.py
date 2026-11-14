import re
import os
import colorsys
import shutil

SLUG = "southern-roots-tree-landscape"
SRC = "templates/dark-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()


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


# ============================================================
# 1. PROTEGER EL BADGE MERKTOP (dorado, nunca cambia)
# ============================================================
m_css = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m_css
badge_css = m_css.group(0)
h = h.replace(badge_css, '@@BADGE_CSS@@', 1)

m_html = re.search(r'<a href="https://merktop\.com".*?</a>', h, flags=re.S)
assert m_html
badge_html = m_html.group(0)
h = h.replace(badge_html, '@@BADGE_HTML@@', 1)

# ============================================================
# 2. PALETA: dorado (pureartistry) -> verde azulado / teal (Southern Roots)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(212, 168, 75), (232, 207, 150), (185, 138, 128), (180, 140, 60), (122, 90, 30),
          (110, 85, 35), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]

TARGET_HUE = 185 / 360.0
SAT_MUL = 1.0


def _shift_hex(hx):
    hx = hx.lstrip('#')
    r, g, b = int(hx[0:2], 16) / 255, int(hx[2:4], 16) / 255, int(hx[4:6], 16) / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return '#%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def _shift_rgb(rgb):
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return (round(r2 * 255), round(g2 * 255), round(b2 * 255))


PALETTE = [(hx, _shift_hex(hx)) for hx in _HEXES]
for old, new in PALETTE:
    rep_all(old, new)

RGBA_FAMILIES = [(rgb, _shift_rgb(rgb)) for rgb in _RGBAS]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

h = h.replace('@@BADGE_CSS@@', badge_css, 1)
h = h.replace('@@BADGE_HTML@@', badge_html, 1)
print("PALETTE done")

# ============================================================
# 3. Globales: no hay booking platform, email ni IG -> tel: + Google reviews
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+18138465751"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Southern+Roots+Tree+and+Landscape+Valrico+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "2222 Durant Rd, Valrico, FL 33596"
NEW_MAPS = "https://www.google.com/maps?q=2222+Durant+Rd,+Valrico,+FL+33596"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Southern Roots Tree and Landscape · Tree Removal in Valrico, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Southern Roots Tree and Landscape, Valrico FL: tree removal, crane-assisted removal, trimming and storm cleanup. 4.9 stars across 410 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Southern Roots Tree and Landscape · Tree Removal in Valrico, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Tree removal, crane-assisted removal, trimming and storm cleanup. 4.9 on Google with 410 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-oak-trunk.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-oak-trunk.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Southern Roots Tree and Landscape",
    "description": "Tree service company in Valrico, FL serving the greater Tampa Bay area: tree removal, crane-assisted removal, tree trimming and pruning, and storm and emergency cleanup.",
    "address": { "@type": "PostalAddress", "streetAddress": "2222 Durant Rd", "addressLocality": "Valrico", "addressRegion": "FL", "postalCode": "33596", "addressCountry": "US" },
    "telephone": "+1-813-846-5751",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "410", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Tree services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tree Removal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Crane-Assisted Removal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tree Trimming &amp; Pruning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Storm &amp; Emergency Cleanup" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN default
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ============================================================
# 6. PRELOADER + NAV
# ============================================================
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">SR</span>\n    <span class="pre-word">Southern Roots</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,201,212,0.35)]" />',
    '<img src="assets/hero-oak-trunk.jpg" alt="Southern Roots Tree and Landscape" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,201,212,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Southern <span class="text-[color:var(--accent-deep)]">Roots</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call for a quote" data-en="Call for a quote">Call for a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Valrico, FL · Tree Service" data-en="Valrico, FL · Tree Service">Valrico, FL · Tree Service</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Safety is the priority, always." data-en="Safety is the priority, always.">Safety is the priority, always.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Tree removal, cranes" data-en="Tree removal, cranes">Tree removal, cranes</span><br /><span data-es="and cleanup, done " data-en="and cleanup, done ">and cleanup, done </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area. Bill and his crew have handled jobs large and small, with a 4.9 rating across 410 Google reviews." data-en="Tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area. Bill and his crew have handled jobs large and small, with a 4.9 rating across 410 Google reviews.">Tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area. Bill and his crew have handled jobs large and small, with a 4.9 rating across 410 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.9 · 410 reviews on Google" data-en="4.9 · 410 reviews on Google">4.9 · 410 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (813) 846-5751" data-en="Call (813) 846-5751">Call (813) 846-5751</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Trabajo real" data-en="Real work">Real work</span>\n          <span data-es="Precios claros" data-en="Clear pricing">Clear pricing</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Direct contact</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-oak-trunk.jpg" alt="A Southern Roots climber cutting the top of a large oak tree in Valrico, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">24 Hours</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="410">410</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Removal <span class="text-shine">&amp;</span> Cranes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Trimming · Cleanup" data-en="Trimming · Cleanup">Trimming · Cleanup</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">24</span> Hours</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Open every day" data-en="Open every day">Open every day</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Valrico</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Tampa Bay, FL" data-en="Tampa Bay, FL">Tampa Bay, FL</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Tree Removal"),
    ("Loc Retwist", "Crane Removal"),
    ("Knotless Braids", "Tree Trimming"),
    ("K-Tip Extensions", "Storm Cleanup"),
    ("Keratin", "Deadwooding"),
    ("Orlando, FL", "Valrico, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ============================================================
# 10. LA EXPERIENCIA
# ============================================================
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-1 gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal">
          <img src="assets/about-crew-roof.jpg" alt="Southern Roots crew members removing a tree over a Valrico home with a bucket lift" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Safety first," data-en="Safety first,">Safety first,</span><br /><span class="text-shine" data-es="quality is the standard" data-en="quality is the standard">quality is the standard</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Southern Roots Tree and Landscape is led by Bill and a full crew covering tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area, with their own cranes and bucket trucks." data-en="Southern Roots Tree and Landscape is led by Bill and a full crew covering tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area, with their own cranes and bucket trucks.">Southern Roots Tree and Landscape is led by Bill and a full crew covering tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area, with their own cranes and bucket trucks.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Customers describe a crew that comes out same day, works hard and safely on even the tallest trees, and leaves the property clean. The result: a 4.9-star rating across 410 Google reviews." data-en="Customers describe a crew that comes out same day, works hard and safely on even the tallest trees, and leaves the property clean. The result: a 4.9-star rating across 410 Google reviews.">Customers describe a crew that comes out same day, works hard and safely on even the tallest trees, and leaves the property clean. The result: a 4.9-star rating across 410 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="410">410</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Disponibilidad" data-en="Availability">Availability</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,201,212,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/hero-oak-trunk.jpg" alt="Southern Roots Tree and Landscape" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,201,212,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Bill · <span class="text-[color:var(--ink-40)]" data-es="Owner" data-en="Owner">Owner</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call it in" data-en="Call it in">Call it in</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call with the tree that needs attention, and a crew member often comes out the very same day for a free estimate." data-en="Call with the tree that needs attention, and a crew member often comes out the very same day for a free estimate.">Call with the tree that needs attention, and a crew member often comes out the very same day for a free estimate.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Free estimate" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Bill looks at the tree, the property and the access needed, then gives a clear, upfront price on the spot." data-en="Bill looks at the tree, the property and the access needed, then gives a clear, upfront price on the spot.">Bill looks at the tree, the property and the access needed, then gives a clear, upfront price on the spot.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The takedown" data-en="The takedown">The takedown</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Climbers, bucket trucks or a crane, whatever the tree and the property need, worked safely from top to bottom." data-en="Climbers, bucket trucks or a crane, whatever the tree and the property need, worked safely from top to bottom.">Climbers, bucket trucks or a crane, whatever the tree and the property need, worked safely from top to bottom.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The cleanup" data-en="The cleanup">The cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Logs, limbs and debris hauled off the same visit, leaving the lawn clear and ready for hurricane season." data-en="Logs, limbs and debris hauled off the same visit, leaving the lawn clear and ready for hurricane season.">Logs, limbs and debris hauled off the same visit, leaving the lawn clear and ready for hurricane season.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Tree work for" data-en="Tree work for">Tree work for</span> <span class="text-shine" data-es="every property" data-en="every property">every property</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two trees or properties are the same, so every job gets its own free estimate before any work begins." data-en="No two trees or properties are the same, so every job gets its own free estimate before any work begins.">No two trees or properties are the same, so every job gets its own free estimate before any work begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(75,201,212,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tree Removal" data-en="Tree Removal">Tree Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Dead, damaged or oversized trees removed completely, with the crew and equipment to handle 75-foot-plus trees." data-en="Dead, damaged or oversized trees removed completely, with the crew and equipment to handle 75-foot-plus trees.">Dead, damaged or oversized trees removed completely, with the crew and equipment to handle 75-foot-plus trees.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tight spaces" data-en="Tight spaces">Tight spaces</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Crane-Assisted Removal" data-en="Crane-Assisted Removal">Crane-Assisted Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Large trees near homes, pools or power lines lowered piece by piece with a crane for a controlled, safe takedown." data-en="Large trees near homes, pools or power lines lowered piece by piece with a crane for a controlled, safe takedown.">Large trees near homes, pools or power lines lowered piece by piece with a crane for a controlled, safe takedown.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it healthy" data-en="Keep it healthy">Keep it healthy</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tree Trimming &amp; Pruning" data-en="Tree Trimming &amp; Pruning">Tree Trimming &amp; Pruning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Oaks and other shade trees trimmed, deadwooded and pruned clear of roofs, power lines and walkways." data-en="Oaks and other shade trees trimmed, deadwooded and pruned clear of roofs, power lines and walkways.">Oaks and other shade trees trimmed, deadwooded and pruned clear of roofs, power lines and walkways.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Same day" data-en="Same day">Same day</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Storm &amp; Emergency Cleanup" data-en="Storm &amp; Emergency Cleanup">Storm &amp; Emergency Cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Fallen trees and storm debris cleared fast, day or night, to get the property safe again." data-en="Fallen trees and storm debris cleared fast, day or night, to get the property safe again.">Fallen trees and storm debris cleared fast, day or night, to get the property safe again.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Removal" data-en="Removal">Removal</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Full tree removal" data-en="Full tree removal">Full tree removal</li>
            <li class="flex items-center gap-2" data-es="Crane-assisted takedowns" data-en="Crane-assisted takedowns">Crane-assisted takedowns</li>
            <li class="flex items-center gap-2" data-es="Dead &amp; hazard tree removal" data-en="Dead &amp; hazard tree removal">Dead &amp; hazard tree removal</li>
            <li class="flex items-center gap-2" data-es="Stump grinding" data-en="Stump grinding">Stump grinding</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Trimming" data-en="Trimming">Trimming</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Tree trimming &amp; pruning" data-en="Tree trimming &amp; pruning">Tree trimming &amp; pruning</li>
            <li class="flex items-center gap-2" data-es="Deadwooding" data-en="Deadwooding">Deadwooding</li>
            <li class="flex items-center gap-2" data-es="Canopy thinning" data-en="Canopy thinning">Canopy thinning</li>
            <li class="flex items-center gap-2" data-es="Roofline clearance" data-en="Roofline clearance">Roofline clearance</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Cleanup" data-en="Cleanup">Cleanup</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Storm damage cleanup" data-en="Storm damage cleanup">Storm damage cleanup</li>
            <li class="flex items-center gap-2" data-es="Emergency tree removal" data-en="Emergency tree removal">Emergency tree removal</li>
            <li class="flex items-center gap-2" data-es="Debris &amp; log haul away" data-en="Debris &amp; log haul away">Debris &amp; log haul away</li>
            <li class="flex items-center gap-2" data-es="Free estimates" data-en="Free estimates">Free estimates</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on tree size and access. Call (813) 846-5751, open 24 hours, for a free estimate." data-en="Pricing depends on tree size and access. Call (813) 846-5751, open 24 hours, for a free estimate.">Pricing depends on tree size and access. Call (813) 846-5751, open 24 hours, for a free estimate.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="work" data-en="work">work</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (813) 846-5751
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Remocion con grua junto a la calle" data-en="Crane-assisted removal on a residential street">Crane-assisted removal on a residential street</span><img src="assets/gallery-crane-removal.jpg" alt="A crane lowering a cut tree section during a Southern Roots tree removal" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Camion con canasta junto a la casa" data-en="Bucket truck working close to the home">Bucket truck working close to the home</span><img src="assets/gallery-bucket-truck.jpg" alt="A Southern Roots bucket truck removing a large oak next to a house" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Corte en lo alto con camion canasta" data-en="Topping a tree from the bucket">Topping a tree from the bucket</span><img src="assets/gallery-bucket-topping.jpg" alt="A Southern Roots crew member in a bucket truck topping a tall tree" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Retiro de arbol cubierto de enredaderas" data-en="Clearing a vine-covered tree">Clearing a vine-covered tree</span><img src="assets/gallery-vine-tree.jpg" alt="A Southern Roots climber working on a tree covered in vines" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Poda de madera muerta en pino alto" data-en="Deadwooding a tall pine">Deadwooding a tall pine</span><img src="assets/gallery-deadwooding.jpg" alt="A Southern Roots climber deadwooding a tall pine tree" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 15. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Valrico" data-en="What Valrico">What Valrico</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="4.9 out of 5 · 410 reviews on Google" data-en="4.9 out of 5 · 410 reviews on Google">4.9 out of 5 · 410 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Southern Roots did a great job on our oak! They came out the same day for a free estimate and had our tree trimmed 2 days later. They supported law enforcement, were friendly, and communicated well. I've included before and after pictures. Now we are ready for hurricane season."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ashley Velazquez</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Thank you to Bill and his team for taking care of our property! We had several trees that were overhanging the roof, and we contacted Bill for an estimate before we replaced the roof. We were on a short time frame and needed the work done..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Amber Robinson</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The entire crew did an awesome job from start to finish. They worked hard and safely while taking down several dead trees and some very tall trees (75ft plus) that was extremely close to both my house and my neighbor's house. They took..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chad</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 410 reviews on Google" data-en="Read all 410 reviews on Google">Read all 410 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 16. UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Valrico, FL</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,201,212,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,201,212,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,201,212,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open 24 hours, every day of the week." data-en="Open 24 hours, every day of the week.">Open 24 hours, every day of the week.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,201,212,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (813) 846-5751" data-en="Call (813) 846-5751">Call (813) 846-5751</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,201,212,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Reviews" data-en="Reviews">Reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.9 stars across 410 verified Google reviews." data-en="4.9 stars across 410 verified Google reviews.">4.9 stars across 410 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,201,212,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Southern Roots Tree and Landscape, 2222 Durant Rd, Valrico FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 17. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Safety is the priority, always." data-en="Safety is the priority, always.">Safety is the priority, always.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call," data-en="One call,">One call,</span> <span class="text-shine" data-es="any size tree" data-en="any size tree">any size tree</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (813) 846-5751 for a free estimate on your tree removal, crane job or storm cleanup. Open 24 hours, every day." data-en="Call (813) 846-5751 for a free estimate on your tree removal, crane job or storm cleanup. Open 24 hours, every day.">Call (813) 846-5751 for a free estimate on your tree removal, crane job or storm cleanup. Open 24 hours, every day.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (813) 846-5751" data-en="Call (813) 846-5751">Call (813) 846-5751</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ============================================================
# 18. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Southern Roots</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,225,232,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/hero-oak-trunk.jpg" alt="Southern Roots Tree and Landscape" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,225,232,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Southern Roots</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Tree service serving Valrico and the greater Tampa Bay area, FL." data-en="Tree service serving Valrico and the greater Tampa Bay area, FL.">Tree service serving Valrico and the greater Tampa Bay area, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#abe4e9]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#abe4e9]" data-es="Call (813) 846-5751" data-en="Call (813) 846-5751">Call (813) 846-5751</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#abe4e9]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#abe4e9]">4.9 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Southern Roots Tree and Landscape.</p>')
print("FOOTER done")

# ============================================================
# 19. Boton flotante
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#081a1c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Southern Roots">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#081a1c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
print("BOOK-FLOAT done")

# ============================================================
# 20. Limpieza tel: target=_blank/rel
# ============================================================
h = h.replace(f'href="{NEW_TEL}" target="_blank" rel="noopener"', f'href="{NEW_TEL}"')
print("CLEANUP done")

# ============================================================
# 21. Traduccion ES
# ============================================================
T = {
    "Valrico, FL · Tree Service": "Valrico, FL · Servicio de Arboles",
    "Safety is the priority, always.": "La seguridad es la prioridad, siempre.",
    "Tree removal, cranes": "Remocion de arboles, gruas",
    "and cleanup, done ": "y limpieza, hecho ",
    "right": "bien",
    "Tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area. Bill and his crew have handled jobs large and small, with a 4.9 rating across 410 Google reviews.":
        "Remocion de arboles, trabajos con grua, poda y limpieza tras tormentas en Valrico y el area de Tampa Bay. Bill y su equipo han manejado trabajos grandes y pequenos, con calificacion de 4.9 en 410 resenas de Google.",
    "4.9 · 410 reviews on Google": "4.9 · 410 resenas en Google",
    "Call (813) 846-5751": "Llama al (813) 846-5751",
    "Open": "Abierto",
    "Every day of the week": "Todos los dias de la semana",
    "Trimming · Cleanup": "Poda · Limpieza",
    "Open every day": "Abierto todos los dias",
    "Tampa Bay, FL": "Tampa Bay, FL",
    "Safety first,": "Seguridad primero,",
    "quality is the standard": "la calidad es el estandar",
    "Southern Roots Tree and Landscape is led by Bill and a full crew covering tree removal, crane-assisted takedowns, trimming and storm cleanup across Valrico and the greater Tampa Bay area, with their own cranes and bucket trucks.":
        "Southern Roots Tree and Landscape es dirigido por Bill y un equipo completo que cubre remocion de arboles, trabajos con grua, poda y limpieza tras tormentas en Valrico y el area de Tampa Bay, con sus propias gruas y camiones con canasta.",
    "Customers describe a crew that comes out same day, works hard and safely on even the tallest trees, and leaves the property clean. The result: a 4.9-star rating across 410 Google reviews.":
        "Los clientes describen un equipo que llega el mismo dia, trabaja duro y con seguridad incluso en los arboles mas altos, y deja la propiedad limpia. El resultado: una calificacion de 4.9 estrellas en 410 resenas de Google.",
    "Owner": "Dueno",
    "How it works": "Asi se trabaja",
    "Call it in": "Llama y cuenta",
    "Call with the tree that needs attention, and a crew member often comes out the very same day for a free estimate.":
        "Llama con el arbol que necesita atencion, y un miembro del equipo llega muchas veces el mismo dia para una cotizacion gratis.",
    "Free estimate": "Cotizacion gratis",
    "Bill looks at the tree, the property and the access needed, then gives a clear, upfront price on the spot.":
        "Bill revisa el arbol, la propiedad y el acceso necesario, y da un precio claro y directo en el momento.",
    "The takedown": "La bajada",
    "Climbers, bucket trucks or a crane, whatever the tree and the property need, worked safely from top to bottom.":
        "Trabajadores que suben, camiones con canasta o grua, lo que necesite el arbol y la propiedad, trabajado con seguridad de arriba hacia abajo.",
    "The cleanup": "La limpieza",
    "Logs, limbs and debris hauled off the same visit, leaving the lawn clear and ready for hurricane season.":
        "Troncos, ramas y escombros se retiran en la misma visita, dejando el pasto limpio y listo para la temporada de huracanes.",
    "Tree work for": "Trabajo de arboles para",
    "every property": "cada propiedad",
    "No two trees or properties are the same, so every job gets its own free estimate before any work begins.":
        "Ningun arbol o propiedad es igual a otro, asi que cada trabajo recibe su propia cotizacion gratis antes de comenzar.",
    "Most requested": "Lo mas solicitado",
    "Tree Removal": "Remocion de Arboles",
    "Dead, damaged or oversized trees removed completely, with the crew and equipment to handle 75-foot-plus trees.":
        "Arboles muertos, danados o demasiado grandes se remueven por completo, con el equipo y la maquinaria para manejar arboles de mas de 75 pies.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Tight spaces": "Espacios reducidos",
    "Crane-Assisted Removal": "Remocion con Grua",
    "Large trees near homes, pools or power lines lowered piece by piece with a crane for a controlled, safe takedown.":
        "Arboles grandes cerca de casas, piscinas o lineas electricas se bajan por secciones con una grua para una remocion controlada y segura.",
    "Keep it healthy": "Mantenlo sano",
    "Tree Trimming &amp; Pruning": "Poda y Corte de Arboles",
    "Oaks and other shade trees trimmed, deadwooded and pruned clear of roofs, power lines and walkways.":
        "Robles y otros arboles de sombra se podan, se les quita la madera muerta y se despejan de techos, lineas electricas y caminos.",
    "Same day": "El mismo dia",
    "Storm &amp; Emergency Cleanup": "Limpieza de Emergencia y Tormentas",
    "Fallen trees and storm debris cleared fast, day or night, to get the property safe again.":
        "Arboles caidos y escombros de tormenta se limpian rapido, de dia o de noche, para que la propiedad vuelva a estar segura.",
    "Removal": "Remocion",
    "Full tree removal": "Remocion completa de arboles",
    "Crane-assisted takedowns": "Remociones con grua",
    "Dead &amp; hazard tree removal": "Remocion de arboles muertos o peligrosos",
    "Stump grinding": "Trituracion de tocones",
    "Trimming": "Poda",
    "Tree trimming &amp; pruning": "Poda y corte de arboles",
    "Deadwooding": "Remocion de madera muerta",
    "Canopy thinning": "Aclareo de follaje",
    "Roofline clearance": "Despeje de techos",
    "Cleanup": "Limpieza",
    "Storm damage cleanup": "Limpieza de danos por tormenta",
    "Emergency tree removal": "Remocion de emergencia",
    "Debris &amp; log haul away": "Retiro de escombros y troncos",
    "Free estimates": "Cotizaciones gratis",
    "Pricing depends on tree size and access. Call (813) 846-5751, open 24 hours, for a free estimate.":
        "El precio depende del tamano del arbol y el acceso. Llama al (813) 846-5751, abierto 24 horas, para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Valrico": "Lo que dicen los",
    "customers say": "clientes en Valrico",
    "Read all 410 reviews on Google": "Lee las 410 resenas en Google",
    "Serving": "Sirviendo a",
    "Hours": "Horario",
    "Open 24 hours, every day of the week.": "Abierto 24 horas, todos los dias de la semana.",
    "Reviews": "Resenas",
    "4.9 stars across 410 verified Google reviews.": "4.9 estrellas en 410 resenas verificadas de Google.",
    "One call,": "Una llamada,",
    "any size tree": "cualquier tamano de arbol",
    "Call (813) 846-5751 for a free estimate on your tree removal, crane job or storm cleanup. Open 24 hours, every day.":
        "Llama al (813) 846-5751 para una cotizacion gratis de tu remocion de arbol, trabajo con grua o limpieza tras tormenta. Abierto 24 horas, todos los dias.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Tree service serving Valrico and the greater Tampa Bay area, FL.": "Servicio de arboles en Valrico y el area de Tampa Bay, FL.",
    "Contact": "Contacto",
}

_missing = []
for _en, _es in T.items():
    _pat = f'data-es="{_en}" data-en="{_en}"'
    _new = f'data-es="{_es}" data-en="{_en}"'
    if _pat in h:
        h = h.replace(_pat, _new)
    else:
        _missing.append(_en)
assert not _missing, "missing ES translations for: " + repr(_missing)
print("TRANSLATE ES done,", len(T), "strings")

with open(DST, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", DST)
