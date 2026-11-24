import re
import os
import colorsys

SLUG = "heatoffthestreetcatering"
SRC = "templates/dark-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()

# ============================================================
# 0. Funciones de shift de color (ver scripts/build_cekcaterers.py para el
#    patron original). TARGET_HUE = ember/fire rojo-naranja, hue ~16 grados,
#    distinto de los ya usados (caramelo 33, coral 345, esmeralda 155,
#    teal 180, violeta 255, wine/burgundy ~352, azul electrico rtdiagnostic
#    ~217, gold original ~40).
# ============================================================
TARGET_HUE = 16 / 360.0
SAT_MUL = 1.05
SKIP_RGB = {"255,255,255", "0,0,0"}


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


def S(text):
    def _hexsub(mm):
        hx = mm.group(0)
        return hx if hx.lower() == '#ffffff' else _shift_hex(hx)
    text = re.sub(r'#[0-9a-fA-F]{6}', _hexsub, text)

    def _rgbasub(mm):
        trip = mm.group(1)
        if trip in SKIP_RGB:
            return mm.group(0)
        r, g, b = (int(x) for x in trip.split(','))
        r2, g2, b2 = _shift_rgb((r, g, b))
        return f'rgba({r2},{g2},{b2},{mm.group(2)})'
    text = re.sub(r'rgba\((\d+,\d+,\d+),([0-9.]+)\)', _rgbasub, text)
    return text


def rep(a, b, n=1):
    global h
    a = S(a)
    b = S(b)
    assert a in h, "NO ANCHOR: " + a[:200]
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None, _raw=False):
    global h
    if not _raw:
        a = S(a)
        b = S(b)
    c = h.count(a)
    assert c > 0, "NO ANCHOR: " + a[:200]
    if expect is not None:
        assert c == expect, f"count {c} != expected {expect} for " + a[:80]
    h = h.replace(a, b)


# ============================================================
# 1. PROTEGER EL BADGE MERKTOP (queda dorado siempre)
# ============================================================
m_css = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m_css
badge_css = m_css.group(0)
h = h.replace(badge_css, '@@BADGE_CSS@@', 1)

m_html = re.search(r'<a href="https://merktop\.com".*?</a>', h, flags=re.S)
assert m_html
badge_html = m_html.group(0)
h = h.replace(badge_html, '@@BADGE_HTML@@', 1)

# El unico #D4A84B (mayusculas) del esqueleto vive dentro de .merktop-dot, que ya
# quedo protegido como parte de badge_css (el regex del badge llega hasta
# @keyframes mkPulse inclusive), asi que no necesita proteccion aparte.
assert '#D4A84B' not in h

# ============================================================
# 2. PALETA: gold original (#d4a84b/#b8934a) -> ember rojo-naranja
# ============================================================
hex_candidates = sorted(set(re.findall(r'#[0-9a-fA-F]{6}', h)))
hex_candidates = [c for c in hex_candidates if c.lower() != '#ffffff']
PALETTE = [(hx, _shift_hex(hx)) for hx in hex_candidates]
for old, new in PALETTE:
    rep_all(old, new, _raw=True)

rgba_triples = sorted(set(re.findall(r'rgba\((\d+,\d+,\d+)', h)))
RGBA_FAMILIES = []
for trip in rgba_triples:
    if trip in SKIP_RGB:
        continue
    r, g, b = (int(x) for x in trip.split(','))
    RGBA_FAMILIES.append(((r, g, b), _shift_rgb((r, g, b))))
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

h = h.replace('@@BADGE_CSS@@', badge_css, 1)
h = h.replace('@@BADGE_HTML@@', badge_html, 1)
print("PALETTE done,", len(PALETTE), "hex,", len(RGBA_FAMILIES), "rgba families")

