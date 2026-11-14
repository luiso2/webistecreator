import re
import shutil

SLUG = "a1-stump-grinding-tree-service"
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
# 2. Paleta: plum-pink (lashbloom) -> verde oliva / musgo (A-1 Stump Grinding)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#6ea04a"),
    ("#5c2140", "#3a5c21"),
    ("#f0bed7", "#d3f0be"),
    ("#faf2f6", "#f5faf2"),
    ("#c47a9c", "#99c47a"),
    ("#8a5573", "#6b8a55"),
    ("#f3e0ea", "#e8f3e0"),
    ("#d9a8c2", "#bcd9a8"),
    ("#7d3457", "#527d34"),
    ("#5f2c48", "#415f2c"),
    ("#33222c", "#293322"),
    ("#fbf3f8", "#f6fbf3"),
    ("#fbeff5", "#f4fbef"),
    ("#f8dfeb", "#e9f8df"),
    ("#f6f1ea", "#eff6ea"),
    ("#f2d5e3", "#e1f2d5"),
    ("#f2cfe0", "#def2cf"),
    ("#efd0e0", "#ddefd0"),
    ("#e5c1d4", "#d0e5c1"),
    ("#dc9dbe", "#b7dc9d"),
    ("#d3a2bc", "#b6d3a2"),
    ("#c9789f", "#9ac978"),
    ("#b25a85", "#7fb25a"),
    ("#2a1722", "#1f2a17"),
    ("#1f0f18", "#161f0f"),
    ("#1c0f16", "#141c0f"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(110,160,74"),
    ("rgba(51,34,44", "rgba(41,51,34"),
    ("rgba(240,190,215", "rgba(211,240,190"),
    ("rgba(70,25,50", "rgba(44,70,25"),
    ("rgba(250,242,246", "rgba(245,250,242"),
    ("rgba(125,52,87", "rgba(82,125,52"),
    ("rgba(253,246,250", "rgba(249,253,246"),
    ("rgba(40,16,30", "rgba(26,40,16"),
    ("rgba(233,205,186", "rgba(206,233,186"),
    ("rgba(185,138,128", "rgba(152,185,128"),
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
NEW_TEL = "tel:+18133092323"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_REVIEWS_URL = "https://www.google.com/search?q=A-1+Stump+Grinding+Tree+Service+Dover+FL+reviews"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_REVIEWS_LABEL = "Google Reviews"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

NEW_ADDR = "13338 Jaudon Ranch Rd, Dover, FL 33527"
NEW_MAPS = "https://www.google.com/maps?q=13338+Jaudon+Ranch+Rd,+Dover,+FL+33527"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>A-1 Stump Grinding &amp; Tree Service · Stump Grinding in Dover, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="A-1 Stump Grinding &amp; Tree Service, Dover FL: stump grinding, tree removal, storm damage cleanup and lot clearing. 4.9 stars across 16 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="A-1 Stump Grinding &amp; Tree Service · Stump Grinding in Dover, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Stump grinding, tree removal, storm damage cleanup and lot clearing. 4.9 on Google with 16 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-owner-stump.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-owner-stump.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "A-1 Stump Grinding &amp; Tree Service",
    "description": "Tree service company in Dover, FL: stump grinding, full stump removal, tree removal, storm damage cleanup and lot clearing.",
    "address": { "@type": "PostalAddress", "streetAddress": "13338 Jaudon Ranch Rd", "addressLocality": "Dover", "addressRegion": "FL", "postalCode": "33527", "addressCountry": "US" },
    "telephone": "+1-813-309-2323",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "16", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "07:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Tree &amp; stump services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Stump Grinding" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Full Stump Removal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tree Removal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Lot &amp; Storm Cleanup" } }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,160,74,0.35)]" />',
    '<img src="assets/hero-owner-stump.jpg" alt="A-1 Stump Grinding and Tree Service" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,160,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">A-1 <span class="text-[color:var(--accent-deep)]">Stump</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">A1</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">A-1 Stump Grinding</span>')
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
    'data-es="Dover, FL · Stump &amp; Tree Service" data-en="Dover, FL · Stump &amp; Tree Service">Dover, FL · Stump &amp; Tree Service</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="That stump? Not for long." data-en="That stump? Not for long.">That stump? Not for long.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Stump grinding, removal" data-en="Stump grinding, removal">Stump grinding, removal</span><br /><span data-es="and cleanup, done " data-en="and cleanup, done ">and cleanup, done </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Stump grinding, full stump removal, tree removal and storm cleanup across Dover and the greater Tampa Bay area. Lee returns calls fast and walks you through every step, with a 4.9 rating across 16 Google reviews." data-en="Stump grinding, full stump removal, tree removal and storm cleanup across Dover and the greater Tampa Bay area. Lee returns calls fast and walks you through every step, with a 4.9 rating across 16 Google reviews.">Stump grinding, full stump removal, tree removal and storm cleanup across Dover and the greater Tampa Bay area. Lee returns calls fast and walks you through every step, with a 4.9 rating across 16 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 16 reviews on Google" data-en="4.9 · 16 reviews on Google">4.9 · 16 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (813) 309-2323" data-en="Call (813) 309-2323">Call (813) 309-2323</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-owner-stump.jpg" alt="The A-1 Stump Grinding owner standing on a freshly cut stump with a chainsaw" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">7am - 7pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="16">16</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Stump <span class="text-shine">&amp;</span> Tree</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Grinding · Removal" data-en="Grinding · Removal">Grinding · Removal</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">7am</span> - 7pm</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Open 7 days" data-en="Open 7 days">Open 7 days</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Dover</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Tampa Bay, FL" data-en="Tampa Bay, FL">Tampa Bay, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Stump Grinding"),
    ("Hybrid Set", "Stump Removal"),
    ("Volume Set", "Tree Removal"),
    ("Mega Volume", "Storm Cleanup"),
    ("Bottom Lashes", "Lot Clearing"),
    ("West Palm Beach, FL", "Dover, FL"),
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
          <img src="assets/about-owner-dog.jpg" alt="The A-1 Stump Grinding owner sitting on a cut stump with his dog" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One owner," data-en="One owner,">One owner,</span><br /><span class="text-shine" data-es="always on the phone" data-en="always on the phone">always on the phone</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="A-1 Stump Grinding &amp; Tree Service is led by Lee, who answers the phone himself and explains the job before any machine shows up. Stump grinding, stump removal, tree removal and cleanup across Dover and the Tampa Bay area." data-en="A-1 Stump Grinding &amp; Tree Service is led by Lee, who answers the phone himself and explains the job before any machine shows up. Stump grinding, stump removal, tree removal and cleanup across Dover and the Tampa Bay area.">A-1 Stump Grinding &amp; Tree Service is led by Lee, who answers the phone himself and explains the job before any machine shows up. Stump grinding, stump removal, tree removal and cleanup across Dover and the Tampa Bay area.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Customers describe Lee as quick to call back, patient explaining the options, and happy with the result. The result: a 4.9-star rating across 16 Google reviews." data-en="Customers describe Lee as quick to call back, patient explaining the options, and happy with the result. The result: a 4.9-star rating across 16 Google reviews.">Customers describe Lee as quick to call back, patient explaining the options, and happy with the result. The result: a 4.9-star rating across 16 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="16">16</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Trato directo" data-en="Direct contact">Direct contact</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,160,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/hero-owner-stump.jpg" alt="A-1 Stump Grinding and Tree Service" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(110,160,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Lee · <span class="text-[color:var(--ink-40)]" data-es="Owner" data-en="Owner">Owner</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your stump, start" data-en="Your stump, start">Your stump, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call Lee" data-en="Call Lee">Call Lee</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call with the stump or tree that needs work, and Lee calls back promptly to talk through the job." data-en="Call with the stump or tree that needs work, and Lee calls back promptly to talk through the job.">Call with the stump or tree that needs work, and Lee calls back promptly to talk through the job.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Clear options" data-en="Clear options">Clear options</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Lee explains the options and the price for each one, so you can decide what makes sense before anything starts." data-en="Lee explains the options and the price for each one, so you can decide what makes sense before anything starts.">Lee explains the options and the price for each one, so you can decide what makes sense before anything starts.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The work gets done" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Stump grinder, chainsaw or skid steer, whatever the stump or tree needs, handled with the same promptness every time." data-en="Stump grinder, chainsaw or skid steer, whatever the stump or tree needs, handled with the same promptness every time.">Stump grinder, chainsaw or skid steer, whatever the stump or tree needs, handled with the same promptness every time.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Clean grounds" data-en="Clean grounds">Clean grounds</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Grindings and debris get cleared away, leaving the spot ready for new grass or whatever comes next." data-en="Grindings and debris get cleared away, leaving the spot ready for new grass or whatever comes next.">Grindings and debris get cleared away, leaving the spot ready for new grass or whatever comes next.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Stump &amp; tree work for" data-en="Stump &amp; tree work for">Stump &amp; tree work for</span> <span class="text-shine" data-es="every property" data-en="every property">every property</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two stumps are the same, so every job gets its own clear quote from Lee before any machine shows up." data-en="No two stumps are the same, so every job gets its own clear quote from Lee before any machine shows up.">No two stumps are the same, so every job gets its own clear quote from Lee before any machine shows up.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(110,160,74,0.4); box-shadow: 0 18px 50px rgba(41,51,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Stump Grinding" data-en="Stump Grinding">Stump Grinding</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Stumps ground down flat and level, roots and all, often in a single visit with Lee's own equipment." data-en="Stumps ground down flat and level, roots and all, often in a single visit with Lee's own equipment.">Stumps ground down flat and level, roots and all, often in a single visit with Lee's own equipment.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Roots and all" data-en="Roots and all">Roots and all</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Stump Removal" data-en="Full Stump Removal">Full Stump Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Large or hollow stumps dug out and hauled off completely, when grinding alone will not clear the spot." data-en="Large or hollow stumps dug out and hauled off completely, when grinding alone will not clear the spot.">Large or hollow stumps dug out and hauled off completely, when grinding alone will not clear the spot.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Full takedown" data-en="Full takedown">Full takedown</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tree Removal" data-en="Tree Removal">Tree Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pines, oaks and toppled trees taken down and cut up by hand, climbing when the tree calls for it." data-en="Pines, oaks and toppled trees taken down and cut up by hand, climbing when the tree calls for it.">Pines, oaks and toppled trees taken down and cut up by hand, climbing when the tree calls for it.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lot work" data-en="Lot work">Lot work</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lot &amp; Storm Cleanup" data-en="Lot &amp; Storm Cleanup">Lot &amp; Storm Cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Toppled trees, root balls and storm debris cleared and the lot graded level and ready for mulch or sod." data-en="Toppled trees, root balls and storm debris cleared and the lot graded level and ready for mulch or sod.">Toppled trees, root balls and storm debris cleared and the lot graded level and ready for mulch or sod.</p>
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
            <li class="flex items-center gap-2" data-es="Full stump removal" data-en="Full stump removal">Full stump removal</li>
            <li class="flex items-center gap-2" data-es="Root removal" data-en="Root removal">Root removal</li>
            <li class="flex items-center gap-2" data-es="Grindings haul away" data-en="Grindings haul away">Grindings haul away</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Tree Work" data-en="Tree Work">Tree Work</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Tree removal" data-en="Tree removal">Tree removal</li>
            <li class="flex items-center gap-2" data-es="Toppled tree removal" data-en="Toppled tree removal">Toppled tree removal</li>
            <li class="flex items-center gap-2" data-es="Pine &amp; oak takedowns" data-en="Pine &amp; oak takedowns">Pine &amp; oak takedowns</li>
            <li class="flex items-center gap-2" data-es="Tree &amp; stump inspections" data-en="Tree &amp; stump inspections">Tree &amp; stump inspections</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Lot &amp; Cleanup" data-en="Lot &amp; Cleanup">Lot &amp; Cleanup</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Storm damage cleanup" data-en="Storm damage cleanup">Storm damage cleanup</li>
            <li class="flex items-center gap-2" data-es="Lot grading" data-en="Lot grading">Lot grading</li>
            <li class="flex items-center gap-2" data-es="Debris haul away" data-en="Debris haul away">Debris haul away</li>
            <li class="flex items-center gap-2" data-es="Free estimates" data-en="Free estimates">Free estimates</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on stump size and access. Call (813) 309-2323 for a free quote." data-en="Pricing depends on stump size and access. Call (813) 309-2323 for a free quote.">Pricing depends on stump size and access. Call (813) 309-2323 for a free quote.</span></p>')
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
          Call (813) 309-2323
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Seccion de tronco hueco removida" data-en="Hollow trunk section removed">Hollow trunk section removed</span><img src="assets/gallery-hollow-log.jpg" alt="A large hollow tree trunk section cut and removed by A-1 Stump Grinding" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Tocon fresco listo para triturar" data-en="Fresh stump ready for grinding">Fresh stump ready for grinding</span><img src="assets/gallery-fresh-stump.jpg" alt="A freshly cut tree stump in front of a Dover home before grinding" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Corte con motosierra en tocon grande" data-en="Chainsaw cut on a large stump">Chainsaw cut on a large stump</span><img src="assets/gallery-chainsaw-stump.jpg" alt="A Stihl chainsaw cutting into a large tree stump" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Terreno despejado y nivelado" data-en="Lot cleared and graded">Lot cleared and graded</span><img src="assets/gallery-lot-cleared.jpg" alt="A cleared and graded lot in Dover, FL after stump removal" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Subida a un pino alto" data-en="Climbing a tall pine">Climbing a tall pine</span><img src="assets/gallery-pine-climb.jpg" alt="An A-1 Stump Grinding crew member climbing a tall pine tree" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Dover" data-en="What Dover">What Dover</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 16 reviews on Google" data-en="4.9 out of 5 · 16 reviews on Google">4.9 out of 5 · 16 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We recently used A-1 Stump Grinding &amp; Tree Service to remove a stump. Lee promptly returned my initial call, and continued to communicate with me until the job was done. When he came out to give me..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Judith Floyd</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Lee did such an amazing job informing me of the entire process and making sure that I was able to make the best decision possible. He was incredibly friendly and a joy to work with. Also, he was very..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jamie Parker</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I have used A-1 a couple of times for tree and stump work. I have been very happy with the communication and promptness for getting the work completed. I had a pine and oak pair topple over. The root..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Roland Baggs</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 16 reviews on Google" data-en="Read all 16 reviews on Google">Read all 16 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (direccion real disponible)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Dover, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,160,74,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + NEW_ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,160,74,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,160,74,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open 7 AM to 7 PM, every day of the week." data-en="Open 7 AM to 7 PM, every day of the week.">Open 7 AM to 7 PM, every day of the week.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,160,74,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (813) 309-2323" data-en="Call (813) 309-2323">Call (813) 309-2323</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,160,74,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.9 stars across 16 verified Google reviews." data-en="4.9 stars across 16 verified Google reviews.">4.9 stars across 16 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(110,160,74,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: A-1 Stump Grinding and Tree Service, 13338 Jaudon Ranch Rd, Dover FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="That stump? Not for long." data-en="That stump? Not for long.">That stump? Not for long.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call to" data-en="One call to">One call to</span> <span class="text-shine" data-es="Lee" data-en="Lee">Lee</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (813) 309-2323 for a free quote on your stump, tree or lot cleanup job. Open 7 AM to 7 PM, every day." data-en="Call (813) 309-2323 for a free quote on your stump, tree or lot cleanup job. Open 7 AM to 7 PM, every day.">Call (813) 309-2323 for a free quote on your stump, tree or lot cleanup job. Open 7 AM to 7 PM, every day.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (813) 309-2323" data-en="Call (813) 309-2323">Call (813) 309-2323</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">A-1 Stump Grinding</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(211,240,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/hero-owner-stump.jpg" alt="A-1 Stump Grinding and Tree Service" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(211,240,190,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">A-1 Stump Grinding</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Stump &amp; tree service serving Dover, FL and the Tampa Bay area." data-en="Stump &amp; tree service serving Dover, FL and the Tampa Bay area.">Stump &amp; tree service serving Dover, FL and the Tampa Bay area.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#d3f0be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#b7dc9d]" data-es="Call (813) 309-2323" data-en="Call (813) 309-2323">Call (813) 309-2323</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#d3f0be]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#b7dc9d]">4.9 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 A-1 Stump Grinding &amp; Tree Service.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call A-1 Stump Grinding">')
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
    "Dover, FL · Stump &amp; Tree Service": "Dover, FL · Servicio de Tocones y Arboles",
    "That stump? Not for long.": "¿Ese tocon? No por mucho tiempo.",
    "Stump grinding, removal": "Trituracion de tocones, remocion",
    "and cleanup, done ": "y limpieza, hecho ",
    "right": "bien",
    "Stump grinding, full stump removal, tree removal and storm cleanup across Dover and the greater Tampa Bay area. Lee returns calls fast and walks you through every step, with a 4.9 rating across 16 Google reviews.":
        "Trituracion de tocones, remocion completa de tocones, remocion de arboles y limpieza tras tormentas en Dover y el area de Tampa Bay. Lee regresa las llamadas rapido y explica cada paso, con calificacion de 4.9 en 16 resenas de Google.",
    "4.9 · 16 reviews on Google": "4.9 · 16 resenas en Google",
    "Call (813) 309-2323": "Llama al (813) 309-2323",
    "Open": "Abierto",
    "Every day of the week": "Todos los dias de la semana",
    "Grinding · Removal": "Trituracion · Remocion",
    "Open 7 days": "Abierto 7 dias",
    "Tampa Bay, FL": "Tampa Bay, FL",
    "One owner,": "Un dueno,",
    "always on the phone": "siempre al telefono",
    "A-1 Stump Grinding &amp; Tree Service is led by Lee, who answers the phone himself and explains the job before any machine shows up. Stump grinding, stump removal, tree removal and cleanup across Dover and the Tampa Bay area.":
        "A-1 Stump Grinding &amp; Tree Service es dirigido por Lee, quien contesta el telefono personalmente y explica el trabajo antes de que llegue cualquier maquina. Trituracion de tocones, remocion de tocones, remocion de arboles y limpieza en Dover y el area de Tampa Bay.",
    "Customers describe Lee as quick to call back, patient explaining the options, and happy with the result. The result: a 4.9-star rating across 16 Google reviews.":
        "Los clientes describen a Lee como alguien que regresa las llamadas rapido, explica las opciones con paciencia, y deja a todos contentos con el resultado. El resultado: una calificacion de 4.9 estrellas en 16 resenas de Google.",
    "Owner": "Dueno",
    "Your stump, start": "Tu tocon, de inicio",
    "to finish": "hasta el final",
    "Call Lee": "Llama a Lee",
    "Call with the stump or tree that needs work, and Lee calls back promptly to talk through the job.":
        "Llama con el tocon o arbol que necesita trabajo, y Lee regresa la llamada rapido para hablar del trabajo.",
    "Clear options": "Opciones claras",
    "Lee explains the options and the price for each one, so you can decide what makes sense before anything starts.":
        "Lee explica las opciones y el precio de cada una, para que decidas lo que tiene sentido antes de empezar.",
    "The work gets done": "El trabajo se hace",
    "Stump grinder, chainsaw or skid steer, whatever the stump or tree needs, handled with the same promptness every time.":
        "Trituradora de tocones, motosierra o minicargadora, lo que necesite el tocon o arbol, manejado siempre con la misma rapidez.",
    "Clean grounds": "Terreno limpio",
    "Grindings and debris get cleared away, leaving the spot ready for new grass or whatever comes next.":
        "Los residuos de trituracion y escombros se retiran, dejando el lugar listo para pasto nuevo o lo que siga.",
    "Stump &amp; tree work for": "Trabajo de tocones y arboles para",
    "every property": "cada propiedad",
    "No two stumps are the same, so every job gets its own clear quote from Lee before any machine shows up.":
        "Ningun tocon es igual a otro, asi que cada trabajo recibe su propia cotizacion clara de Lee antes de que llegue cualquier maquina.",
    "Most requested": "Lo mas solicitado",
    "Stump Grinding": "Trituracion de Tocones",
    "Stumps ground down flat and level, roots and all, often in a single visit with Lee's own equipment.":
        "Tocones triturados hasta quedar planos y nivelados, raices incluidas, muchas veces en una sola visita con el equipo propio de Lee.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Roots and all": "Raices incluidas",
    "Full Stump Removal": "Remocion Completa de Tocones",
    "Large or hollow stumps dug out and hauled off completely, when grinding alone will not clear the spot.":
        "Tocones grandes o huecos se excavan y retiran por completo, cuando triturar solo no es suficiente para despejar el lugar.",
    "Full takedown": "Remocion completa",
    "Tree Removal": "Remocion de Arboles",
    "Pines, oaks and toppled trees taken down and cut up by hand, climbing when the tree calls for it.":
        "Pinos, robles y arboles caidos se bajan y cortan a mano, subiendo cuando el arbol lo requiere.",
    "Lot work": "Trabajo de terreno",
    "Lot &amp; Storm Cleanup": "Limpieza de Terreno y Tormentas",
    "Toppled trees, root balls and storm debris cleared and the lot graded level and ready for mulch or sod.":
        "Arboles caidos, bolas de raiz y escombros de tormenta se limpian y el terreno se nivela listo para astillas o cesped.",
    "Stump Work": "Trabajo de Tocones",
    "Stump grinding": "Trituracion de tocones",
    "Full stump removal": "Remocion completa de tocones",
    "Root removal": "Remocion de raices",
    "Grindings haul away": "Retiro de residuos de trituracion",
    "Tree Work": "Trabajo de Arboles",
    "Tree removal": "Remocion de arboles",
    "Toppled tree removal": "Remocion de arboles caidos",
    "Pine &amp; oak takedowns": "Remocion de pinos y robles",
    "Tree &amp; stump inspections": "Inspecciones de arboles y tocones",
    "Lot &amp; Cleanup": "Terreno y Limpieza",
    "Storm damage cleanup": "Limpieza de danos por tormenta",
    "Lot grading": "Nivelacion de terreno",
    "Debris haul away": "Retiro de escombros",
    "Free estimates": "Cotizaciones gratis",
    "Pricing depends on stump size and access. Call (813) 309-2323 for a free quote.":
        "El precio depende del tamano del tocon y el acceso. Llama al (813) 309-2323 para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Dover": "Lo que dicen los",
    "customers say": "clientes en Dover",
    "Read all 16 reviews on Google": "Lee las 16 resenas en Google",
    "Serving": "Sirviendo a",
    "Hours": "Horario",
    "Open 7 AM to 7 PM, every day of the week.": "Abierto de 7 AM a 7 PM, todos los dias de la semana.",
    "Reviews": "Resenas",
    "4.9 stars across 16 verified Google reviews.": "4.9 estrellas en 16 resenas verificadas de Google.",
    "One call to": "Una llamada a",
    "Lee": "Lee",
    "Call (813) 309-2323 for a free quote on your stump, tree or lot cleanup job. Open 7 AM to 7 PM, every day.":
        "Llama al (813) 309-2323 para una cotizacion gratis de tu tocon, arbol o limpieza de terreno. Abierto de 7 AM a 7 PM, todos los dias.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Stump &amp; tree service serving Dover, FL and the Tampa Bay area.": "Servicio de tocones y arboles en Dover, FL y el area de Tampa Bay.",
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
