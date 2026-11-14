import re
import shutil

SLUG = "the-greatest-tree-service"
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
# 2. Paleta: plum-pink (lashbloom) -> amber / bark-brown (The Greatest Tree Service)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#a0724a"),
    ("#5c2140", "#5c3d21"),
    ("#f0bed7", "#f0d5be"),
    ("#faf2f6", "#faf6f2"),
    ("#c47a9c", "#c49d7a"),
    ("#8a5573", "#8a6e55"),
    ("#f3e0ea", "#f3e9e0"),
    ("#d9a8c2", "#d9bfa8"),
    ("#7d3457", "#7d5634"),
    ("#5f2c48", "#5f442c"),
    ("#33222c", "#332a22"),
    ("#fbf3f8", "#fbf7f3"),
    ("#fbeff5", "#fbf5ef"),
    ("#f8dfeb", "#f8ebdf"),
    ("#f6f1ea", "#f6f0ea"),
    ("#f2d5e3", "#f2e3d5"),
    ("#f2cfe0", "#f2dfcf"),
    ("#efd0e0", "#efded0"),
    ("#e5c1d4", "#e5d2c1"),
    ("#dc9dbe", "#dcba9d"),
    ("#d3a2bc", "#d3b9a2"),
    ("#c9789f", "#c99e78"),
    ("#b25a85", "#b2835a"),
    ("#2a1722", "#2a2017"),
    ("#1f0f18", "#1f160f"),
    ("#1c0f16", "#1c150f"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(160,114,74"),
    ("rgba(51,34,44", "rgba(51,42,34"),
    ("rgba(240,190,215", "rgba(240,213,190"),
    ("rgba(70,25,50", "rgba(70,46,25"),
    ("rgba(250,242,246", "rgba(250,246,242"),
    ("rgba(125,52,87", "rgba(125,86,52"),
    ("rgba(253,246,250", "rgba(253,249,246"),
    ("rgba(40,16,30", "rgba(40,27,16"),
    ("rgba(233,205,186", "rgba(233,208,186"),
    ("rgba(185,138,128", "rgba(185,155,128"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform, email ni IG -> tel: + Google reviews
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+18133171369"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=The+Greatest+Tree+Service+Tampa+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "2117 W Burke St, Tampa, FL 33604"
NEW_MAPS = "https://www.google.com/maps?q=2117+W+Burke+St,+Tampa,+FL+33604"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>The Greatest Tree Service Inc. · Stump Grinding &amp; Tree Removal in Tampa, FL | 4.7 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="The Greatest Tree Service Inc., Tampa FL: stump grinding, tree removal, trimming and land clearing. 4.7 stars across 15 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="The Greatest Tree Service Inc. · Stump Grinding &amp; Tree Removal in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Stump grinding, tree removal, trimming and land clearing. 4.7 on Google with 15 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-stump-grinder.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-stump-grinder.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "The Greatest Tree Service Inc.",
    "description": "Tree service company in Tampa, FL: stump grinding, tree removal, tree trimming and pruning, and land clearing and mulching.",
    "address": { "@type": "PostalAddress", "streetAddress": "2117 W Burke St", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33604", "addressCountry": "US" },
    "telephone": "+1-813-317-1369",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "15", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "07:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "20:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Tree services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Stump Grinding" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tree Removal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tree Trimming &amp; Pruning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Land Clearing &amp; Mulching" } }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,114,74,0.35)]" />',
    '<img src="assets/hero-stump-grinder.jpg" alt="The Greatest Tree Service" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,114,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">The <span class="text-[color:var(--accent-deep)]">Greatest</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">TGT</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">The Greatest Tree Service</span>')
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
    'data-es="Tampa, FL · Tree Service" data-en="Tampa, FL · Tree Service">Tampa, FL · Tree Service</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Stumps gone, yards cleared." data-en="Stumps gone, yards cleared.">Stumps gone, yards cleared.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Stump grinding, removal" data-en="Stump grinding, removal">Stump grinding, removal</span><br /><span data-es="and clearing, done " data-en="and clearing, done ">and clearing, done </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Stump grinding, tree removal, trimming and land clearing across Tampa. Fast scheduling, fair prices and a crew that cleans up after every job, with a 4.7 rating across 15 Google reviews." data-en="Stump grinding, tree removal, trimming and land clearing across Tampa. Fast scheduling, fair prices and a crew that cleans up after every job, with a 4.7 rating across 15 Google reviews.">Stump grinding, tree removal, trimming and land clearing across Tampa. Fast scheduling, fair prices and a crew that cleans up after every job, with a 4.7 rating across 15 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.7 · 15 reviews on Google" data-en="4.7 · 15 reviews on Google">4.7 · 15 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (813) 317-1369" data-en="Call (813) 317-1369">Call (813) 317-1369</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-stump-grinder.jpg" alt="A stump grinder machine clearing a stump in a Tampa front yard" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">7am - 8pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="15">15</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Stump <span class="text-shine">&amp;</span> Removal</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Grinding · Trimming · Clearing" data-en="Grinding · Trimming · Clearing">Grinding · Trimming · Clearing</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">7am</span> - 8pm</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Open 7 days" data-en="Open 7 days">Open 7 days</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Burke St, FL" data-en="Burke St, FL">Burke St, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Stump Grinding"),
    ("Hybrid Set", "Tree Removal"),
    ("Volume Set", "Tree Trimming"),
    ("Mega Volume", "Land Clearing"),
    ("Bottom Lashes", "Mulching"),
    ("West Palm Beach, FL", "Tampa, FL"),
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
          <img src="assets/about-bucket-oak.jpg" alt="A The Greatest Tree Service crew member in a bucket truck trimming a tall oak" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One crew," data-en="One crew,">One crew,</span><br /><span class="text-shine" data-es="the right equipment" data-en="the right equipment">the right equipment</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="The Greatest Tree Service Inc. runs its own stump grinders, bucket truck and skid steer to handle stump grinding, tree removal, trimming and land clearing across Tampa without waiting on rented equipment." data-en="The Greatest Tree Service Inc. runs its own stump grinders, bucket truck and skid steer to handle stump grinding, tree removal, trimming and land clearing across Tampa without waiting on rented equipment.">The Greatest Tree Service Inc. runs its own stump grinders, bucket truck and skid steer to handle stump grinding, tree removal, trimming and land clearing across Tampa without waiting on rented equipment.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Customers describe the crew as fast, fairly priced and thorough about cleanup. The result: a 4.7-star rating across 15 Google reviews, with repeat customers calling back for every new job." data-en="Customers describe the crew as fast, fairly priced and thorough about cleanup. The result: a 4.7-star rating across 15 Google reviews, with repeat customers calling back for every new job.">Customers describe the crew as fast, fairly priced and thorough about cleanup. The result: a 4.7-star rating across 15 Google reviews, with repeat customers calling back for every new job.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="15">15</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">13</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Horas al dia" data-en="Hours a day">Hours a day</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,114,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/hero-stump-grinder.jpg" alt="The Greatest Tree Service" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,114,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">The Greatest Tree Service · <span class="text-[color:var(--ink-40)]" data-es="Tree crew" data-en="Tree crew">Tree crew</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your yard, cleared" data-en="Your yard, cleared">Your yard, cleared</span> <span class="text-shine" data-es="step by step" data-en="step by step">step by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call it in" data-en="Call it in">Call it in</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call with the stump, tree or lot that needs clearing, and the crew schedules a visit fast." data-en="Call with the stump, tree or lot that needs clearing, and the crew schedules a visit fast.">Call with the stump, tree or lot that needs clearing, and the crew schedules a visit fast.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Fair price" data-en="Fair price">Fair price</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A crew member looks at the job and gives a fair, upfront price before any machine comes off the trailer." data-en="A crew member looks at the job and gives a fair, upfront price before any machine comes off the trailer.">A crew member looks at the job and gives a fair, upfront price before any machine comes off the trailer.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The work gets done" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Stump grinder, bucket truck or skid steer, whatever the job needs, run by a crew that works fast and safe." data-en="Stump grinder, bucket truck or skid steer, whatever the job needs, run by a crew that works fast and safe.">Stump grinder, bucket truck or skid steer, whatever the job needs, run by a crew that works fast and safe.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Clean handoff" data-en="Clean handoff">Clean handoff</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Wood chips, debris and grindings get hauled off, so the property looks better than before the crew showed up." data-en="Wood chips, debris and grindings get hauled off, so the property looks better than before the crew showed up.">Wood chips, debris and grindings get hauled off, so the property looks better than before the crew showed up.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Tree work for" data-en="Tree work for">Tree work for</span> <span class="text-shine" data-es="every property" data-en="every property">every property</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two stumps or lots are the same, so every job gets its own fair quote by phone before any machine shows up." data-en="No two stumps or lots are the same, so every job gets its own fair quote by phone before any machine shows up.">No two stumps or lots are the same, so every job gets its own fair quote by phone before any machine shows up.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(160,114,74,0.4); box-shadow: 0 18px 50px rgba(51,42,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Stump Grinding" data-en="Stump Grinding">Stump Grinding</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Stumps of any size ground down flat with our own Vermeer grinders, roots and all, in a single visit." data-en="Stumps of any size ground down flat with our own Vermeer grinders, roots and all, in a single visit.">Stumps of any size ground down flat with our own Vermeer grinders, roots and all, in a single visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Full takedown" data-en="Full takedown">Full takedown</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tree Removal" data-en="Tree Removal">Tree Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tall or tight-quartered trees taken down with a bucket truck and rigging, piece by piece if needed." data-en="Tall or tight-quartered trees taken down with a bucket truck and rigging, piece by piece if needed.">Tall or tight-quartered trees taken down with a bucket truck and rigging, piece by piece if needed.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it healthy" data-en="Keep it healthy">Keep it healthy</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tree Trimming &amp; Pruning" data-en="Tree Trimming &amp; Pruning">Tree Trimming &amp; Pruning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Deadwood and overgrown limbs trimmed back to keep trees healthy and clear of roofs and power lines." data-en="Deadwood and overgrown limbs trimmed back to keep trees healthy and clear of roofs and power lines.">Deadwood and overgrown limbs trimmed back to keep trees healthy and clear of roofs and power lines.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lot work" data-en="Lot work">Lot work</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Land Clearing &amp; Mulching" data-en="Land Clearing &amp; Mulching">Land Clearing &amp; Mulching</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Overgrown lots and ditches cleared with a skid steer, brush and debris mulched or hauled away." data-en="Overgrown lots and ditches cleared with a skid steer, brush and debris mulched or hauled away.">Overgrown lots and ditches cleared with a skid steer, brush and debris mulched or hauled away.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Stump Work" data-en="Stump Work">Stump Work</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Stump grinding" data-en="Stump grinding">Stump grinding</li>
            <li class="flex items-center gap-2" data-es="Root removal" data-en="Root removal">Root removal</li>
            <li class="flex items-center gap-2" data-es="Grindings haul away" data-en="Grindings haul away">Grindings haul away</li>
            <li class="flex items-center gap-2" data-es="Multiple stump discounts" data-en="Multiple stump discounts">Multiple stump discounts</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Tree Care" data-en="Tree Care">Tree Care</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Tree removal" data-en="Tree removal">Tree removal</li>
            <li class="flex items-center gap-2" data-es="Trimming &amp; pruning" data-en="Trimming &amp; pruning">Trimming &amp; pruning</li>
            <li class="flex items-center gap-2" data-es="Deadwood removal" data-en="Deadwood removal">Deadwood removal</li>
            <li class="flex items-center gap-2" data-es="Storm damage cleanup" data-en="Storm damage cleanup">Storm damage cleanup</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Land &amp; Lots" data-en="Land &amp; Lots">Land &amp; Lots</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Land clearing" data-en="Land clearing">Land clearing</li>
            <li class="flex items-center gap-2" data-es="Brush mulching" data-en="Brush mulching">Brush mulching</li>
            <li class="flex items-center gap-2" data-es="Ditch &amp; drainage clearing" data-en="Ditch &amp; drainage clearing">Ditch &amp; drainage clearing</li>
            <li class="flex items-center gap-2" data-es="Free estimates" data-en="Free estimates">Free estimates</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on size and access. Call (813) 317-1369 for a free quote." data-en="Pricing depends on size and access. Call (813) 317-1369 for a free quote.">Pricing depends on size and access. Call (813) 317-1369 for a free quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="work" data-en="work">work</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (813) 317-1369
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Trituradora de tocones en jardin" data-en="Stump grinder working a front yard">Stump grinder working a front yard</span><img src="assets/gallery-stump-grinder-yard.jpg" alt="A Vermeer stump grinder clearing a tree stump in a Tampa front yard" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Limpieza con garra sobre orugas" data-en="Grapple cleanup on tracks">Grapple cleanup on tracks</span><img src="assets/gallery-grapple-cleanup.jpg" alt="A skid steer with a grapple attachment clearing brush and debris" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Monton de astillas listo para retirar" data-en="Mulch pile ready for haul off">Mulch pile ready for haul off</span><img src="assets/gallery-mulch-pile.jpg" alt="A large pile of wood mulch from a land clearing job" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Trituracion de tocon cerca del agua" data-en="Grinding a stump near wetlands">Grinding a stump near wetlands</span><img src="assets/gallery-wetland-grind.jpg" alt="A stump grinder clearing a stump near a wooded wetland area" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Tampa" data-en="What Tampa">What Tampa</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.7 out of 5 · 15 reviews on Google" data-en="4.7 out of 5 · 15 reviews on Google">4.7 out of 5 · 15 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We had an old maple that needed to come down. These guys were super professional, fast and very reasonably priced. Communication was great. They cleaned everything up and showed up when they said they would. We would would absolutely recommend this company."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joanne Dalton</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I have used the Greatest Tree Service 3 times and I can't recommend them enough! They are always on time, professional, and have the best prices in the Tampa area. They work extremely hard and leave the property spotless when they are..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Caitlyn Mitryk</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We hired this company for the first time and plan to keep them for all future tree service needs! I cannot express how amazing the owner and his staff are, the professionalism, timeliness and quality workmanship is the best that we've seen..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sarah Mannone</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 15 reviews on Google" data-en="Read all 15 reviews on Google">Read all 15 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (direccion real disponible)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Tampa, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,114,74,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + NEW_ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,114,74,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,114,74,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Saturday and Sunday 7 AM to 7 PM. Monday to Friday, 7 AM to 8 PM." data-en="Saturday and Sunday 7 AM to 7 PM. Monday to Friday, 7 AM to 8 PM.">Saturday and Sunday 7 AM to 7 PM. Monday to Friday, 7 AM to 8 PM.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,114,74,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (813) 317-1369" data-en="Call (813) 317-1369">Call (813) 317-1369</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,114,74,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.7 stars across 15 verified Google reviews." data-en="4.7 stars across 15 verified Google reviews.">4.7 stars across 15 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,114,74,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: The Greatest Tree Service Inc., 2117 W Burke St, Tampa FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Stumps gone, yards cleared." data-en="Stumps gone, yards cleared.">Stumps gone, yards cleared.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call clears" data-en="One call clears">One call clears</span> <span class="text-shine" data-es="the yard" data-en="the yard">the yard</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (813) 317-1369 for a free, fair quote on your stump, tree removal or land clearing job. Open 7 days a week." data-en="Call (813) 317-1369 for a free, fair quote on your stump, tree removal or land clearing job. Open 7 days a week.">Call (813) 317-1369 for a free, fair quote on your stump, tree removal or land clearing job. Open 7 days a week.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (813) 317-1369" data-en="Call (813) 317-1369">Call (813) 317-1369</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">The Greatest Tree Service</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,213,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/hero-stump-grinder.jpg" alt="The Greatest Tree Service Inc." class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,213,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">The Greatest Tree Service</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Tree service serving Tampa, FL and the surrounding area." data-en="Tree service serving Tampa, FL and the surrounding area.">Tree service serving Tampa, FL and the surrounding area.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#f0d5be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#dcba9d]" data-es="Call (813) 317-1369" data-en="Call (813) 317-1369">Call (813) 317-1369</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0d5be]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#dcba9d]">4.7 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 The Greatest Tree Service Inc.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call The Greatest Tree Service">')
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
    "Tampa, FL · Tree Service": "Tampa, FL · Servicio de Arboles",
    "Stumps gone, yards cleared.": "Tocones fuera, jardines limpios.",
    "Stump grinding, removal": "Trituracion de tocones, remocion",
    "and clearing, done ": "y limpieza, hecho ",
    "right": "bien",
    "Stump grinding, tree removal, trimming and land clearing across Tampa. Fast scheduling, fair prices and a crew that cleans up after every job, with a 4.7 rating across 15 Google reviews.":
        "Trituracion de tocones, remocion de arboles, poda y limpieza de terrenos en Tampa. Agenda rapida, precios justos y un equipo que limpia despues de cada trabajo, con calificacion de 4.7 en 15 resenas de Google.",
    "4.7 · 15 reviews on Google": "4.7 · 15 resenas en Google",
    "Call (813) 317-1369": "Llama al (813) 317-1369",
    "Open": "Abierto",
    "Every day of the week": "Todos los dias de la semana",
    "Grinding · Trimming · Clearing": "Trituracion · Poda · Limpieza",
    "Open 7 days": "Abierto 7 dias",
    "Burke St, FL": "Burke St, FL",
    "One crew,": "Un equipo,",
    "the right equipment": "con el equipo correcto",
    "The Greatest Tree Service Inc. runs its own stump grinders, bucket truck and skid steer to handle stump grinding, tree removal, trimming and land clearing across Tampa without waiting on rented equipment.":
        "The Greatest Tree Service Inc. opera sus propias trituradoras de tocones, camion con canasta y minicargadora para trituracion de tocones, remocion de arboles, poda y limpieza de terrenos en Tampa, sin esperar equipo rentado.",
    "Customers describe the crew as fast, fairly priced and thorough about cleanup. The result: a 4.7-star rating across 15 Google reviews, with repeat customers calling back for every new job.":
        "Los clientes describen al equipo como rapido, con precios justos y minucioso con la limpieza. El resultado: una calificacion de 4.7 estrellas en 15 resenas de Google, con clientes que vuelven a llamar para cada nuevo trabajo.",
    "Tree crew": "Equipo de arboles",
    "Your yard, cleared": "Tu jardin, limpio",
    "step by step": "paso a paso",
    "Call it in": "Llama y cuenta",
    "Call with the stump, tree or lot that needs clearing, and the crew schedules a visit fast.":
        "Llama con el tocon, arbol o terreno que necesitas limpiar, y el equipo agenda una visita rapido.",
    "Fair price": "Precio justo",
    "A crew member looks at the job and gives a fair, upfront price before any machine comes off the trailer.":
        "Un miembro del equipo revisa el trabajo y da un precio justo y directo antes de bajar cualquier maquina del remolque.",
    "The work gets done": "El trabajo se hace",
    "Stump grinder, bucket truck or skid steer, whatever the job needs, run by a crew that works fast and safe.":
        "Trituradora de tocones, camion con canasta o minicargadora, lo que necesite el trabajo, operado por un equipo rapido y seguro.",
    "Clean handoff": "Entrega limpia",
    "Wood chips, debris and grindings get hauled off, so the property looks better than before the crew showed up.":
        "Las astillas, escombros y residuos de trituracion se retiran, para que la propiedad quede mejor que antes de que llegara el equipo.",
    "Tree work for": "Trabajo de arboles para",
    "every property": "cada propiedad",
    "No two stumps or lots are the same, so every job gets its own fair quote by phone before any machine shows up.":
        "Ningun tocon o terreno es igual a otro, asi que cada trabajo recibe su propia cotizacion justa por telefono antes de que llegue cualquier maquina.",
    "Most requested": "Lo mas solicitado",
    "Stump Grinding": "Trituracion de Tocones",
    "Stumps of any size ground down flat with our own Vermeer grinders, roots and all, in a single visit.":
        "Tocones de cualquier tamano triturados hasta quedar planos con nuestras propias trituradoras Vermeer, raices incluidas, en una sola visita.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Full takedown": "Remocion completa",
    "Tree Removal": "Remocion de Arboles",
    "Tall or tight-quartered trees taken down with a bucket truck and rigging, piece by piece if needed.":
        "Arboles altos o en espacios reducidos bajados con camion con canasta y cuerdas, pieza por pieza si es necesario.",
    "Keep it healthy": "Mantenlo sano",
    "Tree Trimming &amp; Pruning": "Poda y Corte de Arboles",
    "Deadwood and overgrown limbs trimmed back to keep trees healthy and clear of roofs and power lines.":
        "Madera muerta y ramas crecidas se podan para mantener los arboles sanos y despejados de techos y lineas electricas.",
    "Lot work": "Trabajo de terreno",
    "Land Clearing &amp; Mulching": "Limpieza de Terreno y Astillado",
    "Overgrown lots and ditches cleared with a skid steer, brush and debris mulched or hauled away.":
        "Terrenos y zanjas cubiertos de maleza se limpian con minicargadora, la maleza y escombros se astillan o se retiran.",
    "Stump Work": "Trabajo de Tocones",
    "Stump grinding": "Trituracion de tocones",
    "Root removal": "Remocion de raices",
    "Grindings haul away": "Retiro de residuos de trituracion",
    "Multiple stump discounts": "Descuentos por varios tocones",
    "Tree Care": "Cuidado de Arboles",
    "Tree removal": "Remocion de arboles",
    "Trimming &amp; pruning": "Poda y corte",
    "Deadwood removal": "Remocion de madera muerta",
    "Storm damage cleanup": "Limpieza de danos por tormenta",
    "Land &amp; Lots": "Terrenos y Lotes",
    "Land clearing": "Limpieza de terreno",
    "Brush mulching": "Astillado de maleza",
    "Ditch &amp; drainage clearing": "Limpieza de zanjas y drenajes",
    "Free estimates": "Cotizaciones gratis",
    "Pricing depends on size and access. Call (813) 317-1369 for a free quote.":
        "El precio depende del tamano y el acceso. Llama al (813) 317-1369 para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Tampa": "Lo que dicen los",
    "customers say": "clientes en Tampa",
    "Read all 15 reviews on Google": "Lee las 15 resenas en Google",
    "Serving": "Sirviendo a",
    "Hours": "Horario",
    "Saturday and Sunday 7 AM to 7 PM. Monday to Friday, 7 AM to 8 PM.": "Sabado y domingo de 7 AM a 7 PM. Lunes a viernes, de 7 AM a 8 PM.",
    "Reviews": "Resenas",
    "4.7 stars across 15 verified Google reviews.": "4.7 estrellas en 15 resenas verificadas de Google.",
    "One call clears": "Una llamada limpia",
    "the yard": "el jardin",
    "Call (813) 317-1369 for a free, fair quote on your stump, tree removal or land clearing job. Open 7 days a week.":
        "Llama al (813) 317-1369 para una cotizacion gratis y justa de tu tocon, remocion de arbol o limpieza de terreno. Abierto los 7 dias de la semana.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Tree service serving Tampa, FL and the surrounding area.": "Servicio de arboles en Tampa, FL y el area circundante.",
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