# ============================================================
# 3. GLOBALES: sin booking platform ni redes sociales -> tel: real +
#    link de reseñas de Google (la ficha real de Maps)
# ============================================================
NEW_TEL = "tel:+15613458345"
NEW_REVIEWS_URL = "https://www.google.com/maps/place/Heat+off+the+Street+Catering/data=!4m7!3m6!1s0x8aa7c3f70133a573:0xa1a46960ce520e95!8m2!3d28.1624604!4d-81.6153504!16s%2Fg%2F11rnxy__dr!19sChIJc6UzAffDp4oRlQ5SzmBppKE"
NEW_REVIEWS_LABEL = "Google Reviews"
NEW_MAPS = "https://www.google.com/maps?q=West+Palm+Beach,+FL"

OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
rep_all(OLD_BOOK, NEW_TEL, expect=13)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
rep_all(OLD_IG_URL, NEW_REVIEWS_URL, expect=6)

rep_all("@pure.artistrysk", NEW_REVIEWS_LABEL, expect=4)

# Icono: las 3 svg de Instagram (rect+circulo+punto) -> estrella (reseñas reales)
IG_ICON_INNER = '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>'
STAR_ICON_INNER = '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
rep_all(IG_ICON_INNER, STAR_ICON_INNER, expect=3)
print("GLOBALS done")

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Heat off the Street Catering · Catering in Palm Beach County, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Heat off the Street Catering, Palm Beach County FL: chef-led catering for office parties, weddings and private functions. Plated dinners, brunch spreads and passed bites. 5.0 with 17 reviews on Google." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Heat off the Street Catering · Catering in Palm Beach County, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Chef-led catering for parties, weddings and events. 5.0 on Google, 17 reviews. Call for a quote." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-lamb-chops.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-lamb-chops.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FoodEstablishment",
    "name": "Heat off the Street Catering",
    "description": "Chef-led mobile catering company serving Palm Beach County, FL: office parties, weddings and private functions, with plated dinners, brunch spreads and passed bites.",
    "areaServed": "Palm Beach County, FL",
    "telephone": "+1-561-345-8345",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "17", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Catering services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Office Party & Function Catering" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Wedding & Private Event Catering" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Brunch & Passed Hors d'Oeuvres" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plated Entrees & Dinners" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN default (reseñas y negocio en ingles, Palm Beach County FL)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ============================================================
# 6. PRELOADER + NAV
# ============================================================
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">HS</span>\n    <span class="pre-word">Heat off the Street</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    '<img src="assets/hero-lamb-chops.jpg" alt="Heat off the Street Catering" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Heat off the <span class="text-[color:var(--accent-deep)]">Street</span></span>')
rep('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n          <span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Palm Beach County, FL · Catering" data-en="Palm Beach County, FL · Catering">Palm Beach County, FL · Catering</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Real food, cooked with heart." data-en="Real food, cooked with heart.">Real food, cooked with heart.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Chef-led catering that" data-en="Chef-led catering that">Chef-led catering that</span><br /><span data-es="brings real " data-en="brings real ">brings real </span><span class="text-shine" data-es="heat" data-en="heat">heat</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Heat off the Street Catering is a mobile, chef-led catering service run by Chef Patrick across Palm Beach County: plated dinners, brunch spreads, passed bites and full event service for office parties, weddings and private functions, with a perfect 5.0 rating across 17 Google reviews." data-en="Heat off the Street Catering is a mobile, chef-led catering service run by Chef Patrick across Palm Beach County: plated dinners, brunch spreads, passed bites and full event service for office parties, weddings and private functions, with a perfect 5.0 rating across 17 Google reviews.">Heat off the Street Catering is a mobile, chef-led catering service run by Chef Patrick across Palm Beach County: plated dinners, brunch spreads, passed bites and full event service for office parties, weddings and private functions, with a perfect 5.0 rating across 17 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 17 reviews on Google" data-en="5.0 · 17 reviews on Google">5.0 · 17 reviews on Google</span>')
rep('''<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''',
    '''<span data-es="Call (561) 345-8345" data-en="Call (561) 345-8345">Call (561) 345-8345</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''')
