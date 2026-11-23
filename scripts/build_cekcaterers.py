import re
import os
import colorsys

SLUG = "cek-caterers-boca-raton"
SRC = "templates/light-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()

# ============================================================
# 0. Funciones de shift de color (definidas ANTES de rep/rep_all: rep() las
#    usa via S() para que cualquier ancla posterior escrita con los hex/rgba
#    ORIGINALES del esqueleto siga encontrando el texto ya desplazado de paleta).
# ============================================================
TARGET_HUE = 352 / 360.0
SAT_MUL = 0.92
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
    """Aplica el mismo shift de paleta a cualquier hex/rgba literal embebido en
    un string de ancla, para que las anclas escritas con los colores ORIGINALES
    del esqueleto sigan siendo validas despues del paso 2 (paleta global)."""
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
# 2. PALETA: plum-pink (lashbloom) -> wine/burgundy (CEK Caterers)
#    Extraido dinamicamente de lo que queda tras proteger el badge (_raw=True:
#    aqui los valores YA son los literales a buscar/poner, no hay que volver
#    a pasarlos por S()).
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
# 3. GLOBALES: sin booking platform ni Instagram -> tel: + Facebook real
# ============================================================
NEW_TEL = "tel:+15612416977"
NEW_FB_URL = "https://www.facebook.com/cekcaterers/"
NEW_FB_LABEL = "facebook.com/cekcaterers"
NEW_REVIEWS_URL = "https://www.google.com/search?q=CEK+Caterers+Boca+Raton+FL+reviews"
NEW_REVIEWS_LABEL = "Google Reviews"
NEW_ADDR = "17950 N Military Trl, Boca Raton, FL 33496"
NEW_MAPS = "https://www.google.com/maps?q=17950+N+Military+Trl,+Boca+Raton,+FL+33496"

OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
rep_all(OLD_BOOK, NEW_TEL, expect=13)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
rep_all(OLD_IG_URL, NEW_FB_URL, expect=6)

rep_all("@_lashbloom", NEW_FB_LABEL, expect=4)

