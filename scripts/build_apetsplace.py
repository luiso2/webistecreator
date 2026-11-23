import re
import os
import colorsys

SLUG = "a-pets-place-cape-coral"
SRC = "templates/light-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()

# ============================================================
# 0. Funciones de shift de color
# ============================================================
TARGET_HUE = 27 / 360.0
SAT_MUL = 0.93
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
# 2. PALETA: plum-pink (lashbloom) -> warm terracotta/peach (A Pets Place)
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
NEW_TEL = "tel:+12393393555"
NEW_FB_URL = "https://www.facebook.com/APetsPlace/"
NEW_FB_LABEL = "facebook.com/APetsPlace"
NEW_REVIEWS_URL = "https://www.google.com/maps/place/A+Pets+Place/@26.6428684,-82.0017418,17z/data=!3m1!4b1!4m6!3m5!1s0x88db4660a5198269:0x35c8c15b7919b161!8m2!3d26.6428684!4d-82.0017418!16s%2Fg%2F11b6bq_7q7"
NEW_ADDR = "1316 SW 4th Terrace #103, Cape Coral, FL 33991"
NEW_MAPS = "https://www.google.com/maps?q=1316+SW+4th+Terrace+%23103,+Cape+Coral,+FL+33991"

OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
rep_all(OLD_BOOK, NEW_TEL, expect=13)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
rep_all(OLD_IG_URL, NEW_FB_URL, expect=6)

rep_all("@_lashbloom", NEW_FB_LABEL, expect=4)

IG_ICON_INNER = '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>'
FB_ICON_INNER = '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'
rep_all(IG_ICON_INNER, FB_ICON_INNER, expect=3)
print("GLOBALS done")

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>A Pets Place · Dog &amp; Cat Grooming in Cape Coral, FL | 4.8 Stars</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="A Pets Place, Cape Coral FL: cage-free dog and cat grooming with longtime groomer Dana. Baths, haircuts, nail trims and more. 4.8 stars across 57 reviews." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="A Pets Place · Dog &amp; Cat Grooming in Cape Coral, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Cage-free dog and cat grooming in Cape Coral, FL. 4.8 stars, 57 reviews. Call to book." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-shihtzu-groomed.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-shihtzu-groomed.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "A Pets Place",
    "description": "Cage-free dog and cat grooming salon in Cape Coral, FL: baths, haircuts, nail trims, ear cleaning and de-shedding, one pet at a time.",
    "address": { "@type": "PostalAddress", "streetAddress": "1316 SW 4th Terrace #103", "addressLocality": "Cape Coral", "addressRegion": "FL", "postalCode": "33991", "addressCountry": "US" },
    "telephone": "+1-239-339-3555",
    "sameAs": ["''' + NEW_FB_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "57", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "16:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "15:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Pet grooming services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Dog Grooming" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cat Grooming" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Nail Trimming" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "De-Shedding Treatment" } }
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
    '<span class="pre-mono">APP</span>\n    <span class="pre-word">A Pets Place</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<img src="assets/hero-shihtzu-groomed.jpg" alt="A Pets Place" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">A Pets <span class="text-[color:var(--accent-deep)]">Place</span></span>')
