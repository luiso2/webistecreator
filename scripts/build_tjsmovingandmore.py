import re
import colorsys
import shutil

SLUG = "tjs-moving-and-more"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/light-v2/index.html", PATH)
h = open(PATH, encoding="utf-8").read()


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


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> teal-cyan (Tjs Moving and More, SWFL)
# ---------------------------------------------------------------------------
TARGET_HUE = 180 / 360.0
SAT_MUL = 1.0


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


_HEXES = ["#a04a72", "#5c2140", "#f0bed7", "#faf2f6", "#c47a9c", "#8a5573", "#f3e0ea", "#d9a8c2",
          "#7d3457", "#5f2c48", "#33222c", "#fbf3f8", "#fbeff5", "#f8dfeb", "#f6f1ea", "#f2d5e3",
          "#f2cfe0", "#efd0e0", "#e5c1d4", "#dc9dbe", "#d3a2bc", "#c9789f", "#b25a85", "#2a1722",
          "#1f0f18", "#1c0f16"]
_RGBAS = [(160, 74, 114), (51, 34, 44), (240, 190, 215), (70, 25, 50), (250, 242, 246),
          (125, 52, 87), (253, 246, 250), (40, 16, 30), (233, 205, 186), (185, 138, 128)]

for hx in _HEXES:
    rep_all(hx, _shift_hex(hx))

