import re
import os
import colorsys
import shutil

SLUG = "mr-pasta-catering"
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


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> tomato red (Italian, Mr. Pasta Catering)
#    hue-shift via colorsys sobre los MISMOS hex/rgba originales del esqueleto.
# ---------------------------------------------------------------------------
_HEXES = ["#a04a72", "#5c2140", "#f0bed7", "#faf2f6", "#c47a9c", "#8a5573", "#f3e0ea",
          "#d9a8c2", "#7d3457", "#5f2c48", "#33222c", "#fbf3f8", "#fbeff5", "#f8dfeb",
          "#f6f1ea", "#f2d5e3", "#f2cfe0", "#efd0e0", "#e5c1d4", "#dc9dbe", "#d3a2bc",
          "#c9789f", "#b25a85", "#2a1722", "#1f0f18", "#1c0f16"]
_RGBAS = [(160, 74, 114), (51, 34, 44), (240, 190, 215), (70, 25, 50), (250, 242, 246),
          (125, 52, 87), (253, 246, 250), (40, 16, 30), (233, 205, 186), (185, 138, 128)]

TARGET_HUE = 8 / 360.0
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


PALETTE = [(hx, _shift_hex(hx)) for hx in _HEXES]
for old, new in PALETTE:
    rep_all(old, new)

RGBA_FAMILIES = [(rgb, _shift_rgb(rgb)) for rgb in _RGBAS]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

