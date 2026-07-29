import re
import shutil

SLUG = "serrano-handyman-kissimmee"
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
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> steel-blue (Serrano Handyman)
#    Rotacion de hue manteniendo la luminosidad/saturacion ya validada por
#    lakeside-grooming-tallahassee (teal), pasando el hue de ~185 a ~213
#    (azul acero, confianza/construccion), evitando dorado y plum-pink.
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#143f74"),  # accent-deep
    ("#5c2140", "#0c2038"),  # btn-3d sole darkest
    ("#f0bed7", "#a9c1de"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#f2f5f8"),  # bg
    ("#c47a9c", "#3f6ca3"),  # accent-mid
    ("#8a5573", "#1c3c63"),  # dark-band btn shadow deep
    ("#f3e0ea", "#dce5ef"),  # bg-2 / accent-soft
    ("#d9a8c2", "#7899c2"),  # orb-b
    ("#7d3457", "#163255"),  # dark mid
    ("#5f2c48", "#0e2847"),  # step-num gradient end
    ("#33222c", "#1c232b"),  # ink
    ("#fbf3f8", "#f2f6fb"),  # tile-cap text near-white
    ("#fbeff5", "#eaf1fa"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#cddcee"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#eaeff6"),  # theme-color meta
    ("#f2d5e3", "#cddbec"),  # orb-a
    ("#f2cfe0", "#c2d4e9"),  # dark-band shimmer last stop
    ("#efd0e0", "#c8d8eb"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#a9c1de"),  # orb-c pale
    ("#dc9dbe", "#5780b3"),  # scroll-progress end stop
    ("#d3a2bc", "#8eaacd"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#3d689c"),  # shimmer stop
    ("#b25a85", "#1f497d"),  # shimmer stop
    ("#2a1722", "#0b1a2c"),  # cta-final bg gradient start
    ("#1f0f18", "#07111e"),  # cta-final bg gradient end
    ("#1c0f16", "#08111d"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(20,63,116"),    # accent-deep alpha
    ("rgba(51,34,44", "rgba(28,35,43"),       # ink alpha
    ("rgba(240,190,215", "rgba(169,193,222"),  # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(12,32,56"),       # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(242,245,248"),  # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(22,50,85"),      # dark mid alpha
    ("rgba(253,246,250", "rgba(242,246,251"),  # surface alpha
    ("rgba(40,16,30", "rgba(11,26,44"),       # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(169,193,222"),  # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(63,108,163"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel:. Si hay Instagram real.
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+14077601112"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/serranohandyman/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@serranohandyman"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_FB_URL = "https://www.facebook.com/serranohandymanllc/"
NEW_MAPS = "https://www.google.com/maps?q=Kissimmee,+FL"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Serrano Handyman · Home Repair &amp; Remodeling in Kissimmee, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Serrano Handyman LLC, Kissimmee FL: general repairs, painting, gutter cleaning and remodeling with owner Charlie Serrano. 4.9 stars across 110 Google reviews. Call for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Serrano Handyman · Home Repair &amp; Remodeling in Kissimmee, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="General repairs, painting, gutter cleaning and remodeling since 2015. 4.9 on Google with 110 reviews. Call for a free quote." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-roof.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Serrano Handyman LLC",
    "description": "Handyman and home repair company serving Kissimmee, FL and Central Florida since 2015: general repairs, painting, gutter cleaning, ceiling repair, attic ladder upgrades, kitchen and bathroom remodeling.",
    "address": { "@type": "PostalAddress", "addressLocality": "Kissimmee", "addressRegion": "FL", "addressCountry": "US" },
    "areaServed": "Kissimmee, FL",
    "telephone": "+1-407-760-1112",
    "sameAs": ["https://www.instagram.com/serranohandyman/", "https://www.facebook.com/serranohandymanllc/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "110", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "21:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Handyman Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Painting &amp; Pressure Washing" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Gutter &amp; Attic Service" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Remodeling &amp; Custom Installs" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (ya es el default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. NAV (logo monograma + wordmark + preloader)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,63,116,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Serrano Handyman" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,63,116,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Serrano <span class="text-[color:var(--accent-deep)]">Handyman</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">SH</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Serrano Handyman</span>')
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
    'data-es="Kissimmee, FL · Handyman &amp; Home Repair" data-en="Kissimmee, FL · Handyman &amp; Home Repair">Kissimmee, FL · Handyman &amp; Home Repair</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Quality work. Honest prices." data-en="Quality work. Honest prices.">Quality work. Honest prices.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="The handyman Kissimmee" data-en="The handyman Kissimmee">The handyman Kissimmee</span><br /><span data-es="homeowners " data-en="homeowners ">homeowners </span><span class="text-shine" data-es="call first" data-en="call first">call first</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Owner Charlie Serrano has been fixing, painting and remodeling homes across Kissimmee since 2015. From a leaky faucet to a full room repaint, Serrano Handyman shows up, gives an honest quote, and gets the job done right the first time." data-en="Owner Charlie Serrano has been fixing, painting and remodeling homes across Kissimmee since 2015. From a leaky faucet to a full room repaint, Serrano Handyman shows up, gives an honest quote, and gets the job done right the first time.">Owner Charlie Serrano has been fixing, painting and remodeling homes across Kissimmee since 2015. From a leaky faucet to a full room repaint, Serrano Handyman shows up, gives an honest quote, and gets the job done right the first time.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 110 reviews on Google" data-en="4.9 · 110 reviews on Google">4.9 · 110 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (407) 760-1112" data-en="Call (407) 760-1112">Call (407) 760-1112</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-roof.jpg" alt="A roof reshingled by Serrano Handyman in Kissimmee, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">8am - 9pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Mon-Sat · Closed Sunday" data-en="Mon-Sat · Closed Sunday">Mon-Sat · Closed Sunday</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="110">110</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl"><span data-es="Since" data-en="Since">Since</span> <span class="text-shine">2015</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Serving Kissimmee &amp; Central Florida" data-en="Serving Kissimmee &amp; Central Florida">Serving Kissimmee &amp; Central Florida</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">Charlie <span class="text-shine">Serrano</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Owner &amp; handyman" data-en="Owner &amp; handyman">Owner &amp; handyman</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Kissimmee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Central Florida" data-en="Central Florida">Central Florida</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "General Repairs"),
    ("Hybrid Set", "Painting"),
    ("Volume Set", "Gutter Cleaning"),
    ("Mega Volume", "Ceiling Repair"),
    ("Bottom Lashes", "Remodeling"),
    ("West Palm Beach, FL", "Kissimmee, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (solo 1 foto real disponible para esta seccion -> grid 1 col)
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
          <img src="assets/about-patio-deck.jpg" alt="A covered patio and pool deck refreshed by Serrano Handyman" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Eleven years of" data-en="Eleven years of">Eleven years of</span><br /><span class="text-shine" data-es="getting it done right" data-en="getting it done right">getting it done right</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Charlie Serrano started Serrano Handyman LLC in 2015, and eleven years later he is still the name Kissimmee homeowners call first for repairs, painting and remodeling. No project is too small to matter, and every job gets Charlie&#39;s own hands and a straight answer on price before any work begins." data-en="Charlie Serrano started Serrano Handyman LLC in 2015, and eleven years later he is still the name Kissimmee homeowners call first for repairs, painting and remodeling. No project is too small to matter, and every job gets Charlie&#39;s own hands and a straight answer on price before any work begins.">Charlie Serrano started Serrano Handyman LLC in 2015, and eleven years later he is still the name Kissimmee homeowners call first for repairs, painting and remodeling. No project is too small to matter, and every job gets Charlie&#39;s own hands and a straight answer on price before any work begins.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.9-star rating across 110 Google reviews, and neighbors who describe the work as quick, fairly priced and done right the first time." data-en="The result: a 4.9-star rating across 110 Google reviews, and neighbors who describe the work as quick, fairly priced and done right the first time.">The result: a 4.9-star rating across 110 Google reviews, and neighbors who describe the work as quick, fairly priced and done right the first time.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="110">110</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2015</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Serving since" data-en="Serving since">Serving since</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,63,116,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Serrano Handyman" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,63,116,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Charlie Serrano · <span class="text-[color:var(--ink-40)]" data-es="Owner &amp; Handyman" data-en="Owner &amp; Handyman">Owner &amp; Handyman</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your project, start" data-en="Your project, start">Your project, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or text" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text (407) 760-1112 with what needs fixing, painting or building, and Charlie will talk through the job with you." data-en="Call or text (407) 760-1112 with what needs fixing, painting or building, and Charlie will talk through the job with you.">Call or text (407) 760-1112 with what needs fixing, painting or building, and Charlie will talk through the job with you.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Honest quote" data-en="Honest quote">Honest quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get an honest, upfront price for the work, no surprise charges once the job is underway." data-en="You get an honest, upfront price for the work, no surprise charges once the job is underway.">You get an honest, upfront price for the work, no surprise charges once the job is underway.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The work gets done" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="From a quick repair to a full remodel, Charlie handles the job with the same care every time." data-en="From a quick repair to a full remodel, Charlie handles the job with the same care every time.">From a quick repair to a full remodel, Charlie handles the job with the same care every time.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walk the results together" data-en="Walk the results together">Walk the results together</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Before Charlie leaves, you walk through the finished work together, so you know it was done right." data-en="Before Charlie leaves, you walk through the finished work together, so you know it was done right.">Before Charlie leaves, you walk through the finished work together, so you know it was done right.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; solo nombres, sin precios inventados)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine">every home</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two projects are the same, so every job gets its own honest quote by phone, before any work begins." data-en="No two projects are the same, so every job gets its own honest quote by phone, before any work begins.">No two projects are the same, so every job gets its own honest quote by phone, before any work begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Everyday fixes" data-en="Everyday fixes">Everyday fixes</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="General Handyman Repairs" data-en="General Handyman Repairs">General Handyman Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Faucet repairs, door and frame repair, drywall and ceiling patching, and the everyday fixes every home eventually needs." data-en="Faucet repairs, door and frame repair, drywall and ceiling patching, and the everyday fixes every home eventually needs.">Faucet repairs, door and frame repair, drywall and ceiling patching, and the everyday fixes every home eventually needs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(20,63,116,0.4); box-shadow: 0 18px 50px rgba(28,35,43,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Painting &amp; Pressure Washing" data-en="Painting &amp; Pressure Washing">Painting &amp; Pressure Washing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Interior and exterior painting, pool deck restoration, and pressure washing that leaves siding, decks and driveways looking new." data-en="Interior and exterior painting, pool deck restoration, and pressure washing that leaves siding, decks and driveways looking new.">Interior and exterior painting, pool deck restoration, and pressure washing that leaves siding, decks and driveways looking new.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Keep it maintained" data-en="Keep it maintained">Keep it maintained</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gutter &amp; Attic Service" data-en="Gutter &amp; Attic Service">Gutter &amp; Attic Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gutter and downspout cleaning to protect your roof and foundation, plus attic ladder upgrades for safer, easier access." data-en="Gutter and downspout cleaning to protect your roof and foundation, plus attic ladder upgrades for safer, easier access.">Gutter and downspout cleaning to protect your roof and foundation, plus attic ladder upgrades for safer, easier access.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Bigger projects" data-en="Bigger projects">Bigger projects</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Remodeling &amp; Custom Installs" data-en="Remodeling &amp; Custom Installs">Remodeling &amp; Custom Installs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Kitchen and bathroom remodeling, custom LED lighting, and shed, tree or yard cleanup for projects that need more than a quick fix." data-en="Kitchen and bathroom remodeling, custom LED lighting, and shed, tree or yard cleanup for projects that need more than a quick fix.">Kitchen and bathroom remodeling, custom LED lighting, and shed, tree or yard cleanup for projects that need more than a quick fix.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Repairs" data-en="Repairs">Repairs</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Faucet repairs" data-en="Faucet repairs">Faucet repairs</li>
            <li class="flex items-center gap-2" data-es="Door &amp; frame repair" data-en="Door &amp; frame repair">Door &amp; frame repair</li>
            <li class="flex items-center gap-2" data-es="Drywall &amp; ceiling patch" data-en="Drywall &amp; ceiling patch">Drywall &amp; ceiling patch</li>
            <li class="flex items-center gap-2" data-es="General handyman repairs" data-en="General handyman repairs">General handyman repairs</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Paint &amp; Exterior" data-en="Paint &amp; Exterior">Paint &amp; Exterior</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Interior painting" data-en="Interior painting">Interior painting</li>
            <li class="flex items-center gap-2" data-es="Exterior painting" data-en="Exterior painting">Exterior painting</li>
            <li class="flex items-center gap-2" data-es="Pool deck restoration" data-en="Pool deck restoration">Pool deck restoration</li>
            <li class="flex items-center gap-2" data-es="Pressure washing" data-en="Pressure washing">Pressure washing</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Remodel &amp; Install" data-en="Remodel &amp; Install">Remodel &amp; Install</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Kitchen &amp; bath remodeling" data-en="Kitchen &amp; bath remodeling">Kitchen &amp; bath remodeling</li>
            <li class="flex items-center gap-2" data-es="Custom LED lighting" data-en="Custom LED lighting">Custom LED lighting</li>
            <li class="flex items-center gap-2" data-es="Attic ladder upgrades" data-en="Attic ladder upgrades">Attic ladder upgrades</li>
            <li class="flex items-center gap-2" data-es="Shed &amp; yard cleanup" data-en="Shed &amp; yard cleanup">Shed &amp; yard cleanup</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and materials. Call (407) 760-1112 for a free, honest quote." data-en="Pricing depends on scope and materials. Call (407) 760-1112 for a free, honest quote.">Pricing depends on scope and materials. Call (407) 760-1112 for a free, honest quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex; 3 fotos reales curadas)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="work" data-en="work">work</span>')
rep('''<a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_IG_HANDLE + '''
        </a>''',
    '''<a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_IG_HANDLE + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Patio y terreno despejados, escombros retirados" data-en="Yard cleared, shed and debris hauled away">Yard cleared, shed and debris hauled away</span><img src="assets/gallery-shed-yard.jpg" alt="A backyard cleared by Serrano Handyman, shed and debris hauled away" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Techo reparado, imprimado y repintado" data-en="Ceiling patched, primed and repainted">Ceiling patched, primed and repainted</span><img src="assets/gallery-ceiling-repair.jpg" alt="A ceiling patched, primed and repainted by Serrano Handyman" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Reparacion de marco de puerta en proceso" data-en="Door frame repair in progress">Door frame repair in progress</span><img src="assets/gallery-door-repair.jpg" alt="A door frame repair job in progress by Serrano Handyman" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. MARQUEE 2 (reverse) ya cubierto por MARQUEE_WORDS (rep_all)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Kissimmee" data-en="What Kissimmee">What Kissimmee</span> <span class="text-shine" data-es="homeowners say" data-en="homeowners say">homeowners say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 110 reviews on Google" data-en="4.9 out of 5 · 110 reviews on Google">4.9 out of 5 · 110 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mr. Life Savior, is what I call him!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">David 23</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Communication was great. The price quoted was reasonable. The work was excellent. Would use again."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Melissa Quinn</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Quick response. Fair price. Quality work."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">staci</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=Serrano+Handyman+Kissimmee+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 110 reviews on Google" data-en="Read all 110 reviews on Google">Read all 110 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (sin direccion fija confiable: se muestra como area de servicio)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Kissimmee, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,63,116,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Serrano Handyman works by appointment across Kissimmee, FL and the surrounding Central Florida area." data-en="Serrano Handyman works by appointment across Kissimmee, FL and the surrounding Central Florida area.">Serrano Handyman works by appointment across Kissimmee, FL and the surrounding Central Florida area.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,63,116,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,63,116,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Saturday, 8:00 AM to 9:00 PM. Closed Sunday." data-en="Monday to Saturday, 8:00 AM to 9:00 PM. Closed Sunday.">Monday to Saturday, 8:00 AM to 9:00 PM. Closed Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,63,116,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (407) 760-1112" data-en="Call (407) 760-1112">Call (407) 760-1112</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,63,116,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="font-medium mb-1" data-es="Instagram &amp; Facebook" data-en="Instagram &amp; Facebook">Instagram &amp; Facebook</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See recent jobs from Charlie and message any questions before you call." data-en="See recent jobs from Charlie and message any questions before you call.">See recent jobs from Charlie and message any questions before you call.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,63,116,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Serrano Handyman service area, Kissimmee FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Quality work. Honest prices." data-en="Quality work. Honest prices.">Quality work. Honest prices.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call fixes" data-en="One call fixes">One call fixes</span> <span class="text-shine" data-es="it all" data-en="it all">it all</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (407) 760-1112 for a free, honest quote on your repair, paint or remodeling project. Monday to Saturday, 8 AM to 9 PM." data-en="Call (407) 760-1112 for a free, honest quote on your repair, paint or remodeling project. Monday to Saturday, 8 AM to 9 PM.">Call (407) 760-1112 for a free, honest quote on your repair, paint or remodeling project. Monday to Saturday, 8 AM to 9 PM.</p>')
rep('''<a href="tel:+14077601112" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (407) 760-1112" data-en="Call (407) 760-1112">Call (407) 760-1112</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Serrano</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,193,222,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Serrano Handyman" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,193,222,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Serrano Handyman</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Handyman &amp; home repair serving Kissimmee, FL. By appointment." data-en="Handyman &amp; home repair serving Kissimmee, FL. By appointment.">Handyman &amp; home repair serving Kissimmee, FL. By appointment.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="tel:+14077601112" target="_blank" rel="noopener" class="hover:text-[#a9c1de]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Kissimmee, FL &amp; Central Florida" data-en="Kissimmee, FL &amp; Central Florida">Kissimmee, FL &amp; Central Florida</p>
        <p><a href="tel:+14077601112" class="hover:text-[#a9c1de]" data-es="Call (407) 760-1112" data-en="Call (407) 760-1112">Call (407) 760-1112</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9c1de]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9c1de]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9c1de]">Facebook · Serrano Handyman LLC</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Serrano Handyman LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="tel:+14077601112" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+14077601112" class="book-float" aria-label="Call Serrano Handyman">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 20. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace('href="tel:+14077601112" target="_blank" rel="noopener"', 'href="tel:+14077601112"')
print("CLEANUP tel links done")


# ---------------------------------------------------------------------------
# 21. Traduccion ES real para todos los textos NUEVOS (bilingue obligatorio)
# ---------------------------------------------------------------------------
T = {
    "4.9 · 110 reviews on Google": "4.9 · 110 reseñas en Google",
    "4.9 out of 5 · 110 reviews on Google": "4.9 de 5 · 110 reseñas en Google",
    "Attic ladder upgrades": "Actualización de escalera de ático",
    "Bigger projects": "Proyectos grandes",
    "Call": "Llamar",
    "Call (407) 760-1112": "Llama al (407) 760-1112",
    "Call (407) 760-1112 for a free, honest quote on your repair, paint or remodeling project. Monday to Saturday, 8 AM to 9 PM.":
        "Llama al (407) 760-1112 para una cotización gratis y honesta para tu proyecto de reparación, pintura o remodelación. Lunes a sábado, de 8 AM a 9 PM.",
    "Call for a quote": "Llama para cotizar",
    "Call or text": "Llama o escribe",
    "Central Florida": "Centro de Florida",
    "Contact": "Contacto",
    "Faucet repairs, door and frame repair, drywall and ceiling patching, and the everyday fixes every home eventually needs.":
        "Reparación de llaves, puertas y marcos, y parcheo de paredes y techos: los arreglos cotidianos que toda casa necesita tarde o temprano.",
    "Follow": "Síguenos",
    "Follow on Instagram": "Síguenos en Instagram",
    "Handyman &amp; home repair serving Kissimmee, FL. By appointment.": "Reparaciones y remodelación del hogar en Kissimmee, FL. Con cita previa.",
    "Kissimmee, FL · Handyman &amp; Home Repair": "Kissimmee, FL · Reparaciones y Remodelación",
    "Paint &amp; Exterior": "Pintura y Exterior",
    "Call or text (407) 760-1112 with what needs fixing, painting or building, and Charlie will talk through the job with you.":
        "Llama o escribe al (407) 760-1112 con lo que necesitas reparar, pintar o construir, y Charlie hablará contigo sobre el trabajo.",
    "Charlie Serrano started Serrano Handyman LLC in 2015, and eleven years later he is still the name Kissimmee homeowners call first for repairs, painting and remodeling. No project is too small to matter, and every job gets Charlie&#39;s own hands and a straight answer on price before any work begins.":
        "Charlie Serrano fundó Serrano Handyman LLC en 2015, y once años después sigue siendo el nombre al que los dueños de casa en Kissimmee llaman primero para reparaciones, pintura y remodelación. Ningún proyecto es demasiado pequeño, y cada trabajo recibe las propias manos de Charlie y una respuesta clara sobre el precio antes de comenzar.",
    "Custom LED lighting": "Iluminación LED personalizada",
    "Door &amp; frame repair": "Reparación de puertas y marcos",
    "Drywall &amp; ceiling patch": "Reparación de paredes y techos",
    "Eleven years of": "Once años de",
    "Everyday fixes": "Arreglos cotidianos",
    "Exterior painting": "Pintura exterior",
    "Faucet repairs": "Reparación de llaves",
    "From a quick repair to a full remodel, Charlie handles the job with the same care every time.":
        "Desde una reparación rápida hasta una remodelación completa, Charlie maneja el trabajo con el mismo cuidado siempre.",
    "General handyman repairs": "Reparaciones generales del hogar",
    "You get an honest, upfront price for the work, no surprise charges once the job is underway.": "Recibe un precio honesto y claro para el trabajo, sin cargos sorpresa una vez que empieza el trabajo.",
    "getting it done right": "hacerlo bien",
    "Gutter and downspout cleaning to protect your roof and foundation, plus attic ladder upgrades for safer, easier access.":
        "Limpieza de canaletas y bajantes para proteger tu techo y cimientos, más actualización de escalera de ático para un acceso más seguro y fácil.",
    "Hours": "Horario",
    "Honest quote": "Cotización honesta",
    "Instagram &amp; Facebook": "Instagram y Facebook",
    "Interior and exterior painting, pool deck restoration, and pressure washing that leaves siding, decks and driveways looking new.":
        "Pintura interior y exterior, restauración de terrazas de piscina, y lavado a presión que deja fachadas, terrazas y entradas como nuevas.",
    "Interior painting": "Pintura interior",
    "Keep it maintained": "Mantenimiento",
    "Kissimmee, FL &amp; Central Florida": "Kissimmee, FL y Centro de Florida",
    "Kitchen and bathroom remodeling, custom LED lighting, and shed, tree or yard cleanup for projects that need more than a quick fix.":
        "Remodelación de cocina y baño, iluminación LED personalizada, y limpieza de galpones, árboles o patio para proyectos que necesitan más que un arreglo rápido.",
    "Kitchen &amp; bath remodeling": "Remodelación de cocina y baño",
    "Monday to Saturday, 8:00 AM to 9:00 PM. Closed Sunday.": "Lunes a sábado, de 8:00 AM a 9:00 PM. Cerrado los domingos.",
    "Mon-Sat · Closed Sunday": "Lun-Sáb · Cerrado domingo",
    "Most requested": "Lo más solicitado",
    "No two projects are the same, so every job gets its own honest quote by phone, before any work begins.":
        "Ningún proyecto es igual a otro, así que cada trabajo recibe su propia cotización honesta por teléfono, antes de comenzar.",
    "One call fixes": "Una llamada arregla",
    "it all": "todo",
    "Open": "Abierto",
    "Owner &amp; handyman": "Dueño y manitas",
    "Owner &amp; Handyman": "Dueño y Manitas",
    "Owner Charlie Serrano has been fixing, painting and remodeling homes across Kissimmee since 2015. From a leaky faucet to a full room repaint, Serrano Handyman shows up, gives an honest quote, and gets the job done right the first time.":
        "El dueño Charlie Serrano ha estado reparando, pintando y remodelando casas en Kissimmee desde 2015. Desde una llave que gotea hasta repintar un cuarto completo, Serrano Handyman llega, da una cotización honesta, y hace el trabajo bien desde la primera vez.",
    "Pool deck restoration": "Restauración de terraza de piscina",
    "Pressure washing": "Lavado a presión",
    "Pricing depends on scope and materials. Call (407) 760-1112 for a free, honest quote.":
        "El precio depende del alcance y los materiales. Llama al (407) 760-1112 para una cotización gratis y honesta.",
    "Quality work. Honest prices.": "Trabajo de calidad. Precios honestos.",
    "Read all 110 reviews on Google": "Lee las 110 reseñas en Google",
    "Real": "Trabajo",
    "Repairs": "Reparaciones",
    "reviews on Google": "reseñas en Google",
    "See recent jobs from Charlie and message any questions before you call.": "Mira trabajos recientes de Charlie y escribe cualquier duda antes de llamar.",
    "Serrano Handyman works by appointment across Kissimmee, FL and the surrounding Central Florida area.":
        "Serrano Handyman trabaja con cita previa en Kissimmee, FL y el área circundante del centro de Florida.",
    "Service area": "Área de servicio",
    "Serving": "Sirviendo a",
    "Serving Kissimmee &amp; Central Florida": "Sirviendo a Kissimmee y Centro de Florida",
    "Serving since": "Sirviendo desde",
    "Services for": "Servicios para",
    "Shed &amp; yard cleanup": "Limpieza de patio y galpones",
    "Since": "Desde",
    "The handyman Kissimmee": "El manitas al que Kissimmee",
    "homeowners ": "llama ",
    "call first": "primero",
    "The result: a 4.9-star rating across 110 Google reviews, and neighbors who describe the work as quick, fairly priced and done right the first time.":
        "El resultado: una calificación de 4.9 estrellas en 110 reseñas de Google, y vecinos que describen el trabajo como rápido, de precio justo y bien hecho desde la primera vez.",
    "The work gets done": "El trabajo se hace",
    "Before Charlie leaves, you walk through the finished work together, so you know it was done right.":
        "Antes de que Charlie se vaya, revisan juntos el trabajo terminado, para que sepas que quedó bien hecho.",
    "View on map": "Ver en el mapa",
    "Walk the results together": "Revisan los resultados juntos",
    "What Kissimmee": "Lo que dicen los",
    "homeowners say": "dueños de casa en Kissimmee",
    "work": "real",
    "Your project, start": "Tu proyecto, de inicio",
    "to finish": "hasta el final",
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
