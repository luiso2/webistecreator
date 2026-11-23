import re
import os
import colorsys

SLUG = "lockbuster-locksmith-jacksonville"
SRC = "templates/dark-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()

# ============================================================
# 0. Funciones de shift de color (ver build_cekcaterers.py: mismo metodo).
#    TARGET_HUE = 215/360 (azul seguridad profundo): distinto de los hues ya
#    usados en el registro (coral fairy ~350, caramelo ~30, esmeralda ~153,
#    teal acero ~180, violeta dark ~265, gold dark original ~41). 215 cae en
#    el hueco limpio entre teal (180) y violeta (265).
# ============================================================
TARGET_HUE = 215 / 360.0
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
# 2. PALETA: gold (pureartistry) -> deep security blue
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
# 3. GLOBALES: sin booking platform ni IG/FB real -> tel: como CTA principal,
#    y el slot de "redes" pasa a apuntar a una busqueda publica de Google
#    Reviews (unico canal de prueba social que SI es real y verificable).
# ============================================================
NEW_TEL = "tel:+19044545404"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Lockbuster+Locksmith+Jacksonville+FL+reviews"
NEW_REVIEWS_LABEL = "Google Reviews"
NEW_ADDR = "3134 Cornelia Dr, Jacksonville, FL 32257"
NEW_MAPS = "https://www.google.com/maps?q=3134+Cornelia+Dr,+Jacksonville,+FL+32257"

OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
rep_all(OLD_BOOK, NEW_TEL, expect=13)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
rep_all(OLD_IG_URL, NEW_REVIEWS_URL, expect=6)

rep_all("@pure.artistrysk", NEW_REVIEWS_LABEL, expect=4)

# Icono: las 3 svg de Instagram (rect+circulo+punto) -> estrella (prueba social)
IG_ICON_INNER = '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>'
STAR_ICON_INNER = '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
rep_all(IG_ICON_INNER, STAR_ICON_INNER, expect=3)
print("GLOBALS done")

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Lockbuster Locksmith · 24-Hour Locksmith in Jacksonville, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Lockbuster Locksmith, Jacksonville FL: 24-hour residential, commercial and automotive locksmith. Lockouts, lock rekey, lock installation and key cutting. 4.9 stars, 124 reviews on Google. Call (904) 454-5404." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Lockbuster Locksmith · 24-Hour Locksmith in Jacksonville, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Emergency lockouts, lock rekey, lock installation and automotive keys. 4.9 on Google. Call (904) 454-5404." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-van.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Locksmith",
    "name": "Lockbuster Locksmith",
    "description": "24-hour mobile locksmith service in Jacksonville, FL: residential, commercial and automotive lockouts, lock rekey and installation, key cutting, smart locks and access control.",
    "address": { "@type": "PostalAddress", "streetAddress": "3134 Cornelia Dr", "addressLocality": "Jacksonville", "addressRegion": "FL", "postalCode": "32257", "addressCountry": "US" },
    "telephone": "+1-904-454-5404",
    "priceRange": "Free estimates",
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "124", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Locksmith services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Emergency Lockouts" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Lock Rekey &amp; Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Automotive Locksmith" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Access Control &amp; Safes" } }
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
rep('<span class="pre-mono">PA</span>\n    <span class="pre-word">Pure Artistry</span>',
    '<span class="pre-mono">LB</span>\n    <span class="pre-word">Lockbuster Locksmith</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Lockbuster Locksmith" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lockbuster <span class="text-[color:var(--accent-deep)]">Locksmith</span></span>')
