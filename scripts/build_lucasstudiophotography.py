import re
import os
import colorsys
import shutil

SLUG = "lucas-studio-photography"
SRC = "templates/light-v2/index.html"
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
# 2. PALETA: plum-pink (lashbloom) -> azul indigo real (Lucas Studio Photography)
#    hue-shift via colorsys, saturacion similar, manteniendo luminosidad real
# ============================================================
_HEXES = ["#1c0f16", "#1f0f18", "#2a1722", "#33222c", "#5c2140", "#5f2c48", "#7d3457", "#8a5573",
          "#a04a72", "#b25a85", "#c47a9c", "#c9789f", "#d3a2bc", "#d9a8c2", "#dc9dbe", "#e5c1d4",
          "#efd0e0", "#f0bed7", "#f2cfe0", "#f2d5e3", "#f3e0ea", "#f6f1ea", "#f8dfeb", "#faf2f6",
          "#fbeff5", "#fbf3f8"]
_RGBAS = [(160, 74, 114), (51, 34, 44), (240, 190, 215), (70, 25, 50), (250, 242, 246),
          (125, 52, 87), (253, 246, 250), (233, 205, 186), (185, 138, 128), (40, 16, 30)]

TARGET_HUE = 232 / 360.0
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
# 3. Globales: sin Booksy, sin IG -> tel: + Google reviews
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+19042002778"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Lucas+Studio+Photography+Jacksonville+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "2032 Caljon Rd, Jacksonville, FL 32207"
NEW_MAPS = "https://www.google.com/maps?q=2032+Caljon+Rd,+Jacksonville,+FL+32207"

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Lucas Studio Photography · Quinceañera &amp; Portrait Studio in Jacksonville, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Lucas Studio Photography, Jacksonville FL: quinceañera, maternity and bridal portraits shot on real locations around the city. 5.0 stars across 29 Google reviews. Call for availability." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Lucas Studio Photography · Portrait Studio in Jacksonville, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Quinceañera, maternity and bridal portraits. 5.0 on Google with 29 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-quince.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "PhotographyBusiness",
    "name": "Lucas Studio Photography",
    "description": "Portrait photography studio in Jacksonville, FL: quinceañera, maternity and bridal portrait sessions shot on real locations, with custom prints and albums.",
    "address": { "@type": "PostalAddress", "streetAddress": "2032 Caljon Rd", "addressLocality": "Jacksonville", "addressRegion": "FL", "postalCode": "32207", "addressCountry": "US" },
    "telephone": "+1-904-200-2778",
    "areaServed": "Jacksonville, FL",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "29", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Portrait photography services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Quinceañera Portrait Sessions" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Maternity Portraits" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bridal &amp; Event Portraits" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Prints &amp; Custom Albums" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]

print("HEAD done")

# ============================================================
# 5. Idioma: negocio EN -> se queda en EN (default del esqueleto)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ============================================================
# 6. NAV
# ============================================================
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,84,162,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Lucas Studio Photography" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,84,162,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lucas <span class="text-[color:var(--accent-deep)]">Studio</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LS</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Lucas Studio</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call to book" data-en="Call to book">Call to book</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call to book" data-en="Call to book">Call to book</a>')
print("NAV CTA done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Jacksonville, FL · Portrait Studio" data-en="Jacksonville, FL · Portrait Studio">Jacksonville, FL · Portrait Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Every milestone, framed like art." data-en="Every milestone, framed like art.">Every milestone, framed like art.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Quinceañera, maternity" data-en="Quinceañera, maternity">Quinceañera, maternity</span><br /><span data-es="and bridal portraits, made " data-en="and bridal portraits, made ">and bridal portraits, made </span><span class="text-shine" data-es="cinematic" data-en="cinematic">cinematic</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Cinematic quinceañera, maternity and bridal sessions shot on real Jacksonville locations, from garden fountains to grand staircases, with a full crew lighting and directing every scene." data-en="Cinematic quinceañera, maternity and bridal sessions shot on real Jacksonville locations, from garden fountains to grand staircases, with a full crew lighting and directing every scene.">Cinematic quinceañera, maternity and bridal sessions shot on real Jacksonville locations, from garden fountains to grand staircases, with a full crew lighting and directing every scene.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 29 reviews on Google" data-en="5.0 · 29 reviews on Google">5.0 · 29 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (904) 200-2778" data-en="Call (904) 200-2778">Call (904) 200-2778</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-quince.jpg" alt="A quinceañera in a champagne ball gown at a historic Jacksonville mansion, by Lucas Studio Photography" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="By appointment" data-en="By appointment">By appointment</p>
            <p class="font-display text-lg">Quinceañera Session</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Call for availability" data-en="Call for availability">Call for availability</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="29">29</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Quince <span class="text-shine">&amp;</span> Bridal</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Maternity · Portraits" data-en="Maternity · Portraits">Maternity · Portraits</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl" data-es="Real Locations" data-en="Real Locations">Real Locations</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Mansions · Gardens" data-en="Mansions · Gardens">Mansions · Gardens</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Jacksonville</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2032 Caljon Rd</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra aparece x4)
