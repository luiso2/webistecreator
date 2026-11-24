import re
import colorsys

SLUG = "bestiesunlimited"
SRC = "templates/dark-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()

# ============================================================
# 0. Funciones de shift de color (ANTES de rep/rep_all: cualquier ancla
#    escrita con los hex/rgba ORIGINALES del esqueleto se busca ya
#    desplazada de paleta via S()).
# ============================================================
TARGET_HUE = 128 / 360.0   # kelly/forest green (distinto de esmeralda #2f7d5a ~153 y teal ~180)
SAT_MUL = 1.0
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
# 2. PALETA: gold (Pure Artistry) -> kelly/forest green (Besties Unlimited),
#    derivada del verde real visto en el logo/vinil de la vidriera.
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
# 3. GLOBALES: sin booking platform ni Instagram -> tel: + Maps directions
# ============================================================
NEW_TEL = "tel:+15618226505"
NEW_ADDR = "1533 Blue Heron Blvd, Riviera Beach, FL 33404"
NEW_MAPS = "https://www.google.com/maps?q=1533+Blue+Heron+Blvd,+Riviera+Beach,+FL+33404"

OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
rep_all(OLD_BOOK, NEW_TEL, expect=13)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
rep_all(OLD_IG_URL, NEW_MAPS, expect=6)

rep_all("@pure.artistrysk", '<span data-es="Como llegar" data-en="Get directions">Get directions</span>', expect=4)

# Icono: las 3 svg de Instagram -> glifo de pin de mapa (lucide map-pin)
IG_ICON_INNER = '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>'
PIN_ICON_INNER = '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>'
rep_all(IG_ICON_INNER, PIN_ICON_INNER, expect=3)
print("GLOBALS done")

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Besties Unlimited · Event Venue in Riviera Beach, FL | Parties &amp; Catering | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Besties Unlimited, Riviera Beach FL: a spacious private event venue for birthdays and celebrations, with custom decor, chiavari chairs and in-house catering. 5.0 with 10 reviews on Google." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Besties Unlimited · Event Venue in Riviera Beach, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Private event space for birthdays and celebrations. Custom decor, chiavari chairs, in-house catering. 5.0 on Google." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-party-room.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo-window-decal.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "EventVenue",
    "name": "Besties Unlimited",
    "description": "Private event venue in Riviera Beach, FL for birthdays, celebrations and private parties, with custom decor, chiavari chairs and in-house catering available on request.",
    "address": { "@type": "PostalAddress", "streetAddress": "1533 Blue Heron Blvd", "addressLocality": "Riviera Beach", "addressRegion": "FL", "postalCode": "33404", "addressCountry": "US" },
    "telephone": "+1-561-822-6505",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "10", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00" }
    ],
    "amenityFeature": [
      { "@type": "LocationFeatureSpecification", "name": "On-site parking" },
      { "@type": "LocationFeatureSpecification", "name": "In-house catering available" }
    ],
    "maximumAttendeeCapacity": 200
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
    '<span class="pre-mono">BU</span>\n    <span class="pre-word">Besties Unlimited</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    '<img src="assets/logo-window-decal.jpg" alt="Besties Unlimited" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Besties <span class="text-[color:var(--accent-deep)]">Unlimited</span></span>')
