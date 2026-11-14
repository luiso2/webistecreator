import re
import os
import colorsys

SLUG = "anthony-studios"
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
# 1. PROTEGER EL BADGE MERKTOP
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
# 2. PALETA: dorado (pureartistry) -> granate dramatico (Anthony Studios)
# ============================================================
_HEXES = ["#0c0905", "#0f0b07", "#100c05", "#171207", "#191307", "#1c1408", "#241c0e", "#6b5222",
          "#8a744a", "#96742c", "#9a7431", "#b8934a", "#bfa060", "#c9a04a", "#c9ab6b", "#d4a84b",
          "#e5c374", "#e8c476", "#e8cf96", "#e9c3ab", "#ecd9a8", "#f0dc9e", "#f0dcae", "#f5efe3",
          "#f8eed3", "#faf1dc", "#fbf6ea"]
_RGBAS = [(212, 168, 75), (232, 207, 150), (245, 239, 227), (80, 58, 18), (110, 85, 35),
          (122, 90, 30), (180, 140, 60), (54, 42, 38), (15, 11, 7), (232, 210, 160), (185, 138, 128)]

TARGET_HUE = 345 / 360.0
SAT_MUL = 0.95


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
# 3. Globales: sin Booksy, sin IG -> tel: + Google reviews
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+19046318167"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Anthony+Studios+Jacksonville+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=Jacksonville,+FL"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Anthony Studios · Portrait &amp; Event Photography in Jacksonville, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Anthony Studios, Jacksonville FL: quinceañera, maternity and event photography with dramatic, fine-art sets. 5.0 stars across 45 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Anthony Studios · Photography in Jacksonville, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Quinceañera, maternity and event photography. 5.0 on Google with 45 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-mansion-quince.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "PhotographyBusiness",
    "name": "Anthony Studios",
    "description": "Photography studio serving Jacksonville, FL: quinceañera, maternity and event photography with dramatic, fine-art sets and real locations.",
    "areaServed": "Jacksonville, FL",
    "telephone": "+1-904-631-8167",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "45", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "21:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "10:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Photography services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Quinceañera Photography" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Maternity Photography" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Event Photography" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Fine Art Portrait Sets" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN (default del esqueleto)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ============================================================