for rgb in _RGBAS:
    r2, g2, b2 = _shift_rgb(rgb)
    pattern = re.compile(r'rgba\(' + f'{rgb[0]},{rgb[1]},{rgb[2]}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({rgb[0]},{rgb[1]},{rgb[2]},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

RING = "rgba(74,160,160"  # shifted (160,74,114) ring/border color, reused below
HOVERHEX = "#bef0f0"       # shifted #f0bed7 footer hover

# ---------------------------------------------------------------------------
# 3. Globales: sin booking/IG/email -> tel: + Google reviews
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+12394405374"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Tjs+Moving+and+More+Cape+Coral+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=Cape+Coral,+FL"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Tjs Moving and More · Moving Company in Cape Coral, FL | 4.7 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Tjs Moving and More, Cape Coral FL: local moving, packing and loading help, available 24 hours a day. 4.7 stars across 18 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Tjs Moving and More · Moving Company in Cape Coral, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Local moving, packing and loading help, available 24/7. 4.7 on Google with 18 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-office-move.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MovingCompany",
    "name": "Tjs Moving and More",
    "description": "Moving company serving Cape Coral and Fort Myers, FL: local moving, packing and loading help, available 24 hours a day.",
    "areaServed": "Cape Coral, FL",
    "telephone": "+1-239-440-5374",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "18", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Moving services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Local Moving" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Packing &amp; Loading Help" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Office &amp; Commercial Moves" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "U-Haul &amp; Truck Loading" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: EN (resenas en ingles)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.35)]" />',
    '<img src="assets/logo.jpg" alt="Tjs Moving and More" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Tjs <span class="text-[color:var(--accent-deep)]">Moving</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">TM</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Tjs Moving</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Cape Coral, FL · Moving Company" data-en="Cape Coral, FL · Moving Company">Cape Coral, FL · Moving Company</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Moving help, 24/7." data-en="Moving help, 24/7.">Moving help, 24/7.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Local moving and" data-en="Local moving and">Local moving and</span><br /><span data-es="loading help, " data-en="loading help, ">loading help, </span><span class="text-shine" data-es="on call" data-en="on call">on call</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Local moving, packing and loading help across Cape Coral and Fort Myers, available 24 hours a day. The same careful crew for a single room or a full house." data-en="Local moving, packing and loading help across Cape Coral and Fort Myers, available 24 hours a day. The same careful crew for a single room or a full house.">Local moving, packing and loading help across Cape Coral and Fort Myers, available 24 hours a day. The same careful crew for a single room or a full house.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.7 · 18 reviews on Google" data-en="4.7 · 18 reviews on Google">4.7 · 18 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (239) 440-5374" data-en="Call (239) 440-5374">Call (239) 440-5374</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-office-move.jpg" alt="Boxes packed and staged by Tjs Moving and More for an office relocation in Cape Coral, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Available" data-en="Available">Available</p>
            <p class="font-display text-lg">24/7</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="18">18</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Moving <span class="text-shine">&amp;</span> Loading</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Packing · Labor help" data-en="Packing · Labor help">Packing · Labor help</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">24/7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Availability" data-en="Availability">Availability</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Cape Coral</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Southwest Florida" data-en="Southwest Florida">Southwest Florida</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Local Moves"),
    ("Hybrid Set", "Loading Help"),
    ("Volume Set", "Packing Service"),
    ("Mega Volume", "Office Moves"),
    ("Bottom Lashes", "U-Haul Loading"),
    ("West Palm Beach, FL", "Cape Coral, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-1 gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal">
          <img src="assets/about-home-move.jpg" alt="Household items carefully packed by Tjs Moving and More before a move in Cape Coral, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One crew," data-en="One crew,">One crew,</span><br /><span class="text-shine" data-es="careful with every load" data-en="careful with every load">careful with every load</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Tjs Moving and More handles local moves, office relocations and loading help across Cape Coral and Fort Myers. Crews led by Micah and Joseph are known for showing up on time and working fast without rushing the job." data-en="Tjs Moving and More handles local moves, office relocations and loading help across Cape Coral and Fort Myers. Crews led by Micah and Joseph are known for showing up on time and working fast without rushing the job.">Tjs Moving and More handles local moves, office relocations and loading help across Cape Coral and Fort Myers. Crews led by Micah and Joseph are known for showing up on time and working fast without rushing the job.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.7 rating across 18 Google reviews, and customers who call back for every move after." data-en="The result: a 4.7 rating across 18 Google reviews, and customers who call back for every move after.">The result: a 4.7 rating across 18 Google reviews, and customers who call back for every move after.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="18">18</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Disponibilidad" data-en="Availability">Availability</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Tjs Moving and More" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Tjs Moving and More · <span class="text-[color:var(--ink-40)]" data-es="Moving crew" data-en="Moving crew">Moving crew</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your move," data-en="Your move,">Your move,</span> <span class="text-shine" data-es="handled with care" data-en="handled with care">handled with care</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call to book" data-en="Call to book">Call to book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (239) 440-5374 with your move date, and get a straightforward price over the phone, any day of the week." data-en="Call (239) 440-5374 with your move date, and get a straightforward price over the phone, any day of the week.">Call (239) 440-5374 with your move date, and get a straightforward price over the phone, any day of the week.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Packing &amp; loading" data-en="Packing &amp; loading">Packing &amp; loading</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew carefully wraps furniture and loads boxes, trucks or U-Haul trailers so nothing shifts on the road." data-en="The crew carefully wraps furniture and loads boxes, trucks or U-Haul trailers so nothing shifts on the road.">The crew carefully wraps furniture and loads boxes, trucks or U-Haul trailers so nothing shifts on the road.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Careful transport" data-en="Careful transport">Careful transport</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Your things are driven safely to the new address, with the same attention the whole way." data-en="Your things are driven safely to the new address, with the same attention the whole way.">Your things are driven safely to the new address, with the same attention the whole way.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Unload &amp; done" data-en="Unload &amp; done">Unload &amp; done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew unloads and places everything where you want it, then walks the job with you before leaving." data-en="The crew unloads and places everything where you want it, then walks the job with you before leaving.">The crew unloads and places everything where you want it, then walks the job with you before leaving.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine" data-es="every move" data-en="every move">every move</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two moves are the same, so every job gets a straightforward phone quote, any time of day." data-en="No two moves are the same, so every job gets a straightforward phone quote, any time of day.">No two moves are the same, so every job gets a straightforward phone quote, any time of day.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: ''' + RING + ''',0.4); box-shadow: 0 18px 50px rgba(34,51,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Local Moving" data-en="Local Moving">Local Moving</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service local moves across Cape Coral and Fort Myers, from single rooms to full households." data-en="Full-service local moves across Cape Coral and Fort Myers, from single rooms to full households.">Full-service local moves across Cape Coral and Fort Myers, from single rooms to full households.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="By the hour" data-en="By the hour">By the hour</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Packing &amp; Loading Help" data-en="Packing &amp; Loading Help">Packing &amp; Loading Help</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Hourly moving labor to pack, load or unload a truck or storage unit, with careful handling throughout." data-en="Hourly moving labor to pack, load or unload a truck or storage unit, with careful handling throughout.">Hourly moving labor to pack, load or unload a truck or storage unit, with careful handling throughout.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Business moves" data-en="Business moves">Business moves</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Office &amp; Commercial Moves" data-en="Office &amp; Commercial Moves">Office &amp; Commercial Moves</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Office relocations and commercial moves handled with the same punctual, careful crew." data-en="Office relocations and commercial moves handled with the same punctual, careful crew.">Office relocations and commercial moves handled with the same punctual, careful crew.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="DIY movers" data-en="DIY movers">DIY movers</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="U-Haul &amp; Truck Loading" data-en="U-Haul &amp; Truck Loading">U-Haul &amp; Truck Loading</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Loading and unloading help for your own rental truck or trailer, including long-distance moves." data-en="Loading and unloading help for your own rental truck or trailer, including long-distance moves.">Loading and unloading help for your own rental truck or trailer, including long-distance moves.</p>
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
            <li class="flex items-center gap-2" data-es="Local moves" data-en="Local moves">Local moves</li>
            <li class="flex items-center gap-2" data-es="Office moves" data-en="Office moves">Office moves</li>
            <li class="flex items-center gap-2" data-es="Apartment moves" data-en="Apartment moves">Apartment moves</li>
            <li class="flex items-center gap-2" data-es="Full house moves" data-en="Full house moves">Full house moves</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Labor Help" data-en="Labor Help">Labor Help</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Loading &amp; unloading" data-en="Loading &amp; unloading">Loading &amp; unloading</li>
            <li class="flex items-center gap-2" data-es="Packing &amp; wrapping" data-en="Packing &amp; wrapping">Packing &amp; wrapping</li>
            <li class="flex items-center gap-2" data-es="Furniture rearranging" data-en="Furniture rearranging">Furniture rearranging</li>
            <li class="flex items-center gap-2" data-es="Storage unit help" data-en="Storage unit help">Storage unit help</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Availability" data-en="Availability">Availability</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Open 24 hours" data-en="Open 24 hours">Open 24 hours</li>
            <li class="flex items-center gap-2" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</li>
            <li class="flex items-center gap-2" data-es="Same-day service" data-en="Same-day service">Same-day service</li>
            <li class="flex items-center gap-2" data-es="Flexible scheduling" data-en="Flexible scheduling">Flexible scheduling</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on crew size and job length. Call (239) 440-5374 for a free quote." data-en="Pricing depends on crew size and job length. Call (239) 440-5374 for a free quote.">Pricing depends on crew size and job length. Call (239) 440-5374 for a free quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="moving days" data-en="moving days">moving days</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Mudanza comercial, cargada con cuidado" data-en="Commercial relocation, carefully loaded">Commercial relocation, carefully loaded</span><img src="assets/gallery-commercial-load.jpg" alt="An office relocation packed and staged by Tjs Moving and More in Cape Coral, FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Camion empacado y asegurado" data-en="Truck packed and secured">Truck packed and secured</span><img src="assets/gallery-truck-packed.jpg" alt="A moving truck packed and secured by Tjs Moving and More" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cada caja en su lugar" data-en="Every box accounted for">Every box accounted for</span><img src="assets/gallery-storage-totes.jpg" alt="Totes and boxes organized inside a Tjs Moving and More truck" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Listo para el camino" data-en="Ready for the road">Ready for the road</span><img src="assets/gallery-suitcases.jpg" alt="Suitcases and furniture packed securely by Tjs Moving and More" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Empacado con cuidado" data-en="Packed with care">Packed with care</span><img src="assets/gallery-boxes-ladder.jpg" alt="Boxes and equipment packed with care by Tjs Moving and More" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Cape Coral" data-en="What Cape Coral">What Cape Coral</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.7 out of 5 · 18 reviews on Google" data-en="4.7 out of 5 · 18 reviews on Google">4.7 out of 5 · 18 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We had a great experience with TJ's Movers! The crew, led by Micah, was punctual and careful with all of our belongings. They worked efficiently, maintaining a great pace while still taking the time to handle everything with care..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Valtenius Beltrao</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I recently hired TJ's Moving and More for my recent move, and I couldn't be more pleased with their service! From the moment they arrived, they were punctual, showing up right on time, which immediately set a positive tone for the day..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rich Ressler</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We hired TJ's to load our U-haul for our move from SWFL to KY. Our crew was led by Joseph &amp; they were awesome. They helped us out of a bind when we couldn't fit all of our belongings onto the truck &amp; trailer, going above &amp; beyond..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karla Koenig</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 18 reviews on Google" data-en="Read all 18 reviews on Google">Read all 18 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (sin direccion fija: area de servicio)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Cape Coral, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Tjs Moving and More serves Cape Coral, Fort Myers and the surrounding Southwest Florida area, 24 hours a day." data-en="Tjs Moving and More serves Cape Coral, Fort Myers and the surrounding Southwest Florida area, 24 hours a day.">Tjs Moving and More serves Cape Coral, Fort Myers and the surrounding Southwest Florida area, 24 hours a day.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open 24 hours, every day of the week." data-en="Open 24 hours, every day of the week.">Open 24 hours, every day of the week.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_TEL + '''" data-es="Call (239) 440-5374" data-en="Call (239) 440-5374">Call (239) 440-5374</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="font-medium mb-1" data-es="Reviews" data-en="Reviews">Reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.7 stars across 18 Google reviews." data-en="4.7 stars across 18 Google reviews.">4.7 stars across 18 Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Tjs Moving and More service area, Cape Coral FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Moving help, 24/7." data-en="Moving help, 24/7.">Moving help, 24/7.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call" data-en="One call">One call</span> <span class="text-shine" data-es="gets it moving" data-en="gets it moving">gets it moving</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (239) 440-5374 for a free, straightforward quote on your move or loading job. Available 24 hours a day, every day." data-en="Call (239) 440-5374 for a free, straightforward quote on your move or loading job. Available 24 hours a day, every day.">Call (239) 440-5374 for a free, straightforward quote on your move or loading job. Available 24 hours a day, every day.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (239) 440-5374" data-en="Call (239) 440-5374">Call (239) 440-5374</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Tjs Moving</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,240,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Tjs Moving and More" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,240,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Tjs Moving and More</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Mudanzas y ayuda de carga en Cape Coral, FL. Disponible 24/7." data-en="Moving and loading help serving Cape Coral, FL. Available 24/7.">Moving and loading help serving Cape Coral, FL. Available 24/7.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Sirviendo a Cape Coral, FL" data-en="Serving Cape Coral, FL">Serving Cape Coral, FL</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[''' + HOVERHEX + ''']" data-es="Call (239) 440-5374" data-en="Call (239) 440-5374">Call (239) 440-5374</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']">4.7 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Tjs Moving and More.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Tjs Moving and More">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 20. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace(f'href="{NEW_TEL}" target="_blank" rel="noopener"', f'href="{NEW_TEL}"')
print("CLEANUP tel links done")

# ---------------------------------------------------------------------------
# 21. Traduccion ES real para todos los textos NUEVOS (bilingue obligatorio)
# ---------------------------------------------------------------------------
T = {
    "Cape Coral, FL · Moving Company": "Cape Coral, FL · Empresa de Mudanzas",
    "Moving help, 24/7.": "Ayuda de mudanza, 24/7.",
    "Local moving and": "Mudanzas locales y",
    "loading help, ": "ayuda de carga, ",
    "on call": "al instante",
    "Local moving, packing and loading help across Cape Coral and Fort Myers, available 24 hours a day. The same careful crew for a single room or a full house.":
        "Mudanzas locales, empaque y ayuda de carga en Cape Coral y Fort Myers, disponibles las 24 horas. El mismo equipo cuidadoso para una sola habitacion o una casa completa.",
    "4.7 · 18 reviews on Google": "4.7 · 18 resenas en Google",
    "Call (239) 440-5374": "Llama al (239) 440-5374",
    "Available": "Disponible",
    "Every day of the week": "Todos los dias de la semana",
    "Packing · Labor help": "Empaque · Ayuda de carga",
    "Southwest Florida": "Suroeste de Florida",
    "careful with every load": "cuidadoso con cada carga",
    "Tjs Moving and More handles local moves, office relocations and loading help across Cape Coral and Fort Myers. Crews led by Micah and Joseph are known for showing up on time and working fast without rushing the job.":
        "Tjs Moving and More maneja mudanzas locales, reubicaciones de oficina y ayuda de carga en Cape Coral y Fort Myers. Los equipos liderados por Micah y Joseph son conocidos por llegar a tiempo y trabajar rapido sin apresurar el trabajo.",
    "The result: a 4.7 rating across 18 Google reviews, and customers who call back for every move after.":
        "El resultado: una calificacion de 4.7 en 18 resenas de Google, y clientes que vuelven a llamar para cada mudanza despues.",
    "Moving crew": "Equipo de mudanzas",
    "handled with care": "manejada con cuidado",
    "Call to book": "Llama para reservar",
    "Call (239) 440-5374 with your move date, and get a straightforward price over the phone, any day of the week.":
        "Llama al (239) 440-5374 con la fecha de tu mudanza, y recibe un precio claro por telefono, cualquier dia de la semana.",
    "Packing &amp; loading": "Empaque y carga",
    "The crew carefully wraps furniture and loads boxes, trucks or U-Haul trailers so nothing shifts on the road.":
        "El equipo envuelve los muebles con cuidado y carga cajas, camiones o trailers U-Haul para que nada se mueva en el camino.",
    "Careful transport": "Transporte cuidadoso",
    "Your things are driven safely to the new address, with the same attention the whole way.":
        "Tus cosas se transportan de forma segura a la nueva direccion, con la misma atencion todo el camino.",
    "Unload &amp; done": "Descarga y listo",
    "The crew unloads and places everything where you want it, then walks the job with you before leaving.":
        "El equipo descarga y coloca todo donde lo quieras, y revisa el trabajo contigo antes de irse.",
    "every move": "cada mudanza",
    "No two moves are the same, so every job gets a straightforward phone quote, any time of day.":
        "Ninguna mudanza es igual, asi que cada trabajo recibe una cotizacion clara por telefono, a cualquier hora.",
    "Most requested": "Lo mas solicitado",
    "Local Moving": "Mudanzas Locales",
    "Full-service local moves across Cape Coral and Fort Myers, from single rooms to full households.":
        "Mudanzas locales completas en Cape Coral y Fort Myers, desde una sola habitacion hasta casas completas.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "By the hour": "Por hora",
    "Packing &amp; Loading Help": "Empaque y Ayuda de Carga",
    "Hourly moving labor to pack, load or unload a truck or storage unit, with careful handling throughout.":
        "Mano de obra de mudanza por hora para empacar, cargar o descargar un camion o unidad de almacenaje, con manejo cuidadoso en todo momento.",
    "Business moves": "Mudanzas de negocios",
    "Office &amp; Commercial Moves": "Mudanzas de Oficina y Comerciales",
    "Office relocations and commercial moves handled with the same punctual, careful crew.":
        "Reubicaciones de oficina y mudanzas comerciales manejadas por el mismo equipo puntual y cuidadoso.",
    "DIY movers": "Mudanza por tu cuenta",
    "U-Haul &amp; Truck Loading": "Carga de U-Haul y Camiones",
    "Loading and unloading help for your own rental truck or trailer, including long-distance moves.":
        "Ayuda de carga y descarga para tu propio camion o trailer de renta, incluyendo mudanzas de larga distancia.",
    "Moving": "Mudanzas",
    "Local moves": "Mudanzas locales",
    "Office moves": "Mudanzas de oficina",
    "Apartment moves": "Mudanzas de apartamentos",
    "Full house moves": "Mudanzas de casa completa",
    "Labor Help": "Ayuda de Carga",
    "Loading &amp; unloading": "Carga y descarga",
    "Packing &amp; wrapping": "Empaque y envoltura",
    "Furniture rearranging": "Reacomodo de muebles",
    "Storage unit help": "Ayuda con unidades de almacenaje",
    "Availability": "Disponibilidad",
    "Open 24 hours": "Abierto las 24 horas",
    "Same-day service": "Servicio el mismo dia",
    "Flexible scheduling": "Horario flexible",
    "Pricing depends on crew size and job length. Call (239) 440-5374 for a free quote.":
        "El precio depende del tamano del equipo y la duracion del trabajo. Llama al (239) 440-5374 para una cotizacion gratis.",
    "moving days": "dias de mudanza",
    "What Cape Coral": "Lo que dicen los",
    "customers say": "clientes de Cape Coral",
    "4.7 out of 5 · 18 reviews on Google": "4.7 de 5 · 18 resenas en Google",
    "Read all 18 reviews on Google": "Lee las 18 resenas en Google",
    "Serving": "Sirviendo a",
    "Service area": "Area de servicio",
    "Tjs Moving and More serves Cape Coral, Fort Myers and the surrounding Southwest Florida area, 24 hours a day.":
        "Tjs Moving and More sirve a Cape Coral, Fort Myers y el area circundante del suroeste de Florida, las 24 horas.",
    "View on map": "Ver en el mapa",
    "Hours": "Horario",
    "Open 24 hours, every day of the week.": "Abierto las 24 horas, todos los dias de la semana.",
    "Reviews": "Resenas",
    "4.7 stars across 18 Google reviews.": "4.7 estrellas en 18 resenas de Google.",
    "gets it moving": "lo pone en marcha",
    "Call (239) 440-5374 for a free, straightforward quote on your move or loading job. Available 24 hours a day, every day.":
        "Llama al (239) 440-5374 para una cotizacion gratis y clara de tu mudanza o trabajo de carga. Disponible las 24 horas, todos los dias.",
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

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", PATH)
