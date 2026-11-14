import re
import os
import colorsys
import shutil

SLUG = "sky-limit-catering"
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
# 2. PALETA: dorado (pureartistry) -> ambar/naranja (Sky Limit Catering,
#    su propio logo de globo aerostatico naranja y lechon asado)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(212, 168, 75), (232, 207, 150), (185, 138, 128), (180, 140, 60), (122, 90, 30),
          (110, 85, 35), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]

TARGET_HUE = 25 / 360.0
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

RING1 = "rgba(215,132,72"   # era rgba(212,168,75
RING2 = "rgba(234,184,148"  # era rgba(232,207,150
HEX_HOVER = "#ebc5a9"        # era #e9c3ab

# ============================================================
# 3. Globales: no hay booking platform ni email -> tel: + IG real
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+13056094811"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_IG_URL = "https://www.instagram.com/skylimit.catering/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_IG_HANDLE = "@skylimit.catering"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=Miami,+FL"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Sky Limit Catering · Private Event Catering in Miami, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Sky Limit Catering, Miami FL: whole roast pig, paella, grazing tables and full-service catering for weddings, yacht parties and private events. 5.0 stars across 67 Google reviews." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Sky Limit Catering · Private Event Catering in Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Whole roast pig, paella, grazing tables and full-service event catering. 5.0 on Google with 67 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-yacht-table.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CateringService",
    "name": "Sky Limit Catering, Inc",
    "description": "Private event catering company serving Miami, FL: whole roast pig, paella, grazing and charcuterie tables, and full-service catering for weddings, yacht parties and holiday gatherings.",
    "areaServed": "Miami, FL",
    "telephone": "+1-305-609-4811",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "67", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Catering services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Whole Roast Pig" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Paella &amp; Grill" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Grazing &amp; Charcuterie Tables" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Weddings &amp; Yacht Parties" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN default (resenas y branding en ingles)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ============================================================