rep('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n          <span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Cape Coral, FL · Pet Grooming" data-en="Cape Coral, FL · Pet Grooming">Cape Coral, FL · Pet Grooming</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Calm, cage-free grooming for your best friend." data-en="Calm, cage-free grooming for your best friend.">Calm, cage-free grooming for your best friend.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Calm, cage-free grooming" data-en="Calm, cage-free grooming">Calm, cage-free grooming</span><br /><span data-es="for dogs and cats, done " data-en="for dogs and cats, done ">for dogs and cats, done </span><span class="text-shine" data-es="with care" data-en="with care">with care</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="A Pets Place grooms dogs and cats one at a time, with no cages: baths, haircuts, nail trims, ear cleaning and de-shedding in a calm space. Longtime groomer Dana has kept clients coming back for 8, even 16 years, and they still ask for her by name." data-en="A Pets Place grooms dogs and cats one at a time, with no cages: baths, haircuts, nail trims, ear cleaning and de-shedding in a calm space. Longtime groomer Dana has kept clients coming back for 8, even 16 years, and they still ask for her by name.">A Pets Place grooms dogs and cats one at a time, with no cages: baths, haircuts, nail trims, ear cleaning and de-shedding in a calm space. Longtime groomer Dana has kept clients coming back for 8, even 16 years, and they still ask for her by name.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.8 · 57 reviews on Google &amp; Facebook" data-en="4.8 · 57 reviews on Google &amp; Facebook">4.8 · 57 reviews on Google &amp; Facebook</span>')
rep('''<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''',
    '''<span data-es="Call (239) 339-3555" data-en="Call (239) 339-3555">Call (239) 339-3555</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-shihtzu-groomed.jpg" alt="A freshly groomed Shih Tzu after a visit to A Pets Place in Cape Coral" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Hours" data-en="Hours">Hours</p>
            <p class="font-display text-lg">Tue - Sat</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="9 AM - 4 PM" data-en="9 AM - 4 PM">9 AM - 4 PM</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="57">57</span> <span data-es="reviews on Google &amp; FB" data-en="reviews on Google &amp; FB">reviews on Google &amp; FB</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Dogs <span class="text-shine">&amp;</span> Cats</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Grooming for both" data-en="Grooming for both">Grooming for both</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">16 <span class="text-shine" data-es="years" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="One client, still coming back" data-en="One client, still coming back">One client, still coming back</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Cape Coral</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1316 SW 4th Terrace</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Classic Set", "Dog Grooming"),
    ("Hybrid Set", "Cat Grooming"),
    ("Volume Set", "Nail Trim"),
    ("Mega Volume", "De-Shedding"),
    ("Bottom Lashes", "Cage-Free"),
    ("West Palm Beach, FL", "Cape Coral, FL"),
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
          <img src="assets/about-salon-calm-area.jpg" alt="A groomed dog resting calmly on a towel inside A Pets Place, cage-free" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/about-shihtzu-portrait.jpg" alt="Close-up of a freshly groomed Shih Tzu at A Pets Place" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="A cage-free space" data-en="A cage-free space">A cage-free space</span><br /><span class="text-shine" data-es="built around comfort" data-en="built around comfort">built around comfort</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="A Pets Place is a cage-free grooming salon in Cape Coral where dogs and cats are groomed one at a time, never kenneled. Longtime groomer Dana is named by clients again and again, some of whom have followed her for 16 years." data-en="A Pets Place is a cage-free grooming salon in Cape Coral where dogs and cats are groomed one at a time, never kenneled. Longtime groomer Dana is named by clients again and again, some of whom have followed her for 16 years.">A Pets Place is a cage-free grooming salon in Cape Coral where dogs and cats are groomed one at a time, never kenneled. Longtime groomer Dana is named by clients again and again, some of whom have followed her for 16 years.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.8-star rating across 57 reviews between Google and Facebook, clients who drive across town just to see Dana, and a shop reviewers describe as spotless and calm." data-en="The result: a 4.8-star rating across 57 reviews between Google and Facebook, clients who drive across town just to see Dana, and a shop reviewers describe as spotless and calm.">The result: a 4.8-star rating across 57 reviews between Google and Facebook, clients who drive across town just to see Dana, and a shop reviewers describe as spotless and calm.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="57">57</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="One pet at a time" data-en="One pet at a time">One pet at a time</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/hero-shihtzu-groomed.jpg" alt="A Pets Place" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Dana · <span class="text-[color:var(--ink-40)]" data-es="Longtime groomer" data-en="Longtime groomer">Longtime groomer</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Your visit, step by step" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your visit," data-en="Your visit,">Your visit,</span> <span class="text-shine" data-es="paw by paw" data-en="paw by paw">paw by paw</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Drop-off" data-en="Drop-off">Drop-off</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Bring your dog or cat in; Dana checks coat, skin and any special requests before starting." data-en="Bring your dog or cat in; Dana checks coat, skin and any special requests before starting.">Bring your dog or cat in; Dana checks coat, skin and any special requests before starting.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Bath &amp; dry" data-en="Bath &amp; dry">Bath &amp; dry</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A full bath, shampoo suited to their coat, and a gentle hand-dry, one pet at a time, no cages." data-en="A full bath, shampoo suited to their coat, and a gentle hand-dry, one pet at a time, no cages.">A full bath, shampoo suited to their coat, and a gentle hand-dry, one pet at a time, no cages.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Cut &amp; style" data-en="Cut &amp; style">Cut &amp; style</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Haircut, nail trim, ear cleaning and any add-ons like de-shedding, finished to the style you asked for." data-en="Haircut, nail trim, ear cleaning and any add-ons like de-shedding, finished to the style you asked for.">Haircut, nail trim, ear cleaning and any add-ons like de-shedding, finished to the style you asked for.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Ready for pickup" data-en="Ready for pickup">Ready for pickup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call when they are done. Most pets are in and out the same day, calm and freshly groomed." data-en="Call when they are done. Most pets are in and out the same day, calm and freshly groomed.">Call when they are done. Most pets are in and out the same day, calm and freshly groomed.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS (variante adaptada: sin precios, "se cotiza")
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="What we" data-en="What we">What we</span> <span class="text-shine" data-es="groom" data-en="groom">groom</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every pet is sized up before we quote: breed, coat and size change the price. Call us for a quote." data-en="Every pet is sized up before we quote: breed, coat and size change the price. Call us for a quote.">Every pet is sized up before we quote: breed, coat and size change the price. Call us for a quote.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cage-Free" data-en="Cage-Free">Cage-Free</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Dog Grooming" data-en="Dog Grooming">Dog Grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full bath, haircut and style for dogs of any size, groomed one at a time, never kenneled." data-en="Full bath, haircut and style for dogs of any size, groomed one at a time, never kenneled.">Full bath, haircut and style for dogs of any size, groomed one at a time, never kenneled.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every pet is quoted" data-en="Every pet is quoted">Every pet is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Bath &amp; Full Groom" data-en="Bath &amp; Full Groom">Bath &amp; Full Groom</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A complete bath, blow-dry, haircut and finishing touches, the combination most clients book." data-en="A complete bath, blow-dry, haircut and finishing touches, the combination most clients book.">A complete bath, blow-dry, haircut and finishing touches, the combination most clients book.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every pet is quoted" data-en="Every pet is quoted">Every pet is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Feline friendly" data-en="Feline friendly">Feline friendly</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cat Grooming" data-en="Cat Grooming">Cat Grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gentle bathing, de-matting and trims for cats, handled calmly and at their own pace." data-en="Gentle bathing, de-matting and trims for cats, handled calmly and at their own pace.">Gentle bathing, de-matting and trims for cats, handled calmly and at their own pace.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every pet is quoted" data-en="Every pet is quoted">Every pet is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Add-ons" data-en="Add-ons">Add-ons</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Nails, Ears &amp; More" data-en="Nails, Ears &amp; More">Nails, Ears &amp; More</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Nail trims, ear cleaning and de-shedding treatments, added to any grooming visit." data-en="Nail trims, ear cleaning and de-shedding treatments, added to any grooming visit.">Nail trims, ear cleaning and de-shedding treatments, added to any grooming visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Every pet is quoted" data-en="Every pet is quoted">Every pet is quoted</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Services" data-en="Services">Services</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Bathing" data-en="Bathing">Bathing</li>
            <li class="flex items-center gap-2" data-es="Haircuts &amp; styling" data-en="Haircuts &amp; styling">Haircuts &amp; styling</li>
            <li class="flex items-center gap-2" data-es="Nail trimming" data-en="Nail trimming">Nail trimming</li>
            <li class="flex items-center gap-2" data-es="Ear cleaning" data-en="Ear cleaning">Ear cleaning</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="We Groom" data-en="We Groom">We Groom</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Dogs, all sizes" data-en="Dogs, all sizes">Dogs, all sizes</li>
            <li class="flex items-center gap-2" data-es="Cats" data-en="Cats">Cats</li>
            <li class="flex items-center gap-2" data-es="Puppies, first groom" data-en="Puppies, first groom">Puppies, first groom</li>
            <li class="flex items-center gap-2" data-es="Matted or double coats" data-en="Matted or double coats">Matted or double coats</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Always Included" data-en="Always Included">Always Included</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Cage-free care" data-en="Cage-free care">Cage-free care</li>
            <li class="flex items-center gap-2" data-es="One pet at a time" data-en="One pet at a time">One pet at a time</li>
            <li class="flex items-center gap-2" data-es="De-shedding available" data-en="De-shedding available">De-shedding available</li>
            <li class="flex items-center gap-2" data-es="Teeth cleaning add-on" data-en="Teeth cleaning add-on">Teeth cleaning add-on</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + S(NEW_SERVICES_GRID) + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Every pet is quoted by size, breed and coat. Call (239) 339-3555 to ask." data-en="Every pet is quoted by size, breed and coat. Call (239) 339-3555 to ask.">Every pet is quoted by size, breed and coat. Call (239) 339-3555 to ask.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA (1 wide + 4 narrow: 5 fotos reales distintas disponibles)
# ============================================================
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="results" data-en="results">results</span>')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Fresh groom, happy client" data-en="Fresh groom, happy client">Fresh groom, happy client</span><img src="assets/gallery-bichon-happy.jpg" alt="A happy, freshly groomed Bichon dog after a visit to A Pets Place in Cape Coral" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Two best friends, freshly groomed" data-en="Two best friends, freshly groomed">Two best friends, freshly groomed</span><img src="assets/gallery-two-shihtzus-home.jpg" alt="Two groomed Shih Tzu dogs sitting together after visiting A Pets Place" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Clean cut, calm pup" data-en="Clean cut, calm pup">Clean cut, calm pup</span><img src="assets/about-shihtzu-portrait.jpg" alt="Close-up portrait of a freshly groomed Shih Tzu at A Pets Place" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Resting after grooming, no cage" data-en="Resting after grooming, no cage">Resting after grooming, no cage</span><img src="assets/about-salon-calm-area.jpg" alt="A groomed dog resting calmly on a towel inside the cage-free salon" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Fresh haircut, ready to go" data-en="Fresh haircut, ready to go">Fresh haircut, ready to go</span><img src="assets/hero-shihtzu-groomed.jpg" alt="A Shih Tzu with a fresh haircut and ribbon leash at A Pets Place" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + S(NEW_GALLERY_GRID) + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Cape Coral" data-en="What Cape Coral">What Cape Coral</span> <span class="text-shine" data-es="pet parents say" data-en="pet parents say">pet parents say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.8 out of 5 · 57 reviews on Google &amp; Facebook" data-en="4.8 out of 5 · 57 reviews on Google &amp; Facebook">4.8 out of 5 · 57 reviews on Google &amp; Facebook</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"A pets place is the only place we trust to take care of our Saint Bernard Buda. They do an awesome job. I wouldn't hesitate to recommend them to anyone."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Michael Cullen</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Facebook" data-en="Facebook review">Facebook review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Dana has been our choice of grooming for 8 years at least. Both our dogs loved going to see her and the quality of work is second to none. But the best part is she doesn't kennel the dogs, she only has one there at a time."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rob James III</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I love Dana, have been going to her for over 16 years and I have followed her everywhere. She does an awesome job even when the dogs are aggressive, she knows how to handle them."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Vera Conner</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Facebook" data-en="Facebook review">Facebook review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read more reviews on Google" data-en="Read more reviews on Google">Read more reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Cape Coral</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Tuesday to Friday, 9 AM to 4 PM. Saturday, 9 AM to 3 PM. Closed Monday and Sunday." data-en="Tuesday to Friday, 9 AM to 4 PM. Saturday, 9 AM to 3 PM. Closed Monday and Sunday.">Tuesday to Friday, 9 AM to 4 PM. Saturday, 9 AM to 3 PM. Closed Monday and Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (239) 339-3555" data-en="Call (239) 339-3555">Call (239) 339-3555</a>''')
rep('''<p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>''',
    '''<p class="font-medium mb-1" data-es="Facebook" data-en="Facebook">Facebook</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See photos from other pet parents and send us a message before your visit." data-en="See photos from other pet parents and send us a message before your visit.">See photos from other pet parents and send us a message before your visit.</p>''')
rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Map: A Pets Place, 1316 SW 4th Terrace, Cape Coral FL"\n          src="' + NEW_MAPS + '&output=embed"')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Calm, cage-free grooming for your best friend." data-en="Calm, cage-free grooming for your best friend.">Calm, cage-free grooming for your best friend.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your pet&#39;s next groom" data-en="Your pet&#39;s next groom">Your pet&#39;s next groom</span> <span class="text-shine" data-es="is one call away" data-en="is one call away">is one call away</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (239) 339-3555 for a quote on your dog or cat&#39;s next groom. Cage-free, one pet at a time, with Dana&#39;s calm hands." data-en="Call (239) 339-3555 for a quote on your dog or cat&#39;s next groom. Cage-free, one pet at a time, with Dana&#39;s calm hands.">Call (239) 339-3555 for a quote on your dog or cat&#39;s next groom. Cage-free, one pet at a time, with Dana&#39;s calm hands.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (239) 339-3555" data-en="Call (239) 339-3555">Call (239) 339-3555</a>
        <a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Facebook" data-en="Follow on Facebook">Follow on Facebook</a>''')
print("CTA FINAL done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">A Pets Place</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/hero-shihtzu-groomed.jpg" alt="A Pets Place" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">A Pets Place</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Cage-free dog &amp; cat grooming in Cape Coral, FL. By appointment." data-en="Cage-free dog &amp; cat grooming in Cape Coral, FL. By appointment.">Cage-free dog &amp; cat grooming in Cape Coral, FL. By appointment.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#f0bed7]" data-es="Call (239) 339-3555" data-en="Call (239) 339-3555">Call (239) 339-3555</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · ''' + NEW_FB_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Facebook · ''' + NEW_FB_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 A Pets Place.</p>')
print("FOOTER done")

# ============================================================
# 18. Boton flotante (icono calendario -> telefono)
# ============================================================
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf2f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call A Pets Place">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf2f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n  </a>')
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
    "Cape Coral, FL · Pet Grooming": "Cape Coral, FL · Peluqueria Canina",
    "Calm, cage-free grooming for your best friend.": "Peluqueria tranquila y sin jaulas para tu mejor amigo.",
    "Calm, cage-free grooming": "Peluqueria tranquila y sin jaulas",
    "for dogs and cats, done ": "para perros y gatos, hecha ",
    "with care": "con cuidado",
    "A Pets Place grooms dogs and cats one at a time, with no cages: baths, haircuts, nail trims, ear cleaning and de-shedding in a calm space. Longtime groomer Dana has kept clients coming back for 8, even 16 years, and they still ask for her by name.":
        "A Pets Place atiende perros y gatos de uno en uno, sin jaulas: banos, cortes, corte de unas, limpieza de oidos y deslanado en un espacio tranquilo. La peluquera Dana lleva anos ganandose clientes que vuelven por 8, incluso 16 anos, y siguen pidiendo que los atienda ella.",
    "4.8 · 57 reviews on Google &amp; Facebook": "4.8 · 57 resenas en Google y Facebook",
    "Call (239) 339-3555": "Llama al (239) 339-3555",
    "Hours": "Horario",
    "9 AM - 4 PM": "9 AM - 4 PM",
    "reviews on Google &amp; FB": "resenas en Google y FB",
    "Grooming for both": "Atencion para ambos",
    "years": "anos",
    "One client, still coming back": "Una clienta, sigue volviendo",
    "Dogs, all sizes": "Perros, todos los tamanos",
    "Cats": "Gatos",
    "A cage-free space": "Un espacio sin jaulas",
    "built around comfort": "pensado para su comodidad",
    "A Pets Place is a cage-free grooming salon in Cape Coral where dogs and cats are groomed one at a time, never kenneled. Longtime groomer Dana is named by clients again and again, some of whom have followed her for 16 years.":
        "A Pets Place es un salon de peluqueria sin jaulas en Cape Coral donde perros y gatos se atienden de uno en uno, nunca enjaulados. Los clientes mencionan a la peluquera Dana una y otra vez, algunos la han seguido durante 16 anos.",
    "The result: a 4.8-star rating across 57 reviews between Google and Facebook, clients who drive across town just to see Dana, and a shop reviewers describe as spotless and calm.":
        "El resultado: una calificacion de 4.8 estrellas en 57 resenas entre Google y Facebook, clientes que cruzan la ciudad solo para ver a Dana, y un local que las resenas describen como impecable y tranquilo.",
    "One pet at a time": "Una mascota a la vez",
    "Longtime groomer": "Peluquera de toda la vida",
    "Your visit, step by step": "Tu cita, paso a paso",
    "Your visit,": "Tu cita,",
    "paw by paw": "pata por pata",
    "Drop-off": "Entrega",
    "Bring your dog or cat in; Dana checks coat, skin and any special requests before starting.":
        "Trae a tu perro o gato; Dana revisa el pelaje, la piel y cualquier pedido especial antes de empezar.",
    "Bath &amp; dry": "Bano y secado",
    "A full bath, shampoo suited to their coat, and a gentle hand-dry, one pet at a time, no cages.":
        "Un bano completo, shampoo segun su pelaje, y un secado suave a mano, de uno en uno, sin jaulas.",
    "Cut &amp; style": "Corte y estilo",
    "Haircut, nail trim, ear cleaning and any add-ons like de-shedding, finished to the style you asked for.":
        "Corte, corte de unas, limpieza de oidos y extras como deslanado, terminado con el estilo que pediste.",
    "Ready for pickup": "Listo para recoger",
    "Call when they are done. Most pets are in and out the same day, calm and freshly groomed.":
        "Te llamamos cuando este listo. La mayoria de las mascotas entran y salen el mismo dia, tranquilas y recien arregladas.",
    "What we": "Lo que",
    "groom": "atendemos",
    "Every pet is sized up before we quote: breed, coat and size change the price. Call us for a quote.":
        "Cada mascota se evalua antes de cotizar: raza, pelaje y tamano cambian el precio. Llamanos para cotizar.",
    "Cage-Free": "Sin Jaulas",
    "Dog Grooming": "Peluqueria Canina",
    "Full bath, haircut and style for dogs of any size, groomed one at a time, never kenneled.":
        "Bano completo, corte y estilo para perros de cualquier tamano, atendidos de uno en uno, nunca enjaulados.",
    "Every pet is quoted": "Cada mascota se cotiza",
    "Call": "Llamar",
    "Most requested": "Lo mas pedido",
    "Bath &amp; Full Groom": "Bano y Arreglo Completo",
    "A complete bath, blow-dry, haircut and finishing touches, the combination most clients book.":
        "Un bano completo, secado, corte y toques finales, la combinacion que mas reservan los clientes.",
    "Feline friendly": "Amigable con gatos",
    "Cat Grooming": "Peluqueria para Gatos",
    "Gentle bathing, de-matting and trims for cats, handled calmly and at their own pace.":
        "Bano suave, desenredado y recorte para gatos, con calma y a su propio ritmo.",
    "Add-ons": "Extras",
    "Nails, Ears &amp; More": "Unas, Oidos y Mas",
    "Nail trims, ear cleaning and de-shedding treatments, added to any grooming visit.":
        "Corte de unas, limpieza de oidos y tratamientos de deslanado, agregados a cualquier visita de peluqueria.",
    "Services": "Servicios",
    "Bathing": "Bano",
    "Haircuts &amp; styling": "Cortes y estilo",
    "Nail trimming": "Corte de unas",
    "Ear cleaning": "Limpieza de oidos",
    "We Groom": "Atendemos",
    "Puppies, first groom": "Cachorros, primer arreglo",
    "Matted or double coats": "Pelaje enredado o doble capa",
    "Always Included": "Siempre Incluido",
    "Cage-free care": "Cuidado sin jaulas",
    "De-shedding available": "Deslanado disponible",
    "Teeth cleaning add-on": "Extra de limpieza dental",
    "Every pet is quoted by size, breed and coat. Call (239) 339-3555 to ask.":
        "Cada mascota se cotiza segun tamano, raza y pelaje. Llama al (239) 339-3555 para preguntar.",
    "Real": "Resultados",
    "results": "reales",
    "What Cape Coral": "Lo que dicen los",
    "pet parents say": "duenos de mascotas en Cape Coral",
    "4.8 out of 5 · 57 reviews on Google &amp; Facebook": "4.8 de 5 · 57 resenas en Google y Facebook",
    "Read more reviews on Google": "Lee mas resenas en Google",
    "Facebook": "Facebook",
    "See photos from other pet parents and send us a message before your visit.":
        "Mira fotos de otros duenos de mascotas y escribenos antes de tu visita.",
    "Tuesday to Friday, 9 AM to 4 PM. Saturday, 9 AM to 3 PM. Closed Monday and Sunday.":
        "Martes a viernes, 9 AM a 4 PM. Sabado, 9 AM a 3 PM. Cerrado lunes y domingo.",
    "Your pet&#39;s next groom": "El proximo arreglo de tu mascota",
    "is one call away": "esta a una llamada de distancia",
    "Call (239) 339-3555 for a quote on your dog or cat&#39;s next groom. Cage-free, one pet at a time, with Dana&#39;s calm hands.":
        "Llama al (239) 339-3555 para cotizar el proximo arreglo de tu perro o gato. Sin jaulas, de uno en uno, con las manos tranquilas de Dana.",
    "Follow on Facebook": "Seguir en Facebook",
    "Cage-free dog &amp; cat grooming in Cape Coral, FL. By appointment.":
        "Peluqueria canina y felina sin jaulas en Cape Coral, FL. Con cita previa.",
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
