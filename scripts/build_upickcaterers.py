import re
import os
import colorsys
import shutil

SLUG = "upick-caterers"
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
# 2. PALETA: dorado (pureartistry) -> violeta nocturno (Upick Caterers,
#    sus mesas de picoteo bajo luces moradas de evento)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(212, 168, 75), (232, 207, 150), (185, 138, 128), (180, 140, 60), (122, 90, 30),
          (110, 85, 35), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]

TARGET_HUE = 280 / 360.0
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

RING1 = "rgba(167,72,215"   # era rgba(212,168,75
RING2 = "rgba(205,148,234"  # era rgba(232,207,150
HEX_HOVER = "#d5a9eb"        # era #e9c3ab
BOOKFLOAT_STROKE = "#16071c"  # era #1c1408

# ============================================================
# 3. Globales: no hay booking platform ni IG -> tel: + Google reviews
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+17863327065"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Upick+Caterers+Miami+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "14271 SW 120th St Ste 108, Miami, FL 33186"
NEW_MAPS = "https://www.google.com/maps?q=14271+SW+120th+St+Ste+108,+Miami,+FL+33186"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Upick Caterers · Event Catering in West Kendall, Miami, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Upick Caterers, West Kendall, Miami FL: grazing and charcuterie tables, hors d\'oeuvres and full-service catering for weddings, sweet 16s and birthdays. 5.0 stars across 47 Google reviews." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Upick Caterers · Event Catering in West Kendall, Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Grazing tables, hors d\'oeuvres and full-service event catering. 5.0 on Google with 47 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-upick-sign.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CateringService",
    "name": "Upick Caterers",
    "description": "Event catering company in West Kendall, Miami, FL: grazing and charcuterie tables, hors d'oeuvres, dessert tables and full-service catering for weddings, sweet 16s and birthdays.",
    "address": { "@type": "PostalAddress", "streetAddress": "14271 SW 120th St Ste 108", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33186", "addressCountry": "US" },
    "telephone": "+1-786-332-7065",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "47", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Catering services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Grazing &amp; Charcuterie Tables" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Hors d'oeuvres &amp; Appetizer Cones" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Dessert Tables" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Weddings &amp; Milestone Parties" } }
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
    '<span class="pre-mono">UP</span>\n    <span class="pre-word">Upick Caterers</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.35)]" />',
    '<img src="assets/logo.jpg" alt="Upick Caterers" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">U <span class="text-[color:var(--accent-deep)]">Pick</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Get a quote" data-en="Get a quote">Get a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Get a quote" data-en="Get a quote">Get a quote</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="West Kendall, Miami, FL · Event Catering" data-en="West Kendall, Miami, FL · Event Catering">West Kendall, Miami, FL · Event Catering</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="You pick the vision, we build the table." data-en="You pick the vision, we build the table.">You pick the vision, we build the table.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Grazing tables, hors" data-en="Grazing tables, hors">Grazing tables, hors</span><br /><span data-es="d&#39;oeuvres and desserts, " data-en="d&#39;oeuvres and desserts, ">d&#39;oeuvres and desserts, </span><span class="text-shine" data-es="your way" data-en="your way">your way</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Full grazing and charcuterie tables, hors d&#39;oeuvres, dessert displays and full-service catering for weddings, sweet 16s and birthdays across West Kendall and Miami. A perfect 5.0 rating across 47 Google reviews." data-en="Full grazing and charcuterie tables, hors d&#39;oeuvres, dessert displays and full-service catering for weddings, sweet 16s and birthdays across West Kendall and Miami. A perfect 5.0 rating across 47 Google reviews.">Full grazing and charcuterie tables, hors d&#39;oeuvres, dessert displays and full-service catering for weddings, sweet 16s and birthdays across West Kendall and Miami. A perfect 5.0 rating across 47 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 47 reviews on Google" data-en="5.0 · 47 reviews on Google">5.0 · 47 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 332-7065" data-en="Call (786) 332-7065">Call (786) 332-7065</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-upick-sign.jpg" alt="An Upick Caterers grazing table with the U-PICK Catering sign at a Miami event" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Signature" data-en="Signature">Signature</p>
            <p class="font-display text-lg">Grazing Tables</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Styled for your event" data-en="Styled for your event">Styled for your event</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="47">47</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Grazing <span class="text-shine">&amp;</span> Tables</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Charcuterie · Desserts" data-en="Charcuterie · Desserts">Charcuterie · Desserts</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">Full <span class="text-shine">&amp;</span> Service</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Chefs, bartenders, waiters" data-en="Chefs, bartenders, waiters">Chefs, bartenders, waiters</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">West Kendall</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="120th St, Miami, FL" data-en="120th St, Miami, FL">120th St, Miami, FL</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Grazing Tables"),
    ("Loc Retwist", "Charcuterie Boards"),
    ("Knotless Braids", "Hors d&#39;oeuvres"),
    ("K-Tip Extensions", "Dessert Tables"),
    ("Keratin", "Sweet 16 Parties"),
    ("Orlando, FL", "West Kendall, Miami, FL"),
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
          <img src="assets/about-outdoor-grazing.jpg" alt="An Upick Caterers grazing table set up outdoors for a Miami event" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="A team of chefs," data-en="A team of chefs,">A team of chefs,</span><br /><span class="text-shine" data-es="bartenders and waiters" data-en="bartenders and waiters">bartenders and waiters</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Upick Caterers, based in West Kendall, builds grazing and charcuterie tables, hors d&#39;oeuvres and dessert displays for weddings, sweet 16s and birthdays across Miami, with a full team of chefs, bartenders and waiters on site." data-en="Upick Caterers, based in West Kendall, builds grazing and charcuterie tables, hors d&#39;oeuvres and dessert displays for weddings, sweet 16s and birthdays across Miami, with a full team of chefs, bartenders and waiters on site.">Upick Caterers, based in West Kendall, builds grazing and charcuterie tables, hors d&#39;oeuvres and dessert displays for weddings, sweet 16s and birthdays across Miami, with a full team of chefs, bartenders and waiters on site.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Hosts confirm it: a perfect 5.0 rating across 47 Google reviews, with clients praising how fresh everything looks and how beautifully the tables are styled." data-en="Hosts confirm it: a perfect 5.0 rating across 47 Google reviews, with clients praising how fresh everything looks and how beautifully the tables are styled.">Hosts confirm it: a perfect 5.0 rating across 47 Google reviews, with clients praising how fresh everything looks and how beautifully the tables are styled.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="47">47</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Full</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Equipo de servicio" data-en="Service team">Service team</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo.jpg" alt="Upick Caterers" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Upick Caterers · <span class="text-[color:var(--ink-40)]" data-es="Catering Special Event" data-en="Catering Special Event">Catering Special Event</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Share your vision" data-en="Share your vision">Share your vision</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call with your date, guest count and theme, grazing table, hors d&#39;oeuvres or a full wedding spread." data-en="Call with your date, guest count and theme, grazing table, hors d&#39;oeuvres or a full wedding spread.">Call with your date, guest count and theme, grazing table, hors d&#39;oeuvres or a full wedding spread.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="A menu you can see" data-en="A menu you can see">A menu you can see</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A clear quote and menu built around your guest count, from grazing boards to a full plated dinner." data-en="A clear quote and menu built around your guest count, from grazing boards to a full plated dinner.">A clear quote and menu built around your guest count, from grazing boards to a full plated dinner.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Styled on site" data-en="Styled on site">Styled on site</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The team arrives early to style the grazing table and set up the full spread before your guests arrive." data-en="The team arrives early to style the grazing table and set up the full spread before your guests arrive.">The team arrives early to style the grazing table and set up the full spread before your guests arrive.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Served &amp; cleared" data-en="Served &amp; cleared">Served &amp; cleared</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Chefs, bartenders and waiters serve your guests, then clear the setup when the party winds down." data-en="Chefs, bartenders and waiters serve your guests, then clear the setup when the party winds down.">Chefs, bartenders and waiters serve your guests, then clear the setup when the party winds down.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Catering for" data-en="Catering for">Catering for</span> <span class="text-shine" data-es="your special event" data-en="your special event">your special event</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every event gets its own quote built around your menu and guest count. Call to start planning." data-en="Every event gets its own quote built around your menu and guest count. Call to start planning.">Every event gets its own quote built around your menu and guest count. Call to start planning.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: ''' + RING1 + ''',0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Signature" data-en="Signature">Signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Grazing &amp; Charcuterie Tables" data-en="Grazing &amp; Charcuterie Tables">Grazing &amp; Charcuterie Tables</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full grazing tables with cured meats, cheeses, fruit and crackers, styled for the room." data-en="Full grazing tables with cured meats, cheeses, fruit and crackers, styled for the room.">Full grazing tables with cured meats, cheeses, fruit and crackers, styled for the room.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cocktail hour" data-en="Cocktail hour">Cocktail hour</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Hors d&#39;oeuvres &amp; Appetizer Cones" data-en="Hors d&#39;oeuvres &amp; Appetizer Cones">Hors d&#39;oeuvres &amp; Appetizer Cones</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Passed appetizers and individual cones with mozzarella, tomato and fresh herbs for cocktail hour." data-en="Passed appetizers and individual cones with mozzarella, tomato and fresh herbs for cocktail hour.">Passed appetizers and individual cones with mozzarella, tomato and fresh herbs for cocktail hour.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sweet finish" data-en="Sweet finish">Sweet finish</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Dessert Tables" data-en="Dessert Tables">Dessert Tables</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Donuts, mini desserts and sweets styled under party lighting for sweet 16s and birthdays." data-en="Donuts, mini desserts and sweets styled under party lighting for sweet 16s and birthdays.">Donuts, mini desserts and sweets styled under party lighting for sweet 16s and birthdays.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Full service" data-en="Full service">Full service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Weddings &amp; Milestone Parties" data-en="Weddings &amp; Milestone Parties">Weddings &amp; Milestone Parties</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service catering with chefs, bartenders and waiters for weddings, sweet 16s and birthdays." data-en="Full-service catering with chefs, bartenders and waiters for weddings, sweet 16s and birthdays.">Full-service catering with chefs, bartenders and waiters for weddings, sweet 16s and birthdays.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Boards" data-en="Boards">Boards</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Charcuterie &amp; cheese" data-en="Charcuterie &amp; cheese">Charcuterie &amp; cheese</li>
            <li class="flex items-center gap-2" data-es="Fresh fruit displays" data-en="Fresh fruit displays">Fresh fruit displays</li>
            <li class="flex items-center gap-2" data-es="Dips &amp; crackers" data-en="Dips &amp; crackers">Dips &amp; crackers</li>
            <li class="flex items-center gap-2" data-es="Kibbeh &amp; Mediterranean platters" data-en="Kibbeh &amp; Mediterranean platters">Kibbeh &amp; Mediterranean platters</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Cocktail hour" data-en="Cocktail hour">Cocktail hour</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Caprese skewers" data-en="Caprese skewers">Caprese skewers</li>
            <li class="flex items-center gap-2" data-es="Appetizer cones" data-en="Appetizer cones">Appetizer cones</li>
            <li class="flex items-center gap-2" data-es="Passed hors d&#39;oeuvres" data-en="Passed hors d&#39;oeuvres">Passed hors d&#39;oeuvres</li>
            <li class="flex items-center gap-2" data-es="Bartending" data-en="Bartending">Bartending</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Sweets" data-en="Sweets">Sweets</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Donut towers" data-en="Donut towers">Donut towers</li>
            <li class="flex items-center gap-2" data-es="Mini dessert cups" data-en="Mini dessert cups">Mini dessert cups</li>
            <li class="flex items-center gap-2" data-es="Chocolate-covered treats" data-en="Chocolate-covered treats">Chocolate-covered treats</li>
            <li class="flex items-center gap-2" data-es="Themed styling" data-en="Themed styling">Themed styling</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on menu and guest count. Call (786) 332-7065 for a free quote." data-en="Pricing depends on menu and guest count. Call (786) 332-7065 for a free quote.">Pricing depends on menu and guest count. Call (786) 332-7065 for a free quote.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="tables" data-en="tables">tables</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (786) 332-7065
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Mesa de picoteo bajo luces de evento" data-en="Grazing table under party lighting">Grazing table under party lighting</span><img src="assets/gallery-tropical-wide.jpg" alt="An Upick Caterers grazing table styled under green party lighting with the U-PICK sign" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Platon de kibbeh y mediterraneo" data-en="Kibbeh &amp; Mediterranean platter">Kibbeh &amp; Mediterranean platter</span><img src="assets/gallery-kibbeh-platter.jpg" alt="A Mediterranean platter with kibbeh, hummus and dips by Upick Caterers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Tabla de salami y quesos con el logo U-PICK" data-en="Salami &amp; cheese platter, U-PICK branded">Salami &amp; cheese platter, U-PICK branded</span><img src="assets/gallery-salami-cheese.jpg" alt="A salami and cheese platter with fruit next to the U-PICK Catering sign" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Mesa de postres rosada" data-en="Pink dessert table">Pink dessert table</span><img src="assets/gallery-dessert-table.jpg" alt="A pink-lit dessert table with donuts and mini desserts by Upick Caterers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Conos de aperitivo individuales" data-en="Individual appetizer cones">Individual appetizer cones</span><img src="assets/gallery-fruit-cones.jpg" alt="Individual appetizer cones with mozzarella and tomato skewers by Upick Caterers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 15. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Miami" data-en="What Miami">What Miami</span> <span class="text-shine" data-es="hosts say" data-en="hosts say">hosts say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 out of 5 · 47 reviews on Google" data-en="5.0 out of 5 · 47 reviews on Google">5.0 out of 5 · 47 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Thank you Upick Caterers for putting together the food for my 40th birthday party. The food was great."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Pablo Flores</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I would recommend these caterers to anyone looking for top notch catering service! They did catering for my daughters sweet 16 celebration which included appetizers and their signature martini mash. It was exquisite!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Traycier Medina</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Most delicious food ever! We had their hors d'oeuvres and cheese table at our wedding and everyone loved everything! Amazing team of chefs, bartenders, waiters!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rocio Conde Fuentes</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 47 reviews on Google" data-en="Read all 47 reviews on Google">Read all 47 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 16. UBICACION (direccion real disponible)
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">West Kendall</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[' + RING1 + ',0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[' + RING1 + ',0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Get directions</a>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Bookings" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Call with your date and guest count for a free quote." data-en="Call with your date and guest count for a free quote.">Call with your date and guest count for a free quote.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 332-7065" data-en="Call (786) 332-7065">Call (786) 332-7065</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="5.0 stars across 47 verified Google reviews." data-en="5.0 stars across 47 verified Google reviews.">5.0 stars across 47 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Upick Caterers, 14271 SW 120th St, Miami FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 17. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="You pick the vision, we build the table." data-en="You pick the vision, we build the table.">You pick the vision, we build the table.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your table," data-en="Your table,">Your table,</span> <span class="text-shine" data-es="styled your way" data-en="styled your way">styled your way</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (786) 332-7065 for a free quote on your grazing table, hors d&#39;oeuvres, dessert table or full-service event. Serving West Kendall and Miami." data-en="Call (786) 332-7065 for a free quote on your grazing table, hors d&#39;oeuvres, dessert table or full-service event. Serving West Kendall and Miami.">Call (786) 332-7065 for a free quote on your grazing table, hors d&#39;oeuvres, dessert table or full-service event. Serving West Kendall and Miami.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 332-7065" data-en="Call (786) 332-7065">Call (786) 332-7065</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ============================================================
# 18. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Upick</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[''' + RING2 + ''',0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Upick Caterers" class="w-9 h-9 rounded-full object-cover ring-1 ring-[''' + RING2 + ''',0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Upick Caterers</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Event catering serving West Kendall and Miami, FL." data-en="Event catering serving West Kendall and Miami, FL.">Event catering serving West Kendall and Miami, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[''' + HEX_HOVER + ''']" data-es="Call (786) 332-7065" data-en="Call (786) 332-7065">Call (786) 332-7065</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']">5.0 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Upick Caterers.</p>')
print("FOOTER done")

