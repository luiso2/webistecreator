import re
import shutil

SLUG = "flobugspestcontrol"
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


NEW_TEL = "tel:+17862839911"
NEW_REVIEWS_URL = "https://www.google.com/search?q=Flo-Bugs+Pest+Control+Miami+FL+reviews"
NEW_REVIEWS_LABEL = "Google Reviews"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> rojo/garnet (Flo-Bugs, su rotulacion real)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#c23b2e"),
    ("#5c2140", "#7a2018"),
    ("#f0bed7", "#f0a89a"),
    ("#faf2f6", "#faf1ec"),
    ("#c47a9c", "#d9705d"),
    ("#8a5573", "#8a4332"),
    ("#f3e0ea", "#f3ddd2"),
    ("#d9a8c2", "#d9a08f"),
    ("#7d3457", "#7d2e1f"),
    ("#5f2c48", "#5f2317"),
    ("#33222c", "#2a211c"),
    ("#fbf3f8", "#fbf1ec"),
    ("#fbeff5", "#fbede6"),
    ("#f8dfeb", "#f8ded0"),
    ("#f6f1ea", "#f6ede6"),
    ("#f2d5e3", "#f2d8cb"),
    ("#f2cfe0", "#f2d0bd"),
    ("#efd0e0", "#efd2c0"),
    ("#e5c1d4", "#e5c3b0"),
    ("#dc9dbe", "#dc9d82"),
    ("#d3a2bc", "#d3a28a"),
    ("#c9789f", "#c97d60"),
    ("#b25a85", "#b25a3e"),
    ("#2a1722", "#241611"),
    ("#1f0f18", "#1a0f0b"),
    ("#1c0f16", "#180f0b"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(194,59,46"),
    ("rgba(51,34,44", "rgba(42,33,28"),
    ("rgba(240,190,215", "rgba(240,168,154"),
    ("rgba(70,25,50", "rgba(90,35,25"),
    ("rgba(250,242,246", "rgba(250,241,236"),
    ("rgba(125,52,87", "rgba(125,66,50"),
    ("rgba(253,246,250", "rgba(253,246,242"),
    ("rgba(40,16,30", "rgba(36,22,17"),
    ("rgba(233,205,186", "rgba(233,196,181"),
    ("rgba(185,138,128", "rgba(197,122,100"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel:. Si hay IG real se usaria, Flo-Bugs
#    no tiene IG propio verificable -> boton secundario a Google Reviews.
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_REVIEWS_LABEL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Flo-Bugs Pest Control · Termite &amp; Pest Control in Miami, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Flo-Bugs Pest Control, Miami FL: termite control, WDO inspections, mosquito control, general pest control and rodent control. 4.9 stars across 50 Google reviews. Call or text anytime." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Flo-Bugs Pest Control · Termite &amp; Pest Control in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Termite control, WDO inspections, mosquito, pest and rodent control. 4.9 on Google with 50 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/g0.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/g0.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Flo-Bugs Pest Control",
    "description": "Pest control company serving Miami-Dade County, FL: termite control and WDO inspections, mosquito control, general pest control and rodent control.",
    "areaServed": "Miami-Dade County, FL",
    "telephone": "+1-786-283-9911",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "50", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Pest control services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Termite Control &amp; WDO Inspections" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Mosquito Control" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Pest Control" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Rodent Control" } }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,46,0.35)]" />',
    '<img src="assets/raw/g0.jpg" alt="Flo-Bugs Pest Control" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,46,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Flo-<span class="text-[color:var(--accent-deep)]">Bugs</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">FB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Flo-Bugs</span>')
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
    'data-es="Miami-Dade, FL · Pest &amp; Termite Control" data-en="Miami-Dade, FL · Pest &amp; Termite Control">Miami-Dade, FL · Pest &amp; Termite Control</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Bugs do not stand a chance." data-en="Bugs do not stand a chance.">Bugs do not stand a chance.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Termite, pest and rodent" data-en="Termite, pest and rodent">Termite, pest and rodent</span><br /><span data-es="control, handled " data-en="control, handled ">control, handled </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Flo-Bugs treats termites, mosquitoes, roaches, ants and rodents across Miami-Dade, with WDO inspections for home sales and straight talk about what is actually happening in your house. Rated 4.9 with 50 Google reviews." data-en="Flo-Bugs treats termites, mosquitoes, roaches, ants and rodents across Miami-Dade, with WDO inspections for home sales and straight talk about what is actually happening in your house. Rated 4.9 with 50 Google reviews.">Flo-Bugs treats termites, mosquitoes, roaches, ants and rodents across Miami-Dade, with WDO inspections for home sales and straight talk about what is actually happening in your house. Rated 4.9 with 50 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 50 reviews on Google" data-en="4.9 · 50 reviews on Google">4.9 · 50 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 283-9911" data-en="Call (786) 283-9911">Call (786) 283-9911</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            ''' + NEW_REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/g0.jpg" alt="The Flo-Bugs Pest Control service trailer parked at a home in Miami, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Available" data-en="Available">Available</p>
            <p class="font-display text-lg">24/7</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Every day of the week" data-en="Every day of the week">Every day of the week</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="50">50</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Termite <span class="text-shine">&amp;</span> Rodent</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="WDO inspections · Control" data-en="WDO inspections · Control">WDO inspections · Control</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">24/7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Always on call" data-en="Always on call">Always on call</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Miami-Dade</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Service area, FL" data-en="Service area, FL">Service area, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Termite Control"),
    ("Hybrid Set", "WDO Inspections"),
    ("Volume Set", "Mosquito Control"),
    ("Mega Volume", "Pest Control"),
    ("Bottom Lashes", "Rodent Control"),
    ("West Palm Beach, FL", "Miami-Dade, FL"),
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
          <img src="assets/raw/g2.jpg" alt="The Flo-Bugs Pest Control truck with its logo and phone number" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One team," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="always on call" data-en="always on call">always on call</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Flo-Bugs Pest Control is a Miami-Dade team covering termite control, WDO inspections, mosquito control, general pest control and rodent control, working out of their own service trailer and truck across Miami, Little Havana and the surrounding area." data-en="Flo-Bugs Pest Control is a Miami-Dade team covering termite control, WDO inspections, mosquito control, general pest control and rodent control, working out of their own service trailer and truck across Miami, Little Havana and the surrounding area.">Flo-Bugs Pest Control is a Miami-Dade team covering termite control, WDO inspections, mosquito control, general pest control and rodent control, working out of their own service trailer and truck across Miami, Little Havana and the surrounding area.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Customers describe Mike as professional, polite and thorough, with fair pricing and fast, efficient work. The result: a 4.9-star rating across 50 Google reviews." data-en="Customers describe Mike as professional, polite and thorough, with fair pricing and fast, efficient work. The result: a 4.9-star rating across 50 Google reviews.">Customers describe Mike as professional, polite and thorough, with fair pricing and fast, efficient work. The result: a 4.9-star rating across 50 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="50">50</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Siempre disponible" data-en="Always on call">Always on call</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,46,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/g2.jpg" alt="Flo-Bugs Pest Control" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,46,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Mike · <span class="text-[color:var(--ink-40)]" data-es="Lead Technician" data-en="Lead Technician">Lead Technician</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="How Flo-Bugs" data-en="How Flo-Bugs">How Flo-Bugs</span> <span class="text-shine" data-es="gets it done" data-en="gets it done">gets it done</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or text" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text (786) 283-9911 with what you are seeing, termites, rodents, mosquitoes or bugs, and Mike gets back to you to set up a visit." data-en="Call or text (786) 283-9911 with what you are seeing, termites, rodents, mosquitoes or bugs, and Mike gets back to you to set up a visit.">Call or text (786) 283-9911 with what you are seeing, termites, rodents, mosquitoes or bugs, and Mike gets back to you to set up a visit.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Inspection" data-en="Inspection">Inspection</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A technician walks the property, finds where the activity is coming from, and explains it in plain terms before any treatment starts." data-en="A technician walks the property, finds where the activity is coming from, and explains it in plain terms before any treatment starts.">A technician walks the property, finds where the activity is coming from, and explains it in plain terms before any treatment starts.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Treatment" data-en="Treatment">Treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Termite treatment, exclusion, baiting or spraying, whatever the problem calls for, handled the same day in most cases." data-en="Termite treatment, exclusion, baiting or spraying, whatever the problem calls for, handled the same day in most cases.">Termite treatment, exclusion, baiting or spraying, whatever the problem calls for, handled the same day in most cases.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Follow-up" data-en="Follow-up">Follow-up</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Flo-Bugs follows up to confirm the problem is gone and sets a schedule for ongoing prevention if you want it." data-en="Flo-Bugs follows up to confirm the problem is gone and sets a schedule for ongoing prevention if you want it.">Flo-Bugs follows up to confirm the problem is gone and sets a schedule for ongoing prevention if you want it.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Pest problems," data-en="Pest problems,">Pest problems,</span> <span class="text-shine" data-es="handled" data-en="handled">handled</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every property is different, so Flo-Bugs gives a clear quote over the phone before any visit." data-en="Every property is different, so Flo-Bugs gives a clear quote over the phone before any visit.">Every property is different, so Flo-Bugs gives a clear quote over the phone before any visit.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(194,59,46,0.4); box-shadow: 0 18px 50px rgba(42,33,28,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Termite Control" data-en="Termite Control">Termite Control</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full termite treatment plus WDO (Wood Destroying Organism) inspections for home sales and refinancing, with a written report." data-en="Full termite treatment plus WDO (Wood Destroying Organism) inspections for home sales and refinancing, with a written report.">Full termite treatment plus WDO (Wood Destroying Organism) inspections for home sales and refinancing, with a written report.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Prevention" data-en="Prevention">Prevention</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Mosquito Control" data-en="Mosquito Control">Mosquito Control</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Yard treatments that cut down mosquitoes fast, built around Miami's rain and heat cycle." data-en="Yard treatments that cut down mosquitoes fast, built around Miami's rain and heat cycle.">Yard treatments that cut down mosquitoes fast, built around Miami's rain and heat cycle.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="General" data-en="General">General</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pest Control" data-en="Pest Control">Pest Control</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Roaches, ants, spiders and the everyday bugs that show up in Miami homes, handled on a one-time or recurring visit." data-en="Roaches, ants, spiders and the everyday bugs that show up in Miami homes, handled on a one-time or recurring visit.">Roaches, ants, spiders and the everyday bugs that show up in Miami homes, handled on a one-time or recurring visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Rodent" data-en="Rodent">Rodent</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Rodent Control" data-en="Rodent Control">Rodent Control</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Rats and mice trapped and excluded, with entry points sealed so they do not come back." data-en="Rats and mice trapped and excluded, with entry points sealed so they do not come back.">Rats and mice trapped and excluded, with entry points sealed so they do not come back.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on the property and the problem. Call or text (786) 283-9911 for a free quote." data-en="Pricing depends on the property and the problem. Call or text (786) 283-9911 for a free quote.">Pricing depends on the property and the problem. Call or text (786) 283-9911 for a free quote.</span></p>')
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
          Call (786) 283-9911
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Termite damage found" data-en="Termite damage found">Termite damage found</span><img src="assets/raw/g7.jpg" alt="Drywood termite damage found behind a baseboard during a Flo-Bugs inspection" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Mosquito control" data-en="Mosquito control">Mosquito control</span><img src="assets/raw/g5.jpg" alt="A mosquito on skin, the kind of pest Flo-Bugs treats Miami yards for" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Roach control" data-en="Roach control">Roach control</span><img src="assets/raw/g3.jpg" alt="Cockroaches found during a Flo-Bugs pest inspection in Miami" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Termite colony" data-en="Termite colony">Termite colony</span><img src="assets/raw/g6.jpg" alt="Live termites found inside a wood structure during an inspection" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Infestation found" data-en="Infestation found">Infestation found</span><img src="assets/raw/g10.jpg" alt="A roach infestation found in a corner during a Flo-Bugs treatment visit" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Miami" data-en="What Miami">What Miami</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 50 verified reviews on Google" data-en="4.9 out of 5 · 50 verified reviews on Google">4.9 out of 5 · 50 verified reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I just want share my personal experience excellent professional Mike and his teams are the best I love to share the excellent service Mike done in my house I will continue service exterminator for any bugs etc this is the company for the service thank you I really appreciate your hard work Mike"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carlos Cano</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"So professional and reliable...Mike is the best! Highly recommend their services."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lisa Seif</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mike is professional, polite and friendly. Excellent pest control advisor. Really good service. 5 Stars and highly recommended"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Julio Enrique Briceño Rodríguez</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 50 reviews on Google" data-en="Read all 50 reviews on Google">Read all 50 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION (sin direccion fija: negocio de servicio movil -> foto real)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Miami-Dade</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,46,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Flo-Bugs comes to you anywhere in Miami-Dade County, including Little Havana, Flagami, Westchester and the surrounding neighborhoods." data-en="Flo-Bugs comes to you anywhere in Miami-Dade County, including Little Havana, Flagami, Westchester and the surrounding neighborhoods.">Flo-Bugs comes to you anywhere in Miami-Dade County, including Little Havana, Flagami, Westchester and the surrounding neighborhoods.</p>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,46,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Available 24 hours a day, every day of the week." data-en="Available 24 hours a day, every day of the week.">Available 24 hours a day, every day of the week.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,46,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 283-9911" data-en="Call (786) 283-9911">Call (786) 283-9911</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,46,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.9 stars across 50 verified Google reviews." data-en="4.9 stars across 50 verified Google reviews.">4.9 stars across 50 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,46,0.4)]" href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener">''' + NEW_REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame reveal min-h-[380px]" style="transition-delay:180ms">
        <img src="assets/raw/g8.jpg" alt="A Flo-Bugs technician documenting a crawl space during a termite inspection in Miami-Dade" class="w-full h-full min-h-[380px] object-cover" loading="lazy" />
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Bugs do not stand a chance." data-en="Bugs do not stand a chance.">Bugs do not stand a chance.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call," data-en="One call,">One call,</span> <span class="text-shine" data-es="problem solved" data-en="problem solved">problem solved</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call or text (786) 283-9911 for a free quote on termites, rodents, mosquitoes or any pest in your home. Flo-Bugs covers all of Miami-Dade, 24/7." data-en="Call or text (786) 283-9911 for a free quote on termites, rodents, mosquitoes or any pest in your home. Flo-Bugs covers all of Miami-Dade, 24/7.">Call or text (786) 283-9911 for a free quote on termites, rodents, mosquitoes or any pest in your home. Flo-Bugs covers all of Miami-Dade, 24/7.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 283-9911" data-en="Call (786) 283-9911">Call (786) 283-9911</a>
        <a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read Google Reviews" data-en="Read Google Reviews">Read Google Reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Flo-Bugs</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,168,154,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/raw/g0.jpg" alt="Flo-Bugs Pest Control" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,168,154,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Flo-Bugs</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Termite, pest, mosquito and rodent control serving Miami-Dade County, FL." data-en="Termite, pest, mosquito and rodent control serving Miami-Dade County, FL.">Termite, pest, mosquito and rodent control serving Miami-Dade County, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#f0a89a]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Miami-Dade County, FL (mobile service)" data-en="Miami-Dade County, FL (mobile service)">Miami-Dade County, FL (mobile service)</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#f0a89a]" data-es="Call (786) 283-9911" data-en="Call (786) 283-9911">Call (786) 283-9911</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0a89a]">Instagram · ''' + NEW_REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reviews" data-en="Reviews">Reviews</p>
        <p><a href="''' + NEW_REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f0a89a]">4.9 · ''' + NEW_REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Flo-Bugs Pest Control.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Flo-Bugs Pest Control">')
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
    "Miami-Dade, FL · Pest &amp; Termite Control": "Miami-Dade, FL · Control de Plagas y Termitas",
    "Bugs do not stand a chance.": "Las plagas no tienen oportunidad.",
    "Termite, pest and rodent": "Control de termitas, plagas",
    "control, handled ": "y roedores, resuelto ",
    "right": "bien",
    "Flo-Bugs treats termites, mosquitoes, roaches, ants and rodents across Miami-Dade, with WDO inspections for home sales and straight talk about what is actually happening in your house. Rated 4.9 with 50 Google reviews.":
        "Flo-Bugs trata termitas, mosquitos, cucarachas, hormigas y roedores en todo Miami-Dade, con inspecciones WDO para venta de casas y explicaciones claras de lo que realmente pasa en tu casa. Calificacion de 4.9 con 50 resenas de Google.",
    "4.9 · 50 reviews on Google": "4.9 · 50 resenas en Google",
    "Call (786) 283-9911": "Llama al (786) 283-9911",
    "Available": "Disponible",
    "Every day of the week": "Todos los dias de la semana",
    "WDO inspections · Control": "Inspecciones WDO · Control",
    "Always on call": "Siempre disponible",
    "Service area, FL": "Zona de servicio, FL",
    "How Flo-Bugs": "Como trabaja",
    "gets it done": "Flo-Bugs",
    "One team,": "Un equipo,",
    "always on call": "siempre disponible",
    "Flo-Bugs Pest Control is a Miami-Dade team covering termite control, WDO inspections, mosquito control, general pest control and rodent control, working out of their own service trailer and truck across Miami, Little Havana and the surrounding area.":
        "Flo-Bugs Pest Control es un equipo de Miami-Dade dedicado a control de termitas, inspecciones WDO, control de mosquitos, control de plagas en general y control de roedores, trabajando desde su propio trailer y camion en Miami, Little Havana y los alrededores.",
    "Customers describe Mike as professional, polite and thorough, with fair pricing and fast, efficient work. The result: a 4.9-star rating across 50 Google reviews.":
        "Los clientes describen a Mike como profesional, amable y minucioso, con precios justos y un trabajo rapido y eficiente. El resultado: una calificacion de 4.9 estrellas en 50 resenas de Google.",
    "Lead Technician": "Tecnico principal",
    "Call or text": "Llama o escribe",
    "Call or text (786) 283-9911 with what you are seeing, termites, rodents, mosquitoes or bugs, and Mike gets back to you to set up a visit.":
        "Llama o escribe al (786) 283-9911 con lo que estas viendo, termitas, roedores, mosquitos o insectos, y Mike te responde para agendar una visita.",
    "Inspection": "Inspeccion",
    "A technician walks the property, finds where the activity is coming from, and explains it in plain terms before any treatment starts.":
        "Un tecnico recorre la propiedad, encuentra de donde viene la actividad, y lo explica en palabras simples antes de empezar cualquier tratamiento.",
    "Treatment": "Tratamiento",
    "Termite treatment, exclusion, baiting or spraying, whatever the problem calls for, handled the same day in most cases.":
        "Tratamiento de termitas, exclusion, cebos o fumigacion, lo que el problema requiera, resuelto el mismo dia en la mayoria de los casos.",
    "Follow-up": "Seguimiento",
    "Flo-Bugs follows up to confirm the problem is gone and sets a schedule for ongoing prevention if you want it.":
        "Flo-Bugs da seguimiento para confirmar que el problema desaparecio y arma un plan de prevencion continua si lo quieres.",
    "Pest problems,": "Problemas de plagas,",
    "handled": "resueltos",
    "Every property is different, so Flo-Bugs gives a clear quote over the phone before any visit.":
        "Cada propiedad es diferente, asi que Flo-Bugs da una cotizacion clara por telefono antes de cualquier visita.",
    "Most requested": "Lo mas solicitado",
    "Termite Control": "Control de Termitas",
    "Full termite treatment plus WDO (Wood Destroying Organism) inspections for home sales and refinancing, with a written report.":
        "Tratamiento completo de termitas mas inspecciones WDO (organismos que danan la madera) para venta de casas y refinanciamiento, con reporte por escrito.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Prevention": "Prevencion",
    "Mosquito Control": "Control de Mosquitos",
    "Yard treatments that cut down mosquitoes fast, built around Miami's rain and heat cycle.":
        "Tratamientos de jardin que reducen los mosquitos rapido, pensados para el ciclo de lluvia y calor de Miami.",
    "General": "General",
    "Pest Control": "Control de Plagas",
    "Roaches, ants, spiders and the everyday bugs that show up in Miami homes, handled on a one-time or recurring visit.":
        "Cucarachas, hormigas, aranas y los insectos comunes que aparecen en las casas de Miami, resueltos en una visita unica o recurrente.",
    "Rodent": "Roedores",
    "Rodent Control": "Control de Roedores",
    "Rats and mice trapped and excluded, with entry points sealed so they do not come back.":
        "Ratas y ratones atrapados y excluidos, sellando los puntos de entrada para que no regresen.",
    "Pricing depends on the property and the problem. Call or text (786) 283-9911 for a free quote.":
        "El precio depende de la propiedad y el problema. Llama o escribe al (786) 283-9911 para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Miami": "Lo que dicen los",
    "customers say": "clientes en Miami",
    "4.9 out of 5 · 50 verified reviews on Google": "4.9 de 5 · 50 resenas verificadas en Google",
    "Read all 50 reviews on Google": "Lee las 50 resenas en Google",
    "Serving": "Sirviendo a",
    "Service area": "Zona de servicio",
    "Flo-Bugs comes to you anywhere in Miami-Dade County, including Little Havana, Flagami, Westchester and the surrounding neighborhoods.":
        "Flo-Bugs va hasta ti en cualquier parte de Miami-Dade, incluyendo Little Havana, Flagami, Westchester y los barrios cercanos.",
    "Hours": "Horario",
    "Available 24 hours a day, every day of the week.": "Disponible las 24 horas, todos los dias de la semana.",
    "Reviews": "Resenas",
    "4.9 stars across 50 verified Google reviews.": "4.9 estrellas en 50 resenas verificadas de Google.",
    "One call,": "Una llamada,",
    "problem solved": "problema resuelto",
    "Call or text (786) 283-9911 for a free quote on termites, rodents, mosquitoes or any pest in your home. Flo-Bugs covers all of Miami-Dade, 24/7.":
        "Llama o escribe al (786) 283-9911 para una cotizacion gratis de termitas, roedores, mosquitos o cualquier plaga en tu casa. Flo-Bugs cubre todo Miami-Dade, las 24 horas.",
    "Read Google Reviews": "Lee las resenas en Google",
    "Termite, pest, mosquito and rodent control serving Miami-Dade County, FL.": "Control de termitas, plagas, mosquitos y roedores en todo Miami-Dade, FL.",
    "Contact": "Contacto",
    "Miami-Dade County, FL (mobile service)": "Condado de Miami-Dade, FL (servicio movil)",
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
