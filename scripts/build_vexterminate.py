import re
import shutil

SLUG = "vexterminate"
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


NEW_TEL = "tel:+17865478185"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Vex.Terminate+Inc+Miami+FL+reviews"
NEW_REVIEWS_LABEL = "Google Reviews"
NEW_IG_URL = "https://www.instagram.com/vex.terminateinc/"
NEW_IG_HANDLE = "@vex.terminateinc"
NEW_ADDR = "3015 NW 57th St, Miami, FL 33142"
NEW_MAPS = "https://www.google.com/maps?q=3015+NW+57th+St,+Miami,+FL+33142"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: oro (Pure Artistry) -> naranja vivo (Vex.Terminate, su rotulacion real)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#6b5222", "#7a3a0a"),
    ("#d4a84b", "#e8730f"),
    ("#1c1408", "#1a0f05"),
    ("#e9c3ab", "#f2b98a"),
    ("#8a744a", "#8a4f1f"),
    ("#f5efe3", "#f7ede0"),
    ("#f0dc9e", "#f7c583"),
    ("#e8cf96", "#f0c68a"),
    ("#e8c476", "#f5a438"),
    ("#e5c374", "#f2a030"),
    ("#c9a04a", "#e8800f"),
    ("#9a7431", "#8a4a12"),
    ("#96742c", "#8a4710"),
    ("#0f0b07", "#120a05"),
    ("#fbf6ea", "#fbf0e3"),
    ("#faf1dc", "#fbead6"),
    ("#f8eed3", "#f8e0c4"),
    ("#f0dcae", "#f5c58a"),
    ("#ecd9a8", "#f0b87a"),
    ("#c9ab6b", "#cf8a42"),
    ("#bfa060", "#cf8a42"),
    ("#b8934a", "#c97d1f"),
    ("#241c0e", "#241306"),
    ("#191307", "#1f1206"),
    ("#171207", "#1c1106"),
    ("#100c05", "#150d05"),
    ("#0c0905", "#120b05"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(232,115,15"),
    ("rgba(232,207,150", "rgba(242,185,138"),
    ("rgba(185,138,128", "rgba(242,160,110"),
    ("rgba(180,140,60", "rgba(232,128,15"),
    ("rgba(122,90,30", "rgba(138,74,18"),
    ("rgba(80,58,18", "rgba(30,18,8"),
    ("rgba(110,85,35", "rgba(30,18,8"),
    ("rgba(54,42,38", "rgba(40,24,14"),
    ("rgba(15,11,7", "rgba(18,10,5"),
    ("rgba(245,239,227", "rgba(247,236,222"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel:. Si hay IG real (si la hay) se
#    mantiene como segundo CTA tal cual el esqueleto.
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
c = h.count(OLD_IG_URL)
assert c == 6, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
c = h.count(OLD_IG_HANDLE)
assert c == 4, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Vex.Terminate · Termite Tenting &amp; Fumigation in Miami, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Vex.Terminate Inc, Miami FL: termite tent fumigation, spot treatment and preventive termite services for homes and boats. 5.0 stars across 18 Google reviews." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Vex.Terminate · Termite Tenting &amp; Fumigation in Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Tent fumigation, spot treatment and preventive termite service for homes and boats. 5.0 on Google with 18 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/g0.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/g0.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Vex.Terminate Inc",
    "description": "Termite company in Miami, FL: whole-structure tent fumigation, spot treatment and preventive termite service for homes and boats.",
    "address": { "@type": "PostalAddress", "streetAddress": "3015 NW 57th St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33142", "addressCountry": "US" },
    "telephone": "+1-786-547-8185",
    "sameAs": ["https://www.instagram.com/vex.terminateinc/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "18", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Termite services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Tent Fumigation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Spot Treatment" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Preventive Services" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Boat &amp; Marine Tenting" } }
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
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(232,115,15,0.35)]" />',
    '<img src="assets/raw/g9.jpg" alt="Vex.Terminate Inc" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(232,115,15,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Vex.<span class="text-[color:var(--accent-deep)]">Terminate</span></span>')
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">V.</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Vex.Terminate</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miami, FL · Termite Tenting &amp; Fumigation" data-en="Miami, FL · Termite Tenting &amp; Fumigation">Miami, FL · Termite Tenting &amp; Fumigation</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Tenting done right, every time." data-en="Tenting done right, every time.">Tenting done right, every time.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Whole-home tenting," data-en="Whole-home tenting,">Whole-home tenting,</span><br /><span data-es="spot treatment and " data-en="spot treatment and ">spot treatment and </span><span class="text-shine" data-es="prevention" data-en="prevention">prevention</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Vex.Terminate handles full tent fumigation, spot termite treatment and preventive service for homes, and even boats, across Miami. Juan and the team walk through the process before anything starts, with a perfect 5.0 across 18 Google reviews." data-en="Vex.Terminate handles full tent fumigation, spot termite treatment and preventive service for homes, and even boats, across Miami. Juan and the team walk through the process before anything starts, with a perfect 5.0 across 18 Google reviews.">Vex.Terminate handles full tent fumigation, spot termite treatment and preventive service for homes, and even boats, across Miami. Juan and the team walk through the process before anything starts, with a perfect 5.0 across 18 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 18 reviews on Google" data-en="5.0 · 18 reviews on Google">5.0 · 18 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 547-8185" data-en="Call (786) 547-8185">Call (786) 547-8185</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/g0.jpg" alt="A home fully tented for termite fumigation under a clear Miami sky" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Hours" data-en="Hours">Hours</p>
            <p class="font-display text-lg">Mon-Fri 8:30-5</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Call or text anytime" data-en="Call or text anytime">Call or text anytime</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="18">18</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Tent <span class="text-shine">&amp;</span> Spot</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Fumigation · Treatment" data-en="Fumigation · Treatment">Fumigation · Treatment</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Homes <span class="text-shine">&amp;</span> Boats</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Tenting de ambos" data-en="Tenting both">Tenting both</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">3015 NW 57th St</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Tent Fumigation"),
    ("Loc Retwist", "Spot Treatment"),
    ("Knotless Braids", "Preventive Service"),
    ("K-Tip Extensions", "Termite Control"),
    ("Keratin", "Boat Tenting"),
    ("Orlando, FL", "Miami, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/g2.jpg" alt="A boat tented for termite fumigation inside a boatyard in Miami" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/g3.jpg" alt="A boat tented for fumigation at the dock with other boats nearby" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="One company," data-en="One company,">One company,</span><br /><span class="text-shine" data-es="homes and boats alike" data-en="homes and boats alike">homes and boats alike</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Vex.Terminate Inc is a Miami termite company built around tent fumigation, spot treatment and preventive service. Juan walks every customer through the tenting process and the products used before the crew shows up, for houses and for boats tented right at the marina." data-en="Vex.Terminate Inc is a Miami termite company built around tent fumigation, spot treatment and preventive service. Juan walks every customer through the tenting process and the products used before the crew shows up, for houses and for boats tented right at the marina.">Vex.Terminate Inc is a Miami termite company built around tent fumigation, spot treatment and preventive service. Juan walks every customer through the tenting process and the products used before the crew shows up, for houses and for boats tented right at the marina.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Customers describe the team as knowledgeable, friendly and easy to reach by phone or text through the whole job. The result: a perfect 5.0 across 18 Google reviews." data-en="Customers describe the team as knowledgeable, friendly and easy to reach by phone or text through the whole job. The result: a perfect 5.0 across 18 Google reviews.">Customers describe the team as knowledgeable, friendly and easy to reach by phone or text through the whole job. The result: a perfect 5.0 across 18 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="18">18</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">100%</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Tentado correctamente" data-en="Tented right">Tented right</p></div>''')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(232,115,15,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
    '''<img src="assets/raw/g9.jpg" alt="Vex.Terminate Inc" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(232,115,15,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Juan · <span class="text-[color:var(--ink-40)]" data-es="Lead Technician" data-en="Lead Technician">Lead Technician</span></span>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="How a job" data-en="How a job">How a job</span> <span class="text-shine" data-es="gets done" data-en="gets done">gets done</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or text" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text (786) 547-8185 with the termite or pest problem, and Juan walks you through next steps." data-en="Call or text (786) 547-8185 with the termite or pest problem, and Juan walks you through next steps.">Call or text (786) 547-8185 with the termite or pest problem, and Juan walks you through next steps.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Free inspection" data-en="Free inspection">Free inspection</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A technician checks the structure, or the boat, and explains exactly what tenting or treatment the job needs before any price is set." data-en="A technician checks the structure, or the boat, and explains exactly what tenting or treatment the job needs before any price is set.">A technician checks the structure, or the boat, and explains exactly what tenting or treatment the job needs before any price is set.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Tenting day" data-en="Tenting day">Tenting day</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The structure gets sealed and tented, or spot-treated, with clear instructions on what to do while the crew works." data-en="The structure gets sealed and tented, or spot-treated, with clear instructions on what to do while the crew works.">The structure gets sealed and tented, or spot-treated, with clear instructions on what to do while the crew works.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="All clear" data-en="All clear">All clear</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Once the tent comes down, Vex.Terminate confirms everything is clear and sets up preventive service if you want ongoing protection." data-en="Once the tent comes down, Vex.Terminate confirms everything is clear and sets up preventive service if you want ongoing protection.">Once the tent comes down, Vex.Terminate confirms everything is clear and sets up preventive service if you want ongoing protection.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Termite problems," data-en="Termite problems,">Termite problems,</span> <span class="text-shine" data-es="handled" data-en="handled">handled</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every structure is different, so Vex.Terminate gives a clear quote before any tenting or treatment starts." data-en="Every structure is different, so Vex.Terminate gives a clear quote before any tenting or treatment starts.">Every structure is different, so Vex.Terminate gives a clear quote before any tenting or treatment starts.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(232,115,15,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tent Fumigation" data-en="Tent Fumigation">Tent Fumigation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full structure tenting for drywood termites, sealed and monitored from start to finish, for houses and other structures." data-en="Full structure tenting for drywood termites, sealed and monitored from start to finish, for houses and other structures.">Full structure tenting for drywood termites, sealed and monitored from start to finish, for houses and other structures.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Targeted" data-en="Targeted">Targeted</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Spot Treatment" data-en="Spot Treatment">Spot Treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Localized termite treatment for smaller, contained infestations that do not need a full tent." data-en="Localized termite treatment for smaller, contained infestations that do not need a full tent.">Localized termite treatment for smaller, contained infestations that do not need a full tent.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Ongoing" data-en="Ongoing">Ongoing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Preventive Services" data-en="Preventive Services">Preventive Services</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Scheduled termite prevention to catch activity early and keep it from turning into a full tenting job." data-en="Scheduled termite prevention to catch activity early and keep it from turning into a full tenting job.">Scheduled termite prevention to catch activity early and keep it from turning into a full tenting job.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Specialty" data-en="Specialty">Specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Boat &amp; Marine Tenting" data-en="Boat &amp; Marine Tenting">Boat &amp; Marine Tenting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Termite and pest tenting for boats at the marina, the same careful process used on homes." data-en="Termite and pest tenting for boats at the marina, the same careful process used on homes.">Termite and pest tenting for boats at the marina, the same careful process used on homes.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on the structure and the problem. Call or text (786) 547-8185 for a free quote." data-en="Pricing depends on the structure and the problem. Call or text (786) 547-8185 for a free quote.">Pricing depends on the structure and the problem. Call or text (786) 547-8185 for a free quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="tenting jobs" data-en="tenting jobs">tenting jobs</span>')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Whole-home tenting" data-en="Whole-home tenting">Whole-home tenting</span><img src="assets/raw/g0.jpg" alt="A home fully tented for termite fumigation under a clear Miami sky" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Boat tenting at the marina" data-en="Boat tenting at the marina">Boat tenting at the marina</span><img src="assets/raw/g3.jpg" alt="A boat tented for termite fumigation at the dock" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Marina tenting" data-en="Marina tenting">Marina tenting</span><img src="assets/raw/g5.jpg" alt="A boat tented at the marina with other boats nearby" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Night tenting" data-en="Night tenting">Night tenting</span><img src="assets/raw/g7.jpg" alt="A home tent lit up at night during an overnight fumigation" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Backyard tenting" data-en="Backyard tenting">Backyard tenting</span><img src="assets/raw/g8.jpg" alt="A house tented for termite fumigation seen from the backyard" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Hedge-lined tenting" data-en="Hedge-lined tenting">Hedge-lined tenting</span><img src="assets/raw/g10.jpg" alt="A home tented for fumigation with hedges trimmed around the base" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What Miami" data-en="What Miami">What Miami</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 18 verified reviews on Google" data-en="5.0 out of 5 · 18 verified reviews on Google">5.0 out of 5 · 18 verified reviews on Google</span></p>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great service. John took his time inspecting my home, was informative about the tenting procedure, and was easy to reach by phone or text. Highly recommend."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Bertha Vazquez</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great communication from beginning to end. Couldn't be happier with the overall experience and the care that the team took to walk us through the process from beginning to end. Would recommend them to anyone and everyone without any hesitation."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lourdes Di Muont</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"From the beginning it was evident that Juan is extremely knowledgeable about the entire tenting process, the products used, and all the creepy crawlies that would be treated. That along with his kindness made choosing Vex and easy decision…"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily M</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 18 reviews on Google" data-en="Read all 18 reviews on Google">Read all 18 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION (direccion real disponible, con mapa)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Miami</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(232,115,15,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + NEW_ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(232,115,15,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(232,115,15,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Friday, 8:30 AM to 5 PM. Closed Saturday and Sunday." data-en="Monday to Friday, 8:30 AM to 5 PM. Closed Saturday and Sunday.">Monday to Friday, 8:30 AM to 5 PM. Closed Saturday and Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(232,115,15,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 547-8185" data-en="Call (786) 547-8185">Call (786) 547-8185</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(232,115,15,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See the latest tenting jobs and DM any questions before you call." data-en="See the latest tenting jobs and DM any questions before you call.">See the latest tenting jobs and DM any questions before you call.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(232,115,15,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Vex.Terminate Inc, 3015 NW 57th St, Miami FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tenting done right, every time." data-en="Tenting done right, every time.">Tenting done right, every time.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call to" data-en="One call to">One call to</span> <span class="text-shine" data-es="Vex" data-en="Vex">Vex</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call or text (786) 547-8185 for a free quote on tent fumigation, spot treatment or preventive service, for your home or your boat." data-en="Call or text (786) 547-8185 for a free quote on tent fumigation, spot treatment or preventive service, for your home or your boat.">Call or text (786) 547-8185 for a free quote on tent fumigation, spot treatment or preventive service, for your home or your boat.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 547-8185" data-en="Call (786) 547-8185">Call (786) 547-8185</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Vex.Terminate</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(242,185,138,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/raw/g9.jpg" alt="Vex.Terminate Inc" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(242,185,138,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Vex.Terminate</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Termite tenting, spot treatment and preventive service for homes and boats in Miami, FL." data-en="Termite tenting, spot treatment and preventive service for homes and boats in Miami, FL.">Termite tenting, spot treatment and preventive service for homes and boats in Miami, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#f2b98a]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#f2b98a]" data-es="Call (786) 547-8185" data-en="Call (786) 547-8185">Call (786) 547-8185</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f2b98a]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f2b98a]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Vex.Terminate Inc.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Vex.Terminate Inc">')
rep('<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span class="book-float-label" data-es="Call now" data-en="Call now">Call now</span>')
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
    "Miami, FL · Termite Tenting &amp; Fumigation": "Miami, FL · Entoldado y Fumigacion de Termitas",
    "Tenting done right, every time.": "Entoldado bien hecho, siempre.",
    "Whole-home tenting,": "Entoldado completo de la casa,",
    "spot treatment and ": "tratamiento localizado y ",
    "prevention": "prevencion",
    "Vex.Terminate handles full tent fumigation, spot termite treatment and preventive service for homes, and even boats, across Miami. Juan and the team walk through the process before anything starts, with a perfect 5.0 across 18 Google reviews.":
        "Vex.Terminate hace fumigacion completa con entoldado, tratamiento localizado de termitas y servicio preventivo para casas, e incluso botes, en todo Miami. Juan y el equipo explican el proceso antes de empezar, con un 5.0 perfecto en 18 resenas de Google.",
    "5.0 · 18 reviews on Google": "5.0 · 18 resenas en Google",
    "Call (786) 547-8185": "Llama al (786) 547-8185",
    "Hours": "Horario",
    "Call or text anytime": "Llama o escribe cuando quieras",
    "Fumigation · Treatment": "Fumigacion · Tratamiento",
    "How a job": "Como se hace",
    "gets done": "el trabajo",
    "One company,": "Una empresa,",
    "homes and boats alike": "casas y botes por igual",
    "Vex.Terminate Inc is a Miami termite company built around tent fumigation, spot treatment and preventive service. Juan walks every customer through the tenting process and the products used before the crew shows up, for houses and for boats tented right at the marina.":
        "Vex.Terminate Inc es una empresa de termitas en Miami enfocada en fumigacion con entoldado, tratamiento localizado y servicio preventivo. Juan explica a cada cliente el proceso de entoldado y los productos usados antes de que llegue el equipo, tanto para casas como para botes entoldados en la marina.",
    "Customers describe the team as knowledgeable, friendly and easy to reach by phone or text through the whole job. The result: a perfect 5.0 across 18 Google reviews.":
        "Los clientes describen al equipo como conocedor, amable y facil de contactar por telefono o mensaje durante todo el trabajo. El resultado: un 5.0 perfecto en 18 resenas de Google.",
    "Lead Technician": "Tecnico principal",
    "Call or text (786) 547-8185 with the termite or pest problem, and Juan walks you through next steps.":
        "Llama o escribe al (786) 547-8185 con el problema de termitas o plagas, y Juan te explica los siguientes pasos.",
    "Free inspection": "Inspeccion gratis",
    "A technician checks the structure, or the boat, and explains exactly what tenting or treatment the job needs before any price is set.":
        "Un tecnico revisa la estructura, o el bote, y explica exactamente que entoldado o tratamiento necesita el trabajo antes de fijar un precio.",
    "Tenting day": "Dia del entoldado",
    "The structure gets sealed and tented, or spot-treated, with clear instructions on what to do while the crew works.":
        "La estructura se sella y se entolda, o se trata localmente, con instrucciones claras de que hacer mientras trabaja el equipo.",
    "All clear": "Todo despejado",
    "Once the tent comes down, Vex.Terminate confirms everything is clear and sets up preventive service if you want ongoing protection.":
        "Cuando se retira la lona, Vex.Terminate confirma que todo esta despejado y arma un plan de servicio preventivo si quieres proteccion continua.",
    "Termite problems,": "Problemas de termitas,",
    "handled": "resueltos",
    "Every structure is different, so Vex.Terminate gives a clear quote before any tenting or treatment starts.":
        "Cada estructura es diferente, asi que Vex.Terminate da una cotizacion clara antes de empezar cualquier entoldado o tratamiento.",
    "Most requested": "Lo mas solicitado",
    "Tent Fumigation": "Fumigacion con Entoldado",
    "Full structure tenting for drywood termites, sealed and monitored from start to finish, for houses and other structures.":
        "Entoldado completo de la estructura para termitas de madera seca, sellado y monitoreado de principio a fin, para casas y otras estructuras.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Targeted": "Localizado",
    "Spot Treatment": "Tratamiento Localizado",
    "Localized termite treatment for smaller, contained infestations that do not need a full tent.":
        "Tratamiento localizado de termitas para infestaciones mas pequenas y contenidas que no necesitan un entoldado completo.",
    "Ongoing": "Continuo",
    "Preventive Services": "Servicios Preventivos",
    "Scheduled termite prevention to catch activity early and keep it from turning into a full tenting job.":
        "Prevencion programada de termitas para detectar actividad temprano y evitar que se convierta en un trabajo de entoldado completo.",
    "Specialty": "Especialidad",
    "Boat &amp; Marine Tenting": "Entoldado de Botes y Embarcaciones",
    "Termite and pest tenting for boats at the marina, the same careful process used on homes.":
        "Entoldado contra termitas y plagas para botes en la marina, el mismo proceso cuidadoso que se usa en casas.",
    "Pricing depends on the structure and the problem. Call or text (786) 547-8185 for a free quote.":
        "El precio depende de la estructura y el problema. Llama o escribe al (786) 547-8185 para una cotizacion gratis.",
    "Real": "Trabajo",
    "tenting jobs": "real de entoldado",
    "What Miami": "Lo que dicen los",
    "customers say": "clientes en Miami",
    "5.0 out of 5 · 18 verified reviews on Google": "5.0 de 5 · 18 resenas verificadas en Google",
    "Read all 18 reviews on Google": "Lee las 18 resenas en Google",
    "Serving": "Sirviendo a",
    "Address": "Direccion",
    "Monday to Friday, 8:30 AM to 5 PM. Closed Saturday and Sunday.": "Lunes a viernes, 8:30 AM a 5 PM. Cerrado sabado y domingo.",
    "See the latest tenting jobs and DM any questions before you call.": "Mira los trabajos de entoldado mas recientes y escribe por DM cualquier duda antes de llamar.",
    "One call to": "Una llamada a",
    "Vex": "Vex",
    "Call or text (786) 547-8185 for a free quote on tent fumigation, spot treatment or preventive service, for your home or your boat.":
        "Llama o escribe al (786) 547-8185 para una cotizacion gratis de fumigacion con entoldado, tratamiento localizado o servicio preventivo, para tu casa o tu bote.",
    "Follow on Instagram": "Seguir en Instagram",
    "Termite tenting, spot treatment and preventive service for homes and boats in Miami, FL.": "Entoldado de termitas, tratamiento localizado y servicio preventivo para casas y botes en Miami, FL.",
    "Contact": "Contacto",
    "Follow": "Seguir",
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