# 6. NAV
# ============================================================
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(209,78,111,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Anthony Studios" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(209,78,111,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Anthony <span class="text-[color:var(--accent-deep)]">Studios</span></span>')
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">AS</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Anthony Studios</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call to book" data-en="Call to book">Call to book</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call to book" data-en="Call to book">Call to book</a>')
print("NAV CTA done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Jacksonville, FL · Photography" data-en="Jacksonville, FL · Photography">Jacksonville, FL · Photography</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Every shoot, built like a scene." data-en="Every shoot, built like a scene.">Every shoot, built like a scene.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Quinceañera, maternity" data-en="Quinceañera, maternity">Quinceañera, maternity</span><br /><span data-es="and event photography, " data-en="and event photography, ">and event photography, </span><span class="text-shine" data-es="done dramatically" data-en="done dramatically">done dramatically</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Dramatic, fine-art sets for quinceañera, maternity and event photography across Jacksonville, from historic mansions to fire-spark night shoots. A full crew behind every frame, with a perfect 5.0 across 45 Google reviews." data-en="Dramatic, fine-art sets for quinceañera, maternity and event photography across Jacksonville, from historic mansions to fire-spark night shoots. A full crew behind every frame, with a perfect 5.0 across 45 Google reviews.">Dramatic, fine-art sets for quinceañera, maternity and event photography across Jacksonville, from historic mansions to fire-spark night shoots. A full crew behind every frame, with a perfect 5.0 across 45 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 45 reviews on Google" data-en="5.0 · 45 reviews on Google">5.0 · 45 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (904) 631-8167" data-en="Call (904) 631-8167">Call (904) 631-8167</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>',
    'data-es="Real sets" data-en="Real sets">Real sets</span>')
rep('data-es="Servicios claros" data-en="Clear services">Servicios claros</span>',
    'data-es="Full crew" data-en="Full crew">Full crew</span>')
rep('data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Direct contact" data-en="Direct contact">Direct contact</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-mansion-quince.jpg" alt="A quinceañera portrait at a historic Sarasota-style mansion, by Anthony Studios" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Available" data-en="Available">Available</p>
            <p class="font-display text-lg" data-es="Quinceañera Sets" data-en="Quinceañera Sets">Quinceañera Sets</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="45">45</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Quince <span class="text-shine">&amp;</span> Events</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Maternity · Portraits" data-en="Maternity · Portraits">Maternity · Portraits</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl" data-es="Dramatic Sets" data-en="Dramatic Sets">Dramatic Sets</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Fine art &amp; night shoots" data-en="Fine art &amp; night shoots">Fine art &amp; night shoots</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Jacksonville</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="FL · Por cita" data-en="FL · By appointment">FL · By appointment</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Quinceañera"),
    ("Loc Retwist", "Maternity"),
    ("Knotless Braids", "Event Photography"),
    ("K-Tip Extensions", "Fine Art Sets"),
    ("Keratin", "Night Shoots"),
    ("Orlando, FL", "Jacksonville, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ============================================================
# 10. LA EXPERIENCIA
# ============================================================
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/hero-mansion-quince.jpg" alt="A quinceañera portrait at a historic mansion, by Anthony Studios" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-behind-scenes.jpg" alt="Behind the scenes of an Anthony Studios celebration shoot" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="One crew," data-en="One crew,">One crew,</span><br /><span class="text-shine" data-es="building every scene" data-en="building every scene">building every scene</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Anthony Studios is a Jacksonville photography team built around dramatic, fine-art sets: quinceañera gowns against historic mansions, maternity portraits on the beach, and fire-spark night shoots for milestone events." data-en="Anthony Studios is a Jacksonville photography team built around dramatic, fine-art sets: quinceañera gowns against historic mansions, maternity portraits on the beach, and fire-spark night shoots for milestone events.">Anthony Studios is a Jacksonville photography team built around dramatic, fine-art sets: quinceañera gowns against historic mansions, maternity portraits on the beach, and fire-spark night shoots for milestone events.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="The result: a perfect 5.0 across 45 Google reviews, with clients praising the crew punctuality and the quality of the finished photos." data-en="The result: a perfect 5.0 across 45 Google reviews, with clients praising the crew punctuality and the quality of the finished photos.">The result: a perfect 5.0 across 45 Google reviews, with clients praising the crew punctuality and the quality of the finished photos.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="45">45</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Full crew" data-en="Full crew">Full crew</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="En cada sesión" data-en="On every shoot">On every shoot</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(209,78,111,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo.jpg" alt="Anthony Studios" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(209,78,111,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Anthony Studios · <span class="text-[color:var(--ink-40)]" data-es="Photography team" data-en="Photography team">Photography team</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Your shoot," data-en="Your shoot,">Your shoot,</span> <span class="text-shine" data-es="scene by scene" data-en="scene by scene">scene by scene</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call to book" data-en="Call to book">Call to book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text to check availability and talk through the vision for your quinceañera, maternity or event shoot." data-en="Call or text to check availability and talk through the vision for your quinceañera, maternity or event shoot.">Call or text to check availability and talk through the vision for your quinceañera, maternity or event shoot.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Set &amp; wardrobe" data-en="Set &amp; wardrobe">Set &amp; wardrobe</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Gown changes, props and the location, mansion, beach or studio, get planned around the look you want." data-en="Gown changes, props and the location, mansion, beach or studio, get planned around the look you want.">Gown changes, props and the location, mansion, beach or studio, get planned around the look you want.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The shoot" data-en="The shoot">The shoot</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A full crew runs lighting, direction and every gown change, whether it is a daylight garden set or a fire-spark night shoot." data-en="A full crew runs lighting, direction and every gown change, whether it is a daylight garden set or a fire-spark night shoot.">A full crew runs lighting, direction and every gown change, whether it is a daylight garden set or a fire-spark night shoot.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Delivery" data-en="Delivery">Delivery</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Your edited gallery goes out after the shoot, ready to share with family or print for the album." data-en="Your edited gallery goes out after the shoot, ready to share with family or print for the album.">Your edited gallery goes out after the shoot, ready to share with family or print for the album.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Shoots for" data-en="Shoots for">Shoots for</span> <span class="text-shine" data-es="every milestone" data-en="every milestone">every milestone</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every shoot is quoted around the set, gown changes and crew size, with a straight answer by phone." data-en="Every shoot is quoted around the set, gown changes and crew size, with a straight answer by phone.">Every shoot is quoted around the set, gown changes and crew size, with a straight answer by phone.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(209,78,111,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="House signature" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Quinceañera Photography" data-en="Quinceañera Photography">Quinceañera Photography</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Multiple gown changes against historic mansions, fountains and gardens around Jacksonville, directed by a full crew." data-en="Multiple gown changes against historic mansions, fountains and gardens around Jacksonville, directed by a full crew.">Multiple gown changes against historic mansions, fountains and gardens around Jacksonville, directed by a full crew.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Maternity" data-en="Maternity">Maternity</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Maternity Photography" data-en="Maternity Photography">Maternity Photography</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Flowing fabric and fine-art backdrops on the beach or in studio, with gentle direction for every stage." data-en="Flowing fabric and fine-art backdrops on the beach or in studio, with gentle direction for every stage.">Flowing fabric and fine-art backdrops on the beach or in studio, with gentle direction for every stage.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Events" data-en="Events">Events</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Event Photography" data-en="Event Photography">Event Photography</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Birthdays, celebrations and family milestones covered with the same attention as a quinceañera shoot." data-en="Birthdays, celebrations and family milestones covered with the same attention as a quinceañera shoot.">Birthdays, celebrations and family milestones covered with the same attention as a quinceañera shoot.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Signature look" data-en="Signature look">Signature look</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Fine Art Night Shoots" data-en="Fine Art Night Shoots">Fine Art Night Shoots</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Dramatic fire-spark and long-exposure sets for a quinceañera or celebration portrait that stands out." data-en="Dramatic fire-spark and long-exposure sets for a quinceañera or celebration portrait that stands out.">Dramatic fire-spark and long-exposure sets for a quinceañera or celebration portrait that stands out.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on location, gown changes and crew size. Call (904) 631-8167 for a free quote." data-en="Pricing depends on location, gown changes and crew size. Call (904) 631-8167 for a free quote.">Pricing depends on location, gown changes and crew size. Call (904) 631-8167 for a free quote.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA (5 tiles: 1 ancho + 4 cuadrados; 2 fotos maternidad expuestas se descartan)
# ============================================================
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="scenes" data-en="scenes">scenes</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (904) 631-8167
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Chispas de noche" data-en="Fire-spark night shoot">Fire-spark night shoot</span><img src="assets/gallery-fire-spin.jpg" alt="A dramatic fire-spark long-exposure quinceañera portrait by Anthony Studios" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Junto a la fuente" data-en="By the fountain">By the fountain</span><img src="assets/gallery-purple-fountain.jpg" alt="A quinceañera in a lavender gown beside a garden fountain at sunset" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Globos de fantasia" data-en="Fantasy balloon set">Fantasy balloon set</span><img src="assets/gallery-balloon-fantasy.jpg" alt="A creative hot air balloon fantasy portrait in a pink gown by Anthony Studios" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Caballo al atardecer" data-en="Horse at sunset">Horse at sunset</span><img src="assets/gallery-red-horse-sunset.jpg" alt="A quinceañera portrait with a horse at sunset by Anthony Studios" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Portal de hierro" data-en="Iron gateway">Iron gateway</span><img src="assets/gallery-pink-gate.jpg" alt="A quinceañera in a blush gown at an ornate iron gateway" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Jacksonville" data-en="What Jacksonville">What Jacksonville</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 45 reviews on Google" data-en="5.0 out of 5 · 45 reviews on Google">5.0 out of 5 · 45 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely love their work, very professional and polite, would book another session with them again without a doubt. Anthony's studio did such a great job on my recent maternity shoot, I'm just in love with every picture!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Xochil Rangel</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent photographers, very punctual, quality photos and very good prices."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Gabriel Santiago</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"If you are looking for an epic event for you or your family, Anthony Studios is the best. 100% recommended, very professional and the best prices in town."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Gabriel Carrillo</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 45 reviews on Google" data-en="Read all 45 reviews on Google">Read all 45 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION (sin direccion fija: area de servicio)
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Jacksonville, FL</span></h2>')
rep('''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(209,78,111,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Anthony Studios shoots on location across Jacksonville and the surrounding area, by appointment." data-en="Anthony Studios shoots on location across Jacksonville and the surrounding area, by appointment.">Anthony Studios shoots on location across Jacksonville and the surrounding area, by appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(209,78,111,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>''')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(209,78,111,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Friday 8 AM to 9:30 PM, Saturday and Sunday 10 AM to 5 PM." data-en="Monday to Friday 8 AM to 9:30 PM, Saturday and Sunday 10 AM to 5 PM.">Monday to Friday 8 AM to 9:30 PM, Saturday and Sunday 10 AM to 5 PM.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(209,78,111,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (904) 631-8167" data-en="Call (904) 631-8167">Call (904) 631-8167</a>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(209,78,111,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Read what Jacksonville families say about their sessions on Google." data-en="Read what Jacksonville families say about their sessions on Google.">Read what Jacksonville families say about their sessions on Google.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(209,78,111,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Anthony Studios, Jacksonville FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Every shoot, built like a scene." data-en="Every shoot, built like a scene.">Every shoot, built like a scene.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your next" data-en="Your next">Your next</span> <span class="text-shine" data-es="shoot awaits" data-en="shoot awaits">shoot awaits</span></h2>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Call or text today to check availability for your quinceañera, maternity or event photography." data-en="Call or text today to check availability for your quinceañera, maternity or event photography.">Call or text today to check availability for your quinceañera, maternity or event photography.</p>')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + NEW_TEL + '" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (904) 631-8167" data-en="Call (904) 631-8167">Call (904) 631-8167</a>')
rep('<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Google Reviews" data-en="Google Reviews">Google Reviews</a>')
print("CTA done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Anthony Studios</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(230,152,172,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/logo.jpg" alt="Anthony Studios" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(230,152,172,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Anthony Studios</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Photography studio serving Jacksonville, FL. By appointment only." data-en="Photography studio serving Jacksonville, FL. By appointment only.">Photography studio serving Jacksonville, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p data-es="Sirviendo Jacksonville, FL" data-en="Serving Jacksonville, FL">Serving Jacksonville, FL</p>')
rep('<p><a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="hover:text-[#e7adbb]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + NEW_TEL + '" class="hover:text-[#e7adbb]" data-es="Call (904) 631-8167" data-en="Call (904) 631-8167">Call (904) 631-8167</a></p>')
rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n        <p><a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="hover:text-[#e7adbb]">Instagram · ' + NEW_REVIEWS_LABEL + '</a></p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Opiniones" data-en="Reviews">Reviews</p>\n        <p><a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="hover:text-[#e7adbb]">Google Reviews · 5.0 (45)</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Anthony Studios.</p>')
print("FOOTER done")

# ============================================================
# 18. BOTON FLOTANTE
# ============================================================
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1b090d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>
  </a>''',
    '''<a href="''' + NEW_TEL + '''" class="book-float" aria-label="Call Anthony Studios">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1b090d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>
  </a>''')
print("BOOK-FLOAT done")

os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", encoding="utf-8") as f:
    f.write(h)
print("WROTE", DST, len(h), "bytes")