rep('<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + STAR_ICON_INNER + '</svg>\n            ' + NEW_REVIEWS_LABEL + '\n          </a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + STAR_ICON_INNER + '</svg>\n            ' + NEW_REVIEWS_LABEL + '\n          </a>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-lamb-chops.jpg" alt="Grilled lamb chops plated with chimichurri, catered by Heat off the Street Catering" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Availability" data-en="Availability">Availability</p>
            <p class="font-display text-lg">By Appointment</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="17">17</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Weddings <span class="text-shine">&amp;</span> Parties</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Private chef, full service" data-en="Private chef, full service">Private chef, full service</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Plated <span class="text-shine">&amp;</span> Brunch</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Dinners · Brunch · Bites" data-en="Dinners · Brunch · Bites">Dinners · Brunch · Bites</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Palm Beach County</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Mobile · By appointment" data-en="Mobile · By appointment">Mobile · By appointment</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Plated Dinners"),
    ("Loc Retwist", "Brunch Catering"),
    ("Knotless Braids", "Passed Bites"),
    ("K-Tip Extensions", "Private Chef"),
    ("Keratin", "Full Event Service"),
    ("Orlando, FL", "Palm Beach County, FL"),
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
    '''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/about-fish-tacos.jpg" alt="Blackened fish tacos with chipotle crema catered by Heat off the Street Catering" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/about-grilled-chicken.jpg" alt="Grilled chicken breast plated with carrots and broccoli by Heat off the Street Catering" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="One chef," data-en="One chef,">One chef,</span><br /><span class="text-shine" data-es="a perfect record" data-en="a perfect record">a perfect record</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Heat off the Street Catering is led by Chef Patrick, who reviewers call out by name for office parties, weddings and private functions across Palm Beach County. The photos on this page come straight from real plated events: brunch spreads, passed appetizer spoons, salads, tacos, grilled entrees and fine-dining style plates." data-en="Heat off the Street Catering is led by Chef Patrick, who reviewers call out by name for office parties, weddings and private functions across Palm Beach County. The photos on this page come straight from real plated events: brunch spreads, passed appetizer spoons, salads, tacos, grilled entrees and fine-dining style plates.">Heat off the Street Catering is led by Chef Patrick, who reviewers call out by name for office parties, weddings and private functions across Palm Beach County. The photos on this page come straight from real plated events: brunch spreads, passed appetizer spoons, salads, tacos, grilled entrees and fine-dining style plates.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="The result is a perfect 5.0 rating across 17 Google reviews, with guests calling out the seasoning, the presentation and how fast and reasonably priced the service is." data-en="The result is a perfect 5.0 rating across 17 Google reviews, with guests calling out the seasoning, the presentation and how fast and reasonably priced the service is.">The result is a perfect 5.0 rating across 17 Google reviews, with guests calling out the seasoning, the presentation and how fast and reasonably priced the service is.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="17">17</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Chef Pat</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Lead chef" data-en="Lead chef">Lead chef</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/hero-lamb-chops.jpg" alt="Heat off the Street Catering" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Heat off the Street Catering · <span class="text-[color:var(--ink-40)]" data-es="Palm Beach County, FL" data-en="Palm Beach County, FL">Palm Beach County, FL</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="From quote to cleanup" data-en="From quote to cleanup">From quote to cleanup</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Planning your event," data-en="Planning your event,">Planning your event,</span> <span class="text-shine" data-es="step by step" data-en="step by step">step by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Tell us the date" data-en="Tell us the date">Tell us the date</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (561) 345-8345 with your event date, headcount and the vibe you want, and Chef Patrick scopes the menu from there." data-en="Call (561) 345-8345 with your event date, headcount and the vibe you want, and Chef Patrick scopes the menu from there.">Call (561) 345-8345 with your event date, headcount and the vibe you want, and Chef Patrick scopes the menu from there.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Menu planning" data-en="Menu planning">Menu planning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Chef Patrick walks through plated, brunch, passed bites and stations so you land on a menu that fits your event and budget." data-en="Chef Patrick walks through plated, brunch, passed bites and stations so you land on a menu that fits your event and budget.">Chef Patrick walks through plated, brunch, passed bites and stations so you land on a menu that fits your event and budget.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Event day" data-en="Event day">Event day</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The team arrives ready to cook, plate and serve, so the food comes out fresh, hot and seasoned the way the reviews describe." data-en="The team arrives ready to cook, plate and serve, so the food comes out fresh, hot and seasoned the way the reviews describe.">The team arrives ready to cook, plate and serve, so the food comes out fresh, hot and seasoned the way the reviews describe.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Service &amp; cleanup" data-en="Service &amp; cleanup">Service &amp; cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Heat off the Street handles service through the last course and clears out when it is done, so you just enjoy the party." data-en="Heat off the Street handles service through the last course and clears out when it is done, so you just enjoy the party.">Heat off the Street handles service through the last course and clears out when it is done, so you just enjoy the party.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS (variante adaptada: sin precios, "se cotiza")
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Catering built around" data-en="Catering built around">Catering built around</span> <span class="text-shine" data-es="your event" data-en="your event">your event</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every event is different, so every menu is quoted to match it. Call with your date and guest count." data-en="Every event is different, so every menu is quoted to match it. Call with your date and guest count.">Every event is different, so every menu is quoted to match it. Call with your date and guest count.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Reviewer favorite" data-en="Reviewer favorite">Reviewer favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Office Parties &amp; Functions" data-en="Office Parties &amp; Functions">Office Parties &amp; Functions</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service catering for office parties and private functions, the kind of event reviewers say Chef Patrick turned into a huge success." data-en="Full-service catering for office parties and private functions, the kind of event reviewers say Chef Patrick turned into a huge success.">Full-service catering for office parties and private functions, the kind of event reviewers say Chef Patrick turned into a huge success.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Weddings &amp; Private Events" data-en="Weddings &amp; Private Events">Weddings &amp; Private Events</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Plated dinners and full event service for weddings and celebrations, with the seasoning and presentation reviewers call out by name." data-en="Plated dinners and full event service for weddings and celebrations, with the seasoning and presentation reviewers call out by name.">Plated dinners and full event service for weddings and celebrations, with the seasoning and presentation reviewers call out by name.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Morning spreads" data-en="Morning spreads">Morning spreads</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Brunch &amp; Passed Bites" data-en="Brunch &amp; Passed Bites">Brunch &amp; Passed Bites</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Brunch spreads, waffles, breakfast sandwiches and passed hors d'oeuvre spoons, plated and ready to serve." data-en="Brunch spreads, waffles, breakfast sandwiches and passed hors d'oeuvre spoons, plated and ready to serve.">Brunch spreads, waffles, breakfast sandwiches and passed hors d'oeuvre spoons, plated and ready to serve.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Seated service" data-en="Seated service">Seated service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Plated Entrees &amp; Dinners" data-en="Plated Entrees &amp; Dinners">Plated Entrees &amp; Dinners</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Grilled chicken, blackened fish, tacos and lamb chop plates, seasoned and finished the way the photos on this page show." data-en="Grilled chicken, blackened fish, tacos and lamb chop plates, seasoned and finished the way the photos on this page show.">Grilled chicken, blackened fish, tacos and lamb chop plates, seasoned and finished the way the photos on this page show.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Service Styles" data-en="Service Styles">Service Styles</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Plated service" data-en="Plated service">Plated service</li>
            <li class="flex items-center gap-2" data-es="Passed bites" data-en="Passed bites">Passed bites</li>
            <li class="flex items-center gap-2" data-es="Brunch spreads" data-en="Brunch spreads">Brunch spreads</li>
            <li class="flex items-center gap-2" data-es="Family style" data-en="Family style">Family style</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Event Types" data-en="Event Types">Event Types</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Office parties" data-en="Office parties">Office parties</li>
            <li class="flex items-center gap-2" data-es="Weddings" data-en="Weddings">Weddings</li>
            <li class="flex items-center gap-2" data-es="Private functions" data-en="Private functions">Private functions</li>
            <li class="flex items-center gap-2" data-es="Celebrations" data-en="Celebrations">Celebrations</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Always Included" data-en="Always Included">Always Included</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Fresh, seasoned cooking" data-en="Fresh, seasoned cooking">Fresh, seasoned cooking</li>
            <li class="flex items-center gap-2" data-es="On-time service" data-en="On-time service">On-time service</li>
            <li class="flex items-center gap-2" data-es="Direct chef communication" data-en="Direct chef communication">Direct chef communication</li>
            <li class="flex items-center gap-2" data-es="Quote for your headcount" data-en="Quote for your headcount">Quote for your headcount</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + S(NEW_SERVICES_GRID) + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Every menu is quoted to match your event, guest count and venue. Call (561) 345-8345 to start planning." data-en="Every menu is quoted to match your event, guest count and venue. Call (561) 345-8345 to start planning.">Every menu is quoted to match your event, guest count and venue. Call (561) 345-8345 to start planning.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="events" data-en="events">events</span>')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Pescado ennegrecido sobre ensalada, con rosa de remolacha" data-en="Blackened fish over salad, with a beet rose garnish">Blackened fish over salad, with a beet rose garnish</span><img src="assets/gallery-blackened-fish-salad.jpg" alt="A blackened fish filet plated over a fresh salad with a beet rose garnish, catered by Heat off the Street Catering" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cucharas de avena con banana flambeada" data-en="Brulee banana oatmeal spoons">Brulee banana oatmeal spoons</span><img src="assets/gallery-brulee-spoons.jpg" alt="Rows of passed hors d'oeuvre spoons with brulee banana, berries and oatmeal, catered by Heat off the Street Catering" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Sandwich de desayuno" data-en="Breakfast sandwich">Breakfast sandwich</span><img src="assets/gallery-breakfast-sandwich.jpg" alt="A brunch sandwich with egg, mushrooms, caramelized onion and cheddar, catered by Heat off the Street Catering" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Waffles con fruta fresca" data-en="Waffles with fresh fruit">Waffles with fresh fruit</span><img src="assets/gallery-waffles-berries.jpg" alt="Brunch waffles topped with whipped cream, bananas and strawberries, catered by Heat off the Street Catering" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + S(NEW_GALLERY_GRID) + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Palm Beach County" data-en="What Palm Beach County">What Palm Beach County</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 17 reviews on Google" data-en="5.0 out of 5 · 17 reviews on Google">5.0 out of 5 · 17 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Chef Patrick and his staff were amazingly professional and the food was out of this world delicious. Made our office party a huge success and cannot wait to book again for our next event."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jess Lynn</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Chef Pat was just marvelous, food was fantastic, no disappointments. Presentation was just perfect as always. Food quality just as good and to finish with awesome customer service."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Giovanny Rivera</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Oh my gosh awesome service, awesome personality! Food was awesome, Chef Pat did a function for my sister and wow it was awesome the food, excellent presentation and very tasty. I'm positive we'll be doing functions with him again!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rackell Charlton</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all reviews on Google" data-en="Read all reviews on Google">Read all reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION (sin direccion fija: catering movil, area de servicio)
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Palm Beach County</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Heat off the Street Catering is a mobile catering company serving Palm Beach County, FL: office parties, weddings and private functions anywhere in the area." data-en="Heat off the Street Catering is a mobile catering company serving Palm Beach County, FL: office parties, weddings and private functions anywhere in the area.">Heat off the Street Catering is a mobile catering company serving Palm Beach County, FL: office parties, weddings and private functions anywhere in the area.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Availability" data-en="Availability">Availability</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="By appointment, every day of the week. Call ahead with your event date so Chef Patrick can confirm availability." data-en="By appointment, every day of the week. Call ahead with your event date so Chef Patrick can confirm availability.">By appointment, every day of the week. Call ahead with your event date so Chef Patrick can confirm availability.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (561) 345-8345" data-en="Call (561) 345-8345">Call (561) 345-8345</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="font-medium mb-1" data-es="Google Reviews" data-en="Google Reviews">Google Reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Read the real reviews behind the 5.0 rating, straight from the business's Google listing." data-en="Read the real reviews behind the 5.0 rating, straight from the business's Google listing.">Read the real reviews behind the 5.0 rating, straight from the business's Google listing.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Heat off the Street Catering service area, Palm Beach County FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Real food, cooked with heart." data-en="Real food, cooked with heart.">Real food, cooked with heart.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your next event" data-en="Your next event">Your next event</span> <span class="text-shine" data-es="starts with a call" data-en="starts with a call">starts with a call</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (561) 345-8345 for a free quote on your office party, wedding or private function. Chef Patrick handles the menu, the cooking and the service." data-en="Call (561) 345-8345 for a free quote on your office party, wedding or private function. Chef Patrick handles the menu, the cooking and the service.">Call (561) 345-8345 for a free quote on your office party, wedding or private function. Chef Patrick handles the menu, the cooking and the service.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (561) 345-8345" data-en="Call (561) 345-8345">Call (561) 345-8345</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Heat off the Street</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/hero-lamb-chops.jpg" alt="Heat off the Street Catering" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Heat off the Street</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Mobile catering serving Palm Beach County, FL. By appointment, every day of the week." data-en="Mobile catering serving Palm Beach County, FL. By appointment, every day of the week.">Mobile catering serving Palm Beach County, FL. By appointment, every day of the week.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Mobile, serving Palm Beach County, FL" data-en="Mobile, serving Palm Beach County, FL">Mobile, serving Palm Beach County, FL</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#e9c3ab]" data-es="Call (561) 345-8345" data-en="Call (561) 345-8345">Call (561) 345-8345</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Google · 5.0 (17 reviews)</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Heat off the Street Catering.</p>')
print("FOOTER done")

# ============================================================
# 18. Boton flotante (icono calendario -> telefono)
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Heat off the Street Catering">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
print("BOOK-FLOAT done")

# ============================================================
# 19. Limpieza tel: target=_blank/rel sueltos que queden
# ============================================================
h = h.replace(f'href="{NEW_TEL}" target="_blank" rel="noopener"', f'href="{NEW_TEL}"')
print("CLEANUP done")

# ============================================================
# 20. Traduccion ES
# ============================================================
T = {
    "Palm Beach County, FL · Catering": "Condado de Palm Beach, FL · Catering",
    "Real food, cooked with heart.": "Comida real, cocinada con corazon.",
    "Chef-led catering that": "Catering liderado por un chef que",
    "brings real ": "trae ",
    "heat": "calor de verdad",
    "Heat off the Street Catering is a mobile, chef-led catering service run by Chef Patrick across Palm Beach County: plated dinners, brunch spreads, passed bites and full event service for office parties, weddings and private functions, with a perfect 5.0 rating across 17 Google reviews.":
        "Heat off the Street Catering es un servicio de catering movil liderado por el Chef Patrick en todo el condado de Palm Beach: cenas emplatadas, brunch, pasapalos y servicio completo de evento para fiestas de oficina, bodas y funciones privadas, con una calificacion perfecta de 5.0 en 17 resenas de Google.",
    "5.0 · 17 reviews on Google": "5.0 · 17 resenas en Google",
    "Call (561) 345-8345": "Llama al (561) 345-8345",
    "Availability": "Disponibilidad",
    "Every day of the week": "Todos los dias de la semana",
    "reviews on Google": "resenas en Google",
    "Weddings": "Bodas",
    "Private chef, full service": "Chef privado, servicio completo",
    "Dinners · Brunch · Bites": "Cenas · Brunch · Pasapalos",
    "Mobile · By appointment": "Movil · Con cita previa",
    "One chef,": "Un chef,",
    "a perfect record": "un historial perfecto",
    "Heat off the Street Catering is led by Chef Patrick, who reviewers call out by name for office parties, weddings and private functions across Palm Beach County. The photos on this page come straight from real plated events: brunch spreads, passed appetizer spoons, salads, tacos, grilled entrees and fine-dining style plates.":
        "Heat off the Street Catering esta liderado por el Chef Patrick, a quien las resenas mencionan por nombre por fiestas de oficina, bodas y funciones privadas en todo el condado de Palm Beach. Las fotos de esta pagina vienen directo de eventos reales emplatados: brunch, cucharas de entrada, ensaladas, tacos, platos a la parrilla y presentaciones de alta cocina.",
    "The result is a perfect 5.0 rating across 17 Google reviews, with guests calling out the seasoning, the presentation and how fast and reasonably priced the service is.":
        "El resultado es una calificacion perfecta de 5.0 en 17 resenas de Google, con comensales que destacan el sazon, la presentacion y lo rapido y razonable del precio del servicio.",
    "Lead chef": "Chef principal",
    "From quote to cleanup": "De la cotizacion a la limpieza",
    "Planning your event,": "Planear tu evento,",
    "step by step": "paso a paso",
    "Tell us the date": "Cuentanos la fecha",
    "Call (561) 345-8345 with your event date, headcount and the vibe you want, and Chef Patrick scopes the menu from there.":
        "Llama al (561) 345-8345 con la fecha de tu evento, numero de invitados y el estilo que buscas, y el Chef Patrick define el menu desde ahi.",
    "Menu planning": "Planeacion del menu",
    "Chef Patrick walks through plated, brunch, passed bites and stations so you land on a menu that fits your event and budget.":
        "El Chef Patrick repasa opciones emplatadas, de brunch, pasapalos y estaciones para armar un menu que se ajuste a tu evento y presupuesto.",
    "Event day": "Dia del evento",
    "The team arrives ready to cook, plate and serve, so the food comes out fresh, hot and seasoned the way the reviews describe.":
        "El equipo llega listo para cocinar, emplatar y servir, para que la comida salga fresca, caliente y sazonada tal como la describen las resenas.",
    "Service &amp; cleanup": "Servicio y limpieza",
    "Heat off the Street handles service through the last course and clears out when it is done, so you just enjoy the party.":
        "Heat off the Street se encarga del servicio hasta el ultimo plato y recoge todo al terminar, para que tu solo disfrutes la fiesta.",
    "Catering built around": "Catering hecho",
    "your event": "para tu evento",
    "Every event is different, so every menu is quoted to match it. Call with your date and guest count.":
        "Cada evento es distinto, asi que cada menu se cotiza a su medida. Llama con tu fecha y numero de invitados.",
    "Reviewer favorite": "Favorito de las resenas",
    "Office Parties &amp; Functions": "Fiestas de Oficina y Funciones",
    "Full-service catering for office parties and private functions, the kind of event reviewers say Chef Patrick turned into a huge success.":
        "Catering integral para fiestas de oficina y funciones privadas, el tipo de evento que las resenas dicen que el Chef Patrick convirtio en un gran exito.",
    "Every event is quoted": "Cada evento se cotiza",
    "Call": "Llamar",
    "Most requested": "Lo mas pedido",
    "Weddings &amp; Private Events": "Bodas y Eventos Privados",
    "Plated dinners and full event service for weddings and celebrations, with the seasoning and presentation reviewers call out by name.":
        "Cenas emplatadas y servicio completo de evento para bodas y celebraciones, con el sazon y la presentacion que las resenas mencionan por nombre.",
    "Morning spreads": "Spreads de manana",
    "Brunch &amp; Passed Bites": "Brunch y Pasapalos",
    "Brunch spreads, waffles, breakfast sandwiches and passed hors d'oeuvre spoons, plated and ready to serve.":
        "Brunch, waffles, sandwiches de desayuno y cucharas de pasapalos, emplatados y listos para servir.",
    "Seated service": "Servicio sentado",
    "Plated Entrees &amp; Dinners": "Entradas y Cenas Emplatadas",
    "Grilled chicken, blackened fish, tacos and lamb chop plates, seasoned and finished the way the photos on this page show.":
        "Pollo a la parrilla, pescado ennegrecido, tacos y chuletas de cordero, sazonados y terminados tal como muestran las fotos de esta pagina.",
    "Service Styles": "Estilos de Servicio",
    "Plated service": "Servicio emplatado",
    "Passed bites": "Pasapalos",
    "Brunch spreads": "Brunch",
    "Family style": "Estilo familiar",
    "Event Types": "Tipos de Evento",
    "Office parties": "Fiestas de oficina",
    "Private functions": "Funciones privadas",
    "Celebrations": "Celebraciones",
    "Always Included": "Siempre Incluido",
    "Fresh, seasoned cooking": "Comida fresca y sazonada",
    "On-time service": "Servicio puntual",
    "Direct chef communication": "Comunicacion directa con el chef",
    "Quote for your headcount": "Cotizacion segun tus invitados",
    "Every menu is quoted to match your event, guest count and venue. Call (561) 345-8345 to start planning.":
        "Cada menu se cotiza segun tu evento, numero de invitados y lugar. Llama al (561) 345-8345 para empezar a planear.",
    "Real": "Eventos",
    "events": "reales",
    "What Palm Beach County": "Lo que dicen los",
    "clients say": "clientes del condado de Palm Beach",
    "5.0 out of 5 · 17 reviews on Google": "5.0 de 5 · 17 resenas en Google",
    "Read all reviews on Google": "Lee todas las resenas en Google",
    "Serving": "Sirviendo a",
    "Service area": "Area de servicio",
    "Heat off the Street Catering is a mobile catering company serving Palm Beach County, FL: office parties, weddings and private functions anywhere in the area.":
        "Heat off the Street Catering es una empresa de catering movil que sirve al condado de Palm Beach, FL: fiestas de oficina, bodas y funciones privadas en cualquier parte del area.",
    "View on map": "Ver en el mapa",
    "By appointment, every day of the week. Call ahead with your event date so Chef Patrick can confirm availability.":
        "Con cita previa, todos los dias de la semana. Llama con anticipacion con la fecha de tu evento para que el Chef Patrick confirme disponibilidad.",
    "Google Reviews": "Resenas de Google",
    "Read the real reviews behind the 5.0 rating, straight from the business's Google listing.":
        "Lee las resenas reales detras de la calificacion de 5.0, directo de la ficha de Google del negocio.",
    "Your next event": "Tu proximo evento",
    "starts with a call": "empieza con una llamada",
    "Call (561) 345-8345 for a free quote on your office party, wedding or private function. Chef Patrick handles the menu, the cooking and the service.":
        "Llama al (561) 345-8345 para una cotizacion gratis de tu fiesta de oficina, boda o funcion privada. El Chef Patrick se encarga del menu, la cocina y el servicio.",
    "Read Google Reviews": "Lee las resenas de Google",
    "Mobile catering serving Palm Beach County, FL. By appointment, every day of the week.":
        "Catering movil que sirve al condado de Palm Beach, FL. Con cita previa, todos los dias de la semana.",
    "Contact": "Contacto",
    "Mobile, serving Palm Beach County, FL": "Movil, sirviendo al condado de Palm Beach, FL",
    "Reviews": "Resenas",
    "Call now": "Llamar ahora",
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
