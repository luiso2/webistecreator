import re
import os
import colorsys
import shutil

SLUG = "tnt-tree-service-llc"
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
# 2. PALETA: dorado (pureartistry) -> verde bosque (TNT Tree Service)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(212, 168, 75), (232, 207, 150), (185, 138, 128), (180, 140, 60), (122, 90, 30),
          (110, 85, 35), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]

TARGET_HUE = 132 / 360.0
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
NEW_TEL = "tel:+18132704794"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=TNT+Tree+Service+Lutz+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "1915 S Mobile Villa Dr, Lutz, FL 33549"
NEW_MAPS = "https://www.google.com/maps?q=1915+S+Mobile+Villa+Dr,+Lutz,+FL+33549"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>TNT Tree Service LLC · Tree Removal &amp; Trimming in Lutz, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="TNT Tree Service LLC, Lutz FL: palm tree trimming, tree removal, pruning and storm cleanup. 4.9 stars across 11 Google reviews. Open 24 hours, call for a free quote." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="TNT Tree Service LLC · Tree Removal &amp; Trimming in Lutz, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Palm tree trimming, tree removal, pruning and storm cleanup. 4.9 on Google with 11 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-palm-climb.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-palm-climb.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "TNT Tree Service LLC",
    "description": "Tree service company in Lutz, FL serving the Tampa Bay area: palm tree trimming, tree removal, tree trimming and pruning, and storm and yard cleanup.",
    "address": { "@type": "PostalAddress", "streetAddress": "1915 S Mobile Villa Dr", "addressLocality": "Lutz", "addressRegion": "FL", "postalCode": "33549", "addressCountry": "US" },
    "telephone": "+1-813-270-4794",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "11", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Tree services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Palm Tree Trimming" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tree Removal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tree Trimming &amp; Pruning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Storm &amp; Yard Cleanup" } }
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
    '<span class="pre-mono">TNT</span>\n    <span class="pre-word">TNT Tree Service</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,212,102,0.35)]" />',
    '<img src="assets/hero-palm-climb.jpg" alt="TNT Tree Service" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,212,102,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">TNT <span class="text-[color:var(--accent-deep)]">Tree</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call for a quote" data-en="Call for a quote">Call for a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Lutz, FL · Tree Service" data-en="Lutz, FL · Tree Service">Lutz, FL · Tree Service</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Your trees, handled with care." data-en="Your trees, handled with care.">Your trees, handled with care.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Palm trimming, removal" data-en="Palm trimming, removal">Palm trimming, removal</span><br /><span data-es="and cleanup, done " data-en="and cleanup, done ">and cleanup, done </span><span class="text-shine" data-es="safely" data-en="safely">safely</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Palm tree trimming, full tree removal, pruning and storm cleanup across Lutz and the greater Tampa Bay area. A responsive crew that climbs clean and leaves the yard spotless, with a 4.9 rating across 11 Google reviews." data-en="Palm tree trimming, full tree removal, pruning and storm cleanup across Lutz and the greater Tampa Bay area. A responsive crew that climbs clean and leaves the yard spotless, with a 4.9 rating across 11 Google reviews.">Palm tree trimming, full tree removal, pruning and storm cleanup across Lutz and the greater Tampa Bay area. A responsive crew that climbs clean and leaves the yard spotless, with a 4.9 rating across 11 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.9 · 11 reviews on Google" data-en="4.9 · 11 reviews on Google">4.9 · 11 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (813) 270-4794" data-en="Call (813) 270-4794">Call (813) 270-4794</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Trabajo real" data-en="Real work">Real work</span>\n          <span data-es="Precios claros" data-en="Clear pricing">Clear pricing</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Direct contact</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-palm-climb.jpg" alt="A TNT Tree Service climber trimming a tall palm tree in Lutz, FL" class="blur-up w-full h-full object-cover" />')
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
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="11">11</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Palm <span class="text-shine">&amp;</span> Oak</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Trimming · Removal · Pruning" data-en="Trimming · Removal · Pruning">Trimming · Removal · Pruning</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">24</span> Hours</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Open every day" data-en="Open every day">Open every day</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Lutz</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Tampa Bay, FL" data-en="Tampa Bay, FL">Tampa Bay, FL</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Palm Trimming"),
    ("Loc Retwist", "Tree Removal"),
    ("Knotless Braids", "Pruning"),
    ("K-Tip Extensions", "Storm Cleanup"),
    ("Keratin", "Yard Cleanup"),
    ("Orlando, FL", "Lutz, FL"),
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
          <img src="assets/about-oak-climb.jpg" alt="A TNT Tree Service climber cutting a large oak limb in Lutz, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="A crew that" data-en="A crew that">A crew that</span><br /><span class="text-shine" data-es="climbs clean" data-en="climbs clean">climbs clean</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="TNT Tree Service LLC is a Lutz-based tree crew covering palm tree trimming, full tree removal, pruning and storm cleanup across the greater Tampa Bay area. Climbers work clean with ropes and harnesses, leaving a small footprint behind." data-en="TNT Tree Service LLC is a Lutz-based tree crew covering palm tree trimming, full tree removal, pruning and storm cleanup across the greater Tampa Bay area. Climbers work clean with ropes and harnesses, leaving a small footprint behind.">TNT Tree Service LLC is a Lutz-based tree crew covering palm tree trimming, full tree removal, pruning and storm cleanup across the greater Tampa Bay area. Climbers work clean with ropes and harnesses, leaving a small footprint behind.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Customers describe TNT as responsive, fair priced and quick to schedule, even for same-day jobs. The result: a 4.9-star rating across 11 Google reviews." data-en="Customers describe TNT as responsive, fair priced and quick to schedule, even for same-day jobs. The result: a 4.9-star rating across 11 Google reviews.">Customers describe TNT as responsive, fair priced and quick to schedule, even for same-day jobs. The result: a 4.9-star rating across 11 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="11">11</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Disponibilidad" data-en="Availability">Availability</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,212,102,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/hero-palm-climb.jpg" alt="TNT Tree Service" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,212,102,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">TNT Tree Service · <span class="text-[color:var(--ink-40)]" data-es="Tree crew" data-en="Tree crew">Tree crew</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call it in" data-en="Call it in">Call it in</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text what needs trimming or removing, any time of day, and the crew talks through the job with you." data-en="Call or text what needs trimming or removing, any time of day, and the crew talks through the job with you.">Call or text what needs trimming or removing, any time of day, and the crew talks through the job with you.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Fair quote" data-en="Fair quote">Fair quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A crew member comes out fast, often the next day, and gives a fair, upfront price before any climbing starts." data-en="A crew member comes out fast, often the next day, and gives a fair, upfront price before any climbing starts.">A crew member comes out fast, often the next day, and gives a fair, upfront price before any climbing starts.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The climb" data-en="The climb">The climb</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Climbers rope in and work the tree from the top down, cutting clean and keeping the footprint on the lawn small." data-en="Climbers rope in and work the tree from the top down, cutting clean and keeping the footprint on the lawn small.">Climbers rope in and work the tree from the top down, cutting clean and keeping the footprint on the lawn small.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The cleanup" data-en="The cleanup">The cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Branches, logs and debris get hauled away same day, so the yard looks better than before the crew arrived." data-en="Branches, logs and debris get hauled away same day, so the yard looks better than before the crew arrived.">Branches, logs and debris get hauled away same day, so the yard looks better than before the crew arrived.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Tree work for" data-en="Tree work for">Tree work for</span> <span class="text-shine" data-es="every yard" data-en="every yard">every yard</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two trees are the same, so every job gets its own fair, upfront quote by phone before any climbing begins." data-en="No two trees are the same, so every job gets its own fair, upfront quote by phone before any climbing begins.">No two trees are the same, so every job gets its own fair, upfront quote by phone before any climbing begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(72,183,96,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Palm Tree Trimming" data-en="Palm Tree Trimming">Palm Tree Trimming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Climbed and trimmed by hand, the job most Lutz homeowners call TNT about before hurricane season." data-en="Climbed and trimmed by hand, the job most Lutz homeowners call TNT about before hurricane season.">Climbed and trimmed by hand, the job most Lutz homeowners call TNT about before hurricane season.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Full removal" data-en="Full removal">Full removal</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tree Removal" data-en="Tree Removal">Tree Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Dead, leaning or oversized trees taken down in sections, climbed and lowered to protect the rest of the yard." data-en="Dead, leaning or oversized trees taken down in sections, climbed and lowered to protect the rest of the yard.">Dead, leaning or oversized trees taken down in sections, climbed and lowered to protect the rest of the yard.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Shape it up" data-en="Shape it up">Shape it up</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tree Trimming &amp; Pruning" data-en="Tree Trimming &amp; Pruning">Tree Trimming &amp; Pruning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Oaks and other shade trees trimmed and pruned to clear roofs and power lines and keep the canopy healthy." data-en="Oaks and other shade trees trimmed and pruned to clear roofs and power lines and keep the canopy healthy.">Oaks and other shade trees trimmed and pruned to clear roofs and power lines and keep the canopy healthy.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Same day" data-en="Same day">Same day</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Storm &amp; Yard Cleanup" data-en="Storm &amp; Yard Cleanup">Storm &amp; Yard Cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Fallen limbs, storm debris and cut wood hauled away the same day the job is finished." data-en="Fallen limbs, storm debris and cut wood hauled away the same day the job is finished.">Fallen limbs, storm debris and cut wood hauled away the same day the job is finished.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Palms" data-en="Palms">Palms</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Palm tree trimming" data-en="Palm tree trimming">Palm tree trimming</li>
            <li class="flex items-center gap-2" data-es="Frond &amp; seed pod removal" data-en="Frond &amp; seed pod removal">Frond &amp; seed pod removal</li>
            <li class="flex items-center gap-2" data-es="Hurricane prep trims" data-en="Hurricane prep trims">Hurricane prep trims</li>
            <li class="flex items-center gap-2" data-es="Dead palm removal" data-en="Dead palm removal">Dead palm removal</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Removal &amp; Pruning" data-en="Removal &amp; Pruning">Removal &amp; Pruning</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Full tree removal" data-en="Full tree removal">Full tree removal</li>
            <li class="flex items-center gap-2" data-es="Oak &amp; shade tree pruning" data-en="Oak &amp; shade tree pruning">Oak &amp; shade tree pruning</li>
            <li class="flex items-center gap-2" data-es="Canopy thinning" data-en="Canopy thinning">Canopy thinning</li>
            <li class="flex items-center gap-2" data-es="HOA-approved trims" data-en="HOA-approved trims">HOA-approved trims</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Cleanup" data-en="Cleanup">Cleanup</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Storm debris cleanup" data-en="Storm debris cleanup">Storm debris cleanup</li>
            <li class="flex items-center gap-2" data-es="Yard &amp; sidewalk cleanup" data-en="Yard &amp; sidewalk cleanup">Yard &amp; sidewalk cleanup</li>
            <li class="flex items-center gap-2" data-es="Log &amp; branch haul away" data-en="Log &amp; branch haul away">Log &amp; branch haul away</li>
            <li class="flex items-center gap-2" data-es="Free estimates" data-en="Free estimates">Free estimates</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on tree size and access. Call (813) 270-4794, open 24 hours, for a free quote." data-en="Pricing depends on tree size and access. Call (813) 270-4794, open 24 hours, for a free quote.">Pricing depends on tree size and access. Call (813) 270-4794, open 24 hours, for a free quote.</span></p>')
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
          Call (813) 270-4794
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Corte de palma junto a la piscina" data-en="Palm trim next to the pool">Palm trim next to the pool</span><img src="assets/gallery-palm-patio.jpg" alt="A TNT Tree Service crew member trimming a palm next to a backyard pool in Lutz, FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Poda desde el techo" data-en="Pruning from the roofline">Pruning from the roofline</span><img src="assets/gallery-roof-poleaw.jpg" alt="A TNT Tree Service technician using a pole saw to clear limbs from a roofline" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Subida a la palma sin arnes extra" data-en="Free-climbing a tall palm">Free-climbing a tall palm</span><img src="assets/gallery-palm-house.jpg" alt="A TNT Tree Service climber trimming a tall palm tree beside a home" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Corte en medio del follaje" data-en="Cutting deep in the canopy">Cutting deep in the canopy</span><img src="assets/gallery-canopy-cut.jpg" alt="A TNT Tree Service climber cutting a branch deep inside a tree canopy" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Limpieza de ramas en el suelo" data-en="Clearing downed branches">Clearing downed branches</span><img src="assets/gallery-ground-cleanup.jpg" alt="A TNT Tree Service worker in a safety vest clearing downed branches" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 15. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Lutz" data-en="What Lutz">What Lutz</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="4.9 out of 5 · 11 reviews on Google" data-en="4.9 out of 5 · 11 reviews on Google">4.9 out of 5 · 11 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Company was extremely responsive and scheduled palm tree cut quickly. They were able to climb and cut the tree without leaving a big footprint. Not sure I could have asked for anything better. Experience was great! Thanks TNT!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">David Bracciano</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Quick service and very professional. Affordable price also, was really glad I found this company. Cleaned up my palms and cut one day and did it all same day service. I would use them again. UPDATE: used them again to cut down two oaks and handle permitting. Same professionalism and great service!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Wes Writer</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Had a great experience! Needed a couple trees trimmed and a couple removed. They were able to get someone out to give a quote the next day after I contacted them and provided a very fair price. After getting HOA approval I contacted them again to schedule, and they had a team out within a couple days and they did a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mohammad Hasan</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 11 reviews on Google" data-en="Read all 11 reviews on Google">Read all 11 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 16. UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Lutz, FL</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,102,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,102,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,102,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open 24 hours, every day of the week." data-en="Open 24 hours, every day of the week.">Open 24 hours, every day of the week.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,102,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (813) 270-4794" data-en="Call (813) 270-4794">Call (813) 270-4794</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,102,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.9 stars across 11 verified Google reviews." data-en="4.9 stars across 11 verified Google reviews.">4.9 stars across 11 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,102,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: TNT Tree Service LLC, 1915 S Mobile Villa Dr, Lutz FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 17. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Your trees, handled with care." data-en="Your trees, handled with care.">Your trees, handled with care.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call" data-en="One call">One call</span> <span class="text-shine" data-es="clears it all" data-en="clears it all">clears it all</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (813) 270-4794 for a free, honest quote on your palm trimming, tree removal or storm cleanup job. Open 24 hours, every day." data-en="Call (813) 270-4794 for a free, honest quote on your palm trimming, tree removal or storm cleanup job. Open 24 hours, every day.">Call (813) 270-4794 for a free, honest quote on your palm trimming, tree removal or storm cleanup job. Open 24 hours, every day.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (813) 270-4794" data-en="Call (813) 270-4794">Call (813) 270-4794</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ============================================================
# 18. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">TNT Tree Service</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,232,166,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/hero-palm-climb.jpg" alt="TNT Tree Service LLC" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,232,166,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">TNT Tree Service</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Tree service LLC sirviendo a Lutz y el area de Tampa Bay, FL." data-en="Tree service serving Lutz and the Tampa Bay area, FL.">Tree service serving Lutz and the Tampa Bay area, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#abe9b7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#9fe9ae]" data-es="Call (813) 270-4794" data-en="Call (813) 270-4794">Call (813) 270-4794</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#abe9b7]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#9fe9ae]">4.9 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 TNT Tree Service LLC.</p>')
print("FOOTER done")