rep('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n          <span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Riviera Beach, FL · Event Venue" data-en="Riviera Beach, FL · Event Venue">Riviera Beach, FL · Event Venue</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Where every party becomes unforgettable." data-en="Where every party becomes unforgettable.">Where every party becomes unforgettable.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Private parties," data-en="Private parties,">Private parties,</span><br /><span data-es="hosted in " data-en="hosted in ">hosted in </span><span class="text-shine" data-es="full style" data-en="full style">full style</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="A spacious, fully styled event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private celebrations. Chiavari chairs, custom decor and in-house catering available on request, with a perfect 5.0 across 10 Google reviews." data-en="A spacious, fully styled event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private celebrations. Chiavari chairs, custom decor and in-house catering available on request, with a perfect 5.0 across 10 Google reviews.">A spacious, fully styled event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private celebrations. Chiavari chairs, custom decor and in-house catering available on request, with a perfect 5.0 across 10 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 10 reviews on Google" data-en="5.0 · 10 reviews on Google">5.0 · 10 reviews on Google</span>')
rep('''<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''',
    '''<span data-es="Call (561) 822-6505" data-en="Call (561) 822-6505">Call (561) 822-6505</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-party-room.jpg" alt="A fully styled birthday party room at Besties Unlimited in Riviera Beach, FL, with chiavari chairs and gold decor" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Hours" data-en="Hours">Hours</p>
            <p class="font-display text-lg">Mon - Fri</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="9 AM - 6 PM" data-en="9 AM - 6 PM">9 AM - 6 PM</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="10">10</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Parties <span class="text-shine">&amp;</span> Celebrations</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Birthdays · Showers · More" data-en="Birthdays · Showers · More">Birthdays · Showers · More</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">Up to 200</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Guest capacity" data-en="Guest capacity">Guest capacity</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Riviera Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1533 Blue Heron Blvd</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Private Parties"),
    ("Loc Retwist", "Birthday Celebrations"),
    ("Knotless Braids", "Full Venue Rental"),
    ("K-Tip Extensions", "In-House Catering"),
    ("Keratin", "Custom Decor"),
    ("Orlando, FL", "Riviera Beach, FL"),
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
          <img src="assets/about-birthday-celebration.jpg" alt="Guests celebrating a birthday party at Besties Unlimited, with a catering buffet set up in the background" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/about-event-setup.jpg" alt="The Besties Unlimited team setting up a red carpet entrance ahead of an event" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Celebrations," data-en="Celebrations,">Celebrations,</span><br /><span class="text-shine" data-es="handled with care" data-en="handled with care">handled with care</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Besties Unlimited is a private event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private parties. The room gets fully restyled for every event: chiavari chairs, custom backdrops, balloon installs and theme-matched linens." data-en="Besties Unlimited is a private event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private parties. The room gets fully restyled for every event: chiavari chairs, custom backdrops, balloon installs and theme-matched linens.">Besties Unlimited is a private event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private parties. The room gets fully restyled for every event: chiavari chairs, custom backdrops, balloon installs and theme-matched linens.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="The result is a perfect 5.0 rating across 10 Google reviews, with guests calling out the space, the vibe and, more than once, the in-house catering handling the food as well." data-en="The result is a perfect 5.0 rating across 10 Google reviews, with guests calling out the space, the vibe and, more than once, the in-house catering handling the food as well.">The result is a perfect 5.0 rating across 10 Google reviews, with guests calling out the space, the vibe and, more than once, the in-house catering handling the food as well.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="10">10</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Propio" data-en="In-House">In-House</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Catering disponible" data-en="Catering available">Catering available</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/logo-window-decal.jpg" alt="Besties Unlimited" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Besties Unlimited · <span class="text-[color:var(--ink-40)]" data-es="Riviera Beach, FL" data-en="Riviera Beach, FL">Riviera Beach, FL</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="From call to celebration" data-en="From call to celebration">From call to celebration</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Planning your event," data-en="Planning your event,">Planning your event,</span> <span class="text-shine" data-es="step by step" data-en="step by step">step by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Tell us the date" data-en="Tell us the date">Tell us the date</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (561) 822-6505 with your event date and guest count. Private events need at least two weeks notice." data-en="Call (561) 822-6505 with your event date and guest count. Private events need at least two weeks notice.">Call (561) 822-6505 with your event date and guest count. Private events need at least two weeks notice.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walk the space" data-en="Walk the space">Walk the space</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="See the room and go over chair and linen colors, decor options, and whether you want the in-house catering." data-en="See the room and go over chair and linen colors, decor options, and whether you want the in-house catering.">See the room and go over chair and linen colors, decor options, and whether you want the in-house catering.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Setup day" data-en="Setup day">Setup day</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The team transforms the room for your event: balloons, backdrop, table styling and chiavari chairs, all set before your guests arrive." data-en="The team transforms the room for your event: balloons, backdrop, table styling and chiavari chairs, all set before your guests arrive.">The team transforms the room for your event: balloons, backdrop, table styling and chiavari chairs, all set before your guests arrive.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Just celebrate" data-en="Just celebrate">Just celebrate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You and your guests enjoy a spotless, fully styled space while the team handles parking, food and the details." data-en="You and your guests enjoy a spotless, fully styled space while the team handles parking, food and the details.">You and your guests enjoy a spotless, fully styled space while the team handles parking, food and the details.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS (variante adaptada: sin precios, "se cotiza")
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Celebrations built around" data-en="Celebrations built around">Celebrations built around</span> <span class="text-shine" data-es="your event" data-en="your event">your event</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every event gets its own look and price. Call with your date and guest count for a quote." data-en="Every event gets its own look and price. Call with your date and guest count for a quote.">Every event gets its own look and price. Call with your date and guest count for a quote.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most booked" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Private Parties &amp; Celebrations" data-en="Private Parties &amp; Celebrations">Private Parties &amp; Celebrations</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Birthdays, showers and life celebrations hosted in a spotless, fully styled room, reviewers call it spacious and beautifully maintained." data-en="Birthdays, showers and life celebrations hosted in a spotless, fully styled room, reviewers call it spacious and beautifully maintained.">Birthdays, showers and life celebrations hosted in a spotless, fully styled room, reviewers call it spacious and beautifully maintained.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="The whole room" data-en="The whole room">The whole room</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Venue Rental" data-en="Full Venue Rental">Full Venue Rental</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A private room for up to 200 guests, with chiavari chairs, round tables and on-site parking that fills up fast on event days." data-en="A private room for up to 200 guests, with chiavari chairs, round tables and on-site parking that fills up fast on event days.">A private room for up to 200 guests, with chiavari chairs, round tables and on-site parking that fills up fast on event days.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Food handled" data-en="Food handled">Food handled</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="In-House Catering" data-en="In-House Catering">In-House Catering</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Reviewers single out the food, wings and Philly cheesesteaks among their favorites, catering handled start to finish on site." data-en="Reviewers single out the food, wings and Philly cheesesteaks among their favorites, catering handled start to finish on site.">Reviewers single out the food, wings and Philly cheesesteaks among their favorites, catering handled start to finish on site.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="The look" data-en="The look">The look</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Event Styling &amp; Decor" data-en="Event Styling &amp; Decor">Event Styling &amp; Decor</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Balloon installs, neon signage, themed backdrops and table styling, built to match every birthday, shower or theme night." data-en="Balloon installs, neon signage, themed backdrops and table styling, built to match every birthday, shower or theme night.">Balloon installs, neon signage, themed backdrops and table styling, built to match every birthday, shower or theme night.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every event is quoted" data-en="Every event is quoted">Every event is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Event Types" data-en="Event Types">Event Types</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Birthday parties" data-en="Birthday parties">Birthday parties</li>
            <li class="flex items-center gap-2" data-es="Baby &amp; bridal showers" data-en="Baby &amp; bridal showers">Baby &amp; bridal showers</li>
            <li class="flex items-center gap-2" data-es="Graduations" data-en="Graduations">Graduations</li>
            <li class="flex items-center gap-2" data-es="Private gatherings" data-en="Private gatherings">Private gatherings</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Always Included" data-en="Always Included">Always Included</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Chiavari chairs &amp; tables" data-en="Chiavari chairs &amp; tables">Chiavari chairs &amp; tables</li>
            <li class="flex items-center gap-2" data-es="Table linens" data-en="Table linens">Table linens</li>
            <li class="flex items-center gap-2" data-es="On-site parking" data-en="On-site parking">On-site parking</li>
            <li class="flex items-center gap-2" data-es="Custom decor setup" data-en="Custom decor setup">Custom decor setup</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Good To Know" data-en="Good To Know">Good To Know</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Up to 200 guests" data-en="Up to 200 guests">Up to 200 guests</li>
            <li class="flex items-center gap-2" data-es="Book 2+ weeks ahead" data-en="Book 2+ weeks ahead">Book 2+ weeks ahead</li>
            <li class="flex items-center gap-2" data-es="In-house catering available" data-en="In-house catering available">In-house catering available</li>
            <li class="flex items-center gap-2" data-es="Located in Blue Heron Apartments" data-en="Located in Blue Heron Apartments">Located in Blue Heron Apartments</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + S(NEW_SERVICES_GRID) + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Every event is quoted to match your date, guest count and decor. Call (561) 822-6505 to check availability." data-en="Every event is quoted to match your date, guest count and decor. Call (561) 822-6505 to check availability.">Every event is quoted to match your date, guest count and decor. Call (561) 822-6505 to check availability.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="parties" data-en="parties">parties</span>')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Sala montada para una fiesta de cumpleanos" data-en="The room, fully styled for a birthday party">The room, fully styled for a birthday party</span><img src="assets/hero-party-room.jpg" alt="The event room at Besties Unlimited styled in black and gold for a birthday celebration, with chiavari chairs and balloon garlands" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Montaje elegante de mesas" data-en="An elegant table setup">An elegant table setup</span><img src="assets/gallery-elegant-setup.jpg" alt="An elegant navy and white table setup at Besties Unlimited with chair covers and place settings" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Postres del catering propio" data-en="In-house dessert tower">In-house dessert tower</span><img src="assets/gallery-dessert-tower.jpg" alt="A tiered dessert cup tower with lit candles, catered in-house at Besties Unlimited" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Decoracion tematica a medida" data-en="Fully themed event decor">Fully themed event decor</span><img src="assets/gallery-cousins-weekend.jpg" alt="A themed teal, black and silver event setup at Besties Unlimited with custom balloon garlands and signage" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + S(NEW_GALLERY_GRID) + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Riviera Beach" data-en="What Riviera Beach">What Riviera Beach</span> <span class="text-shine" data-es="guests say" data-en="guests say">guests say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 10 reviews on Google" data-en="5.0 out of 5 · 10 reviews on Google">5.0 out of 5 · 10 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I recently attended a birthday party at this venue, and let me tell you! The space was impressive. Spacious throughout, spotless, and beautifully maintained. They even handled the catering, and the wings and Philly cheesesteak were hands down my favorites. I will definitely book my next event here!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dee Jay</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I went to a birthday party and the place was amazing. I truly recommend Besties Unlimited if you want a nice and spacious venue."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Robert Pittman</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Besties Unlimited is a perfect destination for hosting any and all occasions."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Keera Adams</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://www.google.com/maps/place/Besties+Unlimited/data=!4m7!3m6!1s0x88d8d57995b9c0f3:0xe9b0ee64626dbc79!8m2!3d26.7813233!4d-80.0790183!16s%2Fg%2F11xy_gvj1d!19sChIJ88C5lXnV2IgRebxtYmTusOk" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all reviews on Google" data-en="Read all reviews on Google">Read all reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Riviera Beach</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Friday, 9 AM to 6 PM. Closed Saturday and Sunday. Private events need 2+ weeks notice." data-en="Monday to Friday, 9 AM to 6 PM. Closed Saturday and Sunday. Private events need 2+ weeks notice.">Monday to Friday, 9 AM to 6 PM. Closed Saturday and Sunday. Private events need 2+ weeks notice.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (561) 822-6505" data-en="Call (561) 822-6505">Call (561) 822-6505</a>''')