# Icono: las 3 svg de Instagram (rect+circulo+punto) -> glifo de Facebook (lucide)
IG_ICON_INNER = '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>'
FB_ICON_INNER = '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'
rep_all(IG_ICON_INNER, FB_ICON_INNER, expect=3)
print("GLOBALS done")

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>CEK Caterers · Private Event Catering in Boca Raton, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="CEK Caterers, Boca Raton FL: full-service catering for weddings, b\'nai mitzvah, simchas and corporate events. Salad bars, sushi displays, plated dinners and dessert tables. 4.9 stars on Google, 14 reviews." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="CEK Caterers · Private Event Catering in Boca Raton, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Weddings, b\'nai mitzvah, simchas and corporate catering. Salad bars, sushi, plated dinners, dessert tables. 4.9 on Google." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-sushi-display.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-sushi-display.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FoodEstablishment",
    "name": "CEK Caterers",
    "description": "Full-service event catering company in Boca Raton, FL: weddings, b'nai mitzvah, simchas and corporate events, with salad bars, sushi displays, plated dinners and dessert tables.",
    "address": { "@type": "PostalAddress", "streetAddress": "17950 N Military Trl", "addressLocality": "Boca Raton", "addressRegion": "FL", "postalCode": "33496", "addressCountry": "US" },
    "telephone": "+1-561-241-6977",
    "sameAs": ["''' + NEW_FB_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "14", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Catering services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Wedding Catering" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bar &amp; Bat Mitzvah Catering" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Corporate Event Catering" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Simcha &amp; Private Dinner Catering" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN default (ya lo es en el esqueleto)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ============================================================
# 6. PRELOADER + NAV
# ============================================================
rep('<span class="pre-mono">LB</span>\n    <span class="pre-word">Lash Bloom</span>',
    '<span class="pre-mono">CEK</span>\n    <span class="pre-word">CEK Caterers</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<img src="assets/hero-sushi-display.jpg" alt="CEK Caterers" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">CEK <span class="text-[color:var(--accent-deep)]">Caterers</span></span>')
rep('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n          <span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Boca Raton, FL · Event Catering" data-en="Boca Raton, FL · Event Catering">Boca Raton, FL · Event Catering</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Every event, catered with care." data-en="Every event, catered with care.">Every event, catered with care.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Full-service catering for" data-en="Full-service catering for">Full-service catering for</span><br /><span data-es="weddings, simchas and " data-en="weddings, simchas and ">weddings, simchas and </span><span class="text-shine" data-es="corporate events" data-en="corporate events">corporate events</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="From elegant salad bars and sushi displays to plated dinners and dessert tables, CEK Caterers designs and runs private events across Boca Raton and Palm Beach County: weddings, bar and bat mitzvahs, corporate dinners and simchas, with table linens, flowers and the full buffet setup handled on site." data-en="From elegant salad bars and sushi displays to plated dinners and dessert tables, CEK Caterers designs and runs private events across Boca Raton and Palm Beach County: weddings, bar and bat mitzvahs, corporate dinners and simchas, with table linens, flowers and the full buffet setup handled on site.">From elegant salad bars and sushi displays to plated dinners and dessert tables, CEK Caterers designs and runs private events across Boca Raton and Palm Beach County: weddings, bar and bat mitzvahs, corporate dinners and simchas, with table linens, flowers and the full buffet setup handled on site.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 14 reviews on Google" data-en="4.9 · 14 reviews on Google">4.9 · 14 reviews on Google</span>')
rep('''<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''',
    '''<span data-es="Call (561) 241-6977" data-en="Call (561) 241-6977">Call (561) 241-6977</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-sushi-display.jpg" alt="An elegant sushi roll display tower catered by CEK Caterers in Boca Raton, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Hours" data-en="Hours">Hours</p>
            <p class="font-display text-lg">Mon - Fri</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="9 AM - 6 PM" data-en="9 AM - 6 PM">9 AM - 6 PM</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="14">14</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Weddings <span class="text-shine">&amp;</span> Simchas</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Buffet · Plated · Stations" data-en="Buffet · Plated · Stations">Buffet · Plated · Stations</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine" data-es="On-Site" data-en="On-Site">On-Site</span> Setup</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Linens, flowers &amp; styling" data-en="Linens, flowers &amp; styling">Linens, flowers &amp; styling</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Boca Raton</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">17950 N Military Trl</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Classic Set", "Weddings"),
    ("Hybrid Set", "Bar &amp; Bat Mitzvah"),
    ("Volume Set", "Corporate Events"),
    ("Mega Volume", "Simchas"),
    ("Bottom Lashes", "Dessert Tables"),
    ("West Palm Beach, FL", "Boca Raton, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ============================================================
# 10. LA EXPERIENCIA
# ============================================================
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/about-roasted-veg.jpg" alt="A roasted vegetable and mushroom platter catered by CEK Caterers" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/about-dessert-prep.jpg" alt="A member of the CEK Caterers team finishing individual dessert jars" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="A caterer built" data-en="A caterer built">A caterer built</span><br /><span class="text-shine" data-es="around your event" data-en="around your event">around your event</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="CEK Caterers is led by Avi and a team that caters bar and bat mitzvahs, weddings, simchas and corporate dinners across Boca Raton and Palm Beach County. Reviewers single out the sushi displays, scratch salad bars, dessert tables and seasonal roasted vegetable platters, plus the table linens, flowers and full buffet setup handled on site." data-en="CEK Caterers is led by Avi and a team that caters bar and bat mitzvahs, weddings, simchas and corporate dinners across Boca Raton and Palm Beach County. Reviewers single out the sushi displays, scratch salad bars, dessert tables and seasonal roasted vegetable platters, plus the table linens, flowers and full buffet setup handled on site.">CEK Caterers is led by Avi and a team that caters bar and bat mitzvahs, weddings, simchas and corporate dinners across Boca Raton and Palm Beach County. Reviewers single out the sushi displays, scratch salad bars, dessert tables and seasonal roasted vegetable platters, plus the table linens, flowers and full buffet setup handled on site.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result is a 4.9-star rating across 14 Google reviews, 46 total between Google and Facebook. Clients describe Avi as easy to plan with and say his team delivers exactly what was promised, down to the last detail." data-en="The result is a 4.9-star rating across 14 Google reviews, 46 total between Google and Facebook. Clients describe Avi as easy to plan with and say his team delivers exactly what was promised, down to the last detail.">The result is a 4.9-star rating across 14 Google reviews, 46 total between Google and Facebook. Clients describe Avi as easy to plan with and say his team delivers exactly what was promised, down to the last detail.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="14">14</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Avi</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Contacto principal" data-en="Lead contact">Lead contact</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/hero-sushi-display.jpg" alt="CEK Caterers" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">CEK Caterers · <span class="text-[color:var(--ink-40)]" data-es="Boca Raton, FL" data-en="Boca Raton, FL">Boca Raton, FL</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="From quote to cleanup" data-en="From quote to cleanup">From quote to cleanup</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Planning your event," data-en="Planning your event,">Planning your event,</span> <span class="text-shine" data-es="step by step" data-en="step by step">step by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Tell us the date" data-en="Tell us the date">Tell us the date</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (561) 241-6977 with your event date, headcount and venue, and the team scopes the catering from there." data-en="Call (561) 241-6977 with your event date, headcount and venue, and the team scopes the catering from there.">Call (561) 241-6977 with your event date, headcount and venue, and the team scopes the catering from there.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Menu &amp; tasting" data-en="Menu &amp; tasting">Menu &amp; tasting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Avi walks through salad bar, sushi, plated and dessert options to build a menu around your event and guest count." data-en="Avi walks through salad bar, sushi, plated and dessert options to build a menu around your event and guest count.">Avi walks through salad bar, sushi, plated and dessert options to build a menu around your event and guest count.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Setup day" data-en="Setup day">Setup day</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew arrives ahead of time to set linens, flowers, the buffet or plated stations, and the dessert table." data-en="The crew arrives ahead of time to set linens, flowers, the buffet or plated stations, and the dessert table.">The crew arrives ahead of time to set linens, flowers, the buffet or plated stations, and the dessert table.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Service &amp; cleanup" data-en="Service &amp; cleanup">Service &amp; cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Servers run the event floor to table, and the team clears and packs out when it is over, so you just enjoy it." data-en="Servers run the event floor to table, and the team clears and packs out when it is over, so you just enjoy it.">Servers run the event floor to table, and the team clears and packs out when it is over, so you just enjoy it.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS (variante adaptada: sin precios, "se cotiza")
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Catering built around" data-en="Catering built around">Catering built around</span> <span class="text-shine" data-es="your event" data-en="your event">your event</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every event is different, so every menu is quoted to match it. Call or message with your date and guest count." data-en="Every event is different, so every menu is quoted to match it. Call or message with your date and guest count.">Every event is different, so every menu is quoted to match it. Call or message with your date and guest count.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Buffet favorite" data-en="Buffet favorite">Buffet favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Salad Bar &amp; Buffet" data-en="Salad Bar &amp; Buffet">Salad Bar &amp; Buffet</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Scratch salad bars with hearts of palm, chickpeas, dried fruit and cheese, plus full buffet-style service for the whole event." data-en="Scratch salad bars with hearts of palm, chickpeas, dried fruit and cheese, plus full buffet-style service for the whole event.">Scratch salad bars with hearts of palm, chickpeas, dried fruit and cheese, plus full buffet-style service for the whole event.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Weddings &amp; B'nai Mitzvah" data-en="Weddings &amp; B'nai Mitzvah">Weddings &amp; B'nai Mitzvah</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service catering for weddings, bar and bat mitzvahs and simchas, with linens, flowers and the buffet or plated service planned around your event." data-en="Full-service catering for weddings, bar and bat mitzvahs and simchas, with linens, flowers and the buffet or plated service planned around your event.">Full-service catering for weddings, bar and bat mitzvahs and simchas, with linens, flowers and the buffet or plated service planned around your event.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Elevated presentation" data-en="Elevated presentation">Elevated presentation</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Sushi &amp; Plated Dinners" data-en="Sushi &amp; Plated Dinners">Sushi &amp; Plated Dinners</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sushi roll towers, plated appetizers and seasonal roasted vegetable platters for a seated or stationed dinner service." data-en="Sushi roll towers, plated appetizers and seasonal roasted vegetable platters for a seated or stationed dinner service.">Sushi roll towers, plated appetizers and seasonal roasted vegetable platters for a seated or stationed dinner service.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sweet finish" data-en="Sweet finish">Sweet finish</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Dessert Tables" data-en="Dessert Tables">Dessert Tables</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Styled dessert tables and individual dessert jars with berries and chocolate, built to match the rest of the event." data-en="Styled dessert tables and individual dessert jars with berries and chocolate, built to match the rest of the event.">Styled dessert tables and individual dessert jars with berries and chocolate, built to match the rest of the event.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Menu Styles" data-en="Menu Styles">Menu Styles</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Buffet service" data-en="Buffet service">Buffet service</li>
            <li class="flex items-center gap-2" data-es="Plated service" data-en="Plated service">Plated service</li>
            <li class="flex items-center gap-2" data-es="Food stations" data-en="Food stations">Food stations</li>
            <li class="flex items-center gap-2" data-es="Family style" data-en="Family style">Family style</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Event Types" data-en="Event Types">Event Types</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Weddings" data-en="Weddings">Weddings</li>
            <li class="flex items-center gap-2" data-es="Bar &amp; Bat Mitzvah" data-en="Bar &amp; Bat Mitzvah">Bar &amp; Bat Mitzvah</li>
            <li class="flex items-center gap-2" data-es="Corporate dinners" data-en="Corporate dinners">Corporate dinners</li>
            <li class="flex items-center gap-2" data-es="Simchas &amp; life-cycle events" data-en="Simchas &amp; life-cycle events">Simchas &amp; life-cycle events</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Always Included" data-en="Always Included">Always Included</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Table linens" data-en="Table linens">Table linens</li>
            <li class="flex items-center gap-2" data-es="Flowers &amp; styling" data-en="Flowers &amp; styling">Flowers &amp; styling</li>
            <li class="flex items-center gap-2" data-es="Servers on site" data-en="Servers on site">Servers on site</li>
            <li class="flex items-center gap-2" data-es="Full cleanup" data-en="Full cleanup">Full cleanup</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + S(NEW_SERVICES_GRID) + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Every menu is quoted to match your event, guest count and venue. Call (561) 241-6977 to start planning." data-en="Every menu is quoted to match your event, guest count and venue. Call (561) 241-6977 to start planning.">Every menu is quoted to match your event, guest count and venue. Call (561) 241-6977 to start planning.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="events" data-en="events">events</span>')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Salad bar montado para un salon de eventos" data-en="Salad bar set for a banquet hall">Salad bar set for a banquet hall</span><img src="assets/gallery-salad-bar-hall.jpg" alt="A scratch salad bar set up by CEK Caterers with banquet hall tables and chairs in the background" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Toppings del salad bar" data-en="Scratch salad bar toppings">Scratch salad bar toppings</span><img src="assets/gallery-salad-bar-bins.jpg" alt="Wooden crates of fresh salad bar toppings catered by CEK Caterers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Entrada de vegetales emplatada" data-en="Plated vegetable appetizer">Plated vegetable appetizer</span><img src="assets/gallery-plated-veg-stack.jpg" alt="A plated grilled vegetable stack appetizer from CEK Caterers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Platos de vegetales asados" data-en="Roasted vegetable platters, plated">Roasted vegetable platters, plated</span><img src="assets/gallery-roasted-veg-platters.jpg" alt="A row of roasted vegetable platters plated for a CEK Caterers event" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Ensaladas emplatadas individualmente" data-en="Individually plated salads">Individually plated salads</span><img src="assets/gallery-plated-salads.jpg" alt="Individually plated salads with tomatoes and hearts of palm from CEK Caterers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Ensalada de remolacha de postre" data-en="Beet carpaccio dessert salad">Beet carpaccio dessert salad</span><img src="assets/gallery-beet-carpaccio.jpg" alt="A golden beet carpaccio salad with dried fruit and nuts from CEK Caterers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + S(NEW_GALLERY_GRID) + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Boca Raton" data-en="What Boca Raton">What Boca Raton</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 14 reviews on Google" data-en="4.9 out of 5 · 14 reviews on Google">4.9 out of 5 · 14 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I highly recommend CEK Caterers! Avi and his team catered my son's Bar Mitzvah and did a great job from start to finish. He made planning the event and the menu so easy for us. The food was delicious and exceeded expectations. All of our guests loved it!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Evan Rosa</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Avi met every single one of our needs and more! His staff was professional and accommodating to all our needs."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sandrine Cohen</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Facebook" data-en="Facebook review">Facebook review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Avi did an outstanding job making delicious food for my son's Bar Mitzvah. The presentation was beautiful too."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dawn Gordon Fisch</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Facebook" data-en="Facebook review">Facebook review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all reviews on Google" data-en="Read all reviews on Google">Read all reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Boca Raton</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Friday, 9 AM to 6 PM. Call ahead to set up a planning call or tasting." data-en="Monday to Friday, 9 AM to 6 PM. Call ahead to set up a planning call or tasting.">Monday to Friday, 9 AM to 6 PM. Call ahead to set up a planning call or tasting.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (561) 241-6977" data-en="Call (561) 241-6977">Call (561) 241-6977</a>''')
rep('''<p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>''',
    '''<p class="font-medium mb-1" data-es="Facebook" data-en="Facebook">Facebook</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Photos from past weddings, mitzvahs and corporate events, straight from the source." data-en="Photos from past weddings, mitzvahs and corporate events, straight from the source.">Photos from past weddings, mitzvahs and corporate events, straight from the source.</p>''')
rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Map: CEK Caterers, 17950 N Military Trl, Boca Raton FL"\n          src="' + NEW_MAPS + '&output=embed"')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Every event, catered with care." data-en="Every event, catered with care.">Every event, catered with care.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo evento" data-en="Your next event">Your next event</span> <span class="text-shine" data-es="empieza con una llamada" data-en="starts with a call">starts with a call</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (561) 241-6977 for a free quote on your wedding, simcha, bar or bat mitzvah, or corporate event. Avi and the team handle the menu, setup and service." data-en="Call (561) 241-6977 for a free quote on your wedding, simcha, bar or bat mitzvah, or corporate event. Avi and the team handle the menu, setup and service.">Call (561) 241-6977 for a free quote on your wedding, simcha, bar or bat mitzvah, or corporate event. Avi and the team handle the menu, setup and service.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (561) 241-6977" data-en="Call (561) 241-6977">Call (561) 241-6977</a>
        <a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Facebook" data-en="Follow on Facebook">Follow on Facebook</a>''')
print("CTA FINAL done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">CEK Caterers</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/hero-sushi-display.jpg" alt="CEK Caterers" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">CEK Caterers</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Private event catering in Boca Raton, FL. Weddings, simchas, corporate events and more." data-en="Private event catering in Boca Raton, FL. Weddings, simchas, corporate events and more.">Private event catering in Boca Raton, FL. Weddings, simchas, corporate events and more.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#f0bed7]" data-es="Call (561) 241-6977" data-en="Call (561) 241-6977">Call (561) 241-6977</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · ''' + NEW_FB_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Facebook · ''' + NEW_FB_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 CEK Caterers.</p>')
print("FOOTER done")

# ============================================================
# 18. Boton flotante (icono calendario -> telefono)
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf2f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call CEK Caterers">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf2f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n  </a>')
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
    "Boca Raton, FL · Event Catering": "Boca Raton, FL · Catering de Eventos",
    "Every event, catered with care.": "Cada evento, atendido con cuidado.",
    "Full-service catering for": "Catering integral para",
    "weddings, simchas and ": "bodas, simchas y ",
    "corporate events": "eventos corporativos",
    "From elegant salad bars and sushi displays to plated dinners and dessert tables, CEK Caterers designs and runs private events across Boca Raton and Palm Beach County: weddings, bar and bat mitzvahs, corporate dinners and simchas, with table linens, flowers and the full buffet setup handled on site.":
        "Desde salad bars elegantes y displays de sushi hasta cenas emplatadas y mesas de postres, CEK Caterers disena y ejecuta eventos privados en Boca Raton y el condado de Palm Beach: bodas, bar y bat mitzvahs, cenas corporativas y simchas, con manteleria, flores y el montaje completo del buffet incluido.",
    "4.9 · 14 reviews on Google": "4.9 · 14 resenas en Google",
    "Call (561) 241-6977": "Llama al (561) 241-6977",
    "Hours": "Horario",
    "9 AM - 6 PM": "9 AM - 6 PM",
    "reviews on Google": "resenas en Google",
    "Buffet · Plated · Stations": "Buffet · Emplatado · Estaciones",
    "On-Site": "En el Lugar",
    "Linens, flowers &amp; styling": "Manteleria, flores y montaje",
    "Weddings": "Bodas",
    "Bar &amp; Bat Mitzvah": "Bar y Bat Mitzvah",
    "Dessert Tables": "Mesas de Postres",
    "A caterer built": "Un catering hecho",
    "around your event": "para tu evento",
    "CEK Caterers is led by Avi and a team that caters bar and bat mitzvahs, weddings, simchas and corporate dinners across Boca Raton and Palm Beach County. Reviewers single out the sushi displays, scratch salad bars, dessert tables and seasonal roasted vegetable platters, plus the table linens, flowers and full buffet setup handled on site.":
        "CEK Caterers esta liderado por Avi y un equipo que atiende bar y bat mitzvahs, bodas, simchas y cenas corporativas en Boca Raton y el condado de Palm Beach. Las resenas destacan los displays de sushi, los salad bars hechos desde cero, las mesas de postres y los platos de vegetales asados de temporada, ademas de la manteleria, las flores y el montaje completo del buffet.",
    "The result is a 4.9-star rating across 14 Google reviews, 46 total between Google and Facebook. Clients describe Avi as easy to plan with and say his team delivers exactly what was promised, down to the last detail.":
        "El resultado es una calificacion de 4.9 estrellas en 14 resenas de Google, 46 en total entre Google y Facebook. Los clientes describen a Avi como facil de coordinar y dicen que su equipo cumple exactamente lo prometido, hasta el ultimo detalle.",
    "From quote to cleanup": "De la cotizacion a la limpieza",
    "Planning your event,": "Planear tu evento,",
    "step by step": "paso a paso",
    "Tell us the date": "Cuentanos la fecha",
    "Call (561) 241-6977 with your event date, headcount and venue, and the team scopes the catering from there.":
        "Llama al (561) 241-6977 con la fecha de tu evento, numero de invitados y el lugar, y el equipo define el catering desde ahi.",
    "Menu &amp; tasting": "Menu y degustacion",
    "Avi walks through salad bar, sushi, plated and dessert options to build a menu around your event and guest count.":
        "Avi repasa opciones de salad bar, sushi, platos emplatados y postres para armar un menu segun tu evento y numero de invitados.",
    "Setup day": "Dia del montaje",
    "The crew arrives ahead of time to set linens, flowers, the buffet or plated stations, and the dessert table.":
        "El equipo llega con anticipacion para montar manteleria, flores, el buffet o las estaciones emplatadas, y la mesa de postres.",
    "Service &amp; cleanup": "Servicio y limpieza",
    "Servers run the event floor to table, and the team clears and packs out when it is over, so you just enjoy it.":
        "Los meseros atienden el salon mesa por mesa, y el equipo recoge y se retira al terminar, para que tu solo disfrutes.",
    "Catering built around": "Catering hecho",
    "your event": "para tu evento",
    "Every event is different, so every menu is quoted to match it. Call or message with your date and guest count.":
        "Cada evento es distinto, asi que cada menu se cotiza a su medida. Llama o escribe con tu fecha y numero de invitados.",
    "Buffet favorite": "Favorito del buffet",
    "Salad Bar &amp; Buffet": "Salad Bar y Buffet",
    "Scratch salad bars with hearts of palm, chickpeas, dried fruit and cheese, plus full buffet-style service for the whole event.":
        "Salad bars hechos desde cero con palmitos, garbanzos, fruta seca y queso, mas servicio tipo buffet completo para todo el evento.",
    "Every event is quoted": "Cada evento se cotiza",
    "Call": "Llamar",
    "Most requested": "Lo mas pedido",
    "Weddings &amp; B'nai Mitzvah": "Bodas y B'nai Mitzvah",
    "Full-service catering for weddings, bar and bat mitzvahs and simchas, with linens, flowers and the buffet or plated service planned around your event.":
        "Catering integral para bodas, bar y bat mitzvahs y simchas, con manteleria, flores y servicio de buffet o emplatado planeado para tu evento.",
    "Elevated presentation": "Presentacion elevada",
    "Sushi &amp; Plated Dinners": "Sushi y Cenas Emplatadas",
    "Sushi roll towers, plated appetizers and seasonal roasted vegetable platters for a seated or stationed dinner service.":
        "Torres de sushi, entradas emplatadas y platos de vegetales asados de temporada para un servicio sentado o por estaciones.",
    "Sweet finish": "Cierre dulce",
    "Styled dessert tables and individual dessert jars with berries and chocolate, built to match the rest of the event.":
        "Mesas de postres decoradas y frascos de postre individuales con frutos rojos y chocolate, a juego con el resto del evento.",
    "Menu Styles": "Estilos de Menu",
    "Buffet service": "Servicio buffet",
    "Plated service": "Servicio emplatado",
    "Food stations": "Estaciones de comida",
    "Family style": "Estilo familiar",
    "Event Types": "Tipos de Evento",
    "Corporate dinners": "Cenas corporativas",
    "Simchas &amp; life-cycle events": "Simchas y eventos de ciclo de vida",
    "Always Included": "Siempre Incluido",
    "Table linens": "Manteleria",
    "Flowers &amp; styling": "Flores y montaje",
    "Servers on site": "Meseros en el lugar",
    "Full cleanup": "Limpieza completa",
    "Every menu is quoted to match your event, guest count and venue. Call (561) 241-6977 to start planning.":
        "Cada menu se cotiza segun tu evento, numero de invitados y lugar. Llama al (561) 241-6977 para empezar a planear.",
    "Real": "Eventos",
    "events": "reales",
    "What Boca Raton": "Lo que dicen los",
    "clients say": "clientes en Boca Raton",
    "4.9 out of 5 · 14 reviews on Google": "4.9 de 5 · 14 resenas en Google",
    "Read all reviews on Google": "Lee todas las resenas en Google",
    "Facebook": "Facebook",
    "Photos from past weddings, mitzvahs and corporate events, straight from the source.":
        "Fotos de bodas, mitzvahs y eventos corporativos anteriores, directo de la fuente.",
    "Monday to Friday, 9 AM to 6 PM. Call ahead to set up a planning call or tasting.":
        "Lunes a viernes, 9 AM a 6 PM. Llama antes para agendar una llamada de planeacion o una degustacion.",
    "Call (561) 241-6977 for a free quote on your wedding, simcha, bar or bat mitzvah, or corporate event. Avi and the team handle the menu, setup and service.":
        "Llama al (561) 241-6977 para una cotizacion gratis de tu boda, simcha, bar o bat mitzvah, o evento corporativo. Avi y el equipo se encargan del menu, el montaje y el servicio.",
    "Follow on Facebook": "Seguir en Facebook",
    "Private event catering in Boca Raton, FL. Weddings, simchas, corporate events and more.":
        "Catering de eventos privados en Boca Raton, FL. Bodas, simchas, eventos corporativos y mas.",
    "Contact": "Contacto",
    "Follow": "Seguir",
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
