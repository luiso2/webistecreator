import re
import shutil

SLUG = "florida-pressure-pros"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/dark-v2/index.html", PATH)
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


NEW_TEL = "tel:+17866447313"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Florida+Pressure+Pros+North+Miami+FL+reviews"
NEW_REVIEWS_LABEL = "Google Reviews"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: oro (Pure Artistry) -> azul "power wash" (Florida Pressure Pros)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#d4a84b", "#2f8fd4"),
    ("#6b5222", "#123a5c"),
    ("#1c1408", "#081019"),
    ("#e9c3ab", "#a8d4f0"),
    ("#8a744a", "#2a5878"),
    ("#f5efe3", "#eef6fb"),
    ("#f0dc9e", "#bfe3fb"),
    ("#e8cf96", "#bfe0f5"),
    ("#e8c476", "#7ec8f2"),
    ("#e5c374", "#6fb8ec"),
    ("#c9a04a", "#3aa0dc"),
    ("#9a7431", "#184a73"),
    ("#96742c", "#164463"),
    ("#0f0b07", "#061018"),
    ("#fbf6ea", "#eef6fb"),
    ("#faf1dc", "#eaf6fd"),
    ("#f8eed3", "#eaf6fd"),
    ("#f0dcae", "#cfe9fa"),
    ("#ecd9a8", "#bfe0f5"),
    ("#c9ab6b", "#4a90c2"),
    ("#bfa060", "#4a90c2"),
    ("#b8934a", "#1f6fb0"),
    ("#241c0e", "#0e1b28"),
    ("#191307", "#0c1b26"),
    ("#171207", "#0b1a26"),
    ("#100c05", "#071018"),
    ("#0c0905", "#050d14"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGB_TRIPLE_PALETTE = [
    ("212,168,75", "47,143,212"),
    ("232,207,150", "120,185,230"),
    ("185,138,128", "90,150,200"),
    ("180,140,60", "70,150,210"),
    ("122,90,30", "31,111,176"),
    ("80,58,18", "10,25,40"),
    ("110,85,35", "10,40,60"),
    ("54,42,38", "20,40,54"),
    ("15,11,7", "6,16,24"),
    ("245,239,227", "238,246,251"),
]
for old, new in RGB_TRIPLE_PALETTE:
    c = h.count(old)
    assert c > 0, "rgb triple not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform ni IG -> tel: + Google reviews
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
c = h.count(OLD_IG_URL)
assert c == 6, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
c = h.count(OLD_IG_HANDLE)
assert c == 4, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry &middot; Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>'
    if False else
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Florida Pressure Pros · Pressure Washing in North Miami, FL | 4.6 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Florida Pressure Pros, North Miami FL: house washing, driveway and sidewalk cleaning, roof soft washing and gutter cleaning across Miami-Dade and Broward. 4.6 stars across 28 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Florida Pressure Pros · Pressure Washing in North Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="House washing, driveways, roofs and gutters. 4.6 on Google with 28 reviews. Free quotes." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/hero-truck-trailer.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/hero-truck-trailer.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Florida Pressure Pros",
    "description": "Mobile pressure washing and soft washing company serving North Miami and the greater Miami-Dade and Broward area: house washing, driveways, sidewalks, roofs, gutters, patios and fences.",
    "areaServed": [
      { "@type": "City", "name": "North Miami" },
      { "@type": "AdministrativeArea", "name": "Miami-Dade County" },
      { "@type": "AdministrativeArea", "name": "Broward County" }
    ],
    "telephone": "+1-786-644-7313",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "28", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Pressure washing services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "House Washing" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Driveway &amp; Sidewalk Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Roof Soft Washing" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Pool Deck, Patio &amp; Fence Cleaning" } }
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
# 6. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">FP</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Florida Pressure Pros</span>')

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,212,0.35)]" />',
    '<img src="assets/raw/hero-truck-trailer.jpg" alt="Florida Pressure Pros" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,212,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Florida <span class="text-[color:var(--accent-deep)]">Pressure Pros</span></span>')