# ============================================================
# 19. Boton flotante
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#081c0c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call TNT Tree Service">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#081c0c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
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
    "Lutz, FL · Tree Service": "Lutz, FL · Servicio de Arboles",
    "Your trees, handled with care.": "Tus arboles, tratados con cuidado.",
    "Palm trimming, removal": "Poda de palmas, remocion",
    "and cleanup, done ": "y limpieza, hecho ",
    "safely": "con seguridad",
    "Palm tree trimming, full tree removal, pruning and storm cleanup across Lutz and the greater Tampa Bay area. A responsive crew that climbs clean and leaves the yard spotless, with a 4.9 rating across 11 Google reviews.":
        "Poda de palmas, remocion completa de arboles, poda y limpieza tras tormentas en Lutz y el area de Tampa Bay. Un equipo que responde rapido, sube limpio y deja el jardin impecable, con calificacion de 4.9 en 11 resenas de Google.",
    "4.9 · 11 reviews on Google": "4.9 · 11 resenas en Google",
    "Call (813) 270-4794": "Llama al (813) 270-4794",
    "Open": "Abierto",
    "Every day of the week": "Todos los dias de la semana",
    "Trimming · Removal · Pruning": "Poda · Remocion · Corte",
    "Open every day": "Abierto todos los dias",
    "Tampa Bay, FL": "Tampa Bay, FL",
    "A crew that": "Un equipo que",
    "climbs clean": "sube limpio",
    "TNT Tree Service LLC is a Lutz-based tree crew covering palm tree trimming, full tree removal, pruning and storm cleanup across the greater Tampa Bay area. Climbers work clean with ropes and harnesses, leaving a small footprint behind.":
        "TNT Tree Service LLC es un equipo de arboles con base en Lutz que cubre poda de palmas, remocion completa de arboles, poda y limpieza tras tormentas en toda el area de Tampa Bay. Los trabajadores suben con cuerdas y arneses, dejando poco rastro en el jardin.",
    "Customers describe TNT as responsive, fair priced and quick to schedule, even for same-day jobs. The result: a 4.9-star rating across 11 Google reviews.":
        "Los clientes describen a TNT como un equipo que responde rapido, con precios justos y facil de agendar, incluso para trabajos el mismo dia. El resultado: una calificacion de 4.9 estrellas en 11 resenas de Google.",
    "Tree crew": "Equipo de arboles",
    "How it works": "Asi se trabaja",
    "Call it in": "Llama o escribe",
    "Call or text what needs trimming or removing, any time of day, and the crew talks through the job with you.":
        "Llama o escribe lo que necesitas podar o remover, a cualquier hora, y el equipo te explica el trabajo.",
    "Fair quote": "Cotizacion justa",
    "A crew member comes out fast, often the next day, and gives a fair, upfront price before any climbing starts.":
        "Un miembro del equipo llega rapido, muchas veces al dia siguiente, y da un precio justo y directo antes de empezar a subir.",
    "The climb": "La subida",
    "Climbers rope in and work the tree from the top down, cutting clean and keeping the footprint on the lawn small.":
        "Los trabajadores se amarran con cuerdas y trabajan el arbol de arriba hacia abajo, cortando limpio y dejando poco rastro en el pasto.",
    "The cleanup": "La limpieza",
    "Branches, logs and debris get hauled away same day, so the yard looks better than before the crew arrived.":
        "Las ramas, troncos y escombros se retiran el mismo dia, para que el jardin quede mejor que antes de que llegara el equipo.",
    "Tree work for": "Trabajo de arboles para",
    "every yard": "cada jardin",
    "No two trees are the same, so every job gets its own fair, upfront quote by phone before any climbing begins.":
        "Ningun arbol es igual a otro, asi que cada trabajo recibe su propia cotizacion justa por telefono antes de empezar a subir.",
    "Most requested": "Lo mas solicitado",
    "Palm Tree Trimming": "Poda de Palmas",
    "Climbed and trimmed by hand, the job most Lutz homeowners call TNT about before hurricane season.":
        "Subido y podado a mano, el trabajo que mas piden los duenos de casa en Lutz antes de la temporada de huracanes.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Full removal": "Remocion completa",
    "Tree Removal": "Remocion de Arboles",
    "Dead, leaning or oversized trees taken down in sections, climbed and lowered to protect the rest of the yard.":
        "Arboles muertos, inclinados o demasiado grandes se bajan por secciones, subidos y descendidos con cuidado para proteger el resto del jardin.",
    "Shape it up": "Dale forma",
    "Tree Trimming &amp; Pruning": "Poda y Corte de Arboles",
    "Oaks and other shade trees trimmed and pruned to clear roofs and power lines and keep the canopy healthy.":
        "Robles y otros arboles de sombra se podan y cortan para despejar techos y lineas electricas y mantener el follaje sano.",
    "Same day": "El mismo dia",
    "Storm &amp; Yard Cleanup": "Limpieza tras Tormentas y Jardin",
    "Fallen limbs, storm debris and cut wood hauled away the same day the job is finished.":
        "Las ramas caidas, escombros de tormenta y madera cortada se retiran el mismo dia que termina el trabajo.",
    "Palms": "Palmas",
    "Palm tree trimming": "Poda de palmas",
    "Frond &amp; seed pod removal": "Remocion de hojas y vainas",
    "Hurricane prep trims": "Poda previa a huracanes",
    "Dead palm removal": "Remocion de palmas muertas",
    "Removal &amp; Pruning": "Remocion y Poda",
    "Full tree removal": "Remocion completa de arboles",
    "Oak &amp; shade tree pruning": "Poda de robles y arboles de sombra",
    "Canopy thinning": "Aclareo de follaje",
    "HOA-approved trims": "Podas aprobadas por la HOA",
    "Cleanup": "Limpieza",
    "Storm debris cleanup": "Limpieza de escombros de tormenta",
    "Yard &amp; sidewalk cleanup": "Limpieza de jardin y aceras",
    "Log &amp; branch haul away": "Retiro de troncos y ramas",
    "Free estimates": "Cotizaciones gratis",
    "Pricing depends on tree size and access. Call (813) 270-4794, open 24 hours, for a free quote.":
        "El precio depende del tamano del arbol y el acceso. Llama al (813) 270-4794, abierto 24 horas, para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Lutz": "Lo que dicen los",
    "customers say": "clientes en Lutz",
    "Read all 11 reviews on Google": "Lee las 11 resenas en Google",
    "Serving": "Sirviendo a",
    "Hours": "Horario",
    "Open 24 hours, every day of the week.": "Abierto 24 horas, todos los dias de la semana.",
    "Reviews": "Resenas",
    "4.9 stars across 11 verified Google reviews.": "4.9 estrellas en 11 resenas verificadas de Google.",
    "One call": "Una llamada",
    "clears it all": "lo resuelve todo",
    "Call (813) 270-4794 for a free, honest quote on your palm trimming, tree removal or storm cleanup job. Open 24 hours, every day.":
        "Llama al (813) 270-4794 para una cotizacion gratis y honesta de tu poda de palmas, remocion de arboles o limpieza tras tormenta. Abierto 24 horas, todos los dias.",
    "Read Google Reviews": "Lee las resenas en Google",
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