rep('''<p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener"><span data-es="Como llegar" data-en="Get directions">Get directions</span></a>''',
    '''<p class="font-medium mb-1" data-es="Parking" data-en="Parking">Parking</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="On-site parking is available, but it fills up fast on event days, so guests should plan to arrive early." data-en="On-site parking is available, but it fills up fast on event days, so guests should plan to arrive early.">On-site parking is available, but it fills up fast on event days, so guests should plan to arrive early.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>''')
rep('<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Map: Besties Unlimited, 1533 Blue Heron Blvd, Riviera Beach FL"\n          src="' + NEW_MAPS + '&output=embed"')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Where every party becomes unforgettable." data-en="Where every party becomes unforgettable.">Where every party becomes unforgettable.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu proximo evento" data-en="Your next event">Your next event</span> <span class="text-shine" data-es="empieza con una llamada" data-en="starts with a call">starts with a call</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (561) 822-6505 for a free quote on your birthday, shower or private celebration. The team handles the decor, the room and the catering." data-en="Call (561) 822-6505 for a free quote on your birthday, shower or private celebration. The team handles the decor, the room and the catering.">Call (561) 822-6505 for a free quote on your birthday, shower or private celebration. The team handles the decor, the room and the catering.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (561) 822-6505" data-en="Call (561) 822-6505">Call (561) 822-6505</a>
        <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Get directions" data-en="Get directions">Get directions</a>''')
