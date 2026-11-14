import re
import colorsys
import shutil

SLUG = "irc-movers"
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
# 2. Paleta: plum-pink (lashbloom) -> azul acero (IRC Movers, color real del camion)
# ---------------------------------------------------------------------------
TARGET_HUE = 211 / 360.0
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

# ---------------------------------------------------------------------------
# 3. Globales: sin booking/IG/email -> tel: + Google reviews
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+17726465637"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=IRC+Movers+Port+St.+Lucie+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=Port+St.+Lucie,+FL"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>IRC Movers · Moving Company in Port St. Lucie, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="IRC Movers, Port St. Lucie FL: local and long-distance moving, packing and deliveries across the Treasure Coast. 5.0 stars across 1,431 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="IRC Movers · Moving Company in Port St. Lucie, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Local and long-distance moving, packing and deliveries. 5.0 on Google with 1,431 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-truck.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MovingCompany",
    "name": "IRC Movers",
    "description": "Moving company serving Port St. Lucie, Fort Pierce and the Treasure Coast, FL: local and long-distance moving, packing and deliveries.",
    "areaServed": "Port St. Lucie, FL",
    "telephone": "+1-772-646-5637",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "1431", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Moving services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Local Moving" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Long-Distance Moving" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Packing &amp; Unpacking" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Deliveries" } }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,116,160,0.35)]" />',
    '<img src="assets/logo.jpg" alt="IRC Movers" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,116,160,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">IRC <span class="text-[color:var(--accent-deep)]">Movers</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">IRC</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">IRC Movers</span>')
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
    'data-es="Port St. Lucie, FL · Moving Company" data-en="Port St. Lucie, FL · Moving Company">Port St. Lucie, FL · Moving Company</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Moving made simple." data-en="Moving made simple.">Moving made simple.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Moving, packing" data-en="Moving, packing">Moving, packing</span><br /><span data-es="and deliveries, done " data-en="and deliveries, done ">and deliveries, done </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Full-service local and long-distance moving across St. Lucie and Martin County: packing, loading and careful delivery for homes and offices, with a perfect 5.0 rating across more than 1,400 Google reviews." data-en="Full-service local and long-distance moving across St. Lucie and Martin County: packing, loading and careful delivery for homes and offices, with a perfect 5.0 rating across more than 1,400 Google reviews.">Full-service local and long-distance moving across St. Lucie and Martin County: packing, loading and careful delivery for homes and offices, with a perfect 5.0 rating across more than 1,400 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 1,431 reviews on Google" data-en="5.0 · 1,431 reviews on Google">5.0 · 1,431 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (772) 646-5637" data-en="Call (772) 646-5637">Call (772) 646-5637</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-truck.jpg" alt="The I.R.C. Movers truck arriving for a move in Port St. Lucie, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">8 AM - 5 PM</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Mon-Sat · Closed Sunday" data-en="Mon-Sat · Closed Sunday">Mon-Sat · Closed Sunday</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="1431">1431</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Moving <span class="text-shine">&amp;</span> Deliveries</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Packing · Storage" data-en="Packing · Storage">Packing · Storage</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">Mon-Sat</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="8 AM to 5 PM" data-en="8 AM to 5 PM">8 AM to 5 PM</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Port St. Lucie</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Treasure Coast, FL" data-en="Treasure Coast, FL">Treasure Coast, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Local Moves"),
    ("Hybrid Set", "Long-Distance"),
    ("Volume Set", "Packing Service"),
    ("Mega Volume", "Furniture Delivery"),
    ("Bottom Lashes", "Storage Help"),
    ("West Palm Beach, FL", "Port St. Lucie, FL"),
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
          <img src="assets/about-crew.jpg" alt="The IRC Movers crew posing inside their truck after a move in Port St. Lucie, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One crew," data-en="One crew,">One crew,</span><br /><span class="text-shine" data-es="that treats your move like their own" data-en="that treats your move like their own">that treats your move like their own</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="IRC Movers is a Port St. Lucie moving company handling local and long-distance moves, packing and deliveries across the Treasure Coast. Customers across Fort Pierce, Port St. Lucie and Tradition call on the same crew for moves big and small." data-en="IRC Movers is a Port St. Lucie moving company handling local and long-distance moves, packing and deliveries across the Treasure Coast. Customers across Fort Pierce, Port St. Lucie and Tradition call on the same crew for moves big and small.">IRC Movers is a Port St. Lucie moving company handling local and long-distance moves, packing and deliveries across the Treasure Coast. Customers across Fort Pierce, Port St. Lucie and Tradition call on the same crew for moves big and small.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a perfect 5.0 rating across more than 1,400 Google reviews, built one careful move at a time." data-en="The result: a perfect 5.0 rating across more than 1,400 Google reviews, built one careful move at a time.">The result: a perfect 5.0 rating across more than 1,400 Google reviews, built one careful move at a time.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="1431">1431</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Full-Service" data-en="Full-Service">Full-Service</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Packing &amp; Storage" data-en="Packing &amp; Storage">Packing &amp; Storage</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,116,160,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="IRC Movers" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,116,160,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">IRC Movers · <span class="text-[color:var(--ink-40)]" data-es="Local moving crew" data-en="Local moving crew">Local moving crew</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your move," data-en="Your move,">Your move,</span> <span class="text-shine" data-es="start to finish" data-en="start to finish">start to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call to book" data-en="Call to book">Call to book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (772) 646-5637 with your move date and details, and get a straightforward price over the phone." data-en="Call (772) 646-5637 with your move date and details, and get a straightforward price over the phone.">Call (772) 646-5637 with your move date and details, and get a straightforward price over the phone.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Careful packing" data-en="Careful packing">Careful packing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew wraps and protects furniture and boxes everything that needs it, so nothing shifts in transit." data-en="The crew wraps and protects furniture and boxes everything that needs it, so nothing shifts in transit.">The crew wraps and protects furniture and boxes everything that needs it, so nothing shifts in transit.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Loading &amp; drive" data-en="Loading &amp; drive">Loading &amp; drive</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Your things are loaded onto the truck and driven safely to your new address, local or long-distance." data-en="Your things are loaded onto the truck and driven safely to your new address, local or long-distance.">Your things are loaded onto the truck and driven safely to your new address, local or long-distance.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Unload &amp; walkthrough" data-en="Unload &amp; walkthrough">Unload &amp; walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew unloads and places furniture where you want it, then walks the job with you before leaving." data-en="The crew unloads and places furniture where you want it, then walks the job with you before leaving.">The crew unloads and places furniture where you want it, then walks the job with you before leaving.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine" data-es="every move" data-en="every move">every move</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two moves are the same, so every job gets a straightforward phone quote before anything is booked." data-en="No two moves are the same, so every job gets a straightforward phone quote before anything is booked.">No two moves are the same, so every job gets a straightforward phone quote before anything is booked.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(74,116,160,0.4); box-shadow: 0 18px 50px rgba(34,44,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Local Moving" data-en="Local Moving">Local Moving</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service local moves across Port St. Lucie, Fort Pierce and the Treasure Coast, from studio apartments to full homes." data-en="Full-service local moves across Port St. Lucie, Fort Pierce and the Treasure Coast, from studio apartments to full homes.">Full-service local moves across Port St. Lucie, Fort Pierce and the Treasure Coast, from studio apartments to full homes.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Beyond the coast" data-en="Beyond the coast">Beyond the coast</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Long-Distance Moving" data-en="Long-Distance Moving">Long-Distance Moving</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Moves beyond the Treasure Coast handled by the same crew, with careful loading and a flat, upfront price." data-en="Moves beyond the Treasure Coast handled by the same crew, with careful loading and a flat, upfront price.">Moves beyond the Treasure Coast handled by the same crew, with careful loading and a flat, upfront price.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it safe" data-en="Keep it safe">Keep it safe</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Packing &amp; Unpacking" data-en="Packing &amp; Unpacking">Packing &amp; Unpacking</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full or partial packing service with real moving blankets and boxes, so fragile items travel safe." data-en="Full or partial packing service with real moving blankets and boxes, so fragile items travel safe.">Full or partial packing service with real moving blankets and boxes, so fragile items travel safe.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="One piece or many" data-en="One piece or many">One piece or many</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Deliveries" data-en="Deliveries">Deliveries</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Furniture and large-item delivery for single pieces, store purchases and online orders across the area." data-en="Furniture and large-item delivery for single pieces, store purchases and online orders across the area.">Furniture and large-item delivery for single pieces, store purchases and online orders across the area.</p>
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
            <li class="flex items-center gap-2" data-es="Long-distance moves" data-en="Long-distance moves">Long-distance moves</li>
            <li class="flex items-center gap-2" data-es="Apartment &amp; condo moves" data-en="Apartment &amp; condo moves">Apartment &amp; condo moves</li>
            <li class="flex items-center gap-2" data-es="Office moves" data-en="Office moves">Office moves</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Packing" data-en="Packing">Packing</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Full packing service" data-en="Full packing service">Full packing service</li>
            <li class="flex items-center gap-2" data-es="Partial packing" data-en="Partial packing">Partial packing</li>
            <li class="flex items-center gap-2" data-es="Moving boxes &amp; supplies" data-en="Moving boxes &amp; supplies">Moving boxes &amp; supplies</li>
            <li class="flex items-center gap-2" data-es="Furniture wrapping" data-en="Furniture wrapping">Furniture wrapping</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Deliveries" data-en="Deliveries">Deliveries</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Furniture delivery" data-en="Furniture delivery">Furniture delivery</li>
            <li class="flex items-center gap-2" data-es="Appliance delivery" data-en="Appliance delivery">Appliance delivery</li>
            <li class="flex items-center gap-2" data-es="Store pickup &amp; delivery" data-en="Store pickup &amp; delivery">Store pickup &amp; delivery</li>
            <li class="flex items-center gap-2" data-es="Single-item moves" data-en="Single-item moves">Single-item moves</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on move size and distance. Call (772) 646-5637 for a free quote." data-en="Pricing depends on move size and distance. Call (772) 646-5637 for a free quote.">Pricing depends on move size and distance. Call (772) 646-5637 for a free quote.</span></p>')
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Dia de mudanza en Port St. Lucie" data-en="Moving day in Port St. Lucie">Moving day in Port St. Lucie</span><img src="assets/gallery-moving-day.jpg" alt="The IRC Movers crew moving furniture into a home in Port St. Lucie, FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cargado y listo" data-en="Loaded and ready to go">Loaded and ready to go</span><img src="assets/gallery-truck-palms.jpg" alt="The IRC Movers truck loaded and ready to go in Port St. Lucie, FL" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Bodega de empaque y almacenaje" data-en="Packing &amp; storage warehouse">Packing &amp; storage warehouse</span><img src="assets/gallery-warehouse-floor.jpg" alt="The IRC Movers packing and storage warehouse" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Espacio de almacenaje seguro" data-en="Secure storage space">Secure storage space</span><img src="assets/gallery-storage-racks.jpg" alt="Secure storage racking at the IRC Movers warehouse" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Listo para la mudanza" data-en="Ready for move-in day">Ready for move-in day</span><img src="assets/gallery-empty-room.jpg" alt="A home ready for move-in day, serviced by IRC Movers" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Port St. Lucie" data-en="What Port St. Lucie">What Port St. Lucie</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 1,431 reviews on Google" data-en="5.0 out of 5 · 1,431 reviews on Google">5.0 out of 5 · 1,431 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great prices and amazing service. We heard great things about IRC and decided to book our Ft Pierce to Tradition/PSL move. To start, their prices are better than anyone else around the PSL/Ft Pierce area..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Elizabeth Rahal</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Jason, Avery and Tyler were phenomenal! Fast, very efficient, not to mention extremely polite and responsive. Clean truck!! We will always recommend this company! Thank you!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dianna Spacco</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Hiring IRC Movers was an amazing experience from start to finish! After doing my research, I booked my parents' move about a month in advance. As the moving day got closer, I called to confirm everything and spoke with Kevin, who was..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lisa Newman</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 1,431 reviews on Google" data-en="Read all 1,431 reviews on Google">Read all 1,431 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (sin direccion fija: area de servicio)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Port St. Lucie, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,116,160,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="IRC Movers serves Port St. Lucie, Fort Pierce, Tradition and the greater Treasure Coast, for local and long-distance moves." data-en="IRC Movers serves Port St. Lucie, Fort Pierce, Tradition and the greater Treasure Coast, for local and long-distance moves.">IRC Movers serves Port St. Lucie, Fort Pierce, Tradition and the greater Treasure Coast, for local and long-distance moves.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,116,160,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,116,160,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Saturday, 8:00 AM to 5:00 PM. Closed Sunday." data-en="Monday to Saturday, 8:00 AM to 5:00 PM. Closed Sunday.">Monday to Saturday, 8:00 AM to 5:00 PM. Closed Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,116,160,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (772) 646-5637" data-en="Call (772) 646-5637">Call (772) 646-5637</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,116,160,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="5.0 stars across 1,431 Google reviews." data-en="5.0 stars across 1,431 Google reviews.">5.0 stars across 1,431 Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,116,160,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: IRC Movers service area, Port St. Lucie FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Moving made simple." data-en="Moving made simple.">Moving made simple.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call" data-en="One call">One call</span> <span class="text-shine" data-es="moves it all" data-en="moves it all">moves it all</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (772) 646-5637 for a free, straightforward quote on your local or long-distance move. Monday to Saturday, 8 AM to 5 PM." data-en="Call (772) 646-5637 for a free, straightforward quote on your local or long-distance move. Monday to Saturday, 8 AM to 5 PM.">Call (772) 646-5637 for a free, straightforward quote on your local or long-distance move. Monday to Saturday, 8 AM to 5 PM.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (772) 646-5637" data-en="Call (772) 646-5637">Call (772) 646-5637</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">IRC Movers</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,214,240,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="IRC Movers" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,214,240,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">IRC Movers</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Moving company serving Port St. Lucie, FL. Local &amp; long-distance." data-en="Moving company serving Port St. Lucie, FL. Local &amp; long-distance.">Moving company serving Port St. Lucie, FL. Local &amp; long-distance.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#bed6f0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Serving Port St. Lucie, FL" data-en="Serving Port St. Lucie, FL">Serving Port St. Lucie, FL</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#8fb8d9]" data-es="Call (772) 646-5637" data-en="Call (772) 646-5637">Call (772) 646-5637</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#bed6f0]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#8fb8d9]">5.0 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 IRC Movers.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call IRC Movers">')
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
    "Port St. Lucie, FL · Moving Company": "Port St. Lucie, FL · Empresa de Mudanzas",
    "Moving made simple.": "Mudanzas sin complicaciones.",
    "Moving, packing": "Mudanzas, empaque",
    "and deliveries, done ": "y entregas, hechas ",
    "right": "bien",
    "Full-service local and long-distance moving across St. Lucie and Martin County: packing, loading and careful delivery for homes and offices, with a perfect 5.0 rating across more than 1,400 Google reviews.":
        "Mudanzas locales y de larga distancia en los condados de St. Lucie y Martin: empaque, carga y entrega cuidadosa para casas y oficinas, con una calificacion perfecta de 5.0 en mas de 1,400 resenas de Google.",
    "5.0 · 1,431 reviews on Google": "5.0 · 1,431 resenas en Google",
    "Call (772) 646-5637": "Llama al (772) 646-5637",
    "Open": "Abierto",
    "Mon-Sat · Closed Sunday": "Lun-Sab · Cerrado domingo",
    "Packing · Storage": "Empaque · Almacenaje",
    "8 AM to 5 PM": "8 AM a 5 PM",
    "Treasure Coast, FL": "Treasure Coast, FL",
    "that treats your move like their own": "que trata tu mudanza como propia",
    "IRC Movers is a Port St. Lucie moving company handling local and long-distance moves, packing and deliveries across the Treasure Coast. Customers across Fort Pierce, Port St. Lucie and Tradition call on the same crew for moves big and small.":
        "IRC Movers es una empresa de mudanzas de Port St. Lucie que maneja mudanzas locales y de larga distancia, empaque y entregas en todo el Treasure Coast. Clientes de Fort Pierce, Port St. Lucie y Tradition llaman al mismo equipo para mudanzas grandes y pequenas.",
    "The result: a perfect 5.0 rating across more than 1,400 Google reviews, built one careful move at a time.":
        "El resultado: una calificacion perfecta de 5.0 en mas de 1,400 resenas de Google, construida mudanza cuidadosa tras mudanza cuidadosa.",
    "Full-Service": "Servicio Completo",
    "Packing &amp; Storage": "Empaque y Almacenaje",
    "Local moving crew": "Equipo de mudanzas local",
    "start to finish": "de principio a fin",
    "Call to book": "Llama para reservar",
    "Call (772) 646-5637 with your move date and details, and get a straightforward price over the phone.":
        "Llama al (772) 646-5637 con la fecha de tu mudanza y los detalles, y recibe un precio claro por telefono.",
    "Careful packing": "Empaque cuidadoso",
    "The crew wraps and protects furniture and boxes everything that needs it, so nothing shifts in transit.":
        "El equipo envuelve y protege los muebles y empaca todo lo necesario, para que nada se mueva durante el traslado.",
    "Loading &amp; drive": "Carga y traslado",
    "Your things are loaded onto the truck and driven safely to your new address, local or long-distance.":
        "Tus cosas se cargan en el camion y se transportan de forma segura a tu nueva direccion, local o de larga distancia.",
    "Unload &amp; walkthrough": "Descarga y revision",
    "The crew unloads and places furniture where you want it, then walks the job with you before leaving.":
        "El equipo descarga y coloca los muebles donde los quieras, y revisa el trabajo contigo antes de irse.",
    "every move": "cada mudanza",
    "No two moves are the same, so every job gets a straightforward phone quote before anything is booked.":
        "Ninguna mudanza es igual a otra, asi que cada trabajo recibe una cotizacion clara por telefono antes de reservar.",
    "Most requested": "Lo mas solicitado",
    "Local Moving": "Mudanzas Locales",
    "Full-service local moves across Port St. Lucie, Fort Pierce and the Treasure Coast, from studio apartments to full homes.":
        "Mudanzas locales completas en Port St. Lucie, Fort Pierce y el Treasure Coast, desde apartamentos estudio hasta casas completas.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Beyond the coast": "Mas alla de la costa",
    "Long-Distance Moving": "Mudanzas de Larga Distancia",
    "Moves beyond the Treasure Coast handled by the same crew, with careful loading and a flat, upfront price.":
        "Mudanzas mas alla del Treasure Coast manejadas por el mismo equipo, con carga cuidadosa y un precio fijo y claro.",
    "Keep it safe": "Mantenlo seguro",
    "Packing &amp; Unpacking": "Empaque y Desempaque",
    "Full or partial packing service with real moving blankets and boxes, so fragile items travel safe.":
        "Servicio de empaque total o parcial con mantas y cajas reales de mudanza, para que los objetos fragiles viajen seguros.",
    "One piece or many": "Una pieza o varias",
    "Deliveries": "Entregas",
    "Furniture and large-item delivery for single pieces, store purchases and online orders across the area.":
        "Entrega de muebles y articulos grandes, ya sea una sola pieza, compras de tienda o pedidos en linea en toda la zona.",
    "Moving": "Mudanzas",
    "Local moves": "Mudanzas locales",
    "Long-distance moves": "Mudanzas de larga distancia",
    "Apartment &amp; condo moves": "Mudanzas de apartamentos y condominios",
    "Office moves": "Mudanzas de oficina",
    "Packing": "Empaque",
    "Full packing service": "Servicio de empaque completo",
    "Partial packing": "Empaque parcial",
    "Moving boxes &amp; supplies": "Cajas y suministros de mudanza",
    "Furniture wrapping": "Envoltura de muebles",
    "Furniture delivery": "Entrega de muebles",
    "Appliance delivery": "Entrega de electrodomesticos",
    "Store pickup &amp; delivery": "Recogida y entrega de tienda",
    "Single-item moves": "Mudanzas de una sola pieza",
    "Pricing depends on move size and distance. Call (772) 646-5637 for a free quote.":
        "El precio depende del tamano de la mudanza y la distancia. Llama al (772) 646-5637 para una cotizacion gratis.",
    "moving days": "dias de mudanza",
    "What Port St. Lucie": "Lo que dicen los",
    "customers say": "clientes de Port St. Lucie",
    "5.0 out of 5 · 1,431 reviews on Google": "5.0 de 5 · 1,431 resenas en Google",
    "Read all 1,431 reviews on Google": "Lee las 1,431 resenas en Google",
    "Serving": "Sirviendo a",
    "Service area": "Area de servicio",
    "IRC Movers serves Port St. Lucie, Fort Pierce, Tradition and the greater Treasure Coast, for local and long-distance moves.":
        "IRC Movers sirve a Port St. Lucie, Fort Pierce, Tradition y todo el Treasure Coast, para mudanzas locales y de larga distancia.",
    "View on map": "Ver en el mapa",
    "Hours": "Horario",
    "Monday to Saturday, 8:00 AM to 5:00 PM. Closed Sunday.": "Lunes a sabado, de 8:00 AM a 5:00 PM. Cerrado los domingos.",
    "Reviews": "Resenas",
    "5.0 stars across 1,431 Google reviews.": "5.0 estrellas en 1,431 resenas de Google.",
    "moves it all": "mueve todo",
    "Call (772) 646-5637 for a free, straightforward quote on your local or long-distance move. Monday to Saturday, 8 AM to 5 PM.":
        "Llama al (772) 646-5637 para una cotizacion gratis y clara de tu mudanza local o de larga distancia. Lunes a sabado, de 8 AM a 5 PM.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Moving company serving Port St. Lucie, FL. Local &amp; long-distance.": "Empresa de mudanzas en Port St. Lucie, FL. Local y de larga distancia.",
    "Contact": "Contacto",
    "Serving Port St. Lucie, FL": "Sirviendo a Port St. Lucie, FL",
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
