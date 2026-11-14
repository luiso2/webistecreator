import re
import os
import colorsys
import shutil

SLUG = "1000-volts-electric-llc"
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
# 2. PALETA: dorado (pureartistry) -> azul electrico (1000 Volts Electric)
#    hue-shift via colorsys, saturacion similar, manteniendo luminosidad real
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(212, 168, 75), (232, 207, 150), (185, 138, 128), (180, 140, 60), (122, 90, 30),
          (110, 85, 35), (232, 210, 160), (245, 239, 227), (54, 42, 38), (80, 58, 18)]

TARGET_HUE = 210 / 360.0
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

# ============================================================
# 3. Globales: no hay booking platform, email ni IG -> tel: + Google reviews
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+13059041066"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=1000+Volts+Electric+Hallandale+Beach+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "2490 S Park Rd #108, Hallandale Beach, FL 33009"
NEW_MAPS = "https://www.google.com/maps?q=2490+S+Park+Rd+%23108,+Hallandale+Beach,+FL+33009"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>1000 Volts Electric · Licensed Electrician in Hallandale Beach, FL | 4.8 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="1000 Volts Electric LLC, Hallandale Beach FL: panel upgrades, lighting installs, wiring repairs and ventilation. 4.8 stars across 53 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="1000 Volts Electric · Licensed Electrician in Hallandale Beach, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Panel upgrades, lighting, wiring repairs and ventilation installs. 4.8 on Google with 53 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-panel.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Electrician",
    "name": "1000 Volts Electric LLC",
    "description": "Licensed electrical contractor in Hallandale Beach, FL serving Hollywood and the surrounding area: panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs.",
    "address": { "@type": "PostalAddress", "streetAddress": "2490 S Park Rd #108", "addressLocality": "Hallandale Beach", "addressRegion": "FL", "postalCode": "33009", "addressCountry": "US" },
    "telephone": "+1-305-904-1066",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "53", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Electrical services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Panel Upgrades &amp; Meter Service" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Lighting Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Wiring Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Ventilation &amp; Fan Installs" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN default (resenas en ingles)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ============================================================