print("CTA FINAL done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Besties Unlimited</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo-window-decal.jpg" alt="Besties Unlimited" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Besties Unlimited</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Private event venue in Riviera Beach, FL. Private events by appointment." data-en="Private event venue in Riviera Beach, FL. Private events by appointment.">Private event venue in Riviera Beach, FL. Private events by appointment.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#e9c3ab]" data-es="Call (561) 822-6505" data-en="Call (561) 822-6505">Call (561) 822-6505</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · <span data-es="Como llegar" data-en="Get directions">Get directions</span></a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Find Us" data-en="Find Us">Find Us</p>
        <p><a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Get directions" data-en="Get directions">Get directions</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Besties Unlimited.</p>')
print("FOOTER done")

# ============================================================
# 18. Boton flotante (icono calendario -> telefono)
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Besties Unlimited">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>\n  </a>')
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
    "Riviera Beach, FL · Event Venue": "Riviera Beach, FL · Salon de Eventos",
    "Where every party becomes unforgettable.": "Donde cada fiesta se vuelve inolvidable.",
    "Private parties,": "Fiestas privadas,",
    "hosted in ": "organizadas con ",
    "full style": "mucho estilo",
    "A spacious, fully styled event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private celebrations. Chiavari chairs, custom decor and in-house catering available on request, with a perfect 5.0 across 10 Google reviews.":
        "Un espacio de eventos amplio y completamente decorado en Blue Heron Blvd, Riviera Beach, pensado para cumpleanos, baby showers y celebraciones privadas. Sillas chiavari, decoracion a medida y catering propio disponible, con un 5.0 perfecto en 10 resenas de Google.",
    "5.0 · 10 reviews on Google": "5.0 · 10 resenas en Google",
    "Call (561) 822-6505": "Llama al (561) 822-6505",
    "Hours": "Horario",
    "9 AM - 6 PM": "9 AM - 6 PM",
    "reviews on Google": "resenas en Google",
    "Birthdays · Showers · More": "Cumpleanos · Showers · Mas",
    "Guest capacity": "Capacidad de invitados",
    "Celebrations,": "Celebraciones,",
    "handled with care": "atendidas con cuidado",
    "Besties Unlimited is a private event space on Blue Heron Blvd in Riviera Beach, built for birthdays, showers and private parties. The room gets fully restyled for every event: chiavari chairs, custom backdrops, balloon installs and theme-matched linens.":
        "Besties Unlimited es un espacio de eventos privado en Blue Heron Blvd, Riviera Beach, pensado para cumpleanos, showers y fiestas privadas. La sala se redecora por completo para cada evento: sillas chiavari, fondos a medida, instalaciones de globos y manteleria a juego con el tema.",
    "The result is a perfect 5.0 rating across 10 Google reviews, with guests calling out the space, the vibe and, more than once, the in-house catering handling the food as well.":
        "El resultado es una calificacion perfecta de 5.0 en 10 resenas de Google, con invitados que destacan el espacio, el ambiente y, mas de una vez, el catering propio que tambien se encarga de la comida.",
    "From call to celebration": "De la llamada a la celebracion",
    "Planning your event,": "Planear tu evento,",
    "step by step": "paso a paso",
    "Tell us the date": "Cuentanos la fecha",
    "Call (561) 822-6505 with your event date and guest count. Private events need at least two weeks notice.":
        "Llama al (561) 822-6505 con la fecha de tu evento y el numero de invitados. Los eventos privados necesitan al menos dos semanas de aviso.",
    "Walk the space": "Conoce el espacio",
    "See the room and go over chair and linen colors, decor options, and whether you want the in-house catering.":
        "Conoce la sala y revisa colores de sillas y manteleria, opciones de decoracion, y si quieres el catering propio.",
    "Setup day": "Dia del montaje",
    "The team transforms the room for your event: balloons, backdrop, table styling and chiavari chairs, all set before your guests arrive.":
        "El equipo transforma la sala para tu evento: globos, fondo decorativo, montaje de mesas y sillas chiavari, todo listo antes de que lleguen tus invitados.",
    "Just celebrate": "Solo celebra",
    "You and your guests enjoy a spotless, fully styled space while the team handles parking, food and the details.":
        "Tu y tus invitados disfrutan de un espacio impecable y decorado por completo mientras el equipo se encarga del estacionamiento, la comida y los detalles.",
    "Celebrations built around": "Celebraciones hechas",
    "your event": "para tu evento",
    "Every event gets its own look and price. Call with your date and guest count for a quote.":
        "Cada evento tiene su propio estilo y precio. Llama con tu fecha y numero de invitados para una cotizacion.",
    "Most booked": "Lo mas reservado",
    "Private Parties &amp; Celebrations": "Fiestas Privadas y Celebraciones",
    "Birthdays, showers and life celebrations hosted in a spotless, fully styled room, reviewers call it spacious and beautifully maintained.":
        "Cumpleanos, showers y celebraciones de vida en una sala impecable y completamente decorada, las resenas la describen como espaciosa y muy bien mantenida.",
    "Every event is quoted": "Cada evento se cotiza",
    "Call": "Llamar",
    "The whole room": "Toda la sala",
    "Full Venue Rental": "Alquiler del Salon Completo",
    "A private room for up to 200 guests, with chiavari chairs, round tables and on-site parking that fills up fast on event days.":
        "Una sala privada para hasta 200 invitados, con sillas chiavari, mesas redondas y estacionamiento en el lugar que se llena rapido los dias de evento.",
    "Food handled": "La comida resuelta",
    "In-House Catering": "Catering Propio",
    "Reviewers single out the food, wings and Philly cheesesteaks among their favorites, catering handled start to finish on site.":
        "Las resenas destacan la comida, las alitas y los Philly cheesesteaks entre sus favoritos, catering atendido de principio a fin en el lugar.",
    "The look": "El estilo",
    "Event Styling &amp; Decor": "Decoracion y Ambientacion",
    "Balloon installs, neon signage, themed backdrops and table styling, built to match every birthday, shower or theme night.":
        "Instalaciones de globos, letreros de neon, fondos tematicos y montaje de mesas, hechos a la medida de cada cumpleanos, shower o noche tematica.",
    "Event Types": "Tipos de Evento",
    "Birthday parties": "Fiestas de cumpleanos",
    "Baby &amp; bridal showers": "Baby y bridal showers",
    "Graduations": "Graduaciones",
    "Private gatherings": "Reuniones privadas",
    "Always Included": "Siempre Incluido",
    "Chiavari chairs &amp; tables": "Sillas chiavari y mesas",
    "Table linens": "Manteleria",
    "On-site parking": "Estacionamiento en el lugar",
    "Custom decor setup": "Montaje de decoracion a medida",
    "Good To Know": "Bueno Saber",
    "Up to 200 guests": "Hasta 200 invitados",
    "Book 2+ weeks ahead": "Reserva con 2+ semanas de anticipacion",
    "In-house catering available": "Catering propio disponible",
    "Located in Blue Heron Apartments": "Ubicado en Blue Heron Apartments",
    "Every event is quoted to match your date, guest count and decor. Call (561) 822-6505 to check availability.":
        "Cada evento se cotiza segun tu fecha, numero de invitados y decoracion. Llama al (561) 822-6505 para consultar disponibilidad.",
    "Real": "Fiestas",
    "parties": "reales",
    "What Riviera Beach": "Lo que dicen los",
    "guests say": "invitados en Riviera Beach",
    "5.0 out of 5 · 10 reviews on Google": "5.0 de 5 · 10 resenas en Google",
    "Read all reviews on Google": "Lee todas las resenas en Google",
    "Get directions": "Como llegar",
    "Monday to Friday, 9 AM to 6 PM. Closed Saturday and Sunday. Private events need 2+ weeks notice.":
        "Lunes a viernes, 9 AM a 6 PM. Cerrado sabado y domingo. Los eventos privados necesitan 2+ semanas de aviso.",
    "Parking": "Estacionamiento",
    "On-site parking is available, but it fills up fast on event days, so guests should plan to arrive early.":
        "Hay estacionamiento en el lugar, pero se llena rapido los dias de evento, asi que los invitados deben planear llegar temprano.",
    "Call (561) 822-6505 for a free quote on your birthday, shower or private celebration. The team handles the decor, the room and the catering.":
        "Llama al (561) 822-6505 para una cotizacion gratis de tu cumpleanos, shower o celebracion privada. El equipo se encarga de la decoracion, la sala y el catering.",
    "Private event venue in Riviera Beach, FL. Private events by appointment.":
        "Salon de eventos privado en Riviera Beach, FL. Eventos privados con cita previa.",
    "Contact": "Contacto",
    "Find Us": "Encuentranos",
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