h = h.replace('@@BADGE@@', badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform ni IG -> tel: y Google reviews
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+18629448583"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Mr+Pasta+Catering+Miami+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=Miami,+FL"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Mr. Pasta Catering · Italian Catering in Miami, FL | 4.6 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Mr. Pasta Catering, Miami FL: Italian buffets, antipasto boards, holiday roasts and full-service catering for weddings and private events by Chef Julio Cesar. 4.6 stars across 89 Google reviews." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Mr. Pasta Catering · Italian Catering in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Italian buffets, antipasto and full-service event catering. 4.6 on Google with 89 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-team-buffet.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CateringService",
    "name": "Mr. Pasta Catering",
    "description": "Italian catering company serving Miami, FL: pasta and antipasto buffets, holiday roasts and full-service catering for weddings, showers, baptisms and private events, led by Chef Julio Cesar.",
    "areaServed": "Miami, FL",
    "telephone": "+1-862-944-8583",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "89", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Catering services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Pasta &amp; Italian Buffets" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Antipasto &amp; Charcuterie Boards" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Holiday Roasts" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Weddings &amp; Private Events" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,85,74,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Mr. Pasta Catering" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,85,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Mr. <span class="text-[color:var(--accent-deep)]">Pasta</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">MP</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Mr. Pasta Catering</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Get a quote" data-en="Get a quote">Get a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Get a quote" data-en="Get a quote">Get a quote</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Italian Catering" data-en="Miami, FL · Italian Catering">Miami, FL · Italian Catering</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Real Italian food, served right." data-en="Real Italian food, served right.">Real Italian food, served right.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Pasta buffets, antipasto" data-en="Pasta buffets, antipasto">Pasta buffets, antipasto</span><br /><span data-es="boards and roasts for " data-en="boards and roasts for ">boards and roasts for </span><span class="text-shine" data-es="every event" data-en="every event">every event</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Chef Julio Cesar and his team cater weddings, showers, baptisms and corporate lunches across Miami with full Italian buffets, antipasto boards and holiday roasts, set up and cleaned up start to finish. A 4.6 rating across 89 Google reviews." data-en="Chef Julio Cesar and his team cater weddings, showers, baptisms and corporate lunches across Miami with full Italian buffets, antipasto boards and holiday roasts, set up and cleaned up start to finish. A 4.6 rating across 89 Google reviews.">Chef Julio Cesar and his team cater weddings, showers, baptisms and corporate lunches across Miami with full Italian buffets, antipasto boards and holiday roasts, set up and cleaned up start to finish. A 4.6 rating across 89 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.6 · 89 reviews on Google" data-en="4.6 · 89 reviews on Google">4.6 · 89 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (862) 944-8583" data-en="Call (862) 944-8583">Call (862) 944-8583</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-team-buffet.jpg" alt="The Mr. Pasta Catering team with a full Italian buffet spread at a Miami event" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Since" data-en="Since">Since</p>
            <p class="font-display text-lg">2008</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Miami &amp; South Broward" data-en="Miami &amp; South Broward">Miami &amp; South Broward</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="89">89</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Pasta <span class="text-shine">&amp;</span> Roasts</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Antipasto · Buffets" data-en="Antipasto · Buffets">Antipasto · Buffets</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">+15 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Catering en el sur de la Florida" data-en="Catering South Florida">Catering South Florida</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Y el sur de la Florida" data-en="And South Florida">And South Florida</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Pasta Buffets"),
    ("Hybrid Set", "Antipasto Boards"),
    ("Volume Set", "Holiday Roasts"),
    ("Mega Volume", "Wedding Catering"),
    ("Bottom Lashes", "Corporate Lunches"),
    ("West Palm Beach, FL", "Miami, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (1 sola foto real disponible para esta seccion -> grid 1 col)
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
          <img src="assets/about-outdoor-buffet.jpg" alt="An elegant outdoor buffet table set up by Mr. Pasta Catering in Miami" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Chef Julio Cesar," data-en="Chef Julio Cesar,">Chef Julio Cesar,</span><br /><span class="text-shine" data-es="since 2008" data-en="since 2008">since 2008</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Mr. Pasta Catering lleva desde 2008 llevando cocina italiana fresca a bodas, baby showers, bautizos y eventos corporativos en Miami y el sur de Broward. El chef Julio Cesar y su equipo arman el buffet, sirven a los invitados y lo dejan todo limpio al terminar." data-en="Mr. Pasta Catering has been bringing fresh Italian cooking to weddings, showers, baptisms and corporate events across Miami and South Broward since 2008. Chef Julio Cesar and his team set up the buffet, serve the guests and leave everything clean when they go.">Mr. Pasta Catering has been bringing fresh Italian cooking to weddings, showers, baptisms and corporate events across Miami and South Broward since 2008. Chef Julio Cesar and his team set up the buffet, serve the guests and leave everything clean when they go.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 4.6 estrellas en 89 resenas de Google, con clientes que destacan lo abundante de las porciones y lo limpio que queda todo al final del evento." data-en="The result: a 4.6-star rating across 89 Google reviews, with clients praising how generous the portions are and how clean everything is left after the event.">The result: a 4.6-star rating across 89 Google reviews, with clients praising how generous the portions are and how clean everything is left after the event.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="89">89</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2008</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Desde" data-en="Serving since">Serving since</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,85,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Mr. Pasta Catering" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,85,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Chef Julio Cesar · <span class="text-[color:var(--ink-40)]" data-es="Mr. Pasta Catering" data-en="Mr. Pasta Catering">Mr. Pasta Catering</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your event, course" data-en="Your event, course">Your event, course</span> <span class="text-shine" data-es="by course" data-en="by course">by course</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or text" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Share your date, guest count and the kind of event, and Chef Julio Cesar puts together a menu and a quote." data-en="Share your date, guest count and the kind of event, and Chef Julio Cesar puts together a menu and a quote.">Share your date, guest count and the kind of event, and Chef Julio Cesar puts together a menu and a quote.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Menu built for you" data-en="Menu built for you">Menu built for you</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Pasta stations, antipasto boards, roasted meats or a mix of all three, sized for your guest count." data-en="Pasta stations, antipasto boards, roasted meats or a mix of all three, sized for your guest count.">Pasta stations, antipasto boards, roasted meats or a mix of all three, sized for your guest count.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Set up &amp; serve" data-en="Set up &amp; serve">Set up &amp; serve</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The team arrives early, sets up the full buffet and serves your guests, hot food kept hot start to finish." data-en="The team arrives early, sets up the full buffet and serves your guests, hot food kept hot start to finish.">The team arrives early, sets up the full buffet and serves your guests, hot food kept hot start to finish.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Clean finish" data-en="Clean finish">Clean finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Once the last plate is served, the team clears and cleans the buffet, so your only job is to enjoy the event." data-en="Once the last plate is served, the team clears and cleans the buffet, so your only job is to enjoy the event.">Once the last plate is served, the team clears and cleans the buffet, so your only job is to enjoy the event.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Catering para" data-en="Catering for">Catering for</span> <span class="text-shine" data-es="cada ocasion" data-en="every occasion">every occasion</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Cada evento recibe su propia cotizacion segun el menu y el numero de invitados. Llama o escribe para armar la tuya." data-en="Every event gets its own quote based on the menu and guest count. Call or text to put yours together.">Every event gets its own quote based on the menu and guest count. Call or text to put yours together.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(160,85,74,0.4); box-shadow: 0 18px 50px rgba(51,36,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pasta &amp; Italian Buffets" data-en="Pasta &amp; Italian Buffets">Pasta &amp; Italian Buffets</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Chicken parmesan, pasta primavera and full buffet spreads, set up and served for weddings and family celebrations." data-en="Chicken parmesan, pasta primavera and full buffet spreads, set up and served for weddings and family celebrations.">Chicken parmesan, pasta primavera and full buffet spreads, set up and served for weddings and family celebrations.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Boards &amp; platters" data-en="Boards &amp; platters">Boards &amp; platters</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Antipasto &amp; Charcuterie Boards" data-en="Antipasto &amp; Charcuterie Boards">Antipasto &amp; Charcuterie Boards</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cured meats, cheeses, olives and marinated vegetables arranged on large boards for cocktail hour or showers." data-en="Cured meats, cheeses, olives and marinated vegetables arranged on large boards for cocktail hour or showers.">Cured meats, cheeses, olives and marinated vegetables arranged on large boards for cocktail hour or showers.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Seasonal" data-en="Seasonal">Seasonal</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Holiday Roasts" data-en="Holiday Roasts">Holiday Roasts</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Whole roasted turkey with herbs and citrus, carved and plated for Thanksgiving and holiday lunches." data-en="Whole roasted turkey with herbs and citrus, carved and plated for Thanksgiving and holiday lunches.">Whole roasted turkey with herbs and citrus, carved and plated for Thanksgiving and holiday lunches.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Full service" data-en="Full service">Full service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Weddings &amp; Private Events" data-en="Weddings &amp; Private Events">Weddings &amp; Private Events</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Weddings, baptisms, baby showers and corporate lunches, from a 20-guest lunch to a 130-guest reception." data-en="Weddings, baptisms, baby showers and corporate lunches, from a 20-guest lunch to a 130-guest reception.">Weddings, baptisms, baby showers and corporate lunches, from a 20-guest lunch to a 130-guest reception.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Get a quote" data-en="Get a quote">Get a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Pasta station" data-en="Pasta station">Pasta station</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Chicken parmesan" data-en="Chicken parmesan">Chicken parmesan</li>
            <li class="flex items-center gap-2" data-es="Pasta primavera" data-en="Pasta primavera">Pasta primavera</li>
            <li class="flex items-center gap-2" data-es="Baked ziti &amp; lasagna" data-en="Baked ziti &amp; lasagna">Baked ziti &amp; lasagna</li>
            <li class="flex items-center gap-2" data-es="Fresh breads" data-en="Fresh breads">Fresh breads</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Boards" data-en="Boards">Boards</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Cured meats" data-en="Cured meats">Cured meats</li>
            <li class="flex items-center gap-2" data-es="Mozzarella &amp; caprese skewers" data-en="Mozzarella &amp; caprese skewers">Mozzarella &amp; caprese skewers</li>
            <li class="flex items-center gap-2" data-es="Olives &amp; marinated vegetables" data-en="Olives &amp; marinated vegetables">Olives &amp; marinated vegetables</li>
            <li class="flex items-center gap-2" data-es="Fresh fruit platters" data-en="Fresh fruit platters">Fresh fruit platters</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Roasts &amp; events" data-en="Roasts &amp; events">Roasts &amp; events</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Whole roasted turkey" data-en="Whole roasted turkey">Whole roasted turkey</li>
            <li class="flex items-center gap-2" data-es="Full setup &amp; service" data-en="Full setup &amp; service">Full setup &amp; service</li>
            <li class="flex items-center gap-2" data-es="Cleanup included" data-en="Cleanup included">Cleanup included</li>
            <li class="flex items-center gap-2" data-es="Groups up to 130 guests" data-en="Groups up to 130 guests">Groups up to 130 guests</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on menu and guest count. Call (862) 944-8583 for a free quote." data-en="Pricing depends on menu and guest count. Call (862) 944-8583 for a free quote.">Pricing depends on menu and guest count. Call (862) 944-8583 for a free quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="events" data-en="events">events</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (862) 944-8583
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Buffet servido en un evento corporativo" data-en="Buffet served at a corporate event">Buffet served at a corporate event</span><img src="assets/gallery-indoor-buffet.jpg" alt="A full Italian buffet served indoors by Mr. Pasta Catering" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Brochetas caprese" data-en="Caprese skewers">Caprese skewers</span><img src="assets/gallery-caprese-skewers.jpg" alt="A tray of caprese skewers with cherry tomatoes and mozzarella" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Tabla de antipasto" data-en="Antipasto board">Antipasto board</span><img src="assets/gallery-charcuterie.jpg" alt="An antipasto board with cured meats, cheeses and olives" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Pollo a la parmesana" data-en="Chicken parmesan">Chicken parmesan</span><img src="assets/gallery-chicken-parm.jpg" alt="Chicken parmesan prepared by Mr. Pasta Catering" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Pavo asado entero" data-en="Whole roasted turkey">Whole roasted turkey</span><img src="assets/gallery-roast-turkey.jpg" alt="A whole roasted turkey with herbs prepared by Mr. Pasta Catering" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Miami" data-en="What Miami">What Miami</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.6 out of 5 · 89 reviews on Google" data-en="4.6 out of 5 · 89 reviews on Google">4.6 out of 5 · 89 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We had an amazing experience with Mr. Pasta Catering and Chef Julio Cesar for our wedding! The food was absolutely delicious, fresh, and beautifully prepared. Everything was clean, flavorful, and our guests truly enjoyed it."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Axybell Laverde</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Genuinely incredible!! They came for my wedding shower and served my 130 guests! So professional. The food was absolutely INCREDIBLE. And Julio is so talented and beyond kind."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Victoria Miranda</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mr Pasta Catering / Chef Julio Cesar prepared a beautiful delicious lunch in honor of our granddaughter's baptism. Everything was delicious. The amount of food provided was so abundant. They arrived early to set up and cleaned everything when they left."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Aileen Lafont</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 89 reviews on Google" data-en="Read all 89 reviews on Google">Read all 89 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (sin direccion fija: area de servicio)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Miami, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,85,74,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mr. Pasta Catering serves Miami and South Broward, traveling to your venue for weddings, showers, baptisms and corporate events." data-en="Mr. Pasta Catering serves Miami and South Broward, traveling to your venue for weddings, showers, baptisms and corporate events.">Mr. Pasta Catering serves Miami and South Broward, traveling to your venue for weddings, showers, baptisms and corporate events.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,85,74,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,85,74,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Bookings" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Call or text with your event date and guest count for a free quote and menu walkthrough." data-en="Call or text with your event date and guest count for a free quote and menu walkthrough.">Call or text with your event date and guest count for a free quote and menu walkthrough.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,85,74,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (862) 944-8583" data-en="Call (862) 944-8583">Call (862) 944-8583</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,85,74,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.6 stars across 89 verified Google reviews." data-en="4.6 stars across 89 verified Google reviews.">4.6 stars across 89 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,85,74,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Mr. Pasta Catering service area, Miami FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Real Italian food, served right." data-en="Real Italian food, served right.">Real Italian food, served right.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Let\'s plan your" data-en="Let\'s plan your">Let\'s plan your</span> <span class="text-shine" data-es="menu" data-en="menu">menu</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (862) 944-8583 for a free, honest quote on your wedding, shower, baptism or corporate event. Serving Miami and South Broward." data-en="Call (862) 944-8583 for a free, honest quote on your wedding, shower, baptism or corporate event. Serving Miami and South Broward.">Call (862) 944-8583 for a free, honest quote on your wedding, shower, baptism or corporate event. Serving Miami and South Broward.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (862) 944-8583" data-en="Call (862) 944-8583">Call (862) 944-8583</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Mr. Pasta</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,197,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Mr. Pasta Catering" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,197,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Mr. Pasta Catering</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Italian catering serving Miami and South Broward since 2008." data-en="Italian catering serving Miami and South Broward since 2008.">Italian catering serving Miami and South Broward since 2008.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#f0c5be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Miami &amp; South Broward, FL" data-en="Miami &amp; South Broward, FL">Miami &amp; South Broward, FL</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#f0c5be]" data-es="Call (862) 944-8583" data-en="Call (862) 944-8583">Call (862) 944-8583</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0c5be]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0c5be]">4.6 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Mr. Pasta Catering.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Mr. Pasta Catering">')
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
    "Miami, FL · Italian Catering": "Miami, FL · Catering Italiano",
    "Real Italian food, served right.": "Comida italiana real, servida bien.",
    "Pasta buffets, antipasto": "Buffets de pasta, tablas",
    "boards and roasts for ": "de antipasto y asados para ",
    "every event": "cada evento",
    "Chef Julio Cesar and his team cater weddings, showers, baptisms and corporate lunches across Miami with full Italian buffets, antipasto boards and holiday roasts, set up and cleaned up start to finish. A 4.6 rating across 89 Google reviews.":
        "El chef Julio Cesar y su equipo atienden bodas, baby showers, bautizos y almuerzos corporativos en Miami con buffets italianos completos, tablas de antipasto y asados festivos, con montaje y limpieza incluidos de principio a fin. Calificacion de 4.6 en 89 resenas de Google.",
    "4.6 · 89 reviews on Google": "4.6 · 89 resenas en Google",
    "Call (862) 944-8583": "Llama al (862) 944-8583",
    "Since": "Desde",
    "Miami &amp; South Broward": "Miami y el sur de Broward",
    "Antipasto · Buffets": "Antipasto · Buffets",
    "Chef Julio Cesar,": "El chef Julio Cesar,",
    "since 2008": "desde 2008",
    "Mr. Pasta Catering": "Mr. Pasta Catering",
    "Your event, course": "Tu evento, plato",
    "by course": "por plato",
    "Call or text": "Llama o escribe",
    "Share your date, guest count and the kind of event, and Chef Julio Cesar puts together a menu and a quote.":
        "Comparte tu fecha, numero de invitados y tipo de evento, y el chef Julio Cesar arma un menu y una cotizacion.",
    "Menu built for you": "Menu a tu medida",
    "Pasta stations, antipasto boards, roasted meats or a mix of all three, sized for your guest count.":
        "Estaciones de pasta, tablas de antipasto, carnes asadas o una mezcla de los tres, segun tu numero de invitados.",
    "Set up &amp; serve": "Montaje y servicio",
    "The team arrives early, sets up the full buffet and serves your guests, hot food kept hot start to finish.":
        "El equipo llega temprano, monta el buffet completo y sirve a tus invitados, con la comida caliente de principio a fin.",
    "Clean finish": "Limpieza final",
    "Once the last plate is served, the team clears and cleans the buffet, so your only job is to enjoy the event.":
        "Una vez servido el ultimo plato, el equipo recoge y limpia el buffet, para que tu unico trabajo sea disfrutar el evento.",
    "Most requested": "Lo mas solicitado",
    "Pasta &amp; Italian Buffets": "Buffets de Pasta Italiana",
    "Chicken parmesan, pasta primavera and full buffet spreads, set up and served for weddings and family celebrations.":
        "Pollo a la parmesana, pasta primavera y buffets completos, montados y servidos para bodas y celebraciones familiares.",
    "Get a quote": "Pide tu cotizacion",
    "Call": "Llamar",
    "Boards &amp; platters": "Tablas y platones",
    "Antipasto &amp; Charcuterie Boards": "Tablas de Antipasto",
    "Cured meats, cheeses, olives and marinated vegetables arranged on large boards for cocktail hour or showers.":
        "Carnes curadas, quesos, aceitunas y vegetales marinados en grandes tablas para la hora del coctel o baby showers.",
    "Seasonal": "De temporada",
    "Holiday Roasts": "Asados Festivos",
    "Whole roasted turkey with herbs and citrus, carved and plated for Thanksgiving and holiday lunches.":
        "Pavo entero asado con hierbas y citricos, trinchado y servido para el Dia de Accion de Gracias y almuerzos festivos.",
    "Full service": "Servicio completo",
    "Weddings &amp; Private Events": "Bodas y Eventos Privados",
    "Weddings, baptisms, baby showers and corporate lunches, from a 20-guest lunch to a 130-guest reception.":
        "Bodas, bautizos, baby showers y almuerzos corporativos, desde un almuerzo de 20 invitados hasta una recepcion de 130.",
    "Pasta station": "Estacion de pasta",
    "Chicken parmesan": "Pollo a la parmesana",
    "Pasta primavera": "Pasta primavera",
    "Baked ziti &amp; lasagna": "Ziti horneado y lasana",
    "Fresh breads": "Panes frescos",
    "Boards": "Tablas",
    "Cured meats": "Carnes curadas",
    "Mozzarella &amp; caprese skewers": "Brochetas de mozzarella y caprese",
    "Olives &amp; marinated vegetables": "Aceitunas y vegetales marinados",
    "Fresh fruit platters": "Platones de fruta fresca",
    "Roasts &amp; events": "Asados y eventos",
    "Whole roasted turkey": "Pavo entero asado",
    "Full setup &amp; service": "Montaje y servicio completo",
    "Cleanup included": "Limpieza incluida",
    "Groups up to 130 guests": "Grupos de hasta 130 invitados",
    "Pricing depends on menu and guest count. Call (862) 944-8583 for a free quote.":
        "El precio depende del menu y el numero de invitados. Llama al (862) 944-8583 para una cotizacion gratis.",
    "Real": "Eventos",
    "events": "reales",
    "What Miami": "Lo que dicen los",
    "customers say": "clientes en Miami",
    "Read all 89 reviews on Google": "Lee las 89 resenas en Google",
    "Serving": "Sirviendo a",
    "Service area": "Area de servicio",
    "Mr. Pasta Catering serves Miami and South Broward, traveling to your venue for weddings, showers, baptisms and corporate events.":
        "Mr. Pasta Catering sirve a Miami y el sur de Broward, llevando el servicio hasta tu local para bodas, baby showers, bautizos y eventos corporativos.",
    "View on map": "Ver en el mapa",
    "Bookings": "Reservas",
    "Call or text with your event date and guest count for a free quote and menu walkthrough.":
        "Llama o escribe con la fecha de tu evento y el numero de invitados para una cotizacion gratis y repaso del menu.",
    "Reviews": "Resenas",
    "4.6 stars across 89 verified Google reviews.": "4.6 estrellas en 89 resenas verificadas de Google.",
    "Let's plan your": "Vamos a planear tu",
    "menu": "menu",
    "Call (862) 944-8583 for a free, honest quote on your wedding, shower, baptism or corporate event. Serving Miami and South Broward.":
        "Llama al (862) 944-8583 para una cotizacion gratis y honesta de tu boda, baby shower, bautizo o evento corporativo. Sirviendo a Miami y el sur de Broward.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Italian catering serving Miami and South Broward since 2008.": "Catering italiano en Miami y el sur de Broward desde 2008.",
    "Contact": "Contacto",
    "Miami &amp; South Broward, FL": "Miami y el sur de Broward, FL",
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