# ============================================================
# 19. Boton flotante
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>'.replace('#1c1408', BOOKFLOAT_STROKE),
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Upick Caterers">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="' + BOOKFLOAT_STROKE + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
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
    "West Kendall, Miami, FL · Event Catering": "West Kendall, Miami, FL · Catering de Eventos",
    "You pick the vision, we build the table.": "Tu eliges la idea, nosotros armamos la mesa.",
    "Grazing tables, hors": "Mesas de picoteo, pasapalos",
    "d&#39;oeuvres and desserts, ": "y postres, hecho ",
    "your way": "a tu manera",
    "Full grazing and charcuterie tables, hors d&#39;oeuvres, dessert displays and full-service catering for weddings, sweet 16s and birthdays across West Kendall and Miami. A perfect 5.0 rating across 47 Google reviews.":
        "Mesas completas de picoteo y charcuteria, pasapalos, exhibiciones de postres y catering completo para bodas, quince anos y cumpleanos en West Kendall y Miami. Calificacion perfecta de 5.0 en 47 resenas de Google.",
    "5.0 · 47 reviews on Google": "5.0 · 47 resenas en Google",
    "Call (786) 332-7065": "Llama al (786) 332-7065",
    "Signature": "Especialidad",
    "Styled for your event": "Decorado para tu evento",
    "Charcuterie · Desserts": "Charcuteria · Postres",
    "Chefs, bartenders, waiters": "Chefs, bartenders, meseros",
    "120th St, Miami, FL": "120th St, Miami, FL",
    "A team of chefs,": "Un equipo de chefs,",
    "bartenders and waiters": "bartenders y meseros",
    "Upick Caterers, based in West Kendall, builds grazing and charcuterie tables, hors d&#39;oeuvres and dessert displays for weddings, sweet 16s and birthdays across Miami, with a full team of chefs, bartenders and waiters on site.":
        "Upick Caterers, con base en West Kendall, arma mesas de picoteo y charcuteria, pasapalos y exhibiciones de postres para bodas, quince anos y cumpleanos en Miami, con un equipo completo de chefs, bartenders y meseros en el lugar.",
    "Hosts confirm it: a perfect 5.0 rating across 47 Google reviews, with clients praising how fresh everything looks and how beautifully the tables are styled.":
        "Los anfitriones lo confirman: calificacion perfecta de 5.0 en 47 resenas de Google, con clientes que destacan lo fresco que se ve todo y lo bien decoradas que quedan las mesas.",
    "Catering Special Event": "Catering Special Event",
    "How it works": "Asi se trabaja",
    "Share your vision": "Cuentanos tu idea",
    "Call with your date, guest count and theme, grazing table, hors d&#39;oeuvres or a full wedding spread.":
        "Llama con tu fecha, numero de invitados y el tema: mesa de picoteo, pasapalos o un montaje completo de boda.",
    "A menu you can see": "Un menu que puedes ver",
    "A clear quote and menu built around your guest count, from grazing boards to a full plated dinner.":
        "Una cotizacion y menu claros segun tu numero de invitados, desde tablas de picoteo hasta una cena completa.",
    "Styled on site": "Decorado en el lugar",
    "The team arrives early to style the grazing table and set up the full spread before your guests arrive.":
        "El equipo llega temprano para decorar la mesa de picoteo y montar todo antes de que lleguen tus invitados.",
    "Served &amp; cleared": "Servido y recogido",
    "Chefs, bartenders and waiters serve your guests, then clear the setup when the party winds down.":
        "Chefs, bartenders y meseros sirven a tus invitados, y recogen todo cuando termina la fiesta.",
    "Catering for": "Catering para",
    "your special event": "tu evento especial",
    "Every event gets its own quote built around your menu and guest count. Call to start planning.":
        "Cada evento recibe su propia cotizacion segun tu menu y numero de invitados. Llama para empezar a planear.",
    "Get a quote": "Pide tu cotizacion",
    "Call": "Llamar",
    "Grazing &amp; Charcuterie Tables": "Mesas de Picoteo y Charcuteria",
    "Full grazing tables with cured meats, cheeses, fruit and crackers, styled for the room.":
        "Mesas completas de picoteo con carnes curadas, quesos, fruta y galletas, decoradas para el salon.",
    "Cocktail hour": "Hora del coctel",
    "Hors d&#39;oeuvres &amp; Appetizer Cones": "Pasapalos y Conos de Aperitivo",
    "Passed appetizers and individual cones with mozzarella, tomato and fresh herbs for cocktail hour.":
        "Pasapalos servidos y conos individuales con mozzarella, tomate y hierbas frescas para la hora del coctel.",
    "Sweet finish": "Final dulce",
    "Dessert Tables": "Mesas de Postres",
    "Donuts, mini desserts and sweets styled under party lighting for sweet 16s and birthdays.":
        "Donas, mini postres y dulces decorados bajo luces de fiesta para quince anos y cumpleanos.",
    "Full service": "Servicio completo",
    "Weddings &amp; Milestone Parties": "Bodas y Celebraciones Especiales",
    "Full-service catering with chefs, bartenders and waiters for weddings, sweet 16s and birthdays.":
        "Catering completo con chefs, bartenders y meseros para bodas, quince anos y cumpleanos.",
    "Boards": "Tablas",
    "Charcuterie &amp; cheese": "Charcuteria y quesos",
    "Fresh fruit displays": "Exhibiciones de fruta fresca",
    "Dips &amp; crackers": "Dips y galletas",
    "Kibbeh &amp; Mediterranean platters": "Platones de kibbeh y mediterraneos",
    "Caprese skewers": "Brochetas caprese",
    "Appetizer cones": "Conos de aperitivo",
    "Passed hors d&#39;oeuvres": "Pasapalos servidos",
    "Bartending": "Servicio de bar",
    "Sweets": "Dulces",
    "Donut towers": "Torres de donas",
    "Mini dessert cups": "Vasitos de mini postre",
    "Chocolate-covered treats": "Dulces cubiertos de chocolate",
    "Themed styling": "Decoracion tematica",
    "Pricing depends on menu and guest count. Call (786) 332-7065 for a free quote.":
        "El precio depende del menu y el numero de invitados. Llama al (786) 332-7065 para una cotizacion gratis.",
    "Real": "Mesas",
    "tables": "reales",
    "What Miami": "Lo que dicen los",
    "hosts say": "anfitriones en Miami",
    "Read all 47 reviews on Google": "Lee las 47 resenas en Google",
    "Serving": "Sirviendo a",
    "Bookings": "Reservas",
    "Call with your date and guest count for a free quote.":
        "Llama con tu fecha y numero de invitados para una cotizacion gratis.",
    "Reviews": "Resenas",
    "5.0 stars across 47 verified Google reviews.": "5.0 estrellas en 47 resenas verificadas de Google.",
    "Your table,": "Tu mesa,",
    "styled your way": "decorada a tu manera",
    "Call (786) 332-7065 for a free quote on your grazing table, hors d&#39;oeuvres, dessert table or full-service event. Serving West Kendall and Miami.":
        "Llama al (786) 332-7065 para una cotizacion gratis de tu mesa de picoteo, pasapalos, mesa de postres o evento completo. Sirviendo a West Kendall y Miami.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Event catering serving West Kendall and Miami, FL.": "Catering de eventos en West Kendall y Miami, FL.",
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