print("NAV LOGO done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call for a quote" data-en="Call for a quote">Call for a quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="North Miami, FL · Mobile Pressure Washing" data-en="North Miami, FL · Mobile Pressure Washing">North Miami, FL · Mobile Pressure Washing</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Dirt doesn\'t stand a chance." data-en="Dirt doesn\'t stand a chance.">Dirt doesn\'t stand a chance.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Driveways, roofs and homes" data-en="Driveways, roofs and homes">Driveways, roofs and homes</span><br /><span data-es="cleaned " data-en="cleaned ">cleaned </span><span class="text-shine" data-es="like new" data-en="like new">like new</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="House washing, driveways, sidewalks, roofs, gutters, patios and fences, serving North Miami and the wider Miami-Dade and Broward area. Oscar shows up on time with his own rig and explains the job before any water touches your property, with a 4.6 rating across 28 Google reviews." data-en="House washing, driveways, sidewalks, roofs, gutters, patios and fences, serving North Miami and the wider Miami-Dade and Broward area. Oscar shows up on time with his own rig and explains the job before any water touches your property, with a 4.6 rating across 28 Google reviews.">House washing, driveways, sidewalks, roofs, gutters, patios and fences, serving North Miami and the wider Miami-Dade and Broward area. Oscar shows up on time with his own rig and explains the job before any water touches your property, with a 4.6 rating across 28 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.6 · 28 reviews on Google" data-en="4.6 · 28 reviews on Google">4.6 · 28 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 644-7313" data-en="Call (786) 644-7313">Call (786) 644-7313</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/hero-truck-trailer.jpg" alt="The Florida Pressure Pros truck and trailer rig parked in a North Miami neighborhood" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Available" data-en="Available">Available</p>
            <p class="font-display text-lg">24/7</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Call anytime" data-en="Call anytime">Call anytime</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="28">28</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">House <span class="text-shine">&amp;</span> Roof</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Soft washing" data-en="Soft washing">Soft washing</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">Driveways <span class="text-shine">&amp;</span> Decks</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Pressure cleaning" data-en="Pressure cleaning">Pressure cleaning</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">North Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Miami-Dade &amp; Broward, FL" data-en="Miami-Dade &amp; Broward, FL">Miami-Dade &amp; Broward, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2 bloques, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "House Washing"),
    ("Loc Retwist", "Driveway Cleaning"),
    ("Knotless Braids", "Roof Soft Wash"),
    ("K-Tip Extensions", "Gutter Cleaning"),
    ("Keratin", "Pool Deck &amp; Fences"),
    ("Orlando, FL", "North Miami, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (sin direccion fija -> una sola imagen real, variante adaptada)
# ---------------------------------------------------------------------------
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-1 gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal">
          <img src="assets/raw/equipment-rig.jpg" alt="The Florida Pressure Pros pressure washing trailer rig with hose reels and a gas engine, parked in a driveway" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="One owner," data-en="One owner,">One owner,</span><br /><span class="text-shine" data-es="his own rig, on time" data-en="his own rig, on time">his own rig, on time</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Florida Pressure Pros is run by Oscar, who answers the phone himself, drives his own rig to every job and walks each customer through the process before starting. House washing, driveways, roofs, gutters, pool decks, patios and fences across North Miami and the wider Miami-Dade and Broward area." data-en="Florida Pressure Pros is run by Oscar, who answers the phone himself, drives his own rig to every job and walks each customer through the process before starting. House washing, driveways, roofs, gutters, pool decks, patios and fences across North Miami and the wider Miami-Dade and Broward area.">Florida Pressure Pros is run by Oscar, who answers the phone himself, drives his own rig to every job and walks each customer through the process before starting. House washing, driveways, roofs, gutters, pool decks, patios and fences across North Miami and the wider Miami-Dade and Broward area.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="His customers describe him as reliable, professional and hard working, with results they compare to a brand new surface. The result: a 4.6-star rating across 28 verified Google reviews." data-en="His customers describe him as reliable, professional and hard working, with results they compare to a brand new surface. The result: a 4.6-star rating across 28 verified Google reviews.">His customers describe him as reliable, professional and hard working, with results they compare to a brand new surface. The result: a 4.6-star rating across 28 verified Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="28">28</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Disponible" data-en="Available">Available</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,212,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/raw/hero-truck-trailer.jpg" alt="Florida Pressure Pros" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,212,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Oscar · <span class="text-[color:var(--ink-40)]" data-es="Owner" data-en="Owner">Owner</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Your job, start to finish" data-en="Your job, start to finish">Your job, start to finish</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="How it works" data-en="How it works">How it works</span> <span class="text-shine" data-es="here" data-en="here">here</span></h2>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call Oscar" data-en="Call Oscar">Call Oscar</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text with what needs cleaning, and Oscar calls back to talk through the job and give you a quote." data-en="Call or text with what needs cleaning, and Oscar calls back to talk through the job and give you a quote.">Call or text with what needs cleaning, and Oscar calls back to talk through the job and give you a quote.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Free quote" data-en="Free quote">Free quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Oscar explains the right method for your surface, pressure washing or soft washing, and the price before anything starts." data-en="Oscar explains the right method for your surface, pressure washing or soft washing, and the price before anything starts.">Oscar explains the right method for your surface, pressure washing or soft washing, and the price before anything starts.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Clean, right rig for the job" data-en="Clean, right rig for the job">Clean, right rig for the job</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Oscar brings his trailer rig with the right pressure, nozzle and soft wash mix for the surface, so nothing gets damaged." data-en="Oscar brings his trailer rig with the right pressure, nozzle and soft wash mix for the surface, so nothing gets damaged.">Oscar brings his trailer rig with the right pressure, nozzle and soft wash mix for the surface, so nothing gets damaged.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Like-new results" data-en="Like-new results">Like-new results</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a before and after you can see, and Oscar sticks around until you are happy with the result." data-en="You get a before and after you can see, and Oscar sticks around until you are happy with the result.">You get a before and after you can see, and Oscar sticks around until you are happy with the result.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Pressure &amp; soft washing for" data-en="Pressure &amp; soft washing for">Pressure &amp; soft washing for</span> <span class="text-shine" data-es="every surface" data-en="every surface">every surface</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two properties are the same, so every job gets its own clear quote from Oscar before any water starts moving." data-en="No two properties are the same, so every job gets its own clear quote from Oscar before any water starts moving.">No two properties are the same, so every job gets its own clear quote from Oscar before any water starts moving.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(47,143,212,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="House Washing" data-en="House Washing">House Washing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Soft washing takes mildew, algae and grime off siding and stucco without damaging paint or screens." data-en="Soft washing takes mildew, algae and grime off siding and stucco without damaging paint or screens.">Soft washing takes mildew, algae and grime off siding and stucco without damaging paint or screens.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Like-new concrete" data-en="Like-new concrete">Like-new concrete</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Driveways &amp; Sidewalks" data-en="Driveways &amp; Sidewalks">Driveways &amp; Sidewalks</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Oil stains, mold and built-up dirt lifted off pavers, concrete and brick, restoring the original color." data-en="Oil stains, mold and built-up dirt lifted off pavers, concrete and brick, restoring the original color.">Oil stains, mold and built-up dirt lifted off pavers, concrete and brick, restoring the original color.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Gentle on tile" data-en="Gentle on tile">Gentle on tile</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Roof Soft Washing" data-en="Roof Soft Washing">Roof Soft Washing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Black streaks, moss and lichen removed from tile and shingle roofs with a low-pressure soft wash, no broken tiles." data-en="Black streaks, moss and lichen removed from tile and shingle roofs with a low-pressure soft wash, no broken tiles.">Black streaks, moss and lichen removed from tile and shingle roofs with a low-pressure soft wash, no broken tiles.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Outdoor living" data-en="Outdoor living">Outdoor living</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pool Decks, Patios &amp; Fences" data-en="Pool Decks, Patios &amp; Fences">Pool Decks, Patios &amp; Fences</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pool decks, patios and wood or vinyl fences cleaned and refreshed, including gutter cleaning while the ladder is up." data-en="Pool decks, patios and wood or vinyl fences cleaned and refreshed, including gutter cleaning while the ladder is up.">Pool decks, patios and wood or vinyl fences cleaned and refreshed, including gutter cleaning while the ladder is up.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Exteriors" data-en="Exteriors">Exteriors</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="House &amp; wall soft washing" data-en="House &amp; wall soft washing">House &amp; wall soft washing</li>
            <li class="flex items-center gap-2" data-es="Roof soft washing" data-en="Roof soft washing">Roof soft washing</li>
            <li class="flex items-center gap-2" data-es="Gutter cleaning" data-en="Gutter cleaning">Gutter cleaning</li>
            <li class="flex items-center gap-2" data-es="Window &amp; screen rinse" data-en="Window &amp; screen rinse">Window &amp; screen rinse</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Concrete &amp; Pavers" data-en="Concrete &amp; Pavers">Concrete &amp; Pavers</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Driveway cleaning" data-en="Driveway cleaning">Driveway cleaning</li>
            <li class="flex items-center gap-2" data-es="Sidewalk cleaning" data-en="Sidewalk cleaning">Sidewalk cleaning</li>
            <li class="flex items-center gap-2" data-es="Paver &amp; brick restoration" data-en="Paver &amp; brick restoration">Paver &amp; brick restoration</li>
            <li class="flex items-center gap-2" data-es="Stain &amp; rust removal" data-en="Stain &amp; rust removal">Stain &amp; rust removal</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Outdoor Living" data-en="Outdoor Living">Outdoor Living</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Pool deck cleaning" data-en="Pool deck cleaning">Pool deck cleaning</li>
            <li class="flex items-center gap-2" data-es="Patio cleaning" data-en="Patio cleaning">Patio cleaning</li>
            <li class="flex items-center gap-2" data-es="Fence cleaning" data-en="Fence cleaning">Fence cleaning</li>
            <li class="flex items-center gap-2" data-es="Free estimates" data-en="Free estimates">Free estimates</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on size, access and the surface. Call (786) 644-7313 for a free quote, 24/7." data-en="Pricing depends on size, access and the surface. Call (786) 644-7313 for a free quote, 24/7.">Pricing depends on size, access and the surface. Call (786) 644-7313 for a free quote, 24/7.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="work" data-en="work">work</span>')
rep('''<a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (786) 644-7313
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="El equipo de Florida Pressure Pros" data-en="The Florida Pressure Pros rig">The Florida Pressure Pros rig</span><img src="assets/raw/hero-truck-trailer.jpg" alt="The Florida Pressure Pros branded truck and pressure washing trailer parked on a North Miami street" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Camino de ladrillo, antes y despues" data-en="Brick walkway, before &amp; after">Brick walkway, before &amp; after</span><img src="assets/raw/before-after-walkway.jpg" alt="A brick walkway before and after pressure washing, going from stained and dark to bright red brick" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Techo de teja, antes y despues" data-en="Tile roof, before &amp; after">Tile roof, before &amp; after</span><img src="assets/raw/before-after-roof.jpg" alt="A tile roof before and after a soft wash, going from covered in moss and leaves to clean orange tile" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Mancha removida de un patio" data-en="Stain lifted off a patio">Stain lifted off a patio</span><img src="assets/raw/before-after-stain.jpg" alt="A dark stain on a tile patio before and after cleaning, completely removed" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Limpiando una acera" data-en="Cleaning a sidewalk">Cleaning a sidewalk</span><img src="assets/raw/action-sidewalk.jpg" alt="A freshly pressure washed sidewalk in a North Miami neighborhood with the Florida Pressure Pros truck parked nearby" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. MARQUEE REVERSE: ya cubierto en el paso 9 (expect=4 incluye ambos bloques)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What North Miami" data-en="What North Miami">What North Miami</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.6 out of 5 · 28 reviews on Google" data-en="4.6 out of 5 · 28 reviews on Google">4.6 out of 5 · 28 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"It was a pleasure to have Oscar working on my house. He was very professional, knew what he was doing and put a lot of effort into getting the job well done. He is highly recommended if you want your sidewalk and driveway look like new."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Guli</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Oscar had great communication throughout the process, was timely and efficient. I couldn't believe the results on my pool patio it was incredible. I cant say enough great things about his services and will definitely be using again soon!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Aimee Jones</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Oscar did a fantastic job and we will be using him again soon. Oscar was very professional and explained exactly the process to achieve the best outcome. Highly recommended."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jerry Tilley</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 28 reviews on Google" data-en="Read all 28 reviews on Google">Read all 28 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION -> COBERTURA (sin direccion fija: foto real en vez de mapa)
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Service area" data-en="Service area">Service area</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">North Miami</span></h2>')
rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,212,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Coverage" data-en="Coverage">Coverage</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mobile service based in North Miami, covering Miami-Dade and Broward County, FL." data-en="Mobile service based in North Miami, covering Miami-Dade and Broward County, FL.">Mobile service based in North Miami, covering Miami-Dade and Broward County, FL.</p>
            </div>
          </div>''')
rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,212,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open 24 hours, every day of the week. Call or text anytime for a free quote." data-en="Open 24 hours, every day of the week. Call or text anytime for a free quote.">Open 24 hours, every day of the week. Call or text anytime for a free quote.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,212,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 644-7313" data-en="Call (786) 644-7313">Call (786) 644-7313</a>
            </div>
          </div>''')
rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,212,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reviews" data-en="Reviews">Reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.6 stars across 28 verified Google reviews." data-en="4.6 stars across 28 verified Google reviews.">4.6 stars across 28 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,212,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame zoomable reveal min-h-[380px] aspect-[4/5] lg:aspect-auto" style="transition-delay:180ms">
        <img src="assets/raw/action-gutter.jpg" alt="Oscar from Florida Pressure Pros cleaning out a gutter from a ladder on a tile roof" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Dirt doesn\'t stand a chance." data-en="Dirt doesn\'t stand a chance.">Dirt doesn\'t stand a chance.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call to" data-en="One call to">One call to</span> <span class="text-shine" data-es="Oscar" data-en="Oscar">Oscar</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (786) 644-7313 for a free quote on your house, driveway, roof or pool deck. Open 24 hours, every day." data-en="Call (786) 644-7313 for a free quote on your house, driveway, roof or pool deck. Open 24 hours, every day.">Call (786) 644-7313 for a free quote on your house, driveway, roof or pool deck. Open 24 hours, every day.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 644-7313" data-en="Call (786) 644-7313">Call (786) 644-7313</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Florida Pressure Pros</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(120,185,230,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/raw/hero-truck-trailer.jpg" alt="Florida Pressure Pros" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(120,185,230,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Florida Pressure Pros</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Mobile pressure washing serving North Miami, Miami-Dade and Broward, FL." data-en="Mobile pressure washing serving North Miami, Miami-Dade and Broward, FL.">Mobile pressure washing serving North Miami, Miami-Dade and Broward, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#a8d4f0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="North Miami, FL (mobile, no fixed address)" data-en="North Miami, FL (mobile, no fixed address)">North Miami, FL (mobile, no fixed address)</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#a8d4f0]" data-es="Call (786) 644-7313" data-en="Call (786) 644-7313">Call (786) 644-7313</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a8d4f0]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a8d4f0]">4.6 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Florida Pressure Pros.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Florida Pressure Pros">')
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
    "North Miami, FL · Mobile Pressure Washing": "North Miami, FL · Lavado a Presion Movil",
    "Dirt doesn't stand a chance.": "La suciedad no tiene oportunidad.",
    "Driveways, roofs and homes": "Entradas, techos y casas",
    "cleaned ": "limpiados ",
    "like new": "como nuevos",
    "House washing, driveways, sidewalks, roofs, gutters, patios and fences, serving North Miami and the wider Miami-Dade and Broward area. Oscar shows up on time with his own rig and explains the job before any water touches your property, with a 4.6 rating across 28 Google reviews.":
        "Lavado de casas, entradas, aceras, techos, canaletas, patios y cercas, sirviendo a North Miami y toda el area de Miami-Dade y Broward. Oscar llega puntual con su propio equipo y explica el trabajo antes de que toque el agua tu propiedad, con calificacion de 4.6 en 28 resenas de Google.",
    "4.6 · 28 reviews on Google": "4.6 · 28 resenas en Google",
    "Call (786) 644-7313": "Llama al (786) 644-7313",
    "Available": "Disponible",
    "Call anytime": "Llama cuando quieras",
    "Soft washing": "Lavado suave",
    "Pressure cleaning": "Lavado a presion",
    "Miami-Dade &amp; Broward, FL": "Miami-Dade y Broward, FL",
    "One owner,": "Un dueno,",
    "his own rig, on time": "su propio equipo, a tiempo",
    "Florida Pressure Pros is run by Oscar, who answers the phone himself, drives his own rig to every job and walks each customer through the process before starting. House washing, driveways, roofs, gutters, pool decks, patios and fences across North Miami and the wider Miami-Dade and Broward area.":
        "Florida Pressure Pros es dirigido por Oscar, quien contesta el telefono personalmente, maneja su propio equipo a cada trabajo y explica el proceso a cada cliente antes de empezar. Lavado de casas, entradas, techos, canaletas, terrazas de piscina, patios y cercas en North Miami y toda el area de Miami-Dade y Broward.",
    "His customers describe him as reliable, professional and hard working, with results they compare to a brand new surface. The result: a 4.6-star rating across 28 verified Google reviews.":
        "Sus clientes lo describen como confiable, profesional y trabajador, con resultados que comparan con una superficie completamente nueva. El resultado: calificacion de 4.6 estrellas en 28 resenas verificadas de Google.",
    "Owner": "Dueno",
    "Your job, start to finish": "Tu trabajo, de inicio a fin",
    "How it works": "Asi se trabaja",
    "here": "aqui",
    "Call Oscar": "Llama a Oscar",
    "Call or text with what needs cleaning, and Oscar calls back to talk through the job and give you a quote.":
        "Llama o envia un mensaje con lo que necesita limpieza, y Oscar regresa la llamada para hablar del trabajo y darte una cotizacion.",
    "Free quote": "Cotizacion gratis",
    "Oscar explains the right method for your surface, pressure washing or soft washing, and the price before anything starts.":
        "Oscar explica el metodo correcto para tu superficie, lavado a presion o lavado suave, y el precio antes de empezar.",
    "Clean, right rig for the job": "Equipo limpio y correcto para el trabajo",
    "Oscar brings his trailer rig with the right pressure, nozzle and soft wash mix for the surface, so nothing gets damaged.":
        "Oscar trae su remolque equipado con la presion, boquilla y mezcla de lavado suave correcta para la superficie, para que nada se dane.",
    "Like-new results": "Resultados como nuevos",
    "You get a before and after you can see, and Oscar sticks around until you are happy with the result.":
        "Obtienes un antes y despues que puedes ver, y Oscar se queda hasta que estes contento con el resultado.",
    "Pressure &amp; soft washing for": "Lavado a presion y suave para",
    "every surface": "cada superficie",
    "No two properties are the same, so every job gets its own clear quote from Oscar before any water starts moving.":
        "Ninguna propiedad es igual a otra, asi que cada trabajo recibe su propia cotizacion clara de Oscar antes de que el agua empiece a correr.",
    "Most requested": "Lo mas solicitado",
    "House Washing": "Lavado de Casas",
    "Soft washing takes mildew, algae and grime off siding and stucco without damaging paint or screens.":
        "El lavado suave quita moho, algas y mugre del revestimiento y estuco sin danar la pintura ni las mallas.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Like-new concrete": "Concreto como nuevo",
    "Driveways &amp; Sidewalks": "Entradas y Aceras",
    "Oil stains, mold and built-up dirt lifted off pavers, concrete and brick, restoring the original color.":
        "Manchas de aceite, moho y suciedad acumulada se eliminan de adoquines, concreto y ladrillo, restaurando el color original.",
    "Gentle on tile": "Suave con la teja",
    "Roof Soft Washing": "Lavado Suave de Techos",
    "Black streaks, moss and lichen removed from tile and shingle roofs with a low-pressure soft wash, no broken tiles.":
        "Rayas negras, musgo y liquen se eliminan de techos de teja y tejamanil con un lavado suave de baja presion, sin romper tejas.",
    "Outdoor living": "Vida al aire libre",
    "Pool Decks, Patios &amp; Fences": "Terrazas de Piscina, Patios y Cercas",
    "Pool decks, patios and wood or vinyl fences cleaned and refreshed, including gutter cleaning while the ladder is up.":
        "Terrazas de piscina, patios y cercas de madera o vinilo se limpian y refrescan, incluyendo limpieza de canaletas mientras la escalera esta puesta.",
    "Exteriors": "Exteriores",
    "House &amp; wall soft washing": "Lavado suave de casa y paredes",
    "Roof soft washing": "Lavado suave de techo",
    "Gutter cleaning": "Limpieza de canaletas",
    "Window &amp; screen rinse": "Enjuague de ventanas y mallas",
    "Concrete &amp; Pavers": "Concreto y Adoquines",
    "Driveway cleaning": "Limpieza de entradas",
    "Sidewalk cleaning": "Limpieza de aceras",
    "Paver &amp; brick restoration": "Restauracion de adoquines y ladrillo",
    "Stain &amp; rust removal": "Remocion de manchas y oxido",
    "Outdoor Living": "Vida al Aire Libre",
    "Pool deck cleaning": "Limpieza de terraza de piscina",
    "Patio cleaning": "Limpieza de patio",
    "Fence cleaning": "Limpieza de cercas",
    "Free estimates": "Cotizaciones gratis",
    "Pricing depends on size, access and the surface. Call (786) 644-7313 for a free quote, 24/7.":
        "El precio depende del tamano, el acceso y la superficie. Llama al (786) 644-7313 para una cotizacion gratis, 24/7.",
    "Real": "Trabajo",
    "work": "real",
    "What North Miami": "Lo que dicen los",
    "customers say": "clientes en North Miami",
    "Read all 28 reviews on Google": "Lee las 28 resenas en Google",
    "Service area": "Area de servicio",
    "Serving": "Sirviendo a",
    "Coverage": "Cobertura",
    "Mobile service based in North Miami, covering Miami-Dade and Broward County, FL.":
        "Servicio movil con base en North Miami, cubriendo el condado de Miami-Dade y Broward, FL.",
    "Hours": "Horario",
    "Open 24 hours, every day of the week. Call or text anytime for a free quote.":
        "Abierto 24 horas, todos los dias de la semana. Llama o envia un mensaje cuando quieras para una cotizacion gratis.",
    "Reviews": "Resenas",
    "4.6 stars across 28 verified Google reviews.": "4.6 estrellas en 28 resenas verificadas de Google.",
    "One call to": "Una llamada a",
    "Oscar": "Oscar",
    "Call (786) 644-7313 for a free quote on your house, driveway, roof or pool deck. Open 24 hours, every day.":
        "Llama al (786) 644-7313 para una cotizacion gratis de tu casa, entrada, techo o terraza de piscina. Abierto 24 horas, todos los dias.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Mobile pressure washing serving North Miami, Miami-Dade and Broward, FL.": "Lavado a presion movil sirviendo a North Miami, Miami-Dade y Broward, FL.",
    "Contact": "Contacto",
    "North Miami, FL (mobile, no fixed address)": "North Miami, FL (movil, sin direccion fija)",
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