# 6. PRELOADER + NAV
# ============================================================
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">SKY</span>\n    <span class="pre-word">Sky Limit Catering</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.35)]" />',
    '<img src="assets/logo.jpg" alt="Sky Limit Catering" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Sky <span class="text-[color:var(--accent-deep)]">Limit</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Get a quote" data-en="Get a quote">Get a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Get a quote" data-en="Get a quote">Get a quote</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miami, FL · Private Event Catering" data-en="Miami, FL · Private Event Catering">Miami, FL · Private Event Catering</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="You dream it, we cook it." data-en="You dream it, we cook it.">You dream it, we cook it.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Whole roast pig, paella" data-en="Whole roast pig, paella">Whole roast pig, paella</span><br /><span data-es="and grazing tables, made " data-en="and grazing tables, made ">and grazing tables, made </span><span class="text-shine" data-es="to order" data-en="to order">to order</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Whole roast pig on the spit, paella cooked outdoors, grazing and charcuterie tables, and full-service catering for weddings, yacht parties and holiday gatherings across Miami. A perfect 5.0 rating across 67 Google reviews." data-en="Whole roast pig on the spit, paella cooked outdoors, grazing and charcuterie tables, and full-service catering for weddings, yacht parties and holiday gatherings across Miami. A perfect 5.0 rating across 67 Google reviews.">Whole roast pig on the spit, paella cooked outdoors, grazing and charcuterie tables, and full-service catering for weddings, yacht parties and holiday gatherings across Miami. A perfect 5.0 rating across 67 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 67 reviews on Google" data-en="5.0 · 67 reviews on Google">5.0 · 67 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (305) 609-4811" data-en="Call (305) 609-4811">Call (305) 609-4811</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-yacht-table.jpg" alt="A private dining table set up by Sky Limit Catering aboard a yacht" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Signature" data-en="Signature">Signature</p>
            <p class="font-display text-lg">Whole Roast Pig</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Cooked fresh, on site" data-en="Cooked fresh, on site">Cooked fresh, on site</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="67">67</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Pig <span class="text-shine">&amp;</span> Paella</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cooked outdoors, fresh" data-en="Cooked outdoors, fresh">Cooked outdoors, fresh</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">Grazing <span class="text-shine">&amp;</span> Tables</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Charcuterie y mesas de quesos" data-en="Charcuterie &amp; cheese boards">Charcuterie &amp; cheese boards</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Y toda la zona de eventos" data-en="And the surrounding area">And the surrounding area</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Whole Roast Pig"),
    ("Loc Retwist", "Paella"),
    ("Knotless Braids", "Grazing Tables"),
    ("K-Tip Extensions", "Charcuterie Boards"),
    ("Keratin", "Yacht Parties"),
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
          <img src="assets/about-chefs.jpg" alt="The Sky Limit Catering chef team cooking paella outdoors at a Miami event" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="A chef team," data-en="A chef team,">A chef team,</span><br /><span class="text-shine" data-es="built for the big event" data-en="built for the big event">built for the big event</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Sky Limit Catering is a Miami chef team built around a simple motto: you dream it, we cook it. Whole roast pig on the spit, paella cooked outdoors and grazing tables for weddings, yacht parties and holiday gatherings." data-en="Sky Limit Catering is a Miami chef team built around a simple motto: you dream it, we cook it. Whole roast pig on the spit, paella cooked outdoors and grazing tables for weddings, yacht parties and holiday gatherings.">Sky Limit Catering is a Miami chef team built around a simple motto: you dream it, we cook it. Whole roast pig on the spit, paella cooked outdoors and grazing tables for weddings, yacht parties and holiday gatherings.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Clients confirm it: a perfect 5.0 rating across 67 Google reviews, with guests still talking about the Cuban pork and rice long after the party is over." data-en="Clients confirm it: a perfect 5.0 rating across 67 Google reviews, with guests still talking about the Cuban pork and rice long after the party is over.">Clients confirm it: a perfect 5.0 rating across 67 Google reviews, with guests still talking about the Cuban pork and rice long after the party is over.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="67">67</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">100%</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Cocinado en el momento" data-en="Cooked fresh">Cooked fresh</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo.jpg" alt="Sky Limit Catering" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Sky Limit Catering · <span class="text-[color:var(--ink-40)]" data-es="You dream it, we cook it" data-en="You dream it, we cook it">You dream it, we cook it</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Tell us the dream" data-en="Tell us the dream">Tell us the dream</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or DM with your date, guest count and the vibe you want, whole roast pig, paella or a grazing table." data-en="Call or DM with your date, guest count and the vibe you want, whole roast pig, paella or a grazing table.">Call or DM with your date, guest count and the vibe you want, whole roast pig, paella or a grazing table.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="A quote you can see" data-en="A quote you can see">A quote you can see</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a clear price built around your menu and guest count, no guessing games." data-en="You get a clear price built around your menu and guest count, no guessing games.">You get a clear price built around your menu and guest count, no guessing games.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Cooked on site" data-en="Cooked on site">Cooked on site</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The team arrives early and cooks on site, whole roast pig over coals, paella in the open pan, every time." data-en="The team arrives early and cooks on site, whole roast pig over coals, paella in the open pan, every time.">The team arrives early and cooks on site, whole roast pig over coals, paella in the open pan, every time.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Served &amp; cleared" data-en="Served &amp; cleared">Served &amp; cleared</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Your guests get served hot plates, and the team clears the setup when the party is over." data-en="Your guests get served hot plates, and the team clears the setup when the party is over.">Your guests get served hot plates, and the team clears the setup when the party is over.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Catering for" data-en="Catering for">Catering for</span> <span class="text-shine" data-es="every dream event" data-en="every dream event">every dream event</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every event gets its own quote built around your menu and guest count. Call or DM to start planning." data-en="Every event gets its own quote built around your menu and guest count. Call or DM to start planning.">Every event gets its own quote built around your menu and guest count. Call or DM to start planning.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: ''' + RING1 + ''',0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Signature" data-en="Signature">Signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Whole Roast Pig" data-en="Whole Roast Pig">Whole Roast Pig</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A whole pig roasted over coals on a rotating spit, the centerpiece for weddings and large family parties." data-en="A whole pig roasted over coals on a rotating spit, the centerpiece for weddings and large family parties.">A whole pig roasted over coals on a rotating spit, the centerpiece for weddings and large family parties.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cooked outdoors" data-en="Cooked outdoors">Cooked outdoors</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Paella &amp; Grill" data-en="Paella &amp; Grill">Paella &amp; Grill</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Fresh paella cooked live in a wide pan, plus grilled meats, right in front of your guests." data-en="Fresh paella cooked live in a wide pan, plus grilled meats, right in front of your guests.">Fresh paella cooked live in a wide pan, plus grilled meats, right in front of your guests.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Grazing" data-en="Grazing">Grazing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Grazing &amp; Charcuterie Tables" data-en="Grazing &amp; Charcuterie Tables">Grazing &amp; Charcuterie Tables</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full grazing tables with cured meats, cheeses, fruit and crackers, styled for cocktail hour." data-en="Full grazing tables with cured meats, cheeses, fruit and crackers, styled for cocktail hour.">Full grazing tables with cured meats, cheeses, fruit and crackers, styled for cocktail hour.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Full service" data-en="Full service">Full service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Weddings &amp; Yacht Parties" data-en="Weddings &amp; Yacht Parties">Weddings &amp; Yacht Parties</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service catering for weddings, yacht parties and holiday gatherings, cooked and served by the team." data-en="Full-service catering for weddings, yacht parties and holiday gatherings, cooked and served by the team.">Full-service catering for weddings, yacht parties and holiday gatherings, cooked and served by the team.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="On the spit" data-en="On the spit">On the spit</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Whole roast pig" data-en="Whole roast pig">Whole roast pig</li>
            <li class="flex items-center gap-2" data-es="Holiday turkey" data-en="Holiday turkey">Holiday turkey</li>
            <li class="flex items-center gap-2" data-es="Cuban rice &amp; pork" data-en="Cuban rice &amp; pork">Cuban rice &amp; pork</li>
            <li class="flex items-center gap-2" data-es="Fried plantains" data-en="Fried plantains">Fried plantains</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Tables" data-en="Tables">Tables</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Charcuterie boards" data-en="Charcuterie boards">Charcuterie boards</li>
            <li class="flex items-center gap-2" data-es="Cheese &amp; fruit displays" data-en="Cheese &amp; fruit displays">Cheese &amp; fruit displays</li>
            <li class="flex items-center gap-2" data-es="Mini sliders &amp; appetizers" data-en="Mini sliders &amp; appetizers">Mini sliders &amp; appetizers</li>
            <li class="flex items-center gap-2" data-es="Dessert tables" data-en="Dessert tables">Dessert tables</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Events" data-en="Events">Events</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Weddings" data-en="Weddings">Weddings</li>
            <li class="flex items-center gap-2" data-es="Yacht &amp; private parties" data-en="Yacht &amp; private parties">Yacht &amp; private parties</li>
            <li class="flex items-center gap-2" data-es="Holiday gatherings" data-en="Holiday gatherings">Holiday gatherings</li>
            <li class="flex items-center gap-2" data-es="Corporate events" data-en="Corporate events">Corporate events</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on menu and guest count. Call (305) 609-4811 for a free quote." data-en="Pricing depends on menu and guest count. Call (305) 609-4811 for a free quote.">Pricing depends on menu and guest count. Call (305) 609-4811 for a free quote.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="events" data-en="events">events</span>')
