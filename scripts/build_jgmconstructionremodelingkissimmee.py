import re
import shutil

SLUG = "jgm-construction-remodeling-kissimmee"
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
# 2. Paleta: plum-pink (lashbloom) -> terracota/cobre calido (JGM Construction)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#b5651d"),  # accent-deep
    ("#5c2140", "#6b3510"),  # btn-3d sole darkest
    ("#f0bed7", "#e8b788"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#faf3ea"),  # bg
    ("#c47a9c", "#d68a4c"),  # accent-mid
    ("#8a5573", "#8a4a1f"),  # dark-band btn shadow deep
    ("#f3e0ea", "#f2e4d0"),  # bg-2 / accent-soft
    ("#d9a8c2", "#e0b988"),  # orb-b
    ("#7d3457", "#7a4419"),  # dark mid
    ("#5f2c48", "#5c3012"),  # step-num gradient end
    ("#33222c", "#2c2118"),  # ink
    ("#fbf3f8", "#fbf3ea"),  # tile-cap text near-white
    ("#fbeff5", "#f7e9d8"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#ecd3b0"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#f7f0e4"),  # theme-color meta
    ("#f2d5e3", "#f0d9b8"),  # orb-a
    ("#f2cfe0", "#e8c99a"),  # dark-band shimmer last stop
    ("#efd0e0", "#e6cba0"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#e8cca0"),  # orb-c pale
    ("#dc9dbe", "#d99a52"),  # scroll-progress end stop
    ("#d3a2bc", "#d4a06a"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#c9812f"),  # shimmer stop
    ("#b25a85", "#96481a"),  # shimmer stop
    ("#2a1722", "#241708"),  # cta-final bg gradient start
    ("#1f0f18", "#180f05"),  # cta-final bg gradient end
    ("#1c0f16", "#170e06"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(181,101,29"),   # accent-deep alpha
    ("rgba(51,34,44", "rgba(44,33,24"),       # ink alpha
    ("rgba(240,190,215", "rgba(232,183,136"), # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(107,53,16"),      # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(250,243,234"), # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(122,68,25"),     # dark mid alpha
    ("rgba(253,246,250", "rgba(247,233,216"), # surface alpha
    ("rgba(40,16,30", "rgba(35,20,10"),       # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(232,183,136"), # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(224,185,136"), # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel: + maps. IG real: @jgmconstruction.fl
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+14077472700"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/jgmconstruction.fl/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@jgmconstruction.fl"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=3826+Bay+Club+Cir+Unit+204,+Kissimmee,+FL+34741"
NEW_FB_URL = "https://www.facebook.com/p/JGM-Construction-Remodeling-Llc-100091245767944/"
NEW_REVIEWS_URL = "https://reviews.birdeye.com/jgm-construction-remodeling-llc-167560209423826"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>JGM Construction &amp; Remodeling · Kitchen &amp; Bath Remodeling in Kissimmee, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="JGM Construction &amp; Remodeling LLC, Kissimmee FL: kitchen and bathroom remodeling, flooring, drywall repair and painting. 4.9 stars across 41 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="JGM Construction &amp; Remodeling · Kitchen &amp; Bath Remodeling in Kissimmee, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Kitchen and bathroom remodeling, flooring and drywall repair. 4.9 on Google with 41 reviews. Call for a free estimate." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-bathroom.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-bathroom.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "JGM Construction & Remodeling LLC",
    "description": "Construction and remodeling company in Kissimmee, FL run by Juan P. Gonzalez Miranda: kitchen and bathroom remodeling, flooring and tile, drywall repair and interior/exterior painting.",
    "address": { "@type": "PostalAddress", "streetAddress": "3826 Bay Club Cir Unit 204", "addressLocality": "Kissimmee", "addressRegion": "FL", "postalCode": "34741", "addressCountry": "US" },
    "telephone": "+1-407-747-2700",
    "email": "jgmconstruction.fl@hotmail.com",
    "sameAs": ["https://www.instagram.com/jgmconstruction.fl/", "''' + NEW_FB_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "41", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Construction & remodeling services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Kitchen Remodeling" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bathroom Remodeling" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Flooring & Tile Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Drywall Repair & Painting" } }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,101,29,0.35)]" />',
    '<img src="assets/hero-bathroom.jpg" alt="JGM Construction &amp; Remodeling" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,101,29,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">JGM <span class="text-[color:var(--accent-deep)]">Construction</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">JGM</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">JGM Construction</span>')
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
    'data-es="Kissimmee, FL · Construction &amp; Remodeling" data-en="Kissimmee, FL · Construction &amp; Remodeling">Kissimmee, FL · Construction &amp; Remodeling</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Your project is our business." data-en="Your project is our business.">Your project is our business.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Kitchens and baths," data-en="Kitchens and baths,">Kitchens and baths,</span><br /><span data-es="built and finished " data-en="built and finished ">built and finished </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Juan Gonzalez Miranda and the JGM Construction &amp; Remodeling team handle kitchen and bathroom remodels, flooring, drywall repair and painting across Kissimmee and Central Florida, with the kind of clean, careful work that earned a 4.9 rating on Google." data-en="Juan Gonzalez Miranda and the JGM Construction &amp; Remodeling team handle kitchen and bathroom remodels, flooring, drywall repair and painting across Kissimmee and Central Florida, with the kind of clean, careful work that earned a 4.9 rating on Google.">Juan Gonzalez Miranda and the JGM Construction &amp; Remodeling team handle kitchen and bathroom remodels, flooring, drywall repair and painting across Kissimmee and Central Florida, with the kind of clean, careful work that earned a 4.9 rating on Google.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 41 reviews on Google" data-en="4.9 · 41 reviews on Google">4.9 · 41 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (407) 747-2700" data-en="Call (407) 747-2700">Call (407) 747-2700</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-bathroom.jpg" alt="A finished bathroom remodel by JGM Construction &amp; Remodeling, with a freestanding tub and new vanity" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Free estimate" data-en="Free estimate">Free estimate</p>
            <p class="font-display text-lg">Kitchens &amp; Baths</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Flooring · Drywall · Paint" data-en="Flooring · Drywall · Paint">Flooring · Drywall · Paint</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="41">41</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Kitchens <span class="text-shine">&amp;</span> Baths</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Flooring · Drywall · Paint" data-en="Flooring · Drywall · Paint">Flooring · Drywall · Paint</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span data-es="Since" data-en="Since">Since</span> <span class="text-shine">2020</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Juan building in Central Florida" data-en="Juan building in Central Florida">Juan building in Central Florida</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Kissimmee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Bay Club Cir</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Kitchen Remodeling"),
    ("Hybrid Set", "Bathroom Remodeling"),
    ("Volume Set", "Flooring &amp; Tile"),
    ("Mega Volume", "Drywall Repair"),
    ("Bottom Lashes", "Interior Painting"),
    ("West Palm Beach, FL", "Kissimmee, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-jobsite-card.jpg" alt="Juan Gonzalez Miranda on a jobsite in Kissimmee holding a JGM Construction &amp; Remodeling business card" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-tile-floor.jpg" alt="Marble-look tile flooring installed by JGM Construction &amp; Remodeling" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Family-run," data-en="Family-run,">Family-run,</span><br /><span class="text-shine" data-es="detail-first" data-en="detail-first">detail-first</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Juan P. Gonzalez Miranda founded JGM Construction &amp; Remodeling LLC in Kissimmee in 2020, and has run it since as a hands-on, quality by square foot operation. He personally shows up on jobsites, from a kitchen or bathroom remodel to a drywall repair or a concrete walkway, and stays in touch with homeowners until the work is done right." data-en="Juan P. Gonzalez Miranda founded JGM Construction &amp; Remodeling LLC in Kissimmee in 2020, and has run it since as a hands-on, quality by square foot operation. He personally shows up on jobsites, from a kitchen or bathroom remodel to a drywall repair or a concrete walkway, and stays in touch with homeowners until the work is done right.">Juan P. Gonzalez Miranda founded JGM Construction &amp; Remodeling LLC in Kissimmee in 2020, and has run it since as a hands-on, quality by square foot operation. He personally shows up on jobsites, from a kitchen or bathroom remodel to a drywall repair or a concrete walkway, and stays in touch with homeowners until the work is done right.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.9-star rating across 41 Google reviews, with homeowners specifically praising how fast, honest and thorough Juan is, never cutting corners on the work." data-en="The result: a 4.9-star rating across 41 Google reviews, with homeowners specifically praising how fast, honest and thorough Juan is, never cutting corners on the work.">The result: a 4.9-star rating across 41 Google reviews, with homeowners specifically praising how fast, honest and thorough Juan is, never cutting corners on the work.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="41">41</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2020</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Building since" data-en="Building since">Building since</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,101,29,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/hero-bathroom.jpg" alt="JGM Construction &amp; Remodeling" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,101,29,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Juan Gonzalez Miranda · <span class="text-[color:var(--ink-40)]" data-es="Owner / Manager" data-en="Owner / Manager">Owner / Manager</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your project, start" data-en="Your project, start">Your project, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Free estimate" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (407) 747-2700 or email to walk through the project and get a clear, honest scope of work." data-en="Call (407) 747-2700 or email to walk through the project and get a clear, honest scope of work.">Call (407) 747-2700 or email to walk through the project and get a clear, honest scope of work.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Plan &amp; materials" data-en="Plan &amp; materials">Plan &amp; materials</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Juan plans the job and sources materials suited to your kitchen, bathroom, floor or wall." data-en="Juan plans the job and sources materials suited to your kitchen, bathroom, floor or wall.">Juan plans the job and sources materials suited to your kitchen, bathroom, floor or wall.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Clean, careful work" data-en="Clean, careful work">Clean, careful work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The crew works with a quality by square foot standard, keeping your home clean and protected while the job is underway." data-en="The crew works with a quality by square foot standard, keeping your home clean and protected while the job is underway.">The crew works with a quality by square foot standard, keeping your home clean and protected while the job is underway.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walkthrough &amp; warranty" data-en="Walkthrough &amp; warranty">Walkthrough &amp; warranty</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A final walkthrough with you before the job is called done, backed by a workmanship warranty." data-en="A final walkthrough with you before the job is called done, backed by a workmanship warranty.">A final walkthrough with you before the job is called done, backed by a workmanship warranty.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; solo nombres, sin precios inventados)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine">your home</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Every project is quoted after a walkthrough of your home. Call or email for a free, no-obligation estimate." data-en="Every project is quoted after a walkthrough of your home. Call or email for a free, no-obligation estimate.">Every project is quoted after a walkthrough of your home. Call or email for a free, no-obligation estimate.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Kitchen Remodeling" data-en="Kitchen Remodeling">Kitchen Remodeling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cabinets, countertops, sinks and layout updates, planned around how your kitchen actually gets used." data-en="Cabinets, countertops, sinks and layout updates, planned around how your kitchen actually gets used.">Cabinets, countertops, sinks and layout updates, planned around how your kitchen actually gets used.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(181,101,29,0.4); box-shadow: 0 18px 50px rgba(44,33,24,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Signature project" data-en="Signature project">Signature project</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Bathroom Remodeling" data-en="Bathroom Remodeling">Bathroom Remodeling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tubs, showers, vanities and tile, finished start to finish and backed by a workmanship warranty." data-en="Tubs, showers, vanities and tile, finished start to finish and backed by a workmanship warranty.">Tubs, showers, vanities and tile, finished start to finish and backed by a workmanship warranty.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Floors that last" data-en="Floors that last">Floors that last</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Flooring &amp; Tile" data-en="Flooring &amp; Tile">Flooring &amp; Tile</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tile installation for entryways, bathrooms and living spaces, laid clean and level." data-en="Tile installation for entryways, bathrooms and living spaces, laid clean and level.">Tile installation for entryways, bathrooms and living spaces, laid clean and level.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Fix &amp; finish" data-en="Fix &amp; finish">Fix &amp; finish</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Drywall Repair &amp; Painting" data-en="Drywall Repair &amp; Painting">Drywall Repair &amp; Painting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Drywall patching, popcorn ceiling removal and interior or exterior painting, cleaned and detailed." data-en="Drywall patching, popcorn ceiling removal and interior or exterior painting, cleaned and detailed.">Drywall patching, popcorn ceiling removal and interior or exterior painting, cleaned and detailed.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Remodeling" data-en="Remodeling">Remodeling</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Kitchen remodeling" data-en="Kitchen remodeling">Kitchen remodeling</li>
            <li class="flex items-center gap-2" data-es="Bathroom remodeling" data-en="Bathroom remodeling">Bathroom remodeling</li>
            <li class="flex items-center gap-2" data-es="Custom closets" data-en="Custom closets">Custom closets</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Drywall &amp; Paint" data-en="Drywall &amp; Paint">Drywall &amp; Paint</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Drywall repair" data-en="Drywall repair">Drywall repair</li>
            <li class="flex items-center gap-2" data-es="Popcorn ceiling removal" data-en="Popcorn ceiling removal">Popcorn ceiling removal</li>
            <li class="flex items-center gap-2" data-es="Interior &amp; exterior painting" data-en="Interior &amp; exterior painting">Interior &amp; exterior painting</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Finishing &amp; Repairs" data-en="Finishing &amp; Repairs">Finishing &amp; Repairs</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Flooring &amp; tile installation" data-en="Flooring &amp; tile installation">Flooring &amp; tile installation</li>
            <li class="flex items-center gap-2" data-es="Exterior door replacement" data-en="Exterior door replacement">Exterior door replacement</li>
            <li class="flex items-center gap-2" data-es="Fence replacement" data-en="Fence replacement">Fence replacement</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and materials. Call (407) 747-2700 or email for an exact quote." data-en="Pricing depends on scope and materials. Call (407) 747-2700 or email for an exact quote.">Pricing depends on scope and materials. Call (407) 747-2700 or email for an exact quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex; 5 fotos reales, adaptado a lo disponible)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="jobs" data-en="jobs">jobs</span>')
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
        <div class="frame zoomable col-span-2 aspect-[21/9] img-reveal"><span class="tile-cap" data-es="Baño remodelado en Kissimmee" data-en="A finished bathroom remodel in Kissimmee">A finished bathroom remodel in Kissimmee</span><img src="assets/hero-bathroom.jpg" alt="A finished bathroom remodel by JGM Construction &amp; Remodeling, with a freestanding tub and new vanity" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Piso de marmol recien instalado" data-en="Marble-look tile, freshly installed">Marble-look tile, freshly installed</span><img src="assets/about-tile-floor.jpg" alt="Marble-look tile flooring installed by JGM Construction &amp; Remodeling" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="En sitio para un colado de concreto" data-en="On site for a concrete walkway pour">On site for a concrete walkway pour</span><img src="assets/about-jobsite-card.jpg" alt="Juan Gonzalez Miranda on a jobsite in Kissimmee holding a JGM Construction &amp; Remodeling business card" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Esquina de drywall lista para acabado" data-en="Drywall corner bead, ready for finishing">Drywall corner bead, ready for finishing</span><img src="assets/gallery-drywall-corner.jpg" alt="Drywall corner bead repair in progress by JGM Construction &amp; Remodeling" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Reparacion de junta de drywall" data-en="Drywall seam repair in progress">Drywall seam repair in progress</span><img src="assets/gallery-drywall-seam.jpg" alt="Drywall seam repair in progress by JGM Construction &amp; Remodeling" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
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
    '<span data-es="What homeowners" data-en="What homeowners">What homeowners</span> <span class="text-shine" data-es="are saying" data-en="are saying">are saying</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★☆</span> &nbsp;<span data-es="4.9 out of 5 · 41 reviews on Google" data-en="4.9 out of 5 · 41 reviews on Google">4.9 out of 5 · 41 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Thank you Juan for your great customer service, you were fast, don't cut corners, and very efficient with your work thank you"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joseph Rodriguez</span> <span class="text-[color:var(--ink-40)]" data-es="· Reseña de Google" data-en="· Google review">· Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Juan was the best he made sure to do an efficient job. Our wall looks completely brand new, he worked in a timely matter and did an amazing job around the house. I highly recommended booking with him."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Clifford St. Fort</span> <span class="text-[color:var(--ink-40)]" data-es="· Reseña de Google" data-en="· Google review">· Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Juan helped me get our water heater fixed by connecting me with a great plumber. He himself came out personally to look at the water heater and kept in touch to make sure I was satisfied. Juan did our two exterior doors too. The outside color was a dark green color which doesn't cover well. He came out several times to get everything right. They look fantastic."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mammoth Enterprises</span> <span class="text-[color:var(--ink-40)]" data-es="· Reseña de Google" data-en="· Google review">· Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 41 reviews on Google" data-en="Read all 41 reviews on Google">Read all 41 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Kissimmee</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,101,29,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">3826 Bay Club Cir Unit 204, Kissimmee, FL 34741</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,101,29,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,101,29,0.4)]" href="tel:+14077472700" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Free estimate" data-en="Free estimate">Free estimate</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Call or email Juan directly to walk through your project and get a free, no-obligation quote." data-en="Call or email Juan directly to walk through your project and get a free, no-obligation quote.">Call or email Juan directly to walk through your project and get a free, no-obligation quote.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,101,29,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (407) 747-2700" data-en="Call (407) 747-2700">Call (407) 747-2700</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,101,29,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos mas recientes y escribe por DM cualquier duda antes de tu proyecto." data-en="See the latest jobs and message any questions before your project.">See the latest jobs and message any questions before your project.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,101,29,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: JGM Construction &amp; Remodeling, 3826 Bay Club Cir Unit 204, Kissimmee FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Your project is our business." data-en="Your project is our business.">Your project is our business.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Let&#39;s start your" data-en="Let&#39;s start your">Let&#39;s start your</span> <span class="text-shine" data-es="next project" data-en="next project">next project</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (407) 747-2700 or email jgmconstruction.fl@hotmail.com for a free estimate on your kitchen, bathroom, flooring or drywall project in Kissimmee and Central Florida." data-en="Call (407) 747-2700 or email jgmconstruction.fl@hotmail.com for a free estimate on your kitchen, bathroom, flooring or drywall project in Kissimmee and Central Florida.">Call (407) 747-2700 or email jgmconstruction.fl@hotmail.com for a free estimate on your kitchen, bathroom, flooring or drywall project in Kissimmee and Central Florida.</p>')
rep('''<a href="tel:+14077472700" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="tel:+14077472700" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (407) 747-2700" data-en="Call (407) 747-2700">Call (407) 747-2700</a>
        <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Get directions" data-en="Get directions">Get directions</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">JGM</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,183,136,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/hero-bathroom.jpg" alt="JGM Construction &amp; Remodeling" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,183,136,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">JGM Construction</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Construccion y remodelacion en Kissimmee, FL. Presupuestos gratis por telefono o email." data-en="Construction &amp; remodeling in Kissimmee, FL. Free estimates by phone or email.">Construction &amp; remodeling in Kissimmee, FL. Free estimates by phone or email.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="tel:+14077472700" target="_blank" rel="noopener" class="hover:text-[#e8b788]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>3826 Bay Club Cir Unit 204, Kissimmee, FL 34741</p>
        <p><a href="tel:+14077472700" class="hover:text-[#e8b788]" data-es="Call (407) 747-2700" data-en="Call (407) 747-2700">Call (407) 747-2700</a></p>
        <p><a href="mailto:jgmconstruction.fl@hotmail.com" class="hover:text-[#e8b788]">jgmconstruction.fl@hotmail.com</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e8b788]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e8b788]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e8b788]">Facebook · JGM Construction &amp; Remodeling</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 JGM Construction &amp; Remodeling LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="tel:+14077472700" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+14077472700" class="book-float" aria-label="Call JGM Construction &amp; Remodeling">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 20. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace('href="tel:+14077472700" target="_blank" rel="noopener"', 'href="tel:+14077472700"')
print("CLEANUP tel links done")


# ---------------------------------------------------------------------------
# 21. Traduccion ES real para todos los textos NUEVOS (bilingue obligatorio)
# ---------------------------------------------------------------------------
T = {
    "4.9 out of 5 · 41 reviews on Google": "4.9 de 5 · 41 reseñas en Google",
    "4.9 · 41 reviews on Google": "4.9 · 41 reseñas en Google",
    "A final walkthrough with you before the job is called done, backed by a workmanship warranty.":
        "Una revisión final contigo antes de dar el trabajo por terminado, respaldada por una garantía de mano de obra.",
    "Address": "Dirección",
    "Bathroom Remodeling": "Bathroom Remodeling",
    "Building since": "Construyendo desde",
    "Call": "Llamar",
    "Call (407) 747-2700": "Llama al (407) 747-2700",
    "Call for a quote": "Llama para cotizar",
    "Call or email Juan directly to walk through your project and get a free, no-obligation quote.":
        "Llama o escribe a Juan directamente para revisar tu proyecto y obtener una cotización gratis, sin compromiso.",
    "Call (407) 747-2700 or email to walk through the project and get a clear, honest scope of work.":
        "Llama al (407) 747-2700 o escribe por correo para revisar el proyecto y definir un alcance de trabajo claro y honesto.",
    "Call (407) 747-2700 or email jgmconstruction.fl@hotmail.com for a free estimate on your kitchen, bathroom, flooring or drywall project in Kissimmee and Central Florida.":
        "Llama al (407) 747-2700 o escribe a jgmconstruction.fl@hotmail.com para una cotización gratis de tu proyecto de cocina, baño, piso o drywall en Kissimmee y el centro de Florida.",
    "Cabinets, countertops, sinks and layout updates, planned around how your kitchen actually gets used.":
        "Gabinetes, encimeras, fregaderos y cambios de distribución, planeados según el uso real de tu cocina.",
    "Clean, careful work": "Trabajo limpio y cuidadoso",
    "Contact": "Contacto",
    "Custom closets": "Clósets a medida",
    "Drywall &amp; Paint": "Drywall y Pintura",
    "Drywall repair": "Reparación de drywall",
    "Drywall Repair &amp; Painting": "Drywall Repair &amp; Painting",
    "Every project is quoted after a walkthrough of your home. Call or email for a free, no-obligation estimate.":
        "Cada proyecto se cotiza después de revisar tu casa. Llama o escribe por correo para una cotización gratis, sin compromiso.",
    "Exterior door replacement": "Reemplazo de puertas exteriores",
    "Family-run,": "Un negocio familiar,",
    "Fence replacement": "Reemplazo de cercas",
    "Finishing &amp; Repairs": "Acabados y Reparaciones",
    "Fix &amp; finish": "Arreglar y terminar",
    "Flooring &amp; Tile": "Flooring &amp; Tile",
    "Flooring &amp; tile installation": "Instalación de piso y azulejo",
    "Flooring · Drywall · Paint": "Flooring · Drywall · Paint",
    "Floors that last": "Pisos que duran",
    "Free estimate": "Presupuesto gratis",
    "Get directions": "Cómo llegar",
    "Interior &amp; exterior painting": "Pintura interior y exterior",
    "Juan building in Central Florida": "Juan construyendo en el centro de Florida",
    "Juan Gonzalez Miranda and the JGM Construction &amp; Remodeling team handle kitchen and bathroom remodels, flooring, drywall repair and painting across Kissimmee and Central Florida, with the kind of clean, careful work that earned a 4.9 rating on Google.":
        "Juan Gonzalez Miranda y el equipo de JGM Construction &amp; Remodeling se encargan de remodelaciones de cocina y baño, pisos, reparación de drywall y pintura en Kissimmee y el centro de Florida, con el tipo de trabajo limpio y cuidadoso que ganó una calificación de 4.9 en Google.",
    "Juan P. Gonzalez Miranda founded JGM Construction &amp; Remodeling LLC in Kissimmee in 2020, and has run it since as a hands-on, quality by square foot operation. He personally shows up on jobsites, from a kitchen or bathroom remodel to a drywall repair or a concrete walkway, and stays in touch with homeowners until the work is done right.":
        "Juan P. Gonzalez Miranda fundó JGM Construction &amp; Remodeling LLC en Kissimmee en 2020, y la ha dirigido desde entonces con un estándar de calidad por pie cuadrado, presente en persona en cada obra. Se aparece personalmente en cada obra, desde una remodelación de cocina o baño hasta una reparación de drywall o un colado de concreto, y se mantiene en contacto con los dueños de casa hasta que el trabajo queda bien hecho.",
    "Kissimmee, FL · Construction &amp; Remodeling": "Kissimmee, FL · Construcción y Remodelación",
    "Kitchen Remodeling": "Kitchen Remodeling",
    "Kitchen remodeling": "Remodelación de cocina",
    "Kitchens and baths,": "Cocinas y baños,",
    "Let&#39;s start your": "Empecemos tu",
    "Most requested": "Lo más solicitado",
    "next project": "próximo proyecto",
    "Owner / Manager": "Dueño / Gerente",
    "Plan &amp; materials": "Plan y materiales",
    "Popcorn ceiling removal": "Eliminación de techo popcorn",
    "Pricing depends on scope and materials. Call (407) 747-2700 or email for an exact quote.":
        "El precio depende del alcance y los materiales. Llama al (407) 747-2700 o escribe por correo para una cotización exacta.",
    "Read all 41 reviews on Google": "Lee las 41 reseñas en Google",
    "reviews on Google": "reseñas en Google",
    "Serving": "Sirviendo a",
    "Services for": "Servicios para",
    "Signature project": "Proyecto insignia",
    "Since": "Desde",
    "Tubs, showers, vanities and tile, finished start to finish and backed by a workmanship warranty.":
        "Tinas, regaderas, tocadores y azulejo, terminados de principio a fin y respaldados por una garantía de mano de obra.",
    "The crew works with a quality by square foot standard, keeping your home clean and protected while the job is underway.":
        "El equipo trabaja con un estándar de calidad por pie cuadrado, manteniendo tu casa limpia y protegida mientras dura la obra.",
    "The result: a 4.9-star rating across 41 Google reviews, with homeowners specifically praising how fast, honest and thorough Juan is, never cutting corners on the work.":
        "El resultado: una calificación de 4.9 estrellas en 41 reseñas de Google, con dueños de casa que destacan lo rápido, honesto y minucioso que es Juan, sin nunca recortar en el trabajo.",
    "detail-first": "y detallista",
    "Tile installation for entryways, bathrooms and living spaces, laid clean and level.":
        "Instalación de azulejo para entradas, baños y salas, colocado limpio y nivelado.",
    "to finish": "hasta el final",
    "Your project, start": "Tu proyecto, de inicio",
    "Your project is our business.": "Tu proyecto es nuestro negocio.",
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
