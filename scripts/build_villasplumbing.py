import re
import shutil

SLUG = "villa-s-plumbing-llc"
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
# 2. Paleta: plum-pink (lashbloom) -> verde azulado / sea-green (Villa's Plumbing, agua)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#4aa08f"),
    ("#5c2140", "#215c50"),
    ("#f0bed7", "#bef0e6"),
    ("#faf2f6", "#f2faf8"),
    ("#c47a9c", "#7ac4b5"),
    ("#8a5573", "#558a7f"),
    ("#f3e0ea", "#e0f3ef"),
    ("#d9a8c2", "#a8d9cf"),
    ("#7d3457", "#347d6e"),
    ("#5f2c48", "#2c5f55"),
    ("#33222c", "#223330"),
    ("#fbf3f8", "#f3fbf9"),
    ("#fbeff5", "#effbf9"),
    ("#f8dfeb", "#dff8f3"),
    ("#f6f1ea", "#eaf6f4"),
    ("#f2d5e3", "#d5f2ec"),
    ("#f2cfe0", "#cff2eb"),
    ("#efd0e0", "#d0efe9"),
    ("#e5c1d4", "#c1e5de"),
    ("#dc9dbe", "#9ddccf"),
    ("#d3a2bc", "#a2d3c9"),
    ("#c9789f", "#78c9b9"),
    ("#b25a85", "#5ab2a0"),
    ("#2a1722", "#172a26"),
    ("#1f0f18", "#0f1f1c"),
    ("#1c0f16", "#0f1c19"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(74,160,143"),
    ("rgba(51,34,44", "rgba(34,51,48"),
    ("rgba(240,190,215", "rgba(190,240,230"),
    ("rgba(70,25,50", "rgba(25,70,61"),
    ("rgba(250,242,246", "rgba(242,250,248"),
    ("rgba(125,52,87", "rgba(52,125,110"),
    ("rgba(253,246,250", "rgba(246,253,252"),
    ("rgba(40,16,30", "rgba(16,40,35"),
    ("rgba(233,205,186", "rgba(186,233,224"),
    ("rgba(185,138,128", "rgba(128,185,174"),
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
NEW_TEL = "tel:+13057132040"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Villa%27s+Plumbing+Homestead+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "16121 SW 287th St, Homestead, FL 33033"
NEW_MAPS = "https://www.google.com/maps?q=16121+SW+287th+St,+Homestead,+FL+33033"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Villa\'s Plumbing LLC · Septic &amp; Plumbing in Homestead, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Villa\'s Plumbing LLC, Homestead FL: septic tank installation, drain field repair, rough-in plumbing and trenching. 4.9 stars across 19 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Villa\'s Plumbing LLC · Septic &amp; Plumbing in Homestead, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Septic tank installation, drain field repair, rough-in plumbing and trenching. 4.9 on Google with 19 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-excavator.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Plumber",
    "name": "Villa's Plumbing LLC",
    "description": "Residential plumbing and septic contractor in Homestead, FL: septic tank installation, drain field repair, rough-in plumbing, shower pan waterproofing and trenching.",
    "address": { "@type": "PostalAddress", "streetAddress": "16121 SW 287th St", "addressLocality": "Homestead", "addressRegion": "FL", "postalCode": "33033", "addressCountry": "US" },
    "telephone": "+1-305-713-2040",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "19", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "17:30" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Plumbing &amp; septic services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Septic Tank Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Drain Field &amp; Access Repair" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Rough-In Plumbing" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Trenching &amp; Pipe Laying" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: EN default (resenas en ingles)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,143,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Villa\'s Plumbing" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,143,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Villa\'s <span class="text-[color:var(--accent-deep)]">Plumbing</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">VP</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Villa\'s Plumbing</span>')
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
    'data-es="Homestead, FL · Plumbing &amp; Septic" data-en="Homestead, FL · Plumbing &amp; Septic">Homestead, FL · Plumbing &amp; Septic</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Only number you ever need." data-en="Only number you ever need.">Only number you ever need.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Septic, plumbing and" data-en="Septic, plumbing and">Septic, plumbing and</span><br /><span data-es="trenching, done " data-en="trenching, done ">trenching, done </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Septic tank installation, drain field repair, rough-in plumbing and trenching across Homestead and South Miami-Dade. Venancio and his team have handled projects large and small, with a 4.9 rating across 19 Google reviews." data-en="Septic tank installation, drain field repair, rough-in plumbing and trenching across Homestead and South Miami-Dade. Venancio and his team have handled projects large and small, with a 4.9 rating across 19 Google reviews.">Septic tank installation, drain field repair, rough-in plumbing and trenching across Homestead and South Miami-Dade. Venancio and his team have handled projects large and small, with a 4.9 rating across 19 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 19 reviews on Google" data-en="4.9 · 19 reviews on Google">4.9 · 19 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (305) 713-2040" data-en="Call (305) 713-2040">Call (305) 713-2040</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-excavator.jpg" alt="A trenching job for a new sewer line by Villa\'s Plumbing in Homestead, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">7am - 5:30pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Mon-Sat · Closed Sunday" data-en="Mon-Sat · Closed Sunday">Mon-Sat · Closed Sunday</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="19">19</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Septic <span class="text-shine">&amp;</span> Plumbing</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Rough-in · Trenching" data-en="Rough-in · Trenching">Rough-in · Trenching</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">+5</span> <span data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Repeat customers" data-en="Repeat customers">Repeat customers</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Homestead</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="South Miami-Dade, FL" data-en="South Miami-Dade, FL">South Miami-Dade, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Septic Install"),
    ("Hybrid Set", "Drain Field"),
    ("Volume Set", "Rough-In Plumbing"),
    ("Mega Volume", "Shower Pans"),
    ("Bottom Lashes", "Trenching"),
    ("West Palm Beach, FL", "Homestead, FL"),
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
          <img src="assets/about-septic.jpg" alt="A septic drain field installed by Villa\'s Plumbing in Homestead, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One crew," data-en="One crew,">One crew,</span><br /><span class="text-shine" data-es="every job done right" data-en="every job done right">every job done right</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    ('data-es="Villa\'s Plumbing LLC, led by Venancio, handles septic tank installation, drain field repair, rough-in plumbing and trenching across Homestead and South Miami-Dade. From the smallest repair to the largest site job, customers call Villa\'s Plumbing the only number they need." data-en="Villa\'s Plumbing LLC, led by Venancio, handles septic tank installation, drain field repair, rough-in plumbing and trenching across Homestead and South Miami-Dade. From the smallest repair to the largest site job, customers call Villa\'s Plumbing the only number they need.">Villa\'s Plumbing LLC, led by Venancio, handles septic tank installation, drain field repair, rough-in plumbing and trenching across Homestead and South Miami-Dade. From the smallest repair to the largest site job, customers call Villa\'s Plumbing the only number they need.</p>'))
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.9-star rating across 19 Google reviews, and customers who call back time after time, for jobs large and small." data-en="The result: a 4.9-star rating across 19 Google reviews, and customers who call back time after time, for jobs large and small.">The result: a 4.9-star rating across 19 Google reviews, and customers who call back time after time, for jobs large and small.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="19">19</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">+5</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Anos de servicio" data-en="Years of service">Years of service</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,143,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Villa\'s Plumbing" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,143,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Venancio · <span class="text-[color:var(--ink-40)]" data-es="Owner" data-en="Owner">Owner</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your project, start" data-en="Your project, start">Your project, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call it in" data-en="Call it in">Call it in</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call with what needs fixing or installing, and Venancio walks you through the job over the phone." data-en="Call with what needs fixing or installing, and Venancio walks you through the job over the phone.">Call with what needs fixing or installing, and Venancio walks you through the job over the phone.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Honest quote" data-en="Honest quote">Honest quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a clear, upfront price for the work before any digging or plumbing starts." data-en="You get a clear, upfront price for the work before any digging or plumbing starts.">You get a clear, upfront price for the work before any digging or plumbing starts.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The work gets done" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="From a septic install to a rough-in job, the crew handles it with the same care every time." data-en="From a septic install to a rough-in job, the crew handles it with the same care every time.">From a septic install to a rough-in job, the crew handles it with the same care every time.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walkthrough" data-en="Walkthrough">Walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Before the crew leaves, you walk through the finished work together, so you know it was done right." data-en="Before the crew leaves, you walk through the finished work together, so you know it was done right.">Before the crew leaves, you walk through the finished work together, so you know it was done right.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine" data-es="every property" data-en="every property">every property</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two jobs are the same, so every project gets its own honest quote by phone, before any work begins." data-en="No two jobs are the same, so every project gets its own honest quote by phone, before any work begins.">No two jobs are the same, so every project gets its own honest quote by phone, before any work begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(74,160,143,0.4); box-shadow: 0 18px 50px rgba(34,51,48,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Septic Tank Installation" data-en="Septic Tank Installation">Septic Tank Installation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="New septic tank and drain field installation, set and backfilled with the gravel bed a long-lasting system needs." data-en="New septic tank and drain field installation, set and backfilled with the gravel bed a long-lasting system needs.">New septic tank and drain field installation, set and backfilled with the gravel bed a long-lasting system needs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it flowing" data-en="Keep it flowing">Keep it flowing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Drain Field &amp; Access Repair" data-en="Drain Field &amp; Access Repair">Drain Field &amp; Access Repair</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Drain field repair and access ring replacement for septic systems that are backing up or due for service." data-en="Drain field repair and access ring replacement for septic systems that are backing up or due for service.">Drain field repair and access ring replacement for septic systems that are backing up or due for service.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="New construction" data-en="New construction">New construction</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Rough-In Plumbing" data-en="Rough-In Plumbing">Rough-In Plumbing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Rough-in plumbing and shower pan waterproofing for remodels and new builds, framed and inspected right." data-en="Rough-in plumbing and shower pan waterproofing for remodels and new builds, framed and inspected right.">Rough-in plumbing and shower pan waterproofing for remodels and new builds, framed and inspected right.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Site work" data-en="Site work">Site work</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Trenching &amp; Pipe Laying" data-en="Trenching &amp; Pipe Laying">Trenching &amp; Pipe Laying</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trenching and PVC pipe laying for sewer lines, discharge lines and the site work bigger jobs need." data-en="Trenching and PVC pipe laying for sewer lines, discharge lines and the site work bigger jobs need.">Trenching and PVC pipe laying for sewer lines, discharge lines and the site work bigger jobs need.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Septic Systems" data-en="Septic Systems">Septic Systems</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Septic tank install" data-en="Septic tank install">Septic tank install</li>
            <li class="flex items-center gap-2" data-es="Drain field repair" data-en="Drain field repair">Drain field repair</li>
            <li class="flex items-center gap-2" data-es="Access ring replacement" data-en="Access ring replacement">Access ring replacement</li>
            <li class="flex items-center gap-2" data-es="Septic inspections" data-en="Septic inspections">Septic inspections</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Plumbing Rough-In" data-en="Plumbing Rough-In">Plumbing Rough-In</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Rough-in plumbing" data-en="Rough-in plumbing">Rough-in plumbing</li>
            <li class="flex items-center gap-2" data-es="Shower pan waterproofing" data-en="Shower pan waterproofing">Shower pan waterproofing</li>
            <li class="flex items-center gap-2" data-es="Cleanout installs" data-en="Cleanout installs">Cleanout installs</li>
            <li class="flex items-center gap-2" data-es="Pipe repair" data-en="Pipe repair">Pipe repair</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Site Work" data-en="Site Work">Site Work</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Trenching &amp; excavation" data-en="Trenching &amp; excavation">Trenching &amp; excavation</li>
            <li class="flex items-center gap-2" data-es="PVC pipe laying" data-en="PVC pipe laying">PVC pipe laying</li>
            <li class="flex items-center gap-2" data-es="Discharge lines" data-en="Discharge lines">Discharge lines</li>
            <li class="flex items-center gap-2" data-es="Residential &amp; light commercial" data-en="Residential &amp; light commercial">Residential &amp; light commercial</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and materials. Call (305) 713-2040 for a free quote." data-en="Pricing depends on scope and materials. Call (305) 713-2040 for a free quote.">Pricing depends on scope and materials. Call (305) 713-2040 for a free quote.</span></p>')
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
          Call (305) 713-2040
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Anillo de acceso septico reparado" data-en="Septic access ring repaired">Septic access ring repaired</span><img src="assets/gallery-access-ring.jpg" alt="A septic tank access ring repaired by Villa\'s Plumbing in Homestead, FL" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Impermeabilizacion de plato de ducha" data-en="Shower pan waterproofing">Shower pan waterproofing</span><img src="assets/gallery-shower-pan.jpg" alt="Shower pan waterproofing membrane installed by Villa\'s Plumbing" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Linea de descarga en PVC" data-en="PVC discharge line">PVC discharge line</span><img src="assets/gallery-discharge-pipe.jpg" alt="A PVC discharge line installed by Villa\'s Plumbing" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Plomeria bajo la casa" data-en="Rough plumbing underneath the home">Rough plumbing underneath the home</span><img src="assets/gallery-pipe-fitting.jpg" alt="Rough plumbing fitting installed under a home by Villa\'s Plumbing" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Instalacion de registro de limpieza" data-en="Cleanout install">Cleanout install</span><img src="assets/gallery-cleanout.jpg" alt="A plumbing cleanout installed by Villa\'s Plumbing" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Homestead" data-en="What Homestead">What Homestead</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 19 reviews on Google" data-en="4.9 out of 5 · 19 reviews on Google">4.9 out of 5 · 19 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely 100% pleased with all they did for us!! On time and professional through the whole job. I highly recommend Villa Plumbing for all your needs as they can do so much for you! Only number you ever need!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Pamela Gramling</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I have used Villa's Plumbing several times. Venancio and his team are very knowledgeable and trust worthy. They have always been very responsive, punctual, cordial, honest, efficient and fairly priced. They will not give you the runaround. I highly recommend Villa's Pluming."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jen Bahamon</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Time after time, we've called on Villa Plumbing. Over the years they've handled the largest of projects and the smallest. They've..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Enrique</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 19 reviews on Google" data-en="Read all 19 reviews on Google">Read all 19 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (direccion real disponible)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Homestead, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,143,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + NEW_ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,143,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,143,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Saturday, 7:00 AM to 5:30 PM. Closed Sunday." data-en="Monday to Saturday, 7:00 AM to 5:30 PM. Closed Sunday.">Monday to Saturday, 7:00 AM to 5:30 PM. Closed Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,143,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (305) 713-2040" data-en="Call (305) 713-2040">Call (305) 713-2040</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,143,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.9 stars across 19 verified Google reviews." data-en="4.9 stars across 19 verified Google reviews.">4.9 stars across 19 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,143,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Villa\'s Plumbing, 16121 SW 287th St, Homestead FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Only number you ever need." data-en="Only number you ever need.">Only number you ever need.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call fixes" data-en="One call fixes">One call fixes</span> <span class="text-shine" data-es="it all" data-en="it all">it all</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (305) 713-2040 for a free, honest quote on your septic, plumbing or trenching job. Monday to Saturday, 7 AM to 5:30 PM." data-en="Call (305) 713-2040 for a free, honest quote on your septic, plumbing or trenching job. Monday to Saturday, 7 AM to 5:30 PM.">Call (305) 713-2040 for a free, honest quote on your septic, plumbing or trenching job. Monday to Saturday, 7 AM to 5:30 PM.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (305) 713-2040" data-en="Call (305) 713-2040">Call (305) 713-2040</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Villa\'s Plumbing</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,230,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Villa\'s Plumbing" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,230,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Villa\'s Plumbing</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Plumbing &amp; septic serving Homestead, FL and South Miami-Dade." data-en="Plumbing &amp; septic serving Homestead, FL and South Miami-Dade.">Plumbing &amp; septic serving Homestead, FL and South Miami-Dade.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#bef0e6]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#9ddccf]" data-es="Call (305) 713-2040" data-en="Call (305) 713-2040">Call (305) 713-2040</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#bef0e6]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#9ddccf]">4.9 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Villa\'s Plumbing LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Villa\'s Plumbing">')
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
    "Homestead, FL · Plumbing &amp; Septic": "Homestead, FL · Plomeria y Septico",
    "Only number you ever need.": "El unico numero que necesitas.",
    "Septic, plumbing and": "Septico, plomeria y",
    "trenching, done ": "excavacion, hecho ",
    "right": "bien",
    "Septic tank installation, drain field repair, rough-in plumbing and trenching across Homestead and South Miami-Dade. Venancio and his team have handled projects large and small, with a 4.9 rating across 19 Google reviews.":
        "Instalacion de tanques septicos, reparacion de campos de drenaje, plomeria de obra gris y excavacion en Homestead y el sur de Miami-Dade. Venancio y su equipo han manejado proyectos grandes y pequenos, con una calificacion de 4.9 en 19 resenas de Google.",
    "4.9 · 19 reviews on Google": "4.9 · 19 resenas en Google",
    "Call (305) 713-2040": "Llama al (305) 713-2040",
    "Open": "Abierto",
    "Mon-Sat · Closed Sunday": "Lun-Sab · Cerrado domingo",
    "Rough-in · Trenching": "Obra gris · Excavacion",
    "Repeat customers": "Clientes recurrentes",
    "South Miami-Dade, FL": "Sur de Miami-Dade, FL",
    "One crew,": "Un equipo,",
    "every job done right": "cada trabajo bien hecho",
    "Owner": "Dueno",
    "Your project, start": "Tu proyecto, de inicio",
    "to finish": "hasta el final",
    "Call it in": "Llama y cuenta",
    "Call with what needs fixing or installing, and Venancio walks you through the job over the phone.":
        "Llama con lo que necesitas reparar o instalar, y Venancio te explica el trabajo por telefono.",
    "Honest quote": "Cotizacion honesta",
    "You get a clear, upfront price for the work before any digging or plumbing starts.":
        "Recibes un precio claro y directo antes de empezar a excavar o a trabajar en la plomeria.",
    "The work gets done": "El trabajo se hace",
    "From a septic install to a rough-in job, the crew handles it with the same care every time.":
        "Desde una instalacion septica hasta un trabajo de obra gris, el equipo lo maneja con el mismo cuidado siempre.",
    "Walkthrough": "Revision final",
    "Before the crew leaves, you walk through the finished work together, so you know it was done right.":
        "Antes de que el equipo se vaya, revisan juntos el trabajo terminado, para que sepas que quedo bien hecho.",
    "Services for": "Servicios para",
    "every property": "cada propiedad",
    "No two jobs are the same, so every project gets its own honest quote by phone, before any work begins.":
        "Ningun trabajo es igual a otro, asi que cada proyecto recibe su propia cotizacion honesta por telefono, antes de comenzar.",
    "Most requested": "Lo mas solicitado",
    "Septic Tank Installation": "Instalacion de Tanque Septico",
    "New septic tank and drain field installation, set and backfilled with the gravel bed a long-lasting system needs.":
        "Instalacion de tanque septico y campo de drenaje nuevo, colocado y rellenado con la cama de grava que necesita un sistema duradero.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Keep it flowing": "Mantenlo fluyendo",
    "Drain Field &amp; Access Repair": "Reparacion de Campo de Drenaje y Acceso",
    "Drain field repair and access ring replacement for septic systems that are backing up or due for service.":
        "Reparacion de campo de drenaje y reemplazo de anillo de acceso para sistemas septicos que se estan represando o necesitan servicio.",
    "New construction": "Construccion nueva",
    "Rough-In Plumbing": "Plomeria de Obra Gris",
    "Rough-in plumbing and shower pan waterproofing for remodels and new builds, framed and inspected right.":
        "Plomeria de obra gris e impermeabilizacion de plato de ducha para remodelaciones y construcciones nuevas, enmarcada e inspeccionada correctamente.",
    "Site work": "Trabajo de sitio",
    "Trenching &amp; Pipe Laying": "Excavacion e Instalacion de Tuberia",
    "Trenching and PVC pipe laying for sewer lines, discharge lines and the site work bigger jobs need.":
        "Excavacion e instalacion de tuberia de PVC para lineas de alcantarillado, lineas de descarga y el trabajo de sitio que necesitan los proyectos grandes.",
    "Septic Systems": "Sistemas Septicos",
    "Septic tank install": "Instalacion de tanque septico",
    "Drain field repair": "Reparacion de campo de drenaje",
    "Access ring replacement": "Reemplazo de anillo de acceso",
    "Septic inspections": "Inspecciones septicas",
    "Plumbing Rough-In": "Plomeria de Obra Gris",
    "Rough-in plumbing": "Plomeria de obra gris",
    "Shower pan waterproofing": "Impermeabilizacion de plato de ducha",
    "Cleanout installs": "Instalacion de registros de limpieza",
    "Pipe repair": "Reparacion de tuberia",
    "Site Work": "Trabajo de Sitio",
    "Trenching &amp; excavation": "Excavacion de zanjas",
    "PVC pipe laying": "Instalacion de tuberia de PVC",
    "Discharge lines": "Lineas de descarga",
    "Residential &amp; light commercial": "Residencial y comercial ligero",
    "Pricing depends on scope and materials. Call (305) 713-2040 for a free quote.":
        "El precio depende del alcance y los materiales. Llama al (305) 713-2040 para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Homestead": "Lo que dicen los",
    "customers say": "clientes en Homestead",
    "Read all 19 reviews on Google": "Lee las 19 resenas en Google",
    "Serving": "Sirviendo a",
    "Hours": "Horario",
    "Monday to Saturday, 7:00 AM to 5:30 PM. Closed Sunday.": "Lunes a sabado, de 7:00 AM a 5:30 PM. Cerrado los domingos.",
    "Reviews": "Resenas",
    "4.9 stars across 19 verified Google reviews.": "4.9 estrellas en 19 resenas verificadas de Google.",
    "One call fixes": "Una llamada arregla",
    "it all": "todo",
    "Call (305) 713-2040 for a free, honest quote on your septic, plumbing or trenching job. Monday to Saturday, 7 AM to 5:30 PM.":
        "Llama al (305) 713-2040 para una cotizacion gratis y honesta de tu trabajo septico, de plomeria o excavacion. Lunes a sabado, de 7 AM a 5:30 PM.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Plumbing &amp; septic serving Homestead, FL and South Miami-Dade.": "Plomeria y septico en Homestead, FL y el sur de Miami-Dade.",
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