rep('''<a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_IG_HANDLE + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (305) 609-4811
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Mesa de charcuteria y quesos" data-en="Grazing &amp; cheese spread">Grazing &amp; cheese spread</span><img src="assets/gallery-grazing-wide.jpg" alt="A full grazing and charcuterie spread set up by Sky Limit Catering" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Lechon entero en el asador" data-en="Whole pig on the spit">Whole pig on the spit</span><img src="assets/gallery-roast-pig.jpg" alt="A whole pig roasting on a spit over coals by Sky Limit Catering" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Paella cocinada al aire libre" data-en="Paella cooked outdoors">Paella cooked outdoors</span><img src="assets/gallery-paella.jpg" alt="Sky Limit Catering chefs cooking paella outdoors in a large pan" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Tabla de quesos para eventos" data-en="Cheese platter for events">Cheese platter for events</span><img src="assets/gallery-cheese-platter.jpg" alt="An elegant cheese and charcuterie platter by Sky Limit Catering" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Pavo de Thanksgiving con el logo de Sky Limit" data-en="Thanksgiving turkey, Sky Limit branded">Thanksgiving turkey, Sky Limit branded</span><img src="assets/gallery-turkey-branded.jpg" alt="A roasted Thanksgiving turkey plated with the Sky Limit Catering logo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
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
    '<span data-es="5.0 out of 5 · 67 reviews on Google" data-en="5.0 out of 5 · 67 reviews on Google">5.0 out of 5 · 67 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Sky Limit Catering made our wedding unforgettable. From the first tasting to the last bite of the night, this team poured their heart into every detail. The food was absolutely delicious, beautifully presented, and our guests are still talking about it."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Essiel Vega</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Incredible pork! This is exactly the kind of family, passion, and dedication you want behind the food you're eating. You can truly taste the love and care in every bite. Absolutely worth trying!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Melissa Dominguez</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Delicious! They did an amazing job! The Cuban pork was amazing and the Cuban rice was even better. Highly recommend them for any private event. They did a fantastic job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Daniel Gonzalez</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=Sky+Limit+Catering+Miami+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 67 reviews on Google" data-en="Read all 67 reviews on Google">Read all 67 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 16. UBICACION (sin direccion fija: area de servicio)
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Miami, FL</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[' + RING1 + ',0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Sky Limit Catering viaja a tu evento en Miami y el area circundante: bodas, yates y fiestas privadas." data-en="Sky Limit Catering travels to your event across Miami and the surrounding area: weddings, yachts and private parties.">Sky Limit Catering travels to your event across Miami and the surrounding area: weddings, yachts and private parties.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[' + RING1 + ',0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Bookings" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Call or DM with your date and guest count for a free quote." data-en="Call or DM with your date and guest count for a free quote.">Call or DM with your date and guest count for a free quote.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_TEL + '''" data-es="Call (305) 609-4811" data-en="Call (305) 609-4811">Call (305) 609-4811</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See the latest events and DM to start planning your menu." data-en="See the latest events and DM to start planning your menu.">See the latest events and DM to start planning your menu.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Sky Limit Catering service area, Miami FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 17. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="You dream it, we cook it." data-en="You dream it, we cook it.">You dream it, we cook it.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your event," data-en="Your event,">Your event,</span> <span class="text-shine" data-es="cooked to order" data-en="cooked to order">cooked to order</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (305) 609-4811 for a free quote on your whole roast pig, paella, grazing table or full-service event. Serving Miami and the surrounding area." data-en="Call (305) 609-4811 for a free quote on your whole roast pig, paella, grazing table or full-service event. Serving Miami and the surrounding area.">Call (305) 609-4811 for a free quote on your whole roast pig, paella, grazing table or full-service event. Serving Miami and the surrounding area.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (305) 609-4811" data-en="Call (305) 609-4811">Call (305) 609-4811</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>''')
print("CTA FINAL done")

# ============================================================
# 18. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Sky Limit</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[''' + RING2 + ''',0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Sky Limit Catering" class="w-9 h-9 rounded-full object-cover ring-1 ring-[''' + RING2 + ''',0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Sky Limit Catering</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Private event catering serving Miami, FL. You dream it, we cook it." data-en="Private event catering serving Miami, FL. You dream it, we cook it.">Private event catering serving Miami, FL. You dream it, we cook it.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Miami, FL" data-en="Miami, FL">Miami, FL</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[''' + HEX_HOVER + ''']" data-es="Call (305) 609-4811" data-en="Call (305) 609-4811">Call (305) 609-4811</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Sky Limit Catering, Inc.</p>')
print("FOOTER done")

# ============================================================
# 19. Boton flotante
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1007" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Sky Limit Catering">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#07121c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
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
    "Miami, FL · Private Event Catering": "Miami, FL · Catering de Eventos Privados",
    "You dream it, we cook it.": "Tu lo sueñas, nosotros lo cocinamos.",
    "Whole roast pig, paella": "Lechon entero, paella",
    "and grazing tables, made ": "y mesas de picoteo, hecho ",
    "to order": "a tu medida",
    "Whole roast pig on the spit, paella cooked outdoors, grazing and charcuterie tables, and full-service catering for weddings, yacht parties and holiday gatherings across Miami. A perfect 5.0 rating across 67 Google reviews.":
        "Lechon entero en el asador, paella cocinada al aire libre, mesas de picoteo y charcuteria, y catering completo para bodas, fiestas en yates y reuniones festivas en Miami. Calificacion perfecta de 5.0 en 67 resenas de Google.",
    "5.0 · 67 reviews on Google": "5.0 · 67 resenas en Google",
    "Call (305) 609-4811": "Llama al (305) 609-4811",
    "Signature": "Especialidad",
    "Cooked fresh, on site": "Cocinado fresco, en el lugar",
    "Cooked outdoors, fresh": "Cocinado al aire libre, fresco",
    "Grazing": "Picoteo",
    "Tables": "Mesas",
    "A chef team,": "Un equipo de chefs,",
    "built for the big event": "hecho para el gran evento",
    "Sky Limit Catering is a Miami chef team built around a simple motto: you dream it, we cook it. Whole roast pig on the spit, paella cooked outdoors and grazing tables for weddings, yacht parties and holiday gatherings.":
        "Sky Limit Catering es un equipo de chefs en Miami con un lema simple: tu lo sueñas, nosotros lo cocinamos. Lechon entero en el asador, paella al aire libre y mesas de picoteo para bodas, fiestas en yates y reuniones festivas.",
    "Clients confirm it: a perfect 5.0 rating across 67 Google reviews, with guests still talking about the Cuban pork and rice long after the party is over.":
        "Los clientes lo confirman: calificacion perfecta de 5.0 en 67 resenas de Google, con invitados que siguen hablando del puerco y el arroz cubano mucho despues de terminada la fiesta.",
    "You dream it, we cook it": "Tu lo sueñas, nosotros lo cocinamos",
    "How it works": "Asi se trabaja",
    "Tell us the dream": "Cuentanos el sueño",
    "Call or DM with your date, guest count and the vibe you want, whole roast pig, paella or a grazing table.":
        "Llama o escribe por DM con tu fecha, numero de invitados y el estilo que buscas: lechon entero, paella o mesa de picoteo.",
    "A quote you can see": "Una cotizacion clara",
    "You get a clear price built around your menu and guest count, no guessing games.":
        "Recibes un precio claro basado en tu menu y numero de invitados, sin adivinanzas.",
    "Cooked on site": "Cocinado en el lugar",
    "The team arrives early and cooks on site, whole roast pig over coals, paella in the open pan, every time.":
        "El equipo llega temprano y cocina en el lugar: lechon entero sobre brasas, paella en el perol abierto, siempre.",
    "Served &amp; cleared": "Servido y recogido",
    "Your guests get served hot plates, and the team clears the setup when the party is over.":
        "Tus invitados reciben platos calientes, y el equipo recoge todo cuando termina la fiesta.",
    "Catering for": "Catering para",
    "every dream event": "el evento de tus sueños",
    "Every event gets its own quote built around your menu and guest count. Call or DM to start planning.":
        "Cada evento recibe su propia cotizacion segun tu menu y numero de invitados. Llama o escribe por DM para empezar a planear.",
    "Get a quote": "Pide tu cotizacion",
    "Call": "Llamar",
    "A whole pig roasted over coals on a rotating spit, the centerpiece for weddings and large family parties.":
        "Un lechon entero asado sobre brasas en un asador giratorio, el plato central de bodas y grandes fiestas familiares.",
    "Cooked outdoors": "Cocinado al aire libre",
    "Fresh paella cooked live in a wide pan, plus grilled meats, right in front of your guests.":
        "Paella fresca cocinada en vivo en un perol ancho, ademas de carnes a la parrilla, frente a tus invitados.",
    "Full grazing tables with cured meats, cheeses, fruit and crackers, styled for cocktail hour.":
        "Mesas de picoteo completas con carnes curadas, quesos, fruta y galletas, decoradas para la hora del coctel.",
    "Full service": "Servicio completo",
    "Full-service catering for weddings, yacht parties and holiday gatherings, cooked and served by the team.":
        "Catering completo para bodas, fiestas en yates y reuniones festivas, cocinado y servido por el equipo.",
    "On the spit": "En el asador",
    "Whole roast pig": "Lechon entero",
    "Holiday turkey": "Pavo festivo",
    "Cuban rice &amp; pork": "Arroz y puerco cubano",
    "Fried plantains": "Platanos fritos",
    "Charcuterie boards": "Tablas de charcuteria",
    "Cheese &amp; fruit displays": "Exhibiciones de queso y fruta",
    "Mini sliders &amp; appetizers": "Mini hamburguesas y pasapalos",
    "Dessert tables": "Mesas de postres",
    "Events": "Eventos",
    "Weddings": "Bodas",
    "Yacht &amp; private parties": "Fiestas en yates y privadas",
    "Holiday gatherings": "Reuniones festivas",
    "Corporate events": "Eventos corporativos",
    "Pricing depends on menu and guest count. Call (305) 609-4811 for a free quote.":
        "El precio depende del menu y el numero de invitados. Llama al (305) 609-4811 para una cotizacion gratis.",
    "Real": "Eventos",
    "events": "reales",
    "What Miami": "Lo que dicen los",
    "hosts say": "anfitriones en Miami",
    "Read all 67 reviews on Google": "Lee las 67 resenas en Google",
    "Serving": "Sirviendo a",
    "View on map": "Ver en el mapa",
    "Bookings": "Reservas",
    "Call or DM with your date and guest count for a free quote.":
        "Llama o escribe por DM con tu fecha y numero de invitados para una cotizacion gratis.",
    "See the latest events and DM to start planning your menu.":
        "Mira los eventos mas recientes y escribe por DM para empezar a planear tu menu.",
    "Your event,": "Tu evento,",
    "cooked to order": "cocinado a tu medida",
    "Call (305) 609-4811 for a free quote on your whole roast pig, paella, grazing table or full-service event. Serving Miami and the surrounding area.":
        "Llama al (305) 609-4811 para una cotizacion gratis de tu lechon entero, paella, mesa de picoteo o evento completo. Sirviendo a Miami y el area circundante.",
    "Follow on Instagram": "Siguenos en Instagram",
    "Private event catering serving Miami, FL. You dream it, we cook it.": "Catering de eventos privados en Miami, FL. Tu lo sueñas, nosotros lo cocinamos.",
    "Contact": "Contacto",
    "Miami, FL": "Miami, FL",
    "Follow": "Siguenos",
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