# ============================================================
MARQUEE_WORDS = [
    ("Classic Set", "Quinceañera"),
    ("Hybrid Set", "Maternity"),
    ("Volume Set", "Bridal Portraits"),
    ("Mega Volume", "Fine Art Prints"),
    ("Bottom Lashes", "On-Location Shoots"),
    ("West Palm Beach, FL", "Jacksonville, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ============================================================
# 10. LA EXPERIENCIA
# ============================================================
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-session.jpg" alt="The Lucas Studio Photography crew lighting a quinceañera session on location" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-albums.jpg" alt="Finished portrait prints and a custom album by Lucas Studio Photography" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One team," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="crafting every scene" data-en="crafting every scene">crafting every scene</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Lucas Studio Photography is a Jacksonville portrait studio built around cinematic sets: real mansions, gardens and fountains around the city, with a full crew lighting and directing every quinceañera, maternity and bridal session." data-en="Lucas Studio Photography is a Jacksonville portrait studio built around cinematic sets: real mansions, gardens and fountains around the city, with a full crew lighting and directing every quinceañera, maternity and bridal session.">Lucas Studio Photography is a Jacksonville portrait studio built around cinematic sets: real mansions, gardens and fountains around the city, with a full crew lighting and directing every quinceañera, maternity and bridal session.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a perfect 5.0 across 29 Google reviews, with every family going home with finished prints and a custom album of the day." data-en="The result: a perfect 5.0 across 29 Google reviews, with every family going home with finished prints and a custom album of the day.">The result: a perfect 5.0 across 29 Google reviews, with every family going home with finished prints and a custom album of the day.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="29">29</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Full crew" data-en="Full crew">Full crew</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="En cada sesión" data-en="On every shoot">On every shoot</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,84,162,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Lucas Studio Photography" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(72,84,162,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Lucas Studio · <span class="text-[color:var(--ink-40)]" data-es="Portrait &amp; quinceañera studio" data-en="Portrait &amp; quinceañera studio">Portrait &amp; quinceañera studio</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your session," data-en="Your session,">Your session,</span> <span class="text-shine" data-es="scene by scene" data-en="scene by scene">scene by scene</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or text" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Reach out by phone to check availability and talk through your vision for the shoot." data-en="Reach out by phone to check availability and talk through your vision for the shoot.">Reach out by phone to check availability and talk through your vision for the shoot.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Location scout" data-en="Location scout">Location scout</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Pick from the team's real Jacksonville locations, gardens and mansions, or suggest a spot of your own." data-en="Pick from the team's real Jacksonville locations, gardens and mansions, or suggest a spot of your own.">Pick from the team's real Jacksonville locations, gardens and mansions, or suggest a spot of your own.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The session" data-en="The session">The session</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A full crew directs hair, poses and lighting through every gown change, with gear built for cinematic results." data-en="A full crew directs hair, poses and lighting through every gown change, with gear built for cinematic results.">A full crew directs hair, poses and lighting through every gown change, with gear built for cinematic results.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Prints &amp; delivery" data-en="Prints &amp; delivery">Prints &amp; delivery</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You leave with a digital gallery to share, plus the option of a custom album or prints of your favorites." data-en="You leave with a digital gallery to share, plus the option of a custom album or prints of your favorites.">You leave with a digital gallery to share, plus the option of a custom album or prints of your favorites.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Sessions for" data-en="Sessions for">Sessions for</span> <span class="text-shine" data-es="every milestone" data-en="every milestone">every milestone</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every session is quoted around your gown changes, crew size and location, with a straight answer by phone." data-en="Every session is quoted around your gown changes, crew size and location, with a straight answer by phone.">Every session is quoted around your gown changes, crew size and location, with a straight answer by phone.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="On-location" data-en="On-location">On-location</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Quinceañera Sessions" data-en="Quinceañera Sessions">Quinceañera Sessions</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Multiple gown changes across real Jacksonville locations, from grand staircases to garden fountains, with a full crew for hair, lighting and direction." data-en="Multiple gown changes across real Jacksonville locations, from grand staircases to garden fountains, with a full crew for hair, lighting and direction.">Multiple gown changes across real Jacksonville locations, from grand staircases to garden fountains, with a full crew for hair, lighting and direction.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(72,84,162,0.4); box-shadow: 0 18px 50px rgba(34,36,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Maternity Portraits" data-en="Maternity Portraits">Maternity Portraits</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Flowing gowns, fine art backdrops and gentle direction built around how far along you are, indoors or on location." data-en="Flowing gowns, fine art backdrops and gentle direction built around how far along you are, indoors or on location.">Flowing gowns, fine art backdrops and gentle direction built around how far along you are, indoors or on location.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Bridal &amp; events" data-en="Bridal &amp; events">Bridal &amp; events</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Bridal &amp; Event Portraits" data-en="Bridal &amp; Event Portraits">Bridal &amp; Event Portraits</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Bridal portraits, engagement sessions and event coverage with the same cinematic lighting as the quinceañera sets." data-en="Bridal portraits, engagement sessions and event coverage with the same cinematic lighting as the quinceañera sets.">Bridal portraits, engagement sessions and event coverage with the same cinematic lighting as the quinceañera sets.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keepsakes" data-en="Keepsakes">Keepsakes</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Prints &amp; Custom Albums" data-en="Prints &amp; Custom Albums">Prints &amp; Custom Albums</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Finished prints and a hand-built album of your favorites from the session, on top of your full digital gallery." data-en="Finished prints and a hand-built album of your favorites from the session, on top of your full digital gallery.">Finished prints and a hand-built album of your favorites from the session, on top of your full digital gallery.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on location, gown changes and crew size. Call (904) 200-2778 for a free quote." data-en="Pricing depends on location, gown changes and crew size. Call (904) 200-2778 for a free quote.">Pricing depends on location, gown changes and crew size. Call (904) 200-2778 for a free quote.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="sessions" data-en="sessions">sessions</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (904) 200-2778
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Atardecer junto a la fuente" data-en="Garden fountain at sunset">Garden fountain at sunset</span><img src="assets/gallery-garden-sunset.jpg" alt="A quinceañera portrait beside a garden fountain at sunset, by Lucas Studio Photography" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Velo de novia" data-en="Bridal veil">Bridal veil</span><img src="assets/gallery-bride-veil.jpg" alt="A bride with her veil and gown by Lucas Studio Photography" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Vestido borgoña" data-en="Burgundy gown">Burgundy gown</span><img src="assets/gallery-burgundy-doorway.jpg" alt="A quinceañera in a burgundy gown at a stone doorway" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Azul real" data-en="Royal blue">Royal blue</span><img src="assets/gallery-royal-blue.jpg" alt="A quinceañera in a royal blue gown inside a grand living room" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Maternidad bajo el árbol" data-en="Maternity under the oak">Maternity under the oak</span><img src="assets/gallery-maternity-tree.jpg" alt="A maternity portrait under an oak tree by Lucas Studio Photography" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Junto al caballo" data-en="Alongside the horse">Alongside the horse</span><img src="assets/gallery-blue-horse.jpg" alt="A quinceañera in a blue gown beside a black horse at an iron gate" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES (solo 2 reseñas reales encontradas: nunca se rellena con una 3a)
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Jacksonville" data-en="What Jacksonville">What Jacksonville</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 29 reviews on Google" data-en="5.0 out of 5 · 29 reviews on Google">5.0 out of 5 · 29 reviews on Google</span>')
rep('<div class="grid sm:grid-cols-3 gap-5 items-stretch">',
    '<div class="grid sm:grid-cols-2 gap-5 items-stretch max-w-3xl mx-auto">')
rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Best photographer ever. He captured every special moment of our event. I highly recommend him for your next event."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Marian Romero</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Beautiful pictures. The professionalism and love with which they are made is evident in each one of them. Simply lovely."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">ColoredBeach 678</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 29 reviews on Google" data-en="Read all 29 reviews on Google">Read all 29 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION (direccion real; la 3ra caja (sin IG) se vuelve horario real)
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Jacksonville</span></h2>')
rep('''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,84,162,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + NEW_ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,84,162,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>''')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,84,162,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Appointments" data-en="Appointments">Appointments</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="By appointment: call or text to check availability for your session." data-en="By appointment: call or text to check availability for your session.">By appointment: call or text to check availability for your session.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,84,162,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (904) 200-2778" data-en="Call (904) 200-2778">Call (904) 200-2778</a>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,84,162,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mon-Fri y sábado de 8 AM a 9 PM, domingo de 10 AM a 5 PM." data-en="Mon-Sat 8 AM to 9 PM, Sunday 10 AM to 5 PM.">Mon-Sat 8 AM to 9 PM, Sunday 10 AM to 5 PM.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(72,84,162,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Lucas Studio Photography, 2032 Caljon Rd, Jacksonville FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Every milestone, framed like art." data-en="Every milestone, framed like art.">Every milestone, framed like art.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your next" data-en="Your next">Your next</span> <span class="text-shine" data-es="session awaits" data-en="session awaits">session awaits</span></h2>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Call or text today to check availability for your quinceañera, maternity or bridal portraits." data-en="Call or text today to check availability for your quinceañera, maternity or bridal portraits.">Call or text today to check availability for your quinceañera, maternity or bridal portraits.</p>')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + NEW_TEL + '" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (904) 200-2778" data-en="Call (904) 200-2778">Call (904) 200-2778</a>')
rep('<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Google Reviews" data-en="Google Reviews">Google Reviews</a>')
print("CTA done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Lucas Studio</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(189,196,241,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<img src="assets/logo.jpg" alt="Lucas Studio Photography" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(189,196,241,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lucas Studio</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Quinceañera, maternity and bridal portrait studio in Jacksonville, FL. By appointment only." data-en="Quinceañera, maternity and bridal portrait studio in Jacksonville, FL. By appointment only.">Quinceañera, maternity and bridal portrait studio in Jacksonville, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>' + NEW_ADDR + '</p>')
rep('<p><a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="hover:text-[#bdc4f1]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + NEW_TEL + '" class="hover:text-[#bdc4f1]" data-es="Call (904) 200-2778" data-en="Call (904) 200-2778">Call (904) 200-2778</a></p>')
rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n        <p><a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="hover:text-[#bdc4f1]">Instagram · ' + NEW_REVIEWS_LABEL + '</a></p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Opiniones" data-en="Reviews">Reviews</p>\n        <p><a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="hover:text-[#bdc4f1]">Google Reviews · 5.0 (29)</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lucas Studio Photography.</p>')
print("FOOTER done")

# ============================================================
# 18. BOTON FLOTANTE
# ============================================================
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f2f3fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>''',
    '''<a href="''' + NEW_TEL + '''" class="book-float" aria-label="Call Lucas Studio Photography">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f8f8fd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
print("BOOK-FLOAT done")

os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", encoding="utf-8") as f:
    f.write(h)
print("WROTE", DST, len(h), "bytes")
