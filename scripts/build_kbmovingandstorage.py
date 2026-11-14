import re
import colorsys
import shutil

SLUG = "kb-moving-and-storage"
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
# 2. Paleta: plum-pink (lashbloom) -> rojo (K&B Moving, su logo real rojo/blanco)
# ---------------------------------------------------------------------------
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

RING = "rgba(160,85,74"     # shifted (160,74,114)
SHADOW = "rgba(51,36,34"    # shifted (51,34,44)
HOVERHEX = "#f0c5be"        # shifted #f0bed7

# ---------------------------------------------------------------------------
# 3. Globales: sin booking/IG -> tel: / mailto: real encontrado en su rotulo
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+12397380118"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_MAIL_URL = "mailto:kbmovingandstoragellc@gmail.com"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_MAIL_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_MAIL_LABEL = "kbmovingandstoragellc@gmail.com"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_MAIL_LABEL)
print("GLOBALS done")

NEW_REVIEWS_URL = "https://www.google.com/search?q=K%26B+Moving+And+Storage+LLC+Fort+Myers+FL+reviews"
NEW_MAPS = "https://www.google.com/maps?q=Fort+Myers,+FL"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>K&amp;B Moving And Storage · Movers in Fort Myers, FL | 4.8 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="K&amp;B Moving And Storage LLC, Fort Myers FL: local moving, packing and furniture wrapping across Southwest Florida. 4.8 stars across 22 Google reviews. Call or email for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="K&amp;B Moving And Storage · Movers in Fort Myers, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Local moving, packing and furniture wrapping. 4.8 on Google with 22 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-tagline-shirt.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MovingCompany",
    "name": "K&amp;B Moving And Storage LLC",
    "description": "Moving company serving Fort Myers and Southwest Florida: local moving, packing, furniture wrapping and loading help.",
    "areaServed": "Fort Myers, FL",
    "telephone": "+1-239-738-0118",
    "email": "kbmovingandstoragellc@gmail.com",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "22", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Moving services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Local Moving" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Packing &amp; Furniture Wrapping" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Loading &amp; Unloading Help" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Specialty &amp; Motorcycle Moves" } }
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
    '<img src="assets/logo.jpg" alt="K&amp;B Moving And Storage" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">K&amp;B <span class="text-[color:var(--accent-deep)]">Moving</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">K&amp;B</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">K&amp;B Moving</span>')
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
    'data-es="Fort Myers, FL · Movers" data-en="Fort Myers, FL · Movers">Fort Myers, FL · Movers</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="It&#39;s not what you move." data-en="It&#39;s not what you move.">It&#39;s not what you move.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="It&#39;s how you" data-en="It&#39;s how you">It&#39;s how you</span><br /><span data-es="move it, done " data-en="move it, done ">move it, done </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Local moving, packing and furniture wrapping across Fort Myers and Southwest Florida, from single rooms and motorcycles to full households. Licensed and insured, with a 4.8 rating across 22 Google reviews." data-en="Local moving, packing and furniture wrapping across Fort Myers and Southwest Florida, from single rooms and motorcycles to full households. Licensed and insured, with a 4.8 rating across 22 Google reviews.">Local moving, packing and furniture wrapping across Fort Myers and Southwest Florida, from single rooms and motorcycles to full households. Licensed and insured, with a 4.8 rating across 22 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.8 · 22 reviews on Google" data-en="4.8 · 22 reviews on Google">4.8 · 22 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_MAIL_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (239) 738-0118" data-en="Call (239) 738-0118">Call (239) 738-0118</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_MAIL_URL + '''" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
            ''' + NEW_MAIL_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-tagline-shirt.jpg" alt="A K&amp;B Moving And Storage mover carrying boxes on a dolly in Fort Myers, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Rated" data-en="Rated">Rated</p>
            <p class="font-display text-lg">5 Star Reviews</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Licensed &amp; insured" data-en="Licensed &amp; insured">Licensed &amp; insured</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="22">22</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Moving <span class="text-shine">&amp;</span> Storage</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Empaque · Carga" data-en="Packing · Loading">Packing · Loading</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">Licensed</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="&amp; Insured" data-en="&amp; Insured">&amp; Insured</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Fort Myers</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Southwest Florida" data-en="Southwest Florida">Southwest Florida</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Local Moves"),
    ("Hybrid Set", "Furniture Wrapping"),
    ("Volume Set", "Packing Service"),
    ("Mega Volume", "Loading Help"),
    ("Bottom Lashes", "Specialty Moves"),
    ("West Palm Beach, FL", "Fort Myers, FL"),
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
          <img src="assets/about-team-car.jpg" alt="The K&amp;B Moving And Storage team with their branded vehicle in Fort Myers, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One team," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="licensed and insured" data-en="licensed and insured">licensed and insured</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="K&amp;B Moving And Storage LLC is a licensed and insured moving company serving Fort Myers and Southwest Florida. The crew handles everything from a single wrapped armoire to a full household, and even secures motorcycles and specialty items for transport." data-en="K&amp;B Moving And Storage LLC is a licensed and insured moving company serving Fort Myers and Southwest Florida. The crew handles everything from a single wrapped armoire to a full household, and even secures motorcycles and specialty items for transport.">K&amp;B Moving And Storage LLC is a licensed and insured moving company serving Fort Myers and Southwest Florida. The crew handles everything from a single wrapped armoire to a full household, and even secures motorcycles and specialty items for transport.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.8 rating across 22 Google reviews, and customers who call K&amp;B courteous, careful and top notch." data-en="The result: a 4.8 rating across 22 Google reviews, and customers who call K&amp;B courteous, careful and top notch.">The result: a 4.8 rating across 22 Google reviews, and customers who call K&amp;B courteous, careful and top notch.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="22">22</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Insured" data-en="Insured">Insured</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Licensed crew" data-en="Licensed crew">Licensed crew</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="K&amp;B Moving And Storage" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">K&amp;B Moving And Storage · <span class="text-[color:var(--ink-40)]" data-es="Moving crew" data-en="Moving crew">Moving crew</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your move," data-en="Your move,">Your move,</span> <span class="text-shine" data-es="handled with care" data-en="handled with care">handled with care</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or email" data-en="Call or email">Call or email</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Reach out by phone or email with your move date and details, and get a straightforward price." data-en="Reach out by phone or email with your move date and details, and get a straightforward price.">Reach out by phone or email with your move date and details, and get a straightforward price.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Careful wrapping" data-en="Careful wrapping">Careful wrapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Furniture and specialty items get wrapped and secured, even motorcycles, so nothing gets damaged in transit." data-en="Furniture and specialty items get wrapped and secured, even motorcycles, so nothing gets damaged in transit.">Furniture and specialty items get wrapped and secured, even motorcycles, so nothing gets damaged in transit.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Loading &amp; drive" data-en="Loading &amp; drive">Loading &amp; drive</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew loads carefully and drives your things safely to the new address, on time, every time." data-en="The crew loads carefully and drives your things safely to the new address, on time, every time.">The crew loads carefully and drives your things safely to the new address, on time, every time.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Unload &amp; walkthrough" data-en="Unload &amp; walkthrough">Unload &amp; walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew unloads, places furniture where you want it, and walks the finished job with you." data-en="The crew unloads, places furniture where you want it, and walks the finished job with you.">The crew unloads, places furniture where you want it, and walks the finished job with you.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine" data-es="every move" data-en="every move">every move</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two moves are the same, so every job gets its own honest quote by phone or email, before anything is booked." data-en="No two moves are the same, so every job gets its own honest quote by phone or email, before anything is booked.">No two moves are the same, so every job gets its own honest quote by phone or email, before anything is booked.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: ''' + RING + ''',0.4); box-shadow: 0 18px 50px ''' + SHADOW + ''',0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Local Moving" data-en="Local Moving">Local Moving</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-service local moves across Fort Myers and Southwest Florida, from single rooms to full households." data-en="Full-service local moves across Fort Myers and Southwest Florida, from single rooms to full households.">Full-service local moves across Fort Myers and Southwest Florida, from single rooms to full households.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it safe" data-en="Keep it safe">Keep it safe</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Packing &amp; Furniture Wrapping" data-en="Packing &amp; Furniture Wrapping">Packing &amp; Furniture Wrapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full packing service with real moving blankets and shrink wrap, so furniture and boxes travel damage-free." data-en="Full packing service with real moving blankets and shrink wrap, so furniture and boxes travel damage-free.">Full packing service with real moving blankets and shrink wrap, so furniture and boxes travel damage-free.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="By the hour" data-en="By the hour">By the hour</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Loading &amp; Unloading Help" data-en="Loading &amp; Unloading Help">Loading &amp; Unloading Help</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Moving labor to load or unload your own truck, trailer or storage unit, with careful handling throughout." data-en="Moving labor to load or unload your own truck, trailer or storage unit, with careful handling throughout.">Moving labor to load or unload your own truck, trailer or storage unit, with careful handling throughout.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Not your average load" data-en="Not your average load">Not your average load</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Specialty &amp; Motorcycle Moves" data-en="Specialty &amp; Motorcycle Moves">Specialty &amp; Motorcycle Moves</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Motorcycles and other specialty items secured and transported with the same care as any piece of furniture." data-en="Motorcycles and other specialty items secured and transported with the same care as any piece of furniture.">Motorcycles and other specialty items secured and transported with the same care as any piece of furniture.</p>
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
            <li class="flex items-center gap-2" data-es="Apartment moves" data-en="Apartment moves">Apartment moves</li>
            <li class="flex items-center gap-2" data-es="Full house moves" data-en="Full house moves">Full house moves</li>
            <li class="flex items-center gap-2" data-es="Long-distance help" data-en="Long-distance help">Long-distance help</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Packing" data-en="Packing">Packing</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Furniture wrapping" data-en="Furniture wrapping">Furniture wrapping</li>
            <li class="flex items-center gap-2" data-es="Box packing" data-en="Box packing">Box packing</li>
            <li class="flex items-center gap-2" data-es="Shrink wrap &amp; totes" data-en="Shrink wrap &amp; totes">Shrink wrap &amp; totes</li>
            <li class="flex items-center gap-2" data-es="Fragile item care" data-en="Fragile item care">Fragile item care</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Specialty" data-en="Specialty">Specialty</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Motorcycle transport" data-en="Motorcycle transport">Motorcycle transport</li>
            <li class="flex items-center gap-2" data-es="U-Haul loading help" data-en="U-Haul loading help">U-Haul loading help</li>
            <li class="flex items-center gap-2" data-es="Storage unit moves" data-en="Storage unit moves">Storage unit moves</li>
            <li class="flex items-center gap-2" data-es="Residential &amp; light commercial" data-en="Residential &amp; light commercial">Residential &amp; light commercial</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and distance. Call (239) 738-0118 or email for a free quote." data-en="Pricing depends on scope and distance. Call (239) 738-0118 or email for a free quote.">Pricing depends on scope and distance. Call (239) 738-0118 or email for a free quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="moves" data-en="moves">moves</span>')
rep('''<a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_MAIL_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_MAIL_URL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
          ''' + NEW_MAIL_LABEL + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Transporte de motocicleta asegurado" data-en="A motorcycle secured for transport">A motorcycle secured for transport</span><img src="assets/gallery-motorcycle.jpg" alt="A motorcycle strapped and secured inside a K&amp;B Moving And Storage truck" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Armario envuelto para su proteccion" data-en="An armoire wrapped for protection">An armoire wrapped for protection</span><img src="assets/gallery-wrapped-armoire.jpg" alt="A wrapped armoire protected for a move by K&amp;B Moving And Storage" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cajas en movimiento" data-en="Boxes on the move">Boxes on the move</span><img src="assets/gallery-dolly-boxes.jpg" alt="A K&amp;B Moving And Storage mover carrying boxes on a dolly" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Camion cargado con cuidado" data-en="Truck loaded with care">Truck loaded with care</span><img src="assets/gallery-truck-totes.jpg" alt="A moving truck loaded carefully by K&amp;B Moving And Storage" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Listos para descargar" data-en="Ready to unload">Ready to unload</span><img src="assets/gallery-truck-open.jpg" alt="A K&amp;B Moving And Storage truck open and ready to unload" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Fort Myers" data-en="What Fort Myers">What Fort Myers</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.8 out of 5 · 22 reviews on Google" data-en="4.8 out of 5 · 22 reviews on Google">4.8 out of 5 · 22 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Kenny, Eric and Jordan worked diligently! They did an amazing job protecting our belongings on a long trip and also moving it into our new home! They had great attitudes the whole time working!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Libby Swartz</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"K &amp; B Moving and Storage is a top notch mover. They were courteous and polite from the moment they arrived. They were careful with the items that were being moved and the items that were already in the house. They were also very..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dominic Pisano</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"They do an excellent job. Carefully pack and move your possessions with no damage. Very accommodating. I've used them twice for small 2 hour jobs and plan to use them again as we move..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jack Murray</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 22 reviews on Google" data-en="Read all 22 reviews on Google">Read all 22 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (sin direccion fija: area de servicio)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Fort Myers, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="K&amp;B Moving And Storage serves Fort Myers, Lehigh Acres and the surrounding Southwest Florida area." data-en="K&amp;B Moving And Storage serves Fort Myers, Lehigh Acres and the surrounding Southwest Florida area.">K&amp;B Moving And Storage serves Fort Myers, Lehigh Acres and the surrounding Southwest Florida area.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Saturday, with evening availability some days. Closed Sunday." data-en="Monday to Saturday, with evening availability some days. Closed Sunday.">Monday to Saturday, with evening availability some days. Closed Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_TEL + '''" data-es="Call (239) 738-0118" data-en="Call (239) 738-0118">Call (239) 738-0118</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener">''' + NEW_MAIL_LABEL + '''</a>
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
              <p class="font-medium mb-1" data-es="Email" data-en="Email">Email</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Send move details and get a written quote back by email." data-en="Send move details and get a written quote back by email.">Send move details and get a written quote back by email.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING + ''',0.4)]" href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener">''' + NEW_MAIL_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: K&amp;B Moving And Storage service area, Fort Myers FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="It&#39;s not what you move." data-en="It&#39;s not what you move.">It&#39;s not what you move.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call fixes" data-en="One call fixes">One call fixes</span> <span class="text-shine" data-es="your move" data-en="your move">your move</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (239) 738-0118 or email for a free, honest quote on your move, packing job or motorcycle transport." data-en="Call (239) 738-0118 or email for a free, honest quote on your move, packing job or motorcycle transport.">Call (239) 738-0118 or email for a free, honest quote on your move, packing job or motorcycle transport.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (239) 738-0118" data-en="Call (239) 738-0118">Call (239) 738-0118</a>
        <a href="''' + NEW_MAIL_URL + '''" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Email for a quote" data-en="Email for a quote">Email for a quote</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">K&amp;B Moving</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,197,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="K&amp;B Moving And Storage" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,197,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">K&amp;B Moving And Storage</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Mudanzas con licencia y seguro en Fort Myers, FL." data-en="Licensed and insured moving company in Fort Myers, FL.">Licensed and insured moving company in Fort Myers, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Sirviendo a Fort Myers, FL" data-en="Serving Fort Myers, FL">Serving Fort Myers, FL</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[''' + HOVERHEX + ''']" data-es="Call (239) 738-0118" data-en="Call (239) 738-0118">Call (239) 738-0118</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HOVERHEX + ''']">Instagram · ''' + NEW_MAIL_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Email" data-en="Email">Email</p>
        <p><a href="''' + NEW_MAIL_URL + '''" class="hover:text-[''' + HOVERHEX + ''']">''' + NEW_MAIL_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 K&amp;B Moving And Storage LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call K&amp;B Moving And Storage">')
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
    "Fort Myers, FL · Movers": "Fort Myers, FL · Mudanzas",
    "It&#39;s not what you move.": "No es lo que mudas.",
    "It&#39;s how you": "Es como lo",
    "move it, done ": "mudas, hecho ",
    "right": "bien",
    "Local moving, packing and furniture wrapping across Fort Myers and Southwest Florida, from single rooms and motorcycles to full households. Licensed and insured, with a 4.8 rating across 22 Google reviews.":
        "Mudanzas locales, empaque y envoltura de muebles en Fort Myers y el suroeste de Florida, desde una sola habitacion y motocicletas hasta casas completas. Con licencia y seguro, y una calificacion de 4.8 en 22 resenas de Google.",
    "4.8 · 22 reviews on Google": "4.8 · 22 resenas en Google",
    "Call (239) 738-0118": "Llama al (239) 738-0118",
    "Rated": "Calificados",
    "Licensed &amp; insured": "Con licencia y seguro",
    "&amp; Insured": "y Seguro",
    "Southwest Florida": "Suroeste de Florida",
    "licensed and insured": "con licencia y seguro",
    "K&amp;B Moving And Storage LLC is a licensed and insured moving company serving Fort Myers and Southwest Florida. The crew handles everything from a single wrapped armoire to a full household, and even secures motorcycles and specialty items for transport.":
        "K&amp;B Moving And Storage LLC es una empresa de mudanzas con licencia y seguro que sirve a Fort Myers y el suroeste de Florida. El equipo maneja desde un solo armario envuelto hasta una casa completa, e incluso asegura motocicletas y articulos especiales para transporte.",
    "The result: a 4.8 rating across 22 Google reviews, and customers who call K&amp;B courteous, careful and top notch.":
        "El resultado: una calificacion de 4.8 en 22 resenas de Google, y clientes que describen a K&amp;B como cortes, cuidadoso y de primera.",
    "Insured": "Asegurados",
    "Licensed crew": "Equipo con licencia",
    "Moving crew": "Equipo de mudanzas",
    "handled with care": "manejada con cuidado",
    "Call or email": "Llama o escribe",
    "Reach out by phone or email with your move date and details, and get a straightforward price.":
        "Contacta por telefono o correo con la fecha de tu mudanza y los detalles, y recibe un precio claro.",
    "Careful wrapping": "Envoltura cuidadosa",
    "Furniture and specialty items get wrapped and secured, even motorcycles, so nothing gets damaged in transit.":
        "Los muebles y articulos especiales se envuelven y aseguran, incluso motocicletas, para que nada se dane en el traslado.",
    "Loading &amp; drive": "Carga y traslado",
    "The crew loads carefully and drives your things safely to the new address, on time, every time.":
        "El equipo carga con cuidado y transporta tus cosas de forma segura a la nueva direccion, a tiempo, siempre.",
    "Unload &amp; walkthrough": "Descarga y revision",
    "The crew unloads, places furniture where you want it, and walks the finished job with you.":
        "El equipo descarga, coloca los muebles donde los quieras, y revisa el trabajo terminado contigo.",
    "every move": "cada mudanza",
    "No two moves are the same, so every job gets its own honest quote by phone or email, before anything is booked.":
        "Ninguna mudanza es igual, asi que cada trabajo recibe su propia cotizacion honesta por telefono o correo, antes de reservar.",
    "Most requested": "Lo mas solicitado",
    "Local Moving": "Mudanzas Locales",
    "Full-service local moves across Fort Myers and Southwest Florida, from single rooms to full households.":
        "Mudanzas locales completas en Fort Myers y el suroeste de Florida, desde una sola habitacion hasta casas completas.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Keep it safe": "Mantenlo seguro",
    "Packing &amp; Furniture Wrapping": "Empaque y Envoltura de Muebles",
    "Full packing service with real moving blankets and shrink wrap, so furniture and boxes travel damage-free.":
        "Servicio de empaque completo con mantas reales de mudanza y plastico envolvente, para que muebles y cajas viajen sin danos.",
    "By the hour": "Por hora",
    "Loading &amp; Unloading Help": "Ayuda de Carga y Descarga",
    "Moving labor to load or unload your own truck, trailer or storage unit, with careful handling throughout.":
        "Mano de obra de mudanza para cargar o descargar tu propio camion, trailer o unidad de almacenaje, con manejo cuidadoso en todo momento.",
    "Not your average load": "No es una carga comun",
    "Specialty &amp; Motorcycle Moves": "Mudanzas Especiales y de Motocicletas",
    "Motorcycles and other specialty items secured and transported with the same care as any piece of furniture.":
        "Motocicletas y otros articulos especiales asegurados y transportados con el mismo cuidado que cualquier mueble.",
    "Moving": "Mudanzas",
    "Local moves": "Mudanzas locales",
    "Apartment moves": "Mudanzas de apartamentos",
    "Full house moves": "Mudanzas de casa completa",
    "Long-distance help": "Ayuda de larga distancia",
    "Packing": "Empaque",
    "Furniture wrapping": "Envoltura de muebles",
    "Box packing": "Empaque de cajas",
    "Shrink wrap &amp; totes": "Plastico envolvente y contenedores",
    "Fragile item care": "Cuidado de articulos fragiles",
    "Specialty": "Especialidad",
    "Motorcycle transport": "Transporte de motocicletas",
    "U-Haul loading help": "Ayuda de carga U-Haul",
    "Storage unit moves": "Mudanzas de unidades de almacenaje",
    "Residential &amp; light commercial": "Residencial y comercial ligero",
    "Pricing depends on scope and distance. Call (239) 738-0118 or email for a free quote.":
        "El precio depende del alcance y la distancia. Llama al (239) 738-0118 o escribe para una cotizacion gratis.",
    "moves": "mudanzas",
    "What Fort Myers": "Lo que dicen los",
    "customers say": "clientes de Fort Myers",
    "4.8 out of 5 · 22 reviews on Google": "4.8 de 5 · 22 resenas en Google",
    "Read all 22 reviews on Google": "Lee las 22 resenas en Google",
    "Serving": "Sirviendo a",
    "Service area": "Area de servicio",
    "K&amp;B Moving And Storage serves Fort Myers, Lehigh Acres and the surrounding Southwest Florida area.":
        "K&amp;B Moving And Storage sirve a Fort Myers, Lehigh Acres y el area circundante del suroeste de Florida.",
    "View on map": "Ver en el mapa",
    "Hours": "Horario",
    "Monday to Saturday, with evening availability some days. Closed Sunday.": "Lunes a sabado, con disponibilidad en la tarde algunos dias. Cerrado los domingos.",
    "Email": "Correo",
    "Send move details and get a written quote back by email.": "Envia los detalles de tu mudanza y recibe una cotizacion por escrito por correo.",
    "your move": "tu mudanza",
    "Call (239) 738-0118 or email for a free, honest quote on your move, packing job or motorcycle transport.":
        "Llama al (239) 738-0118 o escribe para una cotizacion gratis y honesta de tu mudanza, trabajo de empaque o transporte de motocicleta.",
    "Email for a quote": "Escribe para cotizar",
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