# 6. PRELOADER + NAV
# ============================================================
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">1KV</span>\n    <span class="pre-word">1000 Volts Electric</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,143,215,0.35)]" />',
    '<img src="assets/logo.jpg" alt="1000 Volts Electric" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,143,215,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">1000 <span class="text-[color:var(--accent-deep)]">Volts</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call for a quote" data-en="Call for a quote">Call for a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Hallandale Beach, FL · Licensed Electrician" data-en="Hallandale Beach, FL · Licensed Electrician">Hallandale Beach, FL · Licensed Electrician</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Power done right, every time." data-en="Power done right, every time.">Power done right, every time.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Panels, lighting and" data-en="Panels, lighting and">Panels, lighting and</span><br /><span data-es="wiring, fixed " data-en="wiring, fixed ">wiring, fixed </span><span class="text-shine" data-es="fast" data-en="fast">fast</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs across Hallandale Beach and Hollywood. Fast, attentive and background checked, with a 4.8 rating across 53 Google reviews." data-en="Panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs across Hallandale Beach and Hollywood. Fast, attentive and background checked, with a 4.8 rating across 53 Google reviews.">Panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs across Hallandale Beach and Hollywood. Fast, attentive and background checked, with a 4.8 rating across 53 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.8 · 53 reviews on Google" data-en="4.8 · 53 reviews on Google">4.8 · 53 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (305) 904-1066" data-en="Call (305) 904-1066">Call (305) 904-1066</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Trabajo real" data-en="Real work">Real work</span>\n          <span data-es="Precios claros" data-en="Clear pricing">Clear pricing</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Direct contact</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-panel.jpg" alt="A newly wired electrical panel serviced by 1000 Volts Electric in Hallandale Beach, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">7am - 7pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Mon-Sat · Closed Sunday" data-en="Mon-Sat · Closed Sunday">Mon-Sat · Closed Sunday</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="53">53</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Panels <span class="text-shine">&amp;</span> Wiring</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Lighting · Fans · Repairs" data-en="Lighting · Fans · Repairs">Lighting · Fans · Repairs</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">7am <span class="text-shine">-</span> 7pm</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Mon-Sat" data-en="Mon-Sat">Mon-Sat</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Hallandale</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Beach, FL" data-en="Beach, FL">Beach, FL</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Panel Upgrades"),
    ("Loc Retwist", "Lighting Install"),
    ("Knotless Braids", "Wiring Repair"),
    ("K-Tip Extensions", "Meter Service"),
    ("Keratin", "Fan Install"),
    ("Orlando, FL", "Hallandale Beach, FL"),
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
          <img src="assets/about-technician.jpg" alt="A 1000 Volts Electric technician explaining an electrical meter upgrade to a customer" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Licensed," data-en="Licensed,">Licensed,</span><br /><span class="text-shine" data-es="background checked" data-en="background checked">background checked</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="1000 Volts Electric LLC is a licensed electrical contractor serving Hallandale Beach, Hollywood and the surrounding area: panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs." data-en="1000 Volts Electric LLC is a licensed electrical contractor serving Hallandale Beach, Hollywood and the surrounding area: panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs.">1000 Volts Electric LLC is a licensed electrical contractor serving Hallandale Beach, Hollywood and the surrounding area: panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Customers describe the team as fast, attentive and down to earth. The result: a 4.8-star rating across 53 Google reviews." data-en="Customers describe the team as fast, attentive and down to earth. The result: a 4.8-star rating across 53 Google reviews.">Customers describe the team as fast, attentive and down to earth. The result: a 4.8-star rating across 53 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="53">53</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">6+</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Dias a la semana" data-en="Days a week">Days a week</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,143,215,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo.jpg" alt="1000 Volts Electric" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,143,215,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">1000 Volts Electric · <span class="text-[color:var(--ink-40)]" data-es="Licensed electrician" data-en="Licensed electrician">Licensed electrician</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call it in" data-en="Call it in">Call it in</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text with what needs fixing or installing, and the team walks you through it over the phone." data-en="Call or text with what needs fixing or installing, and the team walks you through it over the phone.">Call or text with what needs fixing or installing, and the team walks you through it over the phone.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Honest quote" data-en="Honest quote">Honest quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a clear, upfront price for the job before any work starts, no surprises on the bill." data-en="You get a clear, upfront price for the job before any work starts, no surprises on the bill.">You get a clear, upfront price for the job before any work starts, no surprises on the bill.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The work" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="From a panel upgrade to a wiring repair, the job gets done fast and clean, with background checked technicians." data-en="From a panel upgrade to a wiring repair, the job gets done fast and clean, with background checked technicians.">From a panel upgrade to a wiring repair, the job gets done fast and clean, with background checked technicians.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walkthrough" data-en="Walkthrough">Walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Before the team leaves, you walk through the finished work together, so you know it is done right." data-en="Before the team leaves, you walk through the finished work together, so you know it is done right.">Before the team leaves, you walk through the finished work together, so you know it is done right.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Servicios para" data-en="Services for">Services for</span> <span class="text-shine" data-es="cada hogar" data-en="every home">every home</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two jobs are the same, so every project gets its own honest quote by phone, before any work begins." data-en="No two jobs are the same, so every project gets its own honest quote by phone, before any work begins.">No two jobs are the same, so every project gets its own honest quote by phone, before any work begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(72,143,215,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Panel Upgrades &amp; Meter Service" data-en="Panel Upgrades &amp; Meter Service">Panel Upgrades &amp; Meter Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Breaker panel upgrades, meter bank service and the electrical panel work most homeowners and small buildings call about." data-en="Breaker panel upgrades, meter bank service and the electrical panel work most homeowners and small buildings call about.">Breaker panel upgrades, meter bank service and the electrical panel work most homeowners and small buildings call about.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Brighten up" data-en="Brighten up">Brighten up</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lighting Installation" data-en="Lighting Installation">Lighting Installation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Recessed lighting, kitchen and ceiling fixtures installed clean, with a finish that looks as good as it works." data-en="Recessed lighting, kitchen and ceiling fixtures installed clean, with a finish that looks as good as it works.">Recessed lighting, kitchen and ceiling fixtures installed clean, with a finish that looks as good as it works.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Fixed fast" data-en="Fixed fast">Fixed fast</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Wiring Repairs" data-en="Wiring Repairs">Wiring Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Romex and wiring fixes, outlet and switch repair, and the everyday electrical problems that need a fast, safe fix." data-en="Romex and wiring fixes, outlet and switch repair, and the everyday electrical problems that need a fast, safe fix.">Romex and wiring fixes, outlet and switch repair, and the everyday electrical problems that need a fast, safe fix.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Airflow" data-en="Airflow">Airflow</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Ventilation &amp; Fan Installs" data-en="Ventilation &amp; Fan Installs">Ventilation &amp; Fan Installs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Roof and exhaust fan installation and wiring for bathrooms, kitchens and attics that need better airflow." data-en="Roof and exhaust fan installation and wiring for bathrooms, kitchens and attics that need better airflow.">Roof and exhaust fan installation and wiring for bathrooms, kitchens and attics that need better airflow.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Panels &amp; Meters" data-en="Panels &amp; Meters">Panels &amp; Meters</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Panel upgrades" data-en="Panel upgrades">Panel upgrades</li>
            <li class="flex items-center gap-2" data-es="Meter bank service" data-en="Meter bank service">Meter bank service</li>
            <li class="flex items-center gap-2" data-es="Breaker replacement" data-en="Breaker replacement">Breaker replacement</li>
            <li class="flex items-center gap-2" data-es="Electrical inspections" data-en="Electrical inspections">Electrical inspections</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Lighting" data-en="Lighting">Lighting</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Recessed lighting" data-en="Recessed lighting">Recessed lighting</li>
            <li class="flex items-center gap-2" data-es="Kitchen &amp; ceiling fixtures" data-en="Kitchen &amp; ceiling fixtures">Kitchen &amp; ceiling fixtures</li>
            <li class="flex items-center gap-2" data-es="Outlet &amp; switch install" data-en="Outlet &amp; switch install">Outlet &amp; switch install</li>
            <li class="flex items-center gap-2" data-es="Ceiling fan wiring" data-en="Ceiling fan wiring">Ceiling fan wiring</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Wiring &amp; Install" data-en="Wiring &amp; Install">Wiring &amp; Install</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Wiring repairs" data-en="Wiring repairs">Wiring repairs</li>
            <li class="flex items-center gap-2" data-es="Exhaust &amp; roof fan install" data-en="Exhaust &amp; roof fan install">Exhaust &amp; roof fan install</li>
            <li class="flex items-center gap-2" data-es="General electrical work" data-en="General electrical work">General electrical work</li>
            <li class="flex items-center gap-2" data-es="Free estimates" data-en="Free estimates">Free estimates</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and materials. Call (305) 904-1066 for a free quote." data-en="Pricing depends on scope and materials. Call (305) 904-1066 for a free quote.">Pricing depends on scope and materials. Call (305) 904-1066 for a free quote.</span></p>')
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
          Call (305) 904-1066
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Instalacion de iluminacion empotrada" data-en="Recessed lighting installed">Recessed lighting installed</span><img src="assets/gallery-recessed-lighting.jpg" alt="Recessed kitchen lighting installed by 1000 Volts Electric" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Lampara de techo instalada" data-en="Ceiling fixture install">Ceiling fixture install</span><img src="assets/gallery-ceiling-fixture.jpg" alt="A ceiling light fixture installed by 1000 Volts Electric" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cableado de panel comercial" data-en="Commercial panel wiring">Commercial panel wiring</span><img src="assets/gallery-panel-wiring.jpg" alt="Commercial electrical panel wiring by 1000 Volts Electric" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Reparacion de cableado" data-en="Wiring repair closeup">Wiring repair closeup</span><img src="assets/gallery-wire-splice.jpg" alt="A wiring repair in progress by 1000 Volts Electric" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Instalacion de extractor en techo" data-en="Roof exhaust fan install">Roof exhaust fan install</span><img src="assets/gallery-exhaust-install.jpg" alt="A roof exhaust fan installed by 1000 Volts Electric" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 15. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Hallandale" data-en="What Hallandale">What Hallandale</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="4.8 out of 5 · 53 reviews on Google" data-en="4.8 out of 5 · 53 reviews on Google">4.8 out of 5 · 53 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Joseph is incredible! Fast, efficient, and extremely knowledgeable. Now days it is extremely hard to find someone professional and reliable, Joseph IS THAT GUY! Amazing work, thank you!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Kevin Haxho</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very attentive and down to earth people. If you need work done don't go anywhere else, they will take care of you highly recommend! I own business and I know when the owners care about their work, 1000 Voltz THEY CARE!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">junior izaguirre</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great customer service. I needed a Romex wire lengthened to close a wall up in my kitchen. He fixed the issue within a hour. I'm truly happy with the outcome and how efficient he is. I'd highly recommend him."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mariette Cheremond</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 53 reviews on Google" data-en="Read all 53 reviews on Google">Read all 53 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 16. UBICACION (direccion real disponible)
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Hallandale Beach</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,143,215,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,143,215,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,143,215,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Saturday, 7:00 AM to 7:00 PM. Closed Sunday." data-en="Monday to Saturday, 7:00 AM to 7:00 PM. Closed Sunday.">Monday to Saturday, 7:00 AM to 7:00 PM. Closed Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,143,215,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (305) 904-1066" data-en="Call (305) 904-1066">Call (305) 904-1066</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,143,215,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.8 stars across 53 verified Google reviews." data-en="4.8 stars across 53 verified Google reviews.">4.8 stars across 53 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,143,215,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: 1000 Volts Electric, 2490 S Park Rd, Hallandale Beach FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 17. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Power done right, every time." data-en="Power done right, every time.">Power done right, every time.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call fixes" data-en="One call fixes">One call fixes</span> <span class="text-shine" data-es="it all" data-en="it all">it all</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (305) 904-1066 for a free, honest quote on your panel upgrade, lighting, wiring or ventilation job. Monday to Saturday, 7 AM to 7 PM." data-en="Call (305) 904-1066 for a free, honest quote on your panel upgrade, lighting, wiring or ventilation job. Monday to Saturday, 7 AM to 7 PM.">Call (305) 904-1066 for a free, honest quote on your panel upgrade, lighting, wiring or ventilation job. Monday to Saturday, 7 AM to 7 PM.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (305) 904-1066" data-en="Call (305) 904-1066">Call (305) 904-1066</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ============================================================
# 18. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">1000 Volts</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(148,191,234,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="1000 Volts Electric" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(148,191,234,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">1000 Volts Electric</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Licensed electrician serving Hallandale Beach and Hollywood, FL." data-en="Licensed electrician serving Hallandale Beach and Hollywood, FL.">Licensed electrician serving Hallandale Beach and Hollywood, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#a9caeb]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#a1c2e9]" data-es="Call (305) 904-1066" data-en="Call (305) 904-1066">Call (305) 904-1066</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9caeb]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a1c2e9]">4.8 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 1000 Volts Electric LLC.</p>')
print("FOOTER done")

