import re
import shutil

SLUG = "miami-cleanings-north-miami-beach"
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
# 2. Paleta: plum-pink (lashbloom) -> azul cielo / steel blue (Miami Cleanings)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#1f7a93"),
    ("#5c2140", "#0a2d38"),
    ("#f0bed7", "#bfe6f0"),
    ("#faf2f6", "#eef8fa"),
    ("#c47a9c", "#4fa7c4"),
    ("#8a5573", "#14414e"),
    ("#f3e0ea", "#dcf0f3"),
    ("#d9a8c2", "#9fd3e0"),
    ("#7d3457", "#155a70"),
    ("#5f2c48", "#1a4a5c"),
    ("#33222c", "#1b2a30"),
    ("#fbf3f8", "#eefbfc"),
    ("#fbeff5", "#e8f8fb"),
    ("#f8dfeb", "#d3eef5"),
    ("#f6f1ea", "#eef8fa"),
    ("#f2d5e3", "#cdeaf3"),
    ("#f2cfe0", "#cfeaf2"),
    ("#efd0e0", "#cdeef5"),
    ("#e5c1d4", "#bfe0ec"),
    ("#dc9dbe", "#6ec3dc"),
    ("#d3a2bc", "#9cd0dc"),
    ("#c9789f", "#52a9c9"),
    ("#b25a85", "#3f93b2"),
    ("#2a1722", "#0f2730"),
    ("#1f0f18", "#0a1c22"),
    ("#1c0f16", "#0b1b20"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(31,122,147"),
    ("rgba(51,34,44", "rgba(27,42,48"),
    ("rgba(240,190,215", "rgba(191,230,240"),
    ("rgba(70,25,50", "rgba(10,45,56"),
    ("rgba(250,242,246", "rgba(238,248,250"),
    ("rgba(125,52,87", "rgba(20,65,78"),
    ("rgba(253,246,250", "rgba(240,250,252"),
    ("rgba(40,16,30", "rgba(10,28,34"),
    ("rgba(233,205,186", "rgba(186,224,233"),
    ("rgba(185,138,128", "rgba(128,178,185"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform ni IG propio -> tel: + ficha de Google
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+17862943567"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/maps/place/MIAMI+CLEANINGS/@25.9278947,-80.1664783,17z/data=!4m7!3m6!1s0x88d9ad7687a51567:0x517f7c0a9ea856ed!8m2!3d25.9278947!4d-80.1664783!16s%2Fg%2F11qr9_g1l_"
c = h.count(OLD_IG_URL)
assert c == 6, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c == 4, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Miami Cleanings · Residential Cleaning in North Miami Beach, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Miami Cleanings, North Miami Beach FL: move-in/move-out deep cleaning, pet-friendly deep cleaning and standard home cleaning. 4.9 stars across 18 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Miami Cleanings · Residential Cleaning in North Miami Beach, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Move-in/move-out deep cleaning, pet-friendly cleaning and standard cleaning. 4.9 on Google with 18 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/hero-action.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/hero-action.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HousePainter",
    "@id": "https://siteforge-demos.odd-forest-9504.workers.dev/miami-cleanings-north-miami-beach/",
    "name": "Miami Cleanings",
    "description": "Residential cleaning service covering North Miami Beach and the greater Miami-Dade area: move-in/move-out deep cleaning, pet-friendly deep cleaning and standard home cleaning.",
    "areaServed": { "@type": "City", "name": "North Miami Beach, FL" },
    "telephone": "+1-786-294-3567",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "18", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Cleaning services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Move-In / Move-Out Deep Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Deep Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Standard Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Pet-Friendly Cleaning" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: EN default
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,147,0.35)]" />',
    '<img src="assets/raw/hero-action.jpg" alt="Miami Cleanings" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,147,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Miami <span class="text-[color:var(--accent-deep)]">Cleanings</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">MC</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Miami Cleanings</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call for a quote" data-en="Call for a quote">Call for a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="North Miami Beach, FL · Cleaning Service" data-en="North Miami Beach, FL · Cleaning Service">North Miami Beach, FL · Cleaning Service</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="We come to you, spotless every time." data-en="We come to you, spotless every time.">We come to you, spotless every time.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="A cleaning crew that" data-en="A cleaning crew that">A cleaning crew that</span><br /><span data-es="actually shows up " data-en="actually shows up ">actually shows up </span><span class="text-shine" data-es="on time" data-en="on time">on time</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Move-in and move-out deep cleaning, pet-friendly deep cleaning and standard home cleaning across North Miami Beach and the greater Miami-Dade area. Jose answers the phone himself, quotes the job fairly and sends a crew that leaves every room spotless." data-en="Move-in and move-out deep cleaning, pet-friendly deep cleaning and standard home cleaning across North Miami Beach and the greater Miami-Dade area. Jose answers the phone himself, quotes the job fairly and sends a crew that leaves every room spotless.">Move-in and move-out deep cleaning, pet-friendly deep cleaning and standard home cleaning across North Miami Beach and the greater Miami-Dade area. Jose answers the phone himself, quotes the job fairly and sends a crew that leaves every room spotless.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 18 reviews on Google" data-en="4.9 · 18 reviews on Google">4.9 · 18 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 294-3567" data-en="Call (786) 294-3567">Call (786) 294-3567</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/hero-action.jpg" alt="A Miami Cleanings team member wiping down a glass shower door during a deep clean" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Free quotes" data-en="Free quotes">Free quotes</p>
            <p class="font-display text-lg" data-es="Call Jose" data-en="Call Jose">Call Jose</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Same-day replies" data-en="Same-day replies">Same-day replies</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="18">18</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Move-In <span class="text-shine">&amp;</span> Out</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Deep Cleaning" data-en="Deep Cleaning">Deep Cleaning</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">Free <span class="text-shine" data-es="quotes" data-en="quotes">quotes</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="No obligation" data-en="No obligation">No obligation</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">North Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Miami-Dade, FL" data-en="Miami-Dade, FL">Miami-Dade, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Deep Cleaning"),
    ("Hybrid Set", "Move-Out Cleaning"),
    ("Volume Set", "Move-In Cleaning"),
    ("Mega Volume", "Standard Cleaning"),
    ("Bottom Lashes", "Pet-Friendly"),
    ("West Palm Beach, FL", "North Miami Beach, FL"),
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
    '''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/about-kitchen.jpg" alt="A granite kitchen left spotless by Miami Cleanings after a deep clean" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-living.jpg" alt="A living room and kitchen left spotless after a Miami Cleanings move-out cleaning" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Run by Jose," data-en="Run by Jose,">Run by Jose,</span><br /><span class="text-shine" data-es="who answers his own phone" data-en="who answers his own phone">who answers his own phone</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Miami Cleanings is led by Jose, who comes out to see the place, gives a fair quote on the spot and sends a crew that includes cleaners like Massel, known for careful, detail-focused work. No call center, no subcontractors: the person who quotes the job is the person you can call back." data-en="Miami Cleanings is led by Jose, who comes out to see the place, gives a fair quote on the spot and sends a crew that includes cleaners like Massel, known for careful, detail-focused work. No call center, no subcontractors: the person who quotes the job is the person you can call back.">Miami Cleanings is led by Jose, who comes out to see the place, gives a fair quote on the spot and sends a crew that includes cleaners like Massel, known for careful, detail-focused work. No call center, no subcontractors: the person who quotes the job is the person you can call back.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.9-star rating across 18 verified Google reviews, with move-out clients getting their full security deposit back and move-in clients finding the place smelling and looking brand new." data-en="The result: a 4.9-star rating across 18 verified Google reviews, with move-out clients getting their full security deposit back and move-in clients finding the place smelling and looking brand new.">The result: a 4.9-star rating across 18 verified Google reviews, with move-out clients getting their full security deposit back and move-in clients finding the place smelling and looking brand new.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="18">18</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Trato directo" data-en="Direct contact">Direct contact</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,147,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/hero-action.jpg" alt="Miami Cleanings" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,147,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Jose · <span class="text-[color:var(--ink-40)]" data-es="Dueno" data-en="Owner">Owner</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your home, start" data-en="Your home, start">Your home, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call Jose" data-en="Call Jose">Call Jose</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text with the move-in, move-out or deep clean you need, and Jose calls back promptly to talk through the job." data-en="Call or text with the move-in, move-out or deep clean you need, and Jose calls back promptly to talk through the job.">Call or text with the move-in, move-out or deep clean you need, and Jose calls back promptly to talk through the job.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Free walkthrough" data-en="Free walkthrough">Free walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Jose comes to see the place, or asks the right questions over the phone, and gives a clear, fair quote before anyone shows up." data-en="Jose comes to see the place, or asks the right questions over the phone, and gives a clear, fair quote before anyone shows up.">Jose comes to see the place, or asks the right questions over the phone, and gives a clear, fair quote before anyone shows up.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The deep clean" data-en="The deep clean">The deep clean</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Kitchen, bathrooms, floors, carpets and every room in between, with pet odor and hair treated as its own step, not an afterthought." data-en="Kitchen, bathrooms, floors, carpets and every room in between, with pet odor and hair treated as its own step, not an afterthought.">Kitchen, bathrooms, floors, carpets and every room in between, with pet odor and hair treated as its own step, not an afterthought.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Inspection &amp; handoff" data-en="Inspection &amp; handoff">Inspection &amp; handoff</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Jose walks the space with you before the crew leaves, so nothing gets missed and your deposit or move-in day is covered." data-en="Jose walks the space with you before the crew leaves, so nothing gets missed and your deposit or move-in day is covered.">Jose walks the space with you before the crew leaves, so nothing gets missed and your deposit or move-in day is covered.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Cleaning for" data-en="Cleaning for">Cleaning for</span> <span class="text-shine" data-es="every move" data-en="every move">every move</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two homes are the same, so every job gets its own free, no-obligation quote from Jose before anyone shows up." data-en="No two homes are the same, so every job gets its own free, no-obligation quote from Jose before anyone shows up.">No two homes are the same, so every job gets its own free, no-obligation quote from Jose before anyone shows up.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(31,122,147,0.4); box-shadow: 0 18px 50px rgba(27,42,48,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Move-In / Move-Out Cleaning" data-en="Move-In / Move-Out Cleaning">Move-In / Move-Out Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A full top-to-bottom clean before you hand over the keys or before you unpack, so you get your deposit back or start fresh." data-en="A full top-to-bottom clean before you hand over the keys or before you unpack, so you get your deposit back or start fresh.">A full top-to-bottom clean before you hand over the keys or before you unpack, so you get your deposit back or start fresh.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Top to bottom" data-en="Top to bottom">Top to bottom</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Deep Cleaning" data-en="Deep Cleaning">Deep Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Kitchen grease, bathroom grime, baseboards and the spots a regular clean skips, scrubbed by hand." data-en="Kitchen grease, bathroom grime, baseboards and the spots a regular clean skips, scrubbed by hand.">Kitchen grease, bathroom grime, baseboards and the spots a regular clean skips, scrubbed by hand.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it fresh" data-en="Keep it fresh">Keep it fresh</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Standard Cleaning" data-en="Standard Cleaning">Standard Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="One-time or recurring visits to keep the home dusted, mopped and tidy between deep cleans." data-en="One-time or recurring visits to keep the home dusted, mopped and tidy between deep cleans.">One-time or recurring visits to keep the home dusted, mopped and tidy between deep cleans.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pet owners" data-en="Pet owners">Pet owners</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pet-Friendly Cleaning" data-en="Pet-Friendly Cleaning">Pet-Friendly Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pet hair and odor treated as their own step, so the home comes back smelling and feeling brand new." data-en="Pet hair and odor treated as their own step, so the home comes back smelling and feeling brand new.">Pet hair and odor treated as their own step, so the home comes back smelling and feeling brand new.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Kitchens &amp; Baths" data-en="Kitchens &amp; Baths">Kitchens &amp; Baths</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Kitchen deep clean" data-en="Kitchen deep clean">Kitchen deep clean</li>
            <li class="flex items-center gap-2" data-es="Bathroom &amp; shower scrub" data-en="Bathroom &amp; shower scrub">Bathroom &amp; shower scrub</li>
            <li class="flex items-center gap-2" data-es="Appliance cleaning" data-en="Appliance cleaning">Appliance cleaning</li>
            <li class="flex items-center gap-2" data-es="Cabinet wipe-down" data-en="Cabinet wipe-down">Cabinet wipe-down</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Floors &amp; Carpets" data-en="Floors &amp; Carpets">Floors &amp; Carpets</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Carpet &amp; rug cleaning" data-en="Carpet &amp; rug cleaning">Carpet &amp; rug cleaning</li>
            <li class="flex items-center gap-2" data-es="Mopping &amp; vacuuming" data-en="Mopping &amp; vacuuming">Mopping &amp; vacuuming</li>
            <li class="flex items-center gap-2" data-es="Baseboards &amp; walls" data-en="Baseboards &amp; walls">Baseboards &amp; walls</li>
            <li class="flex items-center gap-2" data-es="Window sills" data-en="Window sills">Window sills</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Extras" data-en="Extras">Extras</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Pet odor &amp; hair removal" data-en="Pet odor &amp; hair removal">Pet odor &amp; hair removal</li>
            <li class="flex items-center gap-2" data-es="Disinfecting" data-en="Disinfecting">Disinfecting</li>
            <li class="flex items-center gap-2" data-es="Organizing" data-en="Organizing">Organizing</li>
            <li class="flex items-center gap-2" data-es="Free quotes" data-en="Free quotes">Free quotes</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on home size and scope of the job. Call (786) 294-3567 for a free, no-obligation quote." data-en="Pricing depends on home size and scope of the job. Call (786) 294-3567 for a free, no-obligation quote.">Pricing depends on home size and scope of the job. Call (786) 294-3567 for a free, no-obligation quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="results" data-en="results">results</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (786) 294-3567
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Patio exterior listo para recibir" data-en="Outdoor living space ready for guests">Outdoor living space ready for guests</span><img src="assets/raw/gallery-patio.jpg" alt="An outdoor patio and kitchen left spotless after a Miami Cleanings deep clean" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Dormitorio listo para mudanza" data-en="Bedroom ready for move-in">Bedroom ready for move-in</span><img src="assets/raw/gallery-bedroom.jpg" alt="A bedroom left spotless and ready after a Miami Cleanings move-in cleaning" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What North Miami Beach" data-en="What North Miami Beach">What North Miami Beach</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 18 reviews on Google" data-en="4.9 out of 5 · 18 reviews on Google">4.9 out of 5 · 18 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"After over 3 months, I was able to move back into my apartment once my ex husband finally left. The smell and dirtiness he left at that place was unlivable."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Haydee Chachamovits</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very excellent services. Massel is very professional and nice! I lived in my old apartment for one year with two cats, but after their cleaning the cat odour and all the hair were gone. The apartment was like brand new. As a result, I got my deposit back successfully."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Xinning Chu</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I have to say that Jose and his staff were very attentive, and left my place shine and clean. He gave me a complimentary inspection."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carmen Malave</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 18 reviews on Google" data-en="Read all 18 reviews on Google">Read all 18 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION -> variante adaptada: sin direccion/mapa (apartamento privado),
#     se reemplaza por una foto real del trabajo + zona de cobertura.
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">North Miami Beach</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,147,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Coverage area" data-en="Coverage area">Coverage area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Miami Cleanings is a mobile crew, not a storefront: Jose and the team come to your home or apartment across North Miami Beach and the greater Miami-Dade area." data-en="Miami Cleanings is a mobile crew, not a storefront: Jose and the team come to your home or apartment across North Miami Beach and the greater Miami-Dade area.">Miami Cleanings is a mobile crew, not a storefront: Jose and the team come to your home or apartment across North Miami Beach and the greater Miami-Dade area.</p>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,147,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Scheduling" data-en="Scheduling">Scheduling</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Call or text and Jose quotes the job the same day, with crews available for move-in, move-out and short-notice deep cleans." data-en="Call or text and Jose quotes the job the same day, with crews available for move-in, move-out and short-notice deep cleans.">Call or text and Jose quotes the job the same day, with crews available for move-in, move-out and short-notice deep cleans.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,147,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 294-3567" data-en="Call (786) 294-3567">Call (786) 294-3567</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,147,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.9 stars across 18 verified Google reviews." data-en="4.9 stars across 18 verified Google reviews.">4.9 stars across 18 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,147,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame reveal min-h-[380px] img-reveal" style="transition-delay:180ms">
        <img src="assets/raw/hero-action.jpg" alt="A Miami Cleanings crew member cleaning a shower during a deep clean in North Miami Beach" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="We come to you, spotless every time." data-en="We come to you, spotless every time.">We come to you, spotless every time.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call to" data-en="One call to">One call to</span> <span class="text-shine" data-es="Jose" data-en="Jose">Jose</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (786) 294-3567 for a free, no-obligation quote on your move-in, move-out or deep clean. Jose replies the same day." data-en="Call (786) 294-3567 for a free, no-obligation quote on your move-in, move-out or deep clean. Jose replies the same day.">Call (786) 294-3567 for a free, no-obligation quote on your move-in, move-out or deep clean. Jose replies the same day.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 294-3567" data-en="Call (786) 294-3567">Call (786) 294-3567</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Miami Cleanings</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(191,230,240,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/raw/hero-action.jpg" alt="Miami Cleanings" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(191,230,240,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Miami Cleanings</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Residential cleaning serving North Miami Beach, FL and Miami-Dade. By appointment." data-en="Residential cleaning serving North Miami Beach, FL and Miami-Dade. By appointment.">Residential cleaning serving North Miami Beach, FL and Miami-Dade. By appointment.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#bfe6f0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="North Miami Beach, FL" data-en="North Miami Beach, FL">North Miami Beach, FL</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#9fd3e0]" data-es="Call (786) 294-3567" data-en="Call (786) 294-3567">Call (786) 294-3567</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#bfe6f0]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#9fd3e0]">4.9 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Miami Cleanings.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Miami Cleanings">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 19. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace(f'href="{NEW_TEL}" target="_blank" rel="noopener"', f'href="{NEW_TEL}"')
print("CLEANUP tel links done")

# ---------------------------------------------------------------------------
# 20. Traduccion ES real para todos los textos NUEVOS (bilingue obligatorio)
# ---------------------------------------------------------------------------
T = {
    "Call for a quote": "Llama para cotizar",
    "North Miami Beach, FL · Cleaning Service": "North Miami Beach, FL · Servicio de Limpieza",
    "We come to you, spotless every time.": "Vamos a tu casa, impecable cada vez.",
    "A cleaning crew that": "Un equipo de limpieza que",
    "actually shows up ": "si llega ",
    "on time": "a tiempo",
    "Move-in and move-out deep cleaning, pet-friendly deep cleaning and standard home cleaning across North Miami Beach and the greater Miami-Dade area. Jose answers the phone himself, quotes the job fairly and sends a crew that leaves every room spotless.":
        "Limpieza profunda de mudanza (entrada y salida), limpieza profunda para hogares con mascotas y limpieza estandar en North Miami Beach y el area de Miami-Dade. Jose contesta el telefono personalmente, cotiza el trabajo de forma justa y envia un equipo que deja cada cuarto impecable.",
    "4.9 · 18 reviews on Google": "4.9 · 18 resenas en Google",
    "Call (786) 294-3567": "Llama al (786) 294-3567",
    "Free quotes": "Cotizacion gratis",
    "Same-day replies": "Respuesta el mismo dia",
    "reviews on Google": "resenas en Google",
    "Deep Cleaning": "Limpieza Profunda",
    "quotes": "cotizaciones",
    "No obligation": "Sin compromiso",
    "Miami-Dade, FL": "Miami-Dade, FL",
    "Run by Jose,": "Dirigido por Jose,",
    "who answers his own phone": "quien contesta su propio telefono",
    "Miami Cleanings is led by Jose, who comes out to see the place, gives a fair quote on the spot and sends a crew that includes cleaners like Massel, known for careful, detail-focused work. No call center, no subcontractors: the person who quotes the job is the person you can call back.":
        "Miami Cleanings es dirigido por Jose, quien va a ver el lugar, da una cotizacion justa en el momento y envia un equipo que incluye limpiadoras como Massel, conocida por su trabajo cuidadoso y detallado. Sin call center ni subcontratistas: la persona que cotiza el trabajo es la misma a la que puedes volver a llamar.",
    "The result: a 4.9-star rating across 18 verified Google reviews, with move-out clients getting their full security deposit back and move-in clients finding the place smelling and looking brand new.":
        "El resultado: una calificacion de 4.9 estrellas en 18 resenas verificadas de Google, con clientes de mudanza de salida recuperando todo su deposito de seguridad y clientes de mudanza de entrada encontrando el lugar oliendo y luciendo como nuevo.",
    "Your home, start": "Tu casa, de inicio",
    "to finish": "hasta el final",
    "Call Jose": "Llama a Jose",
    "Call or text with the move-in, move-out or deep clean you need, and Jose calls back promptly to talk through the job.":
        "Llama o escribe con la mudanza o limpieza profunda que necesitas, y Jose regresa la llamada rapido para hablar del trabajo.",
    "Free walkthrough": "Visita gratis",
    "Jose comes to see the place, or asks the right questions over the phone, and gives a clear, fair quote before anyone shows up.":
        "Jose va a ver el lugar, o hace las preguntas correctas por telefono, y da una cotizacion clara y justa antes de que llegue el equipo.",
    "The deep clean": "La limpieza profunda",
    "Kitchen, bathrooms, floors, carpets and every room in between, with pet odor and hair treated as its own step, not an afterthought.":
        "Cocina, banos, pisos, alfombras y cada cuarto entre medio, con el olor y pelo de mascotas tratados como un paso propio, no como algo secundario.",
    "Inspection &amp; handoff": "Inspeccion y entrega",
    "Jose walks the space with you before the crew leaves, so nothing gets missed and your deposit or move-in day is covered.":
        "Jose recorre el lugar contigo antes de que el equipo se vaya, para que nada quede sin revisar y tu deposito o dia de mudanza queden cubiertos.",
    "Cleaning for": "Limpieza para",
    "every move": "cada mudanza",
    "No two homes are the same, so every job gets its own free, no-obligation quote from Jose before anyone shows up.":
        "Ninguna casa es igual a otra, asi que cada trabajo recibe su propia cotizacion gratis y sin compromiso de Jose antes de que llegue el equipo.",
    "Most requested": "Lo mas solicitado",
    "Move-In / Move-Out Cleaning": "Limpieza de Mudanza (Entrada/Salida)",
    "A full top-to-bottom clean before you hand over the keys or before you unpack, so you get your deposit back or start fresh.":
        "Una limpieza completa de arriba a abajo antes de entregar las llaves o antes de desempacar, para que recuperes tu deposito o empieces de cero.",
    "Call": "Llamar",
    "Top to bottom": "De arriba a abajo",
    "Kitchen grease, bathroom grime, baseboards and the spots a regular clean skips, scrubbed by hand.":
        "Grasa de cocina, suciedad de bano, zocalos y los rincones que una limpieza normal no alcanza, tallados a mano.",
    "Keep it fresh": "Mantenla fresca",
    "Standard Cleaning": "Limpieza Estandar",
    "One-time or recurring visits to keep the home dusted, mopped and tidy between deep cleans.":
        "Visitas unicas o recurrentes para mantener la casa sin polvo, trapeada y ordenada entre limpiezas profundas.",
    "Pet owners": "Dueños de mascotas",
    "Pet-Friendly Cleaning": "Limpieza para Hogares con Mascotas",
    "Pet hair and odor treated as their own step, so the home comes back smelling and feeling brand new.":
        "El pelo y olor de mascotas se tratan como un paso propio, para que la casa quede oliendo y sintiendose como nueva.",
    "Kitchens &amp; Baths": "Cocinas y Baños",
    "Kitchen deep clean": "Limpieza profunda de cocina",
    "Bathroom &amp; shower scrub": "Tallado de bano y ducha",
    "Appliance cleaning": "Limpieza de electrodomesticos",
    "Cabinet wipe-down": "Limpieza de gabinetes",
    "Floors &amp; Carpets": "Pisos y Alfombras",
    "Carpet &amp; rug cleaning": "Limpieza de alfombras y tapetes",
    "Mopping &amp; vacuuming": "Trapeado y aspirado",
    "Baseboards &amp; walls": "Zocalos y paredes",
    "Window sills": "Repisas de ventana",
    "Extras": "Extras",
    "Pet odor &amp; hair removal": "Remocion de olor y pelo de mascotas",
    "Disinfecting": "Desinfeccion",
    "Organizing": "Organizacion",
    "Pricing depends on home size and scope of the job. Call (786) 294-3567 for a free, no-obligation quote.":
        "El precio depende del tamaño de la casa y el alcance del trabajo. Llama al (786) 294-3567 para una cotizacion gratis y sin compromiso.",
    "Real": "Resultados",
    "results": "reales",
    "What North Miami Beach": "Lo que dicen los",
    "customers say": "clientes en North Miami Beach",
    "4.9 out of 5 · 18 reviews on Google": "4.9 de 5 · 18 resenas en Google",
    "Read all 18 reviews on Google": "Lee las 18 resenas en Google",
    "Serving": "Sirviendo a",
    "Coverage area": "Zona de cobertura",
    "Miami Cleanings is a mobile crew, not a storefront: Jose and the team come to your home or apartment across North Miami Beach and the greater Miami-Dade area.":
        "Miami Cleanings es un equipo movil, no un local: Jose y el equipo van a tu casa o apartamento en North Miami Beach y el area de Miami-Dade.",
    "Scheduling": "Agenda",
    "Call or text and Jose quotes the job the same day, with crews available for move-in, move-out and short-notice deep cleans.":
        "Llama o escribe y Jose cotiza el trabajo el mismo dia, con equipos disponibles para mudanzas y limpiezas profundas de ultimo momento.",
    "Reviews": "Resenas",
    "4.9 stars across 18 verified Google reviews.": "4.9 estrellas en 18 resenas verificadas de Google.",
    "One call to": "Una llamada a",
    "Jose": "Jose",
    "Call (786) 294-3567 for a free, no-obligation quote on your move-in, move-out or deep clean. Jose replies the same day.":
        "Llama al (786) 294-3567 para una cotizacion gratis y sin compromiso de tu mudanza o limpieza profunda. Jose responde el mismo dia.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Residential cleaning serving North Miami Beach, FL and Miami-Dade. By appointment.":
        "Limpieza residencial en North Miami Beach, FL y Miami-Dade. Con cita previa.",
    "Contact": "Contacto",
    "North Miami Beach, FL": "North Miami Beach, FL",
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
