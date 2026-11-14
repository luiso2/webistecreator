import re
import colorsys
import shutil

SLUG = "rmp-moving-company"
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
# 2. PALETA: dorado (pureartistry) -> dorado mas brillante (RMP, lujo)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(212, 168, 75), (232, 207, 150), (185, 138, 128), (180, 140, 60), (122, 90, 30),
          (110, 85, 35), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]

TARGET_HUE = 45 / 360.0
SAT_MUL = 1.05


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

RING = "rgba(215,179,72"   # shifted (212,168,75)
HOVERHEX = "#ebdaa9"        # shifted #e9c3ab

# ============================================================
# 3. Globales: sin booking/IG/email -> tel: + Google reviews
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+17865060603"
c = h.count(OLD_BOOK)
assert c >= 5, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=RMP+Moving+Company+Miami+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "1360 SW 3rd St #4, Miami, FL 33135"
NEW_MAPS = "https://www.google.com/maps?q=1360+SW+3rd+St+%234,+Miami,+FL+33135"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>RMP Moving Company · Movers in Miami, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="RMP Moving Company, Miami FL: residential and commercial moving, delivery and dumping services across Miami-Dade. 4.9 stars across 296 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="RMP Moving Company · Movers in Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Residential and commercial moving, delivery and dumping services. 4.9 on Google with 296 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-mansion.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MovingCompany",
    "name": "RMP Moving Company",
    "description": "Residential and commercial moving, delivery and dumping services across Miami-Dade, FL.",
    "address": { "@type": "PostalAddress", "streetAddress": "1360 SW 3rd St #4", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33135", "addressCountry": "US" },
    "telephone": "+1-786-506-0603",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "296", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "07:00", "closes": "23:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Moving services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Residential Moving" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Commercial &amp; Delivery" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Junk &amp; Dumping Services" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Packing &amp; Furniture Wrapping" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN (resenas en ingles)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ============================================================
# 6. PRELOADER + NAV
# ============================================================
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">RMP</span>\n    <span class="pre-word">RMP Moving</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.35)]" />',
    '<img src="assets/logo.jpg" alt="RMP Moving Company" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">RMP <span class="text-[color:var(--accent-deep)]">Moving</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miami, FL · Moving Company" data-en="Miami, FL · Moving Company">Miami, FL · Moving Company</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Moving, delivery &amp; more." data-en="Moving, delivery &amp; more.">Moving, delivery &amp; more.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Moving, delivery" data-en="Moving, delivery">Moving, delivery</span><br /><span data-es="and dumping, done " data-en="and dumping, done ">and dumping, done </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Residential and commercial moving, delivery and dumping services across Miami-Dade, from historic estates to everyday households. Led by Rolando&#39;s crew, with a 4.9 rating across 296 Google reviews." data-en="Residential and commercial moving, delivery and dumping services across Miami-Dade, from historic estates to everyday households. Led by Rolando&#39;s crew, with a 4.9 rating across 296 Google reviews.">Residential and commercial moving, delivery and dumping services across Miami-Dade, from historic estates to everyday households. Led by Rolando&#39;s crew, with a 4.9 rating across 296 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.9 · 296 reviews on Google" data-en="4.9 · 296 reviews on Google">4.9 · 296 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 506-0603" data-en="Call (786) 506-0603">Call (786) 506-0603</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Trabajo real" data-en="Real work">Real work</span>\n          <span data-es="Precios claros" data-en="Clear pricing">Clear pricing</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Direct contact</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-mansion.jpg" alt="The RMP Moving Company truck arriving at a historic Miami home for a move" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">7am - 11pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="296">296</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Moving <span class="text-shine">&amp;</span> Delivery</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Dumping · Packing" data-en="Dumping · Packing">Dumping · Packing</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">7am <span class="text-shine">-</span> 11pm</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Every day" data-en="Every day">Every day</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Miami-Dade, FL" data-en="Miami-Dade, FL">Miami-Dade, FL</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Residential Moves"),
    ("Loc Retwist", "Commercial Moves"),
    ("Knotless Braids", "Furniture Delivery"),
    ("K-Tip Extensions", "Junk Removal"),
    ("Keratin", "Dumping Services"),
    ("Orlando, FL", "Miami, FL"),
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
          <img src="assets/about-crew-team.jpg" alt="The RMP Moving Company crew inside their truck after a move in Miami, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Led by Rolando," data-en="Led by Rolando,">Led by Rolando,</span><br /><span class="text-shine" data-es="a crew that shows up" data-en="a crew that shows up">a crew that shows up</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="RMP Moving Company handles residential and commercial moves, deliveries and dumping services across Miami-Dade. Customers single out Rolando and his crew for showing up on time and treating every home, from a historic estate to an everyday apartment, with the same care." data-en="RMP Moving Company handles residential and commercial moves, deliveries and dumping services across Miami-Dade. Customers single out Rolando and his crew for showing up on time and treating every home, from a historic estate to an everyday apartment, with the same care.">RMP Moving Company handles residential and commercial moves, deliveries and dumping services across Miami-Dade. Customers single out Rolando and his crew for showing up on time and treating every home, from a historic estate to an everyday apartment, with the same care.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="The result: a 4.9 rating across 296 Google reviews, built move after move." data-en="The result: a 4.9 rating across 296 Google reviews, built move after move.">The result: a 4.9 rating across 296 Google reviews, built move after move.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="296">296</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Every day" data-en="Every day">Every day</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="7 AM to 11 PM" data-en="7 AM to 11 PM">7 AM to 11 PM</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo.jpg" alt="RMP Moving Company" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">RMP Moving Company · <span class="text-[color:var(--ink-40)]" data-es="Rolando&#39;s crew" data-en="Rolando&#39;s crew">Rolando&#39;s crew</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call to book" data-en="Call to book">Call to book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (786) 506-0603 with your move date and details, and get a straightforward price over the phone." data-en="Call (786) 506-0603 with your move date and details, and get a straightforward price over the phone.">Call (786) 506-0603 with your move date and details, and get a straightforward price over the phone.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Upfront price" data-en="Upfront price">Upfront price</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a clear, honest price for the job before anything is loaded, no surprises later." data-en="You get a clear, honest price for the job before anything is loaded, no surprises later.">You get a clear, honest price for the job before anything is loaded, no surprises later.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Moving day" data-en="Moving day">Moving day</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew wraps furniture, loads carefully and delivers safely, whether it is a single sofa or a full household." data-en="The crew wraps furniture, loads carefully and delivers safely, whether it is a single sofa or a full household.">The crew wraps furniture, loads carefully and delivers safely, whether it is a single sofa or a full household.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walkthrough" data-en="Walkthrough">Walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Before the crew leaves, you walk through the finished job together, so you know it was done right." data-en="Before the crew leaves, you walk through the finished job together, so you know it was done right.">Before the crew leaves, you walk through the finished job together, so you know it was done right.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine" data-es="every move" data-en="every move">every move</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two jobs are the same, so every move gets its own honest quote by phone, before anything is booked." data-en="No two jobs are the same, so every move gets its own honest quote by phone, before anything is booked.">No two jobs are the same, so every move gets its own honest quote by phone, before anything is booked.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: ''' + RING + ''',0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Residential Moving" data-en="Residential Moving">Residential Moving</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service home moves across Miami-Dade, from single rooms to full estates, loaded and delivered with care." data-en="Full-service home moves across Miami-Dade, from single rooms to full estates, loaded and delivered with care.">Full-service home moves across Miami-Dade, from single rooms to full estates, loaded and delivered with care.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="For businesses" data-en="For businesses">For businesses</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Commercial &amp; Delivery" data-en="Commercial &amp; Delivery">Commercial &amp; Delivery</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Business moves and furniture delivery for offices, stores and online orders across the Miami area." data-en="Business moves and furniture delivery for offices, stores and online orders across the Miami area.">Business moves and furniture delivery for offices, stores and online orders across the Miami area.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clear it out" data-en="Clear it out">Clear it out</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Junk &amp; Dumping Services" data-en="Junk &amp; Dumping Services">Junk &amp; Dumping Services</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Junk removal and dumping services to clear out a home, garage or job site, hauled away the same day." data-en="Junk removal and dumping services to clear out a home, garage or job site, hauled away the same day.">Junk removal and dumping services to clear out a home, garage or job site, hauled away the same day.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it safe" data-en="Keep it safe">Keep it safe</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Packing &amp; Furniture Wrapping" data-en="Packing &amp; Furniture Wrapping">Packing &amp; Furniture Wrapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Furniture wrapped and padded for the trip, so couches, mattresses and antiques travel damage-free." data-en="Furniture wrapped and padded for the trip, so couches, mattresses and antiques travel damage-free.">Furniture wrapped and padded for the trip, so couches, mattresses and antiques travel damage-free.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Moving" data-en="Moving">Moving</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Residential moves" data-en="Residential moves">Residential moves</li>
            <li class="flex items-center gap-2" data-es="Commercial moves" data-en="Commercial moves">Commercial moves</li>
            <li class="flex items-center gap-2" data-es="Apartment &amp; condo moves" data-en="Apartment &amp; condo moves">Apartment &amp; condo moves</li>
            <li class="flex items-center gap-2" data-es="Estate moves" data-en="Estate moves">Estate moves</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Delivery &amp; Dumping" data-en="Delivery &amp; Dumping">Delivery &amp; Dumping</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Furniture delivery" data-en="Furniture delivery">Furniture delivery</li>
            <li class="flex items-center gap-2" data-es="Junk removal" data-en="Junk removal">Junk removal</li>
            <li class="flex items-center gap-2" data-es="Dumping services" data-en="Dumping services">Dumping services</li>
            <li class="flex items-center gap-2" data-es="Same-day service" data-en="Same-day service">Same-day service</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Packing" data-en="Packing">Packing</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Furniture wrapping" data-en="Furniture wrapping">Furniture wrapping</li>
            <li class="flex items-center gap-2" data-es="Packing &amp; unpacking" data-en="Packing &amp; unpacking">Packing &amp; unpacking</li>
            <li class="flex items-center gap-2" data-es="Moving supplies" data-en="Moving supplies">Moving supplies</li>
            <li class="flex items-center gap-2" data-es="Fragile item care" data-en="Fragile item care">Fragile item care</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and distance. Call (786) 506-0603 for a free quote." data-en="Pricing depends on scope and distance. Call (786) 506-0603 for a free quote.">Pricing depends on scope and distance. Call (786) 506-0603 for a free quote.</span></p>')
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
          Call (786) 506-0603
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Mudanza nocturna, bien hecha" data-en="Evening move-in, done right">Evening move-in, done right</span><img src="assets/gallery-night-unload.jpg" alt="RMP Moving Company unloading furniture at a Miami home in the evening" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Listos para cargar" data-en="Ready to load">Ready to load</span><img src="assets/gallery-truck-cones.jpg" alt="The RMP Moving Company truck staged and ready to load in Miami, FL" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Entrega cuidadosa, en cada paso" data-en="Careful delivery, every step">Careful delivery, every step</span><img src="assets/gallery-ramp-entry.jpg" alt="The RMP Moving Company crew carrying furniture into a Miami home" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Envuelto y protegido" data-en="Wrapped and protected">Wrapped and protected</span><img src="assets/gallery-sofa-wrap.jpg" alt="A leather sofa wrapped and taped for a move by RMP Moving Company" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="El equipo de RMP en accion" data-en="The RMP crew at work">The RMP crew at work</span><img src="assets/gallery-shirt-branding.jpg" alt="An RMP Moving Company crew member at work, branded shirt visible" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 15. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Miami" data-en="What Miami">What Miami</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="4.9 out of 5 · 296 reviews on Google" data-en="4.9 out of 5 · 296 reviews on Google">4.9 out of 5 · 296 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"RMP moving provided excellent, professional, on-time moving services for us. We will definitely recommend them to our family, friends and associates. We've had bad experiences with other moving companies in the past..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ricky Trinidad</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Rolando, Fernando and Juan!!! I cannot be more satisfied with this trio! I just moved to Miami from Los Angeles. I had ALL my stuff at my parents house in Boca, and more furniture at our other property in Pompano. They arrived at 9:30am..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Randi Silver</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Rolando + Johnny were amazing. AND it dumped buckets of rain from the get go, big tropical rain drops too, the entire time. Sending lots of love to these guys."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tracy Niedermeyer</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 296 reviews on Google" data-en="Read all 296 reviews on Google">Read all 296 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 16. UBICACION (direccion real disponible, impresa en el camion)
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Miami, FL</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[' + RING + ',0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[' + RING + ',0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open every day, 7:00 AM to 11:00 PM." data-en="Open every day, 7:00 AM to 11:00 PM.">Open every day, 7:00 AM to 11:00 PM.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 506-0603" data-en="Call (786) 506-0603">Call (786) 506-0603</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.9 stars across 296 verified Google reviews." data-en="4.9 stars across 296 verified Google reviews.">4.9 stars across 296 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: RMP Moving Company, 1360 SW 3rd St, Miami FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 17. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Moving, delivery &amp; more." data-en="Moving, delivery &amp; more.">Moving, delivery &amp; more.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call fixes" data-en="One call fixes">One call fixes</span> <span class="text-shine" data-es="it all" data-en="it all">it all</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (786) 506-0603 for a free, honest quote on your move, delivery or dumping job. Open every day, 7 AM to 11 PM." data-en="Call (786) 506-0603 for a free, honest quote on your move, delivery or dumping job. Open every day, 7 AM to 11 PM.">Call (786) 506-0603 for a free, honest quote on your move, delivery or dumping job. Open every day, 7 AM to 11 PM.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 506-0603" data-en="Call (786) 506-0603">Call (786) 506-0603</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ============================================================
# 18. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">RMP Moving</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(234,213,148,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="RMP Moving Company" class="w-9 h-9 rounded-full object-cover ring-1 ring-[''' + RING + ''',0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">RMP Moving Company</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Mudanzas, entregas y servicios de desecho en Miami, FL." data-en="Moving, delivery and dumping services serving Miami, FL.">Moving, delivery and dumping services serving Miami, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[''' + HOVERHEX + ''']" data-es="Call (786) 506-0603" data-en="Call (786) 506-0603">Call (786) 506-0603</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']">4.9 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 RMP Moving Company.</p>')
print("FOOTER done")

# ============================================================
# 19. Boton flotante
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#07121c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call RMP Moving Company">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#07121c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
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
    "Miami, FL · Moving Company": "Miami, FL · Empresa de Mudanzas",
    "Moving, delivery &amp; more.": "Mudanzas, entregas y mas.",
    "Moving, delivery": "Mudanzas, entregas",
    "and dumping, done ": "y desechos, hecho ",
    "right": "bien",
    "Residential and commercial moving, delivery and dumping services across Miami-Dade, from historic estates to everyday households. Led by Rolando&#39;s crew, with a 4.9 rating across 296 Google reviews.":
        "Mudanzas residenciales y comerciales, entregas y servicios de desecho en todo Miami-Dade, desde propiedades historicas hasta hogares comunes. Liderado por el equipo de Rolando, con una calificacion de 4.9 en 296 resenas de Google.",
    "4.9 · 296 reviews on Google": "4.9 · 296 resenas en Google",
    "Call (786) 506-0603": "Llama al (786) 506-0603",
    "Open": "Abierto",
    "Every day of the week": "Todos los dias de la semana",
    "Dumping · Packing": "Desechos · Empaque",
    "Every day": "Todos los dias",
    "Miami-Dade, FL": "Miami-Dade, FL",
    "Led by Rolando,": "Liderado por Rolando,",
    "a crew that shows up": "un equipo que siempre llega",
    "RMP Moving Company handles residential and commercial moves, deliveries and dumping services across Miami-Dade. Customers single out Rolando and his crew for showing up on time and treating every home, from a historic estate to an everyday apartment, with the same care.":
        "RMP Moving Company maneja mudanzas residenciales y comerciales, entregas y servicios de desecho en todo Miami-Dade. Los clientes destacan a Rolando y su equipo por llegar a tiempo y tratar cada hogar, desde una propiedad historica hasta un apartamento comun, con el mismo cuidado.",
    "The result: a 4.9 rating across 296 Google reviews, built move after move.":
        "El resultado: una calificacion de 4.9 en 296 resenas de Google, construida mudanza tras mudanza.",
    "7 AM to 11 PM": "7 AM a 11 PM",
    "Rolando&#39;s crew": "El equipo de Rolando",
    "How it works": "Asi se trabaja",
    "Call to book": "Llama para reservar",
    "Call (786) 506-0603 with your move date and details, and get a straightforward price over the phone.":
        "Llama al (786) 506-0603 con la fecha de tu mudanza y los detalles, y recibe un precio claro por telefono.",
    "Upfront price": "Precio claro",
    "You get a clear, honest price for the job before anything is loaded, no surprises later.":
        "Recibes un precio claro y honesto por el trabajo antes de cargar nada, sin sorpresas despues.",
    "Moving day": "Dia de mudanza",
    "The crew wraps furniture, loads carefully and delivers safely, whether it is a single sofa or a full household.":
        "El equipo envuelve los muebles, carga con cuidado y entrega de forma segura, ya sea un solo sofa o un hogar completo.",
    "Walkthrough": "Revision final",
    "Before the crew leaves, you walk through the finished job together, so you know it was done right.":
        "Antes de que el equipo se vaya, revisan juntos el trabajo terminado, para que sepas que quedo bien hecho.",
    "every move": "cada mudanza",
    "No two jobs are the same, so every move gets its own honest quote by phone, before anything is booked.":
        "Ningun trabajo es igual a otro, asi que cada mudanza recibe su propia cotizacion honesta por telefono, antes de reservar.",
    "Most requested": "Lo mas solicitado",
    "Residential Moving": "Mudanzas Residenciales",
    "Full-service home moves across Miami-Dade, from single rooms to full estates, loaded and delivered with care.":
        "Mudanzas residenciales completas en todo Miami-Dade, desde una sola habitacion hasta propiedades completas, cargadas y entregadas con cuidado.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "For businesses": "Para negocios",
    "Commercial &amp; Delivery": "Comercial y Entregas",
    "Business moves and furniture delivery for offices, stores and online orders across the Miami area.":
        "Mudanzas de negocios y entrega de muebles para oficinas, tiendas y pedidos en linea en toda el area de Miami.",
    "Clear it out": "Despeja el espacio",
    "Junk &amp; Dumping Services": "Servicios de Basura y Desecho",
    "Junk removal and dumping services to clear out a home, garage or job site, hauled away the same day.":
        "Servicios de remocion de basura y desecho para despejar un hogar, garaje o sitio de trabajo, retirado el mismo dia.",
    "Keep it safe": "Mantenlo seguro",
    "Packing &amp; Furniture Wrapping": "Empaque y Envoltura de Muebles",
    "Furniture wrapped and padded for the trip, so couches, mattresses and antiques travel damage-free.":
        "Muebles envueltos y acolchados para el viaje, para que sofas, colchones y antiguedades viajen sin danos.",
    "Moving": "Mudanzas",
    "Residential moves": "Mudanzas residenciales",
    "Commercial moves": "Mudanzas comerciales",
    "Apartment &amp; condo moves": "Mudanzas de apartamentos y condominios",
    "Estate moves": "Mudanzas de propiedades grandes",
    "Delivery &amp; Dumping": "Entregas y Desechos",
    "Furniture delivery": "Entrega de muebles",
    "Junk removal": "Remocion de basura",
    "Dumping services": "Servicios de desecho",
    "Same-day service": "Servicio el mismo dia",
    "Packing": "Empaque",
    "Furniture wrapping": "Envoltura de muebles",
    "Packing &amp; unpacking": "Empaque y desempaque",
    "Moving supplies": "Suministros de mudanza",
    "Fragile item care": "Cuidado de articulos fragiles",
    "Pricing depends on scope and distance. Call (786) 506-0603 for a free quote.":
        "El precio depende del alcance y la distancia. Llama al (786) 506-0603 para una cotizacion gratis.",
    "work": "real",
    "What Miami": "Lo que dicen los",
    "customers say": "clientes de Miami",
    "Read all 296 reviews on Google": "Lee las 296 resenas en Google",
    "Serving": "Sirviendo a",
    "Hours": "Horario",
    "Open every day, 7:00 AM to 11:00 PM.": "Abierto todos los dias, de 7:00 AM a 11:00 PM.",
    "Reviews": "Resenas",
    "4.9 stars across 296 verified Google reviews.": "4.9 estrellas en 296 resenas verificadas de Google.",
    "One call fixes": "Una llamada arregla",
    "it all": "todo",
    "Call (786) 506-0603 for a free, honest quote on your move, delivery or dumping job. Open every day, 7 AM to 11 PM.":
        "Llama al (786) 506-0603 para una cotizacion gratis y honesta de tu mudanza, entrega o trabajo de desecho. Abierto todos los dias, de 7 AM a 11 PM.",
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
