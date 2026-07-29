import re
import shutil

SLUG = "adaina-cleaning-port-st-lucie"
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
# 2. Paleta: plum-pink (lashbloom) -> aqua/mint fresco (Adaina Cleaning)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#2f8f7a"),  # accent-deep
    ("#5c2140", "#123f34"),  # btn-3d sole darkest
    ("#f0bed7", "#a9e2d1"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#faf8f0"),  # bg
    ("#c47a9c", "#6cc4ab"),  # accent-mid
    ("#8a5573", "#1f6b5a"),  # dark-band btn shadow deep
    ("#f3e0ea", "#e3f2ea"),  # bg-2 / accent-soft
    ("#d9a8c2", "#8ed4bd"),  # orb-b
    ("#7d3457", "#1a5c4d"),  # dark mid
    ("#5f2c48", "#1d5c4d"),  # step-num gradient end
    ("#33222c", "#20302c"),  # ink
    ("#fbf3f8", "#f2faf6"),  # tile-cap text near-white
    ("#fbeff5", "#eafaf3"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#cdeee1"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#eef6f1"),  # theme-color meta
    ("#f2d5e3", "#cdeee0"),  # orb-a
    ("#f2cfe0", "#c2ebd9"),  # dark-band shimmer last stop
    ("#efd0e0", "#c8ecdd"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#a9dfcb"),  # orb-c pale
    ("#dc9dbe", "#57b89a"),  # scroll-progress end stop
    ("#d3a2bc", "#8ecdb8"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#3fae91"),  # shimmer stop
    ("#b25a85", "#237a63"),  # shimmer stop
    ("#2a1722", "#0b2420"),  # cta-final bg gradient start
    ("#1f0f18", "#071a16"),  # cta-final bg gradient end
    ("#1c0f16", "#081b17"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(47,143,122"),   # accent-deep alpha
    ("rgba(51,34,44", "rgba(32,48,44"),       # ink alpha
    ("rgba(240,190,215", "rgba(169,226,209"), # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(18,63,52"),       # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(250,248,240"), # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(26,92,77"),      # dark mid alpha
    ("rgba(253,246,250", "rgba(238,250,244"), # surface alpha
    ("rgba(40,16,30", "rgba(9,30,25"),        # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(169,226,209"), # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(75,163,140"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel:. IG real, sin Booksy.
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+17728285555"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/adainacleaning/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@adainacleaning"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=893+SW+Koler+Ave,+Port+St.+Lucie,+FL+34953"
NEW_FB_URL = "https://www.facebook.com/AdainaCleaning/"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Adaina Cleaning Services · House Cleaning in Port St. Lucie, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Adaina Cleaning Services, Port St. Lucie FL: recurring, deep and move-in/move-out house cleaning with a perfect 5.0 across 73 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Adaina Cleaning Services · House Cleaning in Port St. Lucie, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Recurring, deep and move-in/move-out house cleaning. 5.0 on Google with 73 reviews. Call for a free estimate." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-clean-bedroom.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo-icon.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Adaina Cleaning Services",
    "description": "Residential and commercial house cleaning company in Port St. Lucie, FL: recurring weekly/biweekly/monthly cleaning, whole-house deep cleaning, move-in/move-out cleaning and office cleaning, licensed, insured and uniformed.",
    "address": { "@type": "PostalAddress", "streetAddress": "893 SW Koler Ave", "addressLocality": "Port St. Lucie", "addressRegion": "FL", "postalCode": "34953", "addressCountry": "US" },
    "telephone": "+1-772-828-5555",
    "sameAs": ["https://www.instagram.com/adainacleaning/", "https://www.facebook.com/AdainaCleaning/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "73", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Cleaning services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Recurring House Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Deep Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Move-In / Move-Out Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Commercial / Office Cleaning" } }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,122,0.35)]" />',
    '<img src="assets/logo-icon.jpg" alt="Adaina Cleaning Services" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,122,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Adaina <span class="text-[color:var(--accent-deep)]">Cleaning</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">AC</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Adaina Cleaning</span>')
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
    'data-es="Port St. Lucie, FL · House Cleaning" data-en="Port St. Lucie, FL · House Cleaning">Port St. Lucie, FL · House Cleaning</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Spotless homes, honest people." data-en="Spotless homes, honest people.">Spotless homes, honest people.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Cleaning you can" data-en="Cleaning you can">Cleaning you can</span><br /><span data-es="actually " data-en="actually ">actually </span><span class="text-shine" data-es="trust" data-en="trust">trust</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Adaina Cleaning Services has been cleaning homes and offices around Port St. Lucie since 2017: recurring visits, deep cleans and move-in/move-out cleaning from a licensed, insured, uniformed team that reviewers describe as honest and dependable, every time." data-en="Adaina Cleaning Services has been cleaning homes and offices around Port St. Lucie since 2017: recurring visits, deep cleans and move-in/move-out cleaning from a licensed, insured, uniformed team that reviewers describe as honest and dependable, every time.">Adaina Cleaning Services has been cleaning homes and offices around Port St. Lucie since 2017: recurring visits, deep cleans and move-in/move-out cleaning from a licensed, insured, uniformed team that reviewers describe as honest and dependable, every time.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 73 reviews on Google" data-en="5.0 · 73 reviews on Google">5.0 · 73 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (772) 828-5555" data-en="Call (772) 828-5555">Call (772) 828-5555</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <span data-es="Get directions" data-en="Get directions">Get directions</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-clean-bedroom.jpg" alt="A real client bedroom, freshly cleaned and made up by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">8am - 5pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Mon-Fri · Free estimates" data-en="Mon-Fri · Free estimates">Mon-Fri · Free estimates</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="73">73</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl"><span data-es="Since" data-en="Since">Since</span> <span class="text-shine">2017</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Registered in Port St. Lucie" data-en="Registered in Port St. Lucie">Registered in Port St. Lucie</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">Licensed <span class="text-shine">&amp;</span> Insured</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Uniformed cleaning team" data-en="Uniformed cleaning team">Uniformed cleaning team</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Port St. Lucie</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">893 SW Koler Ave</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Recurring Cleaning"),
    ("Hybrid Set", "Deep Cleaning"),
    ("Volume Set", "Move-In / Move-Out"),
    ("Mega Volume", "Commercial Cleaning"),
    ("Bottom Lashes", "Licensed &amp; Insured"),
    ("West Palm Beach, FL", "Port St. Lucie, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/before-carpet.jpg" alt="A real client carpet before a deep clean by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/before-sofa.jpg" alt="A real client bed frame before a deep clean by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Nearly a decade of" data-en="Nearly a decade of">Nearly a decade of</span><br /><span class="text-shine" data-es="honest work" data-en="honest work">honest work</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Adaina Mendonca registered Adaina Cleaning Services in Port St. Lucie back in 2017, and has been cleaning homes and offices around the city ever since. Her uniformed, licensed and insured team handles recurring visits, deep cleans, move-in/move-out cleaning and commercial cleaning, with a free estimate and no contract required to get started." data-en="Adaina Mendonca registered Adaina Cleaning Services in Port St. Lucie back in 2017, and has been cleaning homes and offices around the city ever since. Her uniformed, licensed and insured team handles recurring visits, deep cleans, move-in/move-out cleaning and commercial cleaning, with a free estimate and no contract required to get started.">Adaina Mendonca registered Adaina Cleaning Services in Port St. Lucie back in 2017, and has been cleaning homes and offices around the city ever since. Her uniformed, licensed and insured team handles recurring visits, deep cleans, move-in/move-out cleaning and commercial cleaning, with a free estimate and no contract required to get started.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a perfect 5.0 across 73 Google reviews, and neighbors on Nextdoor and Yelp who keep calling Adaina\'s team honest, dependable and hard working, cleaning every corner of the house." data-en="The result: a perfect 5.0 across 73 Google reviews, and neighbors on Nextdoor and Yelp who keep calling Adaina\'s team honest, dependable and hard working, cleaning every corner of the house.">The result: a perfect 5.0 across 73 Google reviews, and neighbors on Nextdoor and Yelp who keep calling Adaina\'s team honest, dependable and hard working, cleaning every corner of the house.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="73">73</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2017</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Cleaning since" data-en="Cleaning since">Cleaning since</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,122,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo-icon.jpg" alt="Adaina Cleaning Services" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,143,122,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Adaina · <span class="text-[color:var(--ink-40)]" data-es="Owner" data-en="Owner">Owner</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="From call to" data-en="From call to">From call to</span> <span class="text-shine" data-es="clean home" data-en="clean home">clean home</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Free estimate" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (772) 828-5555 and tell Adaina's team about your home, no contract required, ever." data-en="Call (772) 828-5555 and tell Adaina's team about your home, no contract required, ever.">Call (772) 828-5555 and tell Adaina's team about your home, no contract required, ever.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Uniformed team arrives" data-en="Uniformed team arrives">Uniformed team arrives</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A licensed, insured, uniformed cleaner arrives on schedule and gets straight to work, room by room." data-en="A licensed, insured, uniformed cleaner arrives on schedule and gets straight to work, room by room.">A licensed, insured, uniformed cleaner arrives on schedule and gets straight to work, room by room.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Every corner, done right" data-en="Every corner, done right">Every corner, done right</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Counters, floors, bathrooms and kitchens: the same deep-clean standard reviewers describe as spotless, every single visit." data-en="Counters, floors, bathrooms and kitchens: the same deep-clean standard reviewers describe as spotless, every single visit.">Counters, floors, bathrooms and kitchens: the same deep-clean standard reviewers describe as spotless, every single visit.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="You come home to clean" data-en="You come home to clean">You come home to clean</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Weekly, biweekly, monthly or a one-time deep clean, your home is left the way the reviews describe: honest work, done right." data-en="Weekly, biweekly, monthly or a one-time deep clean, your home is left the way the reviews describe: honest work, done right.">Weekly, biweekly, monthly or a one-time deep clean, your home is left the way the reviews describe: honest work, done right.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; solo nombres, sin precios inventados)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Cleaning for" data-en="Cleaning for">Cleaning for</span> <span class="text-shine">every home</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Free estimates by phone. Every visit is tailored to the size of your home and how deep a clean it needs." data-en="Free estimates by phone. Every visit is tailored to the size of your home and how deep a clean it needs.">Free estimates by phone. Every visit is tailored to the size of your home and how deep a clean it needs.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Everyday care" data-en="Everyday care">Everyday care</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Recurring House Cleaning" data-en="Recurring House Cleaning">Recurring House Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Weekly, biweekly or monthly visits to keep every room dusted, vacuumed, mopped and wiped down, on a schedule that fits your home." data-en="Weekly, biweekly or monthly visits to keep every room dusted, vacuumed, mopped and wiped down, on a schedule that fits your home.">Weekly, biweekly or monthly visits to keep every room dusted, vacuumed, mopped and wiped down, on a schedule that fits your home.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(47,143,122,0.4); box-shadow: 0 18px 50px rgba(32,48,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Deep Cleaning" data-en="Deep Cleaning">Deep Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A whole-house deep clean, top to bottom: inside the fridge and oven, baseboards, window sills and every corner a regular clean skips." data-en="A whole-house deep clean, top to bottom: inside the fridge and oven, baseboards, window sills and every corner a regular clean skips.">A whole-house deep clean, top to bottom: inside the fridge and oven, baseboards, window sills and every corner a regular clean skips.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Moving day" data-en="Moving day">Moving day</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Move-In / Move-Out Cleaning" data-en="Move-In / Move-Out Cleaning">Move-In / Move-Out Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="An empty home cleaned from top to bottom before you move in, or spotless for the next owner or your final walkthrough." data-en="An empty home cleaned from top to bottom before you move in, or spotless for the next owner or your final walkthrough.">An empty home cleaned from top to bottom before you move in, or spotless for the next owner or your final walkthrough.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="For businesses" data-en="For businesses">For businesses</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Commercial &amp; Office Cleaning" data-en="Commercial &amp; Office Cleaning">Commercial &amp; Office Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Recurring cleaning for offices and small businesses around Port St. Lucie, on the schedule that keeps your space presentable." data-en="Recurring cleaning for offices and small businesses around Port St. Lucie, on the schedule that keeps your space presentable.">Recurring cleaning for offices and small businesses around Port St. Lucie, on the schedule that keeps your space presentable.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Every Visit Includes" data-en="Every Visit Includes">Every Visit Includes</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Dusting &amp; wipe-down" data-en="Dusting &amp; wipe-down">Dusting &amp; wipe-down</li>
            <li class="flex items-center gap-2" data-es="Vacuum &amp; mop all floors" data-en="Vacuum &amp; mop all floors">Vacuum &amp; mop all floors</li>
            <li class="flex items-center gap-2" data-es="Bathrooms disinfected" data-en="Bathrooms disinfected">Bathrooms disinfected</li>
            <li class="flex items-center gap-2" data-es="Kitchen counters &amp; sink" data-en="Kitchen counters &amp; sink">Kitchen counters &amp; sink</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Deep Clean Adds" data-en="Deep Clean Adds">Deep Clean Adds</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Inside oven &amp; fridge" data-en="Inside oven &amp; fridge">Inside oven &amp; fridge</li>
            <li class="flex items-center gap-2" data-es="Baseboards &amp; window sills" data-en="Baseboards &amp; window sills">Baseboards &amp; window sills</li>
            <li class="flex items-center gap-2" data-es="Ceiling fans &amp; vents" data-en="Ceiling fans &amp; vents">Ceiling fans &amp; vents</li>
            <li class="flex items-center gap-2" data-es="Cabinet fronts" data-en="Cabinet fronts">Cabinet fronts</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Good To Know" data-en="Good To Know">Good To Know</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Free estimates" data-en="Free estimates">Free estimates</li>
            <li class="flex items-center gap-2" data-es="Licensed &amp; insured" data-en="Licensed &amp; insured">Licensed &amp; insured</li>
            <li class="flex items-center gap-2" data-es="No contract required" data-en="No contract required">No contract required</li>
            <li class="flex items-center gap-2" data-es="Professional uniformed staff" data-en="Professional uniformed staff">Professional uniformed staff</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on home size and how deep a clean it needs. Call (772) 828-5555 for a free, exact quote." data-en="Pricing depends on home size and how deep a clean it needs. Call (772) 828-5555 for a free, exact quote.">Pricing depends on home size and how deep a clean it needs. Call (772) 828-5555 for a free, exact quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex, 6 fotos reales curadas)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real homes," data-en="Real homes,">Real homes,</span> <span class="text-shine" data-es="real results" data-en="real results">real results</span>')
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

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Una limpieza real de mudanza, de principio a fin" data-en="A real move-day clean, start to finish">A real move-day clean, start to finish</span><img src="assets/gallery-before-after.jpg" alt="A real client bedroom before and after a cleaning visit by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Un hogar recien terminado" data-en="A home, freshly done">A home, freshly done</span><img src="assets/after-living-room.jpg" alt="A tidy, freshly cleaned living and dining room" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cada cocina, a fondo" data-en="Every kitchen, deep cleaned">Every kitchen, deep cleaned</span><img src="assets/before-kitchen.jpg" alt="A real client kitchen before a cleaning visit by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Recamaras, de arriba a abajo" data-en="Bedrooms, top to bottom">Bedrooms, top to bottom</span><img src="assets/before-bedroom.jpg" alt="A real client bedroom before a cleaning visit by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Baños dejados impecables" data-en="Bathrooms scrubbed spotless">Bathrooms scrubbed spotless</span><img src="assets/before-tub.jpg" alt="A real client bathtub before a deep clean by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Hasta el microondas" data-en="Even the microwave">Even the microwave</span><img src="assets/before-microwave.jpg" alt="A real client microwave interior before a deep clean by Adaina Cleaning Services" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What our" data-en="What our">What our</span> <span class="text-shine" data-es="neighbors say" data-en="neighbors say">neighbors say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 73 reviews on Google" data-en="5.0 out of 5 · 73 reviews on Google">5.0 out of 5 · 73 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Adaina Cleaning Services are great. Very honest &amp; they do a great job!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">C.G.</span> <span class="text-[color:var(--ink-40)]">· Nextdoor</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent service, would highly recommend. Hard working team cleaned every corner of my house."</blockquote>
          <figcaption class="text-sm"><span class="text-[color:var(--ink-40)]" data-es="Yelp review" data-en="Yelp review">Yelp review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I've been using Adaina's Cleaning Service since 2012. Their trustworthiness is their best asset."</blockquote>
          <figcaption class="text-sm"><span class="text-[color:var(--ink-40)]" data-es="Thumbtack review" data-en="Thumbtack review">Thumbtack review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=Adaina+Cleaning+Services+Port+St+Lucie+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 73 reviews on Google" data-en="Read all 73 reviews on Google">Read all 73 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Port St. Lucie</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,122,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">893 SW Koler Ave, Port St. Lucie, FL 34953</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,122,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,122,0.4)]" href="tel:+17728285555" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Friday, 8:00 AM to 5:00 PM. Closed Saturday and Sunday." data-en="Monday to Friday, 8:00 AM to 5:00 PM. Closed Saturday and Sunday.">Monday to Friday, 8:00 AM to 5:00 PM. Closed Saturday and Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,122,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (772) 828-5555" data-en="Call (772) 828-5555">Call (772) 828-5555</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,122,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See real before-and-after cleans and message any questions before your visit." data-en="See real before-and-after cleans and message any questions before your visit.">See real before-and-after cleans and message any questions before your visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,143,122,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Adaina Cleaning Services, 893 SW Koler Ave, Port St. Lucie FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Spotless homes, honest people." data-en="Spotless homes, honest people.">Spotless homes, honest people.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Ready for a" data-en="Ready for a">Ready for a</span> <span class="text-shine" data-es="cleaner home?" data-en="cleaner home?">cleaner home?</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (772) 828-5555 for a free estimate. No contract required, ever." data-en="Call (772) 828-5555 for a free estimate. No contract required, ever.">Call (772) 828-5555 for a free estimate. No contract required, ever.</p>')
rep('''<a href="tel:+17728285555" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="tel:+17728285555" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (772) 828-5555" data-en="Call (772) 828-5555">Call (772) 828-5555</a>
        <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Get directions" data-en="Get directions">Get directions</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Adaina</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,226,209,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo-icon.jpg" alt="Adaina Cleaning Services" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,226,209,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Adaina Cleaning</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Residential &amp; commercial cleaning in Port St. Lucie, FL. Licensed, insured, by appointment." data-en="Residential &amp; commercial cleaning in Port St. Lucie, FL. Licensed, insured, by appointment.">Residential &amp; commercial cleaning in Port St. Lucie, FL. Licensed, insured, by appointment.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="tel:+17728285555" target="_blank" rel="noopener" class="hover:text-[#a9e2d1]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>893 SW Koler Ave, Port St. Lucie, FL 34953</p>
        <p><a href="tel:+17728285555" class="hover:text-[#a9e2d1]" data-es="Call (772) 828-5555" data-en="Call (772) 828-5555">Call (772) 828-5555</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9e2d1]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9e2d1]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9e2d1]">Facebook · Adaina Cleaning Services</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Adaina Cleaning Services.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="tel:+17728285555" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+17728285555" class="book-float" aria-label="Call Adaina Cleaning Services">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 20. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace('href="tel:+17728285555" target="_blank" rel="noopener"', 'href="tel:+17728285555"')
print("CLEANUP tel links done")


# ---------------------------------------------------------------------------
# 21. Traduccion ES real para todos los textos NUEVOS (bilingue obligatorio)
# ---------------------------------------------------------------------------
T = {
    "5.0 · 73 reviews on Google": "5.0 · 73 reseñas en Google",
    "5.0 out of 5 · 73 reviews on Google": "5.0 de 5 · 73 reseñas en Google",
    "A licensed, insured, uniformed cleaner arrives on schedule and gets straight to work, room by room.":
        "Una limpiadora licenciada, asegurada y uniformada llega a la hora acordada y se pone a trabajar de inmediato, cuarto por cuarto.",
    "A real move-day clean, start to finish": "Una limpieza real de mudanza, de principio a fin",
    "A tidy, freshly cleaned living and dining room": "Una sala y comedor ordenados y recién limpiados",
    "A whole-house deep clean, top to bottom: inside the fridge and oven, baseboards, window sills and every corner a regular clean skips.":
        "Una limpieza profunda de toda la casa, de arriba a abajo: dentro del refrigerador y el horno, zócalos, marcos de ventanas y cada rincón que una limpieza regular deja pasar.",
    "A home, freshly done": "Un hogar recién terminado",
    "Adaina Cleaning Services are great. Very honest &amp; they do a great job!": "Adaina Cleaning Services are great. Very honest &amp; they do a great job!",
    "Adaina Mendonca registered Adaina Cleaning Services in Port St. Lucie back in 2017, and has been cleaning homes and offices around the city ever since. Her uniformed, licensed and insured team handles recurring visits, deep cleans, move-in/move-out cleaning and commercial cleaning, with a free estimate and no contract required to get started.":
        "Adaina Mendonca registró Adaina Cleaning Services en Port St. Lucie en 2017, y desde entonces ha estado limpiando casas y oficinas por toda la ciudad. Su equipo uniformado, licenciado y asegurado se encarga de visitas recurrentes, limpiezas profundas, mudanzas y limpieza comercial, con cotización gratis y sin contrato para empezar.",
    "Adaina Cleaning Services has been cleaning homes and offices around Port St. Lucie since 2017: recurring visits, deep cleans and move-in/move-out cleaning from a licensed, insured, uniformed team that reviewers describe as honest and dependable, every time.":
        "Adaina Cleaning Services lleva desde 2017 limpiando casas y oficinas por todo Port St. Lucie: visitas recurrentes, limpiezas profundas y limpiezas de mudanza de un equipo licenciado, asegurado y uniformado que las reseñas describen como honesto y confiable, cada vez.",
    "An empty home cleaned from top to bottom before you move in, or spotless for the next owner or your final walkthrough.":
        "Una casa vacía limpiada de arriba a abajo antes de que te mudes, o impecable para el próximo dueño o tu inspección final.",
    "Address": "Dirección",
    "Baseboards &amp; window sills": "Zócalos y marcos de ventana",
    "Bathrooms disinfected": "Baños desinfectados",
    "Bathrooms scrubbed spotless": "Baños dejados impecables",
    "Bedrooms, top to bottom": "Recámaras, de arriba a abajo",
    "Cabinet fronts": "Frentes de gabinetes",
    "Call": "Llamar",
    "Call (772) 828-5555": "Llama al (772) 828-5555",
    "Call (772) 828-5555 and tell Adaina's team about your home, no contract required, ever.":
        "Llama al (772) 828-5555 y cuéntale al equipo de Adaina sobre tu casa, sin contrato jamás.",
    "Call (772) 828-5555 for a free estimate. No contract required, ever.":
        "Llama al (772) 828-5555 para una cotización gratis. Sin contrato jamás.",
    "Call for a quote": "Llama para cotizar",
    "Call now": "Llama ahora",
    "Ceiling fans &amp; vents": "Ventiladores de techo y ductos",
    "Cleaning for": "Limpieza para",
    "Cleaning you can": "Una limpieza en la que",
    "Commercial &amp; Office Cleaning": "Commercial &amp; Office Cleaning",
    "Contact": "Contacto",
    "Counters, floors, bathrooms and kitchens: the same deep-clean standard reviewers describe as spotless, every single visit.":
        "Cubiertas, pisos, baños y cocinas: el mismo estándar de limpieza profunda que las reseñas describen como impecable, en cada visita.",
    "Deep Clean Adds": "La Limpieza Profunda Suma",
    "Dusting &amp; wipe-down": "Sacudido y limpieza de superficies",
    "Even the microwave": "Hasta el microondas",
    "Every Visit Includes": "Cada Visita Incluye",
    "Every kitchen, deep cleaned": "Cada cocina, a fondo",
    "Excellent service, would highly recommend. Hard working team cleaned every corner of my house.":
        "Excellent service, would highly recommend. Hard working team cleaned every corner of my house.",
    "Follow": "Síguenos",
    "For businesses": "Para negocios",
    "Free estimate": "Cotización gratis",
    "Free estimates": "Cotizaciones gratis",
    "From call to": "De la llamada a",
    "Good To Know": "Bueno Saberlo",
    "Hours": "Horario",
    "I've been using Adaina's Cleaning Service since 2012. Their trustworthiness is their best asset.":
        "I've been using Adaina's Cleaning Service since 2012. Their trustworthiness is their best asset.",
    "Inside oven &amp; fridge": "Dentro del horno y el refrigerador",
    "Kitchen counters &amp; sink": "Cubiertas y fregadero de cocina",
    "Licensed &amp; insured": "Licenciada y asegurada",
    "Licensed": "Licenciada",
    "Insured": "Asegurada",
    "Most requested": "Lo más solicitado",
    "Moving day": "Día de mudanza",
    "Nearly a decade of": "Casi una década de",
    "No contract required": "Sin contrato requerido",
    "Open": "Abierto",
    "Owner": "Dueña",
    "Pricing depends on home size and how deep a clean it needs. Call (772) 828-5555 for a free, exact quote.":
        "El precio depende del tamaño de la casa y qué tan profunda debe ser la limpieza. Llama al (772) 828-5555 para una cotización exacta y gratis.",
    "Professional uniformed staff": "Personal uniformado y profesional",
    "Read all 73 reviews on Google": "Lee las 73 reseñas en Google",
    "Recurring House Cleaning": "Recurring House Cleaning",
    "Registered in Port St. Lucie": "Registrada en Port St. Lucie",
    "Serving": "Sirviendo a",
    "See real before-and-after cleans and message any questions before your visit.":
        "Mira limpiezas reales de antes y después, y escribe cualquier duda antes de tu visita.",
    "Since": "Desde",
    "Spotless homes, honest people.": "Hogares impecables, gente honesta.",
    "Thumbtack review": "Reseña de Thumbtack",
    "Uniformed cleaning team": "Equipo de limpieza uniformado",
    "Uniformed team arrives": "Llega el equipo uniformado",
    "Weekly, biweekly, monthly or a one-time deep clean, your home is left the way the reviews describe: honest work, done right.":
        "Semanal, quincenal, mensual o una limpieza profunda única, tu casa queda tal como describen las reseñas: trabajo honesto, bien hecho.",
    "You come home to clean": "Llegas a una casa limpia",
    "Yelp review": "Reseña de Yelp",
    "actually ": "realmente ",
    "cleaner home?": "una casa más limpia?",
    "clean home": "casa limpia",
    "trust": "confías",
    "Recurring Cleaning": "Limpieza Recurrente",
    "Deep Cleaning": "Limpieza Profunda",
    "Move-In / Move-Out": "Mudanza",
    "Commercial Cleaning": "Limpieza Comercial",
    "Licensed &amp; Insured": "Licenciada y Asegurada",
    "Port St. Lucie, FL": "Port St. Lucie, FL",
    "Weekly, biweekly or monthly visits to keep every room dusted, vacuumed, mopped and wiped down, on a schedule that fits your home.":
        "Visitas semanales, quincenales o mensuales para mantener cada cuarto sacudido, aspirado, trapeado y limpio, en el horario que le acomode a tu casa.",
    "Recurring cleaning for offices and small businesses around Port St. Lucie, on the schedule that keeps your space presentable.":
        "Limpieza recurrente para oficinas y pequeños negocios de Port St. Lucie, en el horario que mantiene tu espacio presentable.",
    "Free estimates by phone. Every visit is tailored to the size of your home and how deep a clean it needs.":
        "Cotizaciones gratis por teléfono. Cada visita se ajusta al tamaño de tu casa y qué tan profunda debe ser la limpieza.",
    "Cleaning for every home": "Limpieza para cada hogar",
    "Get directions": "Cómo llegar",
    "Every kitchen, deep cleaned.": "Cada cocina, a fondo.",
    "Port St. Lucie, FL · House Cleaning": "Port St. Lucie, FL · Limpieza de Casas",
    "The result: a perfect 5.0 across 73 Google reviews, and neighbors on Nextdoor and Yelp who keep calling Adaina's team honest, dependable and hard working, cleaning every corner of the house.":
        "El resultado: un 5.0 perfecto en 73 reseñas de Google, y vecinos en Nextdoor y Yelp que siguen describiendo al equipo de Adaina como honesto, confiable y trabajador, limpiando cada rincón de la casa.",
}

_missing = []
for _en, _es in T.items():
    _pat = f'data-es="{_en}" data-en="{_en}"'
    _new = f'data-es="{_es}" data-en="{_en}"'
    if _pat in h:
        h = h.replace(_pat, _new)
    else:
        _missing.append(_en)
if _missing:
    print("WARNING missing ES translations for:", _missing)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", PATH)