PHONE_SVG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
rep('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    PHONE_SVG + '\n          <span data-es="Call Now" data-en="Call Now">Call Now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call Now" data-en="Call Now">Call Now</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Jacksonville, FL · 24-Hour Locksmith" data-en="Jacksonville, FL · 24-Hour Locksmith">Jacksonville, FL · 24-Hour Locksmith</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Locked out? We have got you." data-en="Locked out? We have got you.">Locked out? We have got you.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Lockouts, rekeys and" data-en="Lockouts, rekeys and">Lockouts, rekeys and</span><br /><span data-es="new locks, handled " data-en="new locks, handled ">new locks, handled </span><span class="text-shine" data-es="fast" data-en="fast">fast</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="From emergency lockouts to full lock changes, Lockbuster Locksmith handles residential, commercial and automotive jobs across Jacksonville. Licensed technicians, free estimates, and a 4.9-star rating across 124 Google reviews." data-en="From emergency lockouts to full lock changes, Lockbuster Locksmith handles residential, commercial and automotive jobs across Jacksonville. Licensed technicians, free estimates, and a 4.9-star rating across 124 Google reviews.">From emergency lockouts to full lock changes, Lockbuster Locksmith handles residential, commercial and automotive jobs across Jacksonville. Licensed technicians, free estimates, and a 4.9-star rating across 124 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.9 · 124 reviews on Google" data-en="4.9 · 124 reviews on Google">4.9 · 124 reviews on Google</span>')
rep('''<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''',
    '''<span data-es="Call (904) 454-5404" data-en="Call (904) 454-5404">Call (904) 454-5404</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-van.jpg" alt="Lockbuster Locksmith company van with its branded door sign, Jacksonville FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Available" data-en="Available">Available</p>
            <p class="font-display text-lg">24/7</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Emergency service" data-en="Emergency service">Emergency service</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="124">124</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Lockouts <span class="text-shine">&amp;</span> Rekeys</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Residential · Commercial · Auto" data-en="Residential · Commercial · Auto">Residential · Commercial · Auto</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">Free <span class="text-shine" data-es="Estimates" data-en="Estimates">Estimates</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="No hidden fees" data-en="No hidden fees">No hidden fees</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Jacksonville</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">3134 Cornelia Dr</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Lockouts"),
    ("Loc Retwist", "Lock Rekey"),
    ("Knotless Braids", "Key Cutting"),
    ("K-Tip Extensions", "Auto Locksmith"),
    ("Keratin", "Smart Locks"),
    ("Orlando, FL", "Jacksonville, FL"),
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
          <img src="assets/about-rekey-pins.jpg" alt="Lockbuster Locksmith technician rekeying a lock cylinder with a pin kit" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/about-smartlock-install.jpg" alt="Smart keypad deadbolt freshly installed by Lockbuster Locksmith" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="One team," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="ready day or night" data-en="ready day or night">ready day or night</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Lockbuster Locksmith is a 24-hour, mobile locksmith service covering the Jacksonville area: residential and commercial lockouts, automotive key and ignition work, lock installation and rekeying, high-security locks and access control systems. Technicians come to you, whether it is a home, a business or a car." data-en="Lockbuster Locksmith is a 24-hour, mobile locksmith service covering the Jacksonville area: residential and commercial lockouts, automotive key and ignition work, lock installation and rekeying, high-security locks and access control systems. Technicians come to you, whether it is a home, a business or a car.">Lockbuster Locksmith is a 24-hour, mobile locksmith service covering the Jacksonville area: residential and commercial lockouts, automotive key and ignition work, lock installation and rekeying, high-security locks and access control systems. Technicians come to you, whether it is a home, a business or a car.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="The result is a 4.9-star rating across 124 Google reviews and a 5.0 average on HomeAdvisor, with clients describing fast response times, fair pricing and technicians who get the job done the first time." data-en="The result is a 4.9-star rating across 124 Google reviews and a 5.0 average on HomeAdvisor, with clients describing fast response times, fair pricing and technicians who get the job done the first time.">The result is a 4.9-star rating across 124 Google reviews and a 5.0 average on HomeAdvisor, with clients describing fast response times, fair pricing and technicians who get the job done the first time.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="124">124</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Disponible" data-en="Available">Available</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/avatar-tech.jpg" alt="Lockbuster Locksmith technician" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Lockbuster Locksmith · <span class="text-[color:var(--ink-40)]" data-es="Licensed Technician" data-en="Licensed Technician">Licensed Technician</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call anytime" data-en="Call anytime">Call anytime</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (904) 454-5404, 24 hours a day. Tell us if it is a home, business or vehicle lockout, or a lock job you need done." data-en="Call (904) 454-5404, 24 hours a day. Tell us if it is a home, business or vehicle lockout, or a lock job you need done.">Call (904) 454-5404, 24 hours a day. Tell us if it is a home, business or vehicle lockout, or a lock job you need done.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Fast arrival" data-en="Fast arrival">Fast arrival</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A licensed technician heads your way with the tools and stock to handle most lockouts, rekeys and lock installs on the first visit." data-en="A licensed technician heads your way with the tools and stock to handle most lockouts, rekeys and lock installs on the first visit.">A licensed technician heads your way with the tools and stock to handle most lockouts, rekeys and lock installs on the first visit.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Diagnose &amp; quote" data-en="Diagnose &amp; quote">Diagnose &amp; quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a clear price before any work starts: free estimates on every job, whether it is a simple lockout or a full rekey." data-en="You get a clear price before any work starts: free estimates on every job, whether it is a simple lockout or a full rekey.">You get a clear price before any work starts: free estimates on every job, whether it is a simple lockout or a full rekey.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Job done right" data-en="Job done right">Job done right</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Doors unlocked, locks rekeyed or installed, keys cut and tested on the spot, so you are back to your day with working locks." data-en="Doors unlocked, locks rekeyed or installed, keys cut and tested on the spot, so you are back to your day with working locks.">Doors unlocked, locks rekeyed or installed, keys cut and tested on the spot, so you are back to your day with working locks.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS (variante adaptada: sin precios, "se cotiza gratis")
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Call for any" data-en="Call for any">Call for any</span> <span class="text-shine" data-es="lock or key job" data-en="lock or key job">lock or key job</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every job gets a free estimate before any work starts. Call (904) 454-5404, 24 hours a day." data-en="Every job gets a free estimate before any work starts. Call (904) 454-5404, 24 hours a day.">Every job gets a free estimate before any work starts. Call (904) 454-5404, 24 hours a day.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="24/7 Service" data-en="24/7 Service">24/7 Service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Emergency Lockouts" data-en="Emergency Lockouts">Emergency Lockouts</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Locked out of your home, business or car? A technician comes to you, any hour, with damage-free entry tools." data-en="Locked out of your home, business or car? A technician comes to you, any hour, with damage-free entry tools.">Locked out of your home, business or car? A technician comes to you, any hour, with damage-free entry tools.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lock Rekey &amp; Installation" data-en="Lock Rekey &amp; Installation">Lock Rekey &amp; Installation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Rekey your existing locks, install new deadbolts and smart locks, or set up a master key system for a business." data-en="Rekey your existing locks, install new deadbolts and smart locks, or set up a master key system for a business.">Rekey your existing locks, install new deadbolts and smart locks, or set up a master key system for a business.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Auto Locksmith" data-en="Auto Locksmith">Auto Locksmith</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Car Keys &amp; Ignition" data-en="Car Keys &amp; Ignition">Car Keys &amp; Ignition</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Key cutting, transponder and smart key programming, and ignition repair for most makes and models." data-en="Key cutting, transponder and smart key programming, and ignition repair for most makes and models.">Key cutting, transponder and smart key programming, and ignition repair for most makes and models.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Commercial" data-en="Commercial">Commercial</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Access Control &amp; Safes" data-en="Access Control &amp; Safes">Access Control &amp; Safes</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Access control systems, master keying, and safe opening and repair for Jacksonville businesses." data-en="Access control systems, master keying, and safe opening and repair for Jacksonville businesses.">Access control systems, master keying, and safe opening and repair for Jacksonville businesses.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + S(NEW_SERVICES_GRID) + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Free estimates on every job. Available 24 hours for emergency lockouts across Jacksonville. Call (904) 454-5404." data-en="Free estimates on every job. Available 24 hours for emergency lockouts across Jacksonville. Call (904) 454-5404.">Free estimates on every job. Available 24 hours for emergency lockouts across Jacksonville. Call (904) 454-5404.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA (4 tiles reales: la variante adaptada no rellena con stock)
# ============================================================
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="jobs" data-en="jobs">jobs</span>')
# Nota: el link de cabecera de galeria ("@pure.artistrysk" -> href IG, icono IG) ya quedo
# resuelto por el paso global (seccion 3): href = NEW_REVIEWS_URL, icono = estrella,
# texto = "Google Reviews". No hace falta tocarlo de nuevo aqui.

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Instalando una cerradura" data-en="Installing a deadbolt lock">Installing a deadbolt lock</span><img src="assets/gallery-deadbolt-install.jpg" alt="Lockbuster Locksmith technician installing a deadbolt lock on a residential door" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cerradura inteligente" data-en="Smart keypad deadbolt">Smart keypad deadbolt</span><img src="assets/gallery-keypad-close.jpg" alt="Close-up of a smart keypad deadbolt lock installed by Lockbuster Locksmith" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Programación de llave" data-en="Automotive key programming">Automotive key programming</span><img src="assets/gallery-auto-key-fob.jpg" alt="Automotive key fob being programmed by Lockbuster Locksmith with a diagnostic tool" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Control de acceso comercial" data-en="Commercial access control">Commercial access control</span><img src="assets/gallery-exit-door.jpg" alt="Commercial door deadbolt and press-to-exit access control hardware serviced by Lockbuster Locksmith" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + S(NEW_GALLERY_GRID) + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES (quotes VERBATIM reales de HomeAdvisor, con nombre real)
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Jacksonville" data-en="What Jacksonville">What Jacksonville</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 on Google (124 reviews), plus a 5.0 average on HomeAdvisor" data-en="4.9 out of 5 on Google (124 reviews), plus a 5.0 average on HomeAdvisor">4.9 out of 5 on Google (124 reviews), plus a 5.0 average on HomeAdvisor</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Showed up on time. Quoted and then performed all work immediately. Rekeyed and repaired 7 electronic deadbolt lock sets. Installed 2 new deadbolts. Replaced one that did not work correctly. Fixed a sliding door lock. All done in less than 4 hours. I would hire again. Great locksmith."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tim H.</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de HomeAdvisor" data-en="HomeAdvisor review">HomeAdvisor review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Eli does outstanding sufficient work. He was on time and even made extra copies of my keys. I would definitely recommend him to family and friends."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Zina H.</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de HomeAdvisor" data-en="HomeAdvisor review">HomeAdvisor review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"He did a great job, was very professional and easy to work with. He is friendly, knows the industry, answers questions and offers good rates. I would recommend him for anyone."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Brandon M.</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de HomeAdvisor" data-en="HomeAdvisor review">HomeAdvisor review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read reviews on Google" data-en="Read reviews on Google">Read reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Jacksonville</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Available 24 hours a day, 7 days a week for emergency lockouts. Call anytime." data-en="Available 24 hours a day, 7 days a week for emergency lockouts. Call anytime.">Available 24 hours a day, 7 days a week for emergency lockouts. Call anytime.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (904) 454-5404" data-en="Call (904) 454-5404">Call (904) 454-5404</a>''')
rep('''<p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>''',
    '''<p class="font-medium mb-1" data-es="Reviews" data-en="Reviews">Reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Read real reviews from Jacksonville customers on Google before you call." data-en="Read real reviews from Jacksonville customers on Google before you call.">Read real reviews from Jacksonville customers on Google before you call.</p>''')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener">' + NEW_REVIEWS_LABEL + '</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener">4.9 on Google</a>')
rep('<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Map: Lockbuster Locksmith, 3134 Cornelia Dr, Jacksonville FL"\n          src="' + NEW_MAPS + '&output=embed"')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Locked out? We have got you." data-en="Locked out? We have got you.">Locked out? We have got you.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Help is" data-en="Help is">Help is</span> <span class="text-shine" data-es="one call away" data-en="one call away">one call away</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (904) 454-5404 any time, day or night, for lockouts, rekeys, lock installs or automotive keys anywhere in Jacksonville." data-en="Call (904) 454-5404 any time, day or night, for lockouts, rekeys, lock installs or automotive keys anywhere in Jacksonville.">Call (904) 454-5404 any time, day or night, for lockouts, rekeys, lock installs or automotive keys anywhere in Jacksonville.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (904) 454-5404" data-en="Call (904) 454-5404">Call (904) 454-5404</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Reviews on Google" data-en="Read Reviews on Google">Read Reviews on Google</a>''')
print("CTA FINAL done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Lockbuster Locksmith</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Lockbuster Locksmith" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lockbuster Locksmith</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="24-hour locksmith service in Jacksonville, FL. Licensed and mobile." data-en="24-hour locksmith service in Jacksonville, FL. Licensed and mobile.">24-hour locksmith service in Jacksonville, FL. Licensed and mobile.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#e9c3ab]" data-es="Call (904) 454-5404" data-en="Call (904) 454-5404">Call (904) 454-5404</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Google Reviews · 4.9 (124)</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lockbuster Locksmith.</p>')
print("FOOTER done")

# ============================================================
# 18. Boton flotante (icono calendario -> telefono)
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Lockbuster Locksmith">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call Now" data-en="Call Now">Call Now</span>\n  </a>')
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
    "Jacksonville, FL · 24-Hour Locksmith": "Jacksonville, FL · Cerrajeria 24 Horas",
    "Locked out? We have got you.": "Te quedaste afuera? Nosotros te ayudamos.",
    "Lockouts, rekeys and": "Cerraduras, llaves y",
    "new locks, handled ": "aperturas, resueltas ",
    "fast": "rapido",
    "From emergency lockouts to full lock changes, Lockbuster Locksmith handles residential, commercial and automotive jobs across Jacksonville. Licensed technicians, free estimates, and a 4.9-star rating across 124 Google reviews.":
        "Desde aperturas de emergencia hasta cambios completos de cerradura, Lockbuster Locksmith atiende trabajos residenciales, comerciales y automotrices en todo Jacksonville. Tecnicos con licencia, cotizacion gratis y una calificacion de 4.9 estrellas en 124 resenas de Google.",
    "4.9 · 124 reviews on Google": "4.9 · 124 resenas en Google",
    "Call (904) 454-5404": "Llama al (904) 454-5404",
    "Available": "Disponible",
    "Emergency service": "Servicio de emergencia",
    "reviews on Google": "resenas en Google",
    "Residential · Commercial · Auto": "Residencial · Comercial · Auto",
    "Estimates": "Cotizacion",
    "No hidden fees": "Sin cargos ocultos",
    "Call Now": "Llamar ahora",
    "Auto Locksmith": "Cerrajeria Automotriz",
    "One team,": "Un equipo,",
    "ready day or night": "listo de dia y de noche",
    "Lockbuster Locksmith is a 24-hour, mobile locksmith service covering the Jacksonville area: residential and commercial lockouts, automotive key and ignition work, lock installation and rekeying, high-security locks and access control systems. Technicians come to you, whether it is a home, a business or a car.":
        "Lockbuster Locksmith es un servicio de cerrajeria movil disponible las 24 horas en el area de Jacksonville: aperturas residenciales y comerciales, trabajo de llaves e ignicion automotriz, instalacion y cambio de cerraduras, cerraduras de alta seguridad y sistemas de control de acceso. Los tecnicos van hasta donde estes, ya sea una casa, un negocio o un auto.",
    "The result is a 4.9-star rating across 124 Google reviews and a 5.0 average on HomeAdvisor, with clients describing fast response times, fair pricing and technicians who get the job done the first time.":
        "El resultado es una calificacion de 4.9 estrellas en 124 resenas de Google y un promedio de 5.0 en HomeAdvisor, con clientes que describen tiempos de respuesta rapidos, precios justos y tecnicos que resuelven el trabajo a la primera.",
    "Licensed Technician": "Tecnico con Licencia",
    "Call anytime": "Llama cuando sea",
    "Call (904) 454-5404, 24 hours a day. Tell us if it is a home, business or vehicle lockout, or a lock job you need done.":
        "Llama al (904) 454-5404, las 24 horas. Cuentanos si es una apertura de casa, negocio o vehiculo, o un trabajo de cerradura que necesitas.",
    "Fast arrival": "Llegada rapida",
    "A licensed technician heads your way with the tools and stock to handle most lockouts, rekeys and lock installs on the first visit.":
        "Un tecnico con licencia va en camino con las herramientas y el inventario para resolver la mayoria de aperturas, cambios de llave e instalaciones en la primera visita.",
    "Diagnose &amp; quote": "Diagnostico y cotizacion",
    "You get a clear price before any work starts: free estimates on every job, whether it is a simple lockout or a full rekey.":
        "Recibes un precio claro antes de empezar cualquier trabajo: cotizacion gratis en cada servicio, ya sea una apertura simple o un cambio completo de llave.",
    "Job done right": "Trabajo bien hecho",
    "Doors unlocked, locks rekeyed or installed, keys cut and tested on the spot, so you are back to your day with working locks.":
        "Puertas abiertas, cerraduras cambiadas o instaladas, llaves cortadas y probadas en el momento, para que sigas tu dia con cerraduras que funcionan.",
    "Call for any": "Llama por cualquier",
    "lock or key job": "trabajo de cerradura o llave",
    "Every job gets a free estimate before any work starts. Call (904) 454-5404, 24 hours a day.":
        "Cada trabajo recibe una cotizacion gratis antes de empezar. Llama al (904) 454-5404, las 24 horas.",
    "24/7 Service": "Servicio 24/7",
    "Emergency Lockouts": "Aperturas de Emergencia",
    "Locked out of your home, business or car? A technician comes to you, any hour, with damage-free entry tools.":
        "Te quedaste afuera de tu casa, negocio o auto? Un tecnico llega hasta ti, a cualquier hora, con herramientas que no danan la cerradura.",
    "Free estimate": "Cotizacion gratis",
    "Call": "Llamar",
    "Most requested": "Lo mas solicitado",
    "Lock Rekey &amp; Installation": "Cambio e Instalacion de Cerraduras",
    "Rekey your existing locks, install new deadbolts and smart locks, or set up a master key system for a business.":
        "Cambia la combinacion de tus cerraduras actuales, instala cerrojos nuevos y cerraduras inteligentes, o configura un sistema de llave maestra para un negocio.",
    "Car Keys &amp; Ignition": "Llaves de Auto e Ignicion",
    "Key cutting, transponder and smart key programming, and ignition repair for most makes and models.":
        "Duplicado de llaves, programacion de llaves transponder e inteligentes, y reparacion de ignicion para la mayoria de marcas y modelos.",
    "Commercial": "Comercial",
    "Access Control &amp; Safes": "Control de Acceso y Cajas Fuertes",
    "Access control systems, master keying, and safe opening and repair for Jacksonville businesses.":
        "Sistemas de control de acceso, llaves maestras, y apertura y reparacion de cajas fuertes para negocios de Jacksonville.",
    "Free estimates on every job. Available 24 hours for emergency lockouts across Jacksonville. Call (904) 454-5404.":
        "Cotizacion gratis en cada trabajo. Disponibles las 24 horas para aperturas de emergencia en todo Jacksonville. Llama al (904) 454-5404.",
    "Real": "Trabajos",
    "jobs": "reales",
    "What Jacksonville": "Lo que dicen los",
    "customers say": "clientes en Jacksonville",
    "4.9 out of 5 on Google (124 reviews), plus a 5.0 average on HomeAdvisor": "4.9 de 5 en Google (124 resenas), mas un promedio de 5.0 en HomeAdvisor",
    "Read reviews on Google": "Lee las resenas en Google",
    "Hours": "Horario",
    "Available 24 hours a day, 7 days a week for emergency lockouts. Call anytime.":
        "Disponibles las 24 horas del dia, los 7 dias de la semana para aperturas de emergencia. Llama cuando sea.",
    "Reviews": "Resenas",
    "Read real reviews from Jacksonville customers on Google before you call.":
        "Lee resenas reales de clientes de Jacksonville en Google antes de llamar.",
    "24-hour locksmith service in Jacksonville, FL. Licensed and mobile.": "Servicio de cerrajeria las 24 horas en Jacksonville, FL. Con licencia y movil.",
    "Contact": "Contacto",
    "Follow": "Seguir",
    "Read Reviews on Google": "Lee las Resenas en Google",
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