# ============================================================
# 19. Boton flotante
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#07121c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call 1000 Volts Electric">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#07121c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
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
    "Hallandale Beach, FL · Licensed Electrician": "Hallandale Beach, FL · Electricista con Licencia",
    "Power done right, every time.": "El trabajo electrico bien hecho, siempre.",
    "Panels, lighting and": "Paneles, luces y",
    "wiring, fixed ": "cableado, arreglado ",
    "fast": "rapido",
    "Panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs across Hallandale Beach and Hollywood. Fast, attentive and background checked, with a 4.8 rating across 53 Google reviews.":
        "Actualizacion de paneles y medidores, instalacion de luces, reparacion de cableado e instalacion de ventilacion en Hallandale Beach y Hollywood. Rapido, atento y con verificacion de antecedentes, con calificacion de 4.8 en 53 resenas de Google.",
    "4.8 · 53 reviews on Google": "4.8 · 53 resenas en Google",
    "Call (305) 904-1066": "Llama al (305) 904-1066",
    "Open": "Abierto",
    "Mon-Sat · Closed Sunday": "Lun-Sab · Cerrado domingo",
    "Lighting · Fans · Repairs": "Luces · Ventiladores · Reparaciones",
    "Mon-Sat": "Lun-Sab",
    "Beach, FL": "Beach, FL",
    "Licensed,": "Con licencia,",
    "background checked": "verificacion de antecedentes",
    "1000 Volts Electric LLC is a licensed electrical contractor serving Hallandale Beach, Hollywood and the surrounding area: panel upgrades and meter service, lighting installation, wiring repairs and ventilation installs.":
        "1000 Volts Electric LLC es un contratista electrico con licencia que sirve a Hallandale Beach, Hollywood y el area circundante: actualizacion de paneles y medidores, instalacion de luces, reparacion de cableado e instalacion de ventilacion.",
    "Customers describe the team as fast, attentive and down to earth. The result: a 4.8-star rating across 53 Google reviews.":
        "Los clientes describen al equipo como rapido, atento y sencillo. El resultado: una calificacion de 4.8 estrellas en 53 resenas de Google.",
    "Licensed electrician": "Electricista con licencia",
    "How it works": "Asi se trabaja",
    "Call it in": "Llama o escribe",
    "Call or text with what needs fixing or installing, and the team walks you through it over the phone.":
        "Llama o escribe con lo que necesitas reparar o instalar, y el equipo te explica el proceso por telefono.",
    "Honest quote": "Cotizacion honesta",
    "You get a clear, upfront price for the job before any work starts, no surprises on the bill.":
        "Recibes un precio claro y directo antes de empezar el trabajo, sin sorpresas en la factura.",
    "The work": "El trabajo",
    "From a panel upgrade to a wiring repair, the job gets done fast and clean, with background checked technicians.":
        "Desde una actualizacion de panel hasta una reparacion de cableado, el trabajo se hace rapido y limpio, con tecnicos verificados.",
    "Walkthrough": "Revision final",
    "Before the team leaves, you walk through the finished work together, so you know it is done right.":
        "Antes de que el equipo se vaya, revisan juntos el trabajo terminado, para que sepas que quedo bien hecho.",
    "No two jobs are the same, so every project gets its own honest quote by phone, before any work begins.":
        "Ningun trabajo es igual a otro, asi que cada proyecto recibe su propia cotizacion honesta por telefono, antes de comenzar.",
    "Most requested": "Lo mas solicitado",
    "Panel Upgrades &amp; Meter Service": "Actualizacion de Paneles y Medidores",
    "Breaker panel upgrades, meter bank service and the electrical panel work most homeowners and small buildings call about.":
        "Actualizacion de paneles electricos, servicio de bancos de medidores y el trabajo de paneles que mas piden duenos de casa y edificios pequenos.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Brighten up": "Ilumina tu casa",
    "Lighting Installation": "Instalacion de Iluminacion",
    "Recessed lighting, kitchen and ceiling fixtures installed clean, with a finish that looks as good as it works.":
        "Luces empotradas, lamparas de cocina y techo instaladas con limpieza, con un acabado que se ve tan bien como funciona.",
    "Fixed fast": "Arreglado rapido",
    "Wiring Repairs": "Reparacion de Cableado",
    "Romex and wiring fixes, outlet and switch repair, and the everyday electrical problems that need a fast, safe fix.":
        "Arreglos de Romex y cableado, reparacion de tomacorrientes e interruptores, y los problemas electricos cotidianos que necesitan una solucion rapida y segura.",
    "Airflow": "Ventilacion",
    "Ventilation &amp; Fan Installs": "Instalacion de Ventilacion",
    "Roof and exhaust fan installation and wiring for bathrooms, kitchens and attics that need better airflow.":
        "Instalacion y cableado de extractores de techo para banos, cocinas y aticos que necesitan mejor ventilacion.",
    "Panels &amp; Meters": "Paneles y Medidores",
    "Panel upgrades": "Actualizacion de paneles",
    "Meter bank service": "Servicio de bancos de medidores",
    "Breaker replacement": "Reemplazo de breakers",
    "Electrical inspections": "Inspecciones electricas",
    "Lighting": "Iluminacion",
    "Recessed lighting": "Luces empotradas",
    "Kitchen &amp; ceiling fixtures": "Lamparas de cocina y techo",
    "Outlet &amp; switch install": "Instalacion de tomas e interruptores",
    "Ceiling fan wiring": "Cableado de ventiladores de techo",
    "Wiring &amp; Install": "Cableado e Instalacion",
    "Wiring repairs": "Reparacion de cableado",
    "Exhaust &amp; roof fan install": "Instalacion de extractores de techo",
    "General electrical work": "Trabajo electrico general",
    "Free estimates": "Cotizaciones gratis",
    "Pricing depends on scope and materials. Call (305) 904-1066 for a free quote.":
        "El precio depende del alcance y los materiales. Llama al (305) 904-1066 para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Hallandale": "Lo que dicen los",
    "customers say": "clientes en Hallandale",
    "Read all 53 reviews on Google": "Lee las 53 resenas en Google",
    "Serving": "Sirviendo a",
    "Hours": "Horario",
    "Monday to Saturday, 7:00 AM to 7:00 PM. Closed Sunday.": "Lunes a sabado, de 7:00 AM a 7:00 PM. Cerrado los domingos.",
    "Reviews": "Resenas",
    "4.8 stars across 53 verified Google reviews.": "4.8 estrellas en 53 resenas verificadas de Google.",
    "One call fixes": "Una llamada arregla",
    "it all": "todo",
    "Call (305) 904-1066 for a free, honest quote on your panel upgrade, lighting, wiring or ventilation job. Monday to Saturday, 7 AM to 7 PM.":
        "Llama al (305) 904-1066 para una cotizacion gratis y honesta de tu trabajo de panel, iluminacion, cableado o ventilacion. Lunes a sabado, de 7 AM a 7 PM.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Licensed electrician serving Hallandale Beach and Hollywood, FL.": "Electricista con licencia en Hallandale Beach y Hollywood, FL.",
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
