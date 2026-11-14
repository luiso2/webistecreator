import re
import shutil

SLUG = "marys-health-spa-miramar"
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
# 2. Paleta: plum-pink (lashbloom) -> champagne-gold (Mary's Health Spa, su
#    pared de certificados y luz dorada)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#b8893f"),
    ("#5c2140", "#5c3c14"),
    ("#f0bed7", "#e8cf9e"),
    ("#faf2f6", "#faf5ec"),
    ("#c47a9c", "#c9a06c"),
    ("#8a5573", "#6b4f28"),
    ("#f3e0ea", "#f0e6d2"),
    ("#d9a8c2", "#d8bf8e"),
    ("#7d3457", "#6b4a1e"),
    ("#5f2c48", "#553a16"),
    ("#33222c", "#2e2719"),
    ("#fbf3f8", "#faf6ec"),
    ("#fbeff5", "#faf6ea"),
    ("#f8dfeb", "#f1e3c4"),
    ("#f6f1ea", "#f3ecda"),
    ("#f2d5e3", "#ecdcb8"),
    ("#f2cfe0", "#ecd8b0"),
    ("#efd0e0", "#ecd8b2"),
    ("#e5c1d4", "#ded0a0"),
    ("#dc9dbe", "#cba868"),
    ("#d3a2bc", "#d2bb86"),
    ("#c9789f", "#bd9754"),
    ("#b25a85", "#a87e34"),
    ("#2a1722", "#241c0f"),
    ("#1f0f18", "#1a130a"),
    ("#1c0f16", "#18130a"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(184,137,63"),
    ("rgba(51,34,44", "rgba(46,39,25"),
    ("rgba(240,190,215", "rgba(232,207,158"),
    ("rgba(70,25,50", "rgba(92,60,20"),
    ("rgba(250,242,246", "rgba(250,245,236"),
    ("rgba(125,52,87", "rgba(107,74,30"),
    ("rgba(253,246,250", "rgba(250,246,236"),
    ("rgba(40,16,30", "rgba(36,28,15"),
    ("rgba(233,205,186", "rgba(222,195,130"),
    ("rgba(185,138,128", "rgba(176,140,70"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform propio -> tel: ; IG existe pero
#    perfil vacio/privado -> usamos Google reviews como canal publico
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+17863541717"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://instagram.com/maryhealthspa"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@maryhealthspa"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_ADDR = "12555 Miramar Pkwy Suite 118, Miramar, FL 33027"
NEW_MAPS = "https://www.google.com/maps?q=12555+Miramar+Pkwy+Suite+118,+Miramar,+FL+33027"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    "<title>Mary's Health Spa · Facials &amp; Skincare in Miramar, FL | 4.9 on Google</title>")
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    "<meta name=\"description\" content=\"Mary's Health Spa, Miramar FL: HydraFacial-style water treatments, Korean deep cleansing facials, dermabrasion and cupping. 4.9 stars across 29 Google reviews.\" />")
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    "<meta property=\"og:title\" content=\"Mary's Health Spa · Facials &amp; Skincare in Miramar, FL\" />")
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Water facials, Korean deep cleansing, dermabrasion and cupping. 4.9 on Google with 29 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-certificates.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Mary's Health Spa",
    "description": "Skincare and facial studio in Miramar, FL run by licensed esthetician Marilyn Leach: HydraFacial-style water treatments, Korean deep cleansing facials, dermabrasion and cupping.",
    "address": { "@type": "PostalAddress", "streetAddress": "12555 Miramar Pkwy Suite 118", "addressLocality": "Miramar", "addressRegion": "FL", "postalCode": "33027", "addressCountry": "US" },
    "telephone": "+1-786-354-1717",
    "sameAs": ["https://instagram.com/maryhealthspa"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "29", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Facial &amp; skin services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "HydraFacial-style Water Treatment" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Korean Deep Cleansing Facial" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Diamond Dermabrasion" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cupping Therapy" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">MH</span>')
rep('<span class="pre-word">Lash Bloom</span>', "<span class=\"pre-word\">Mary's Health Spa</span>")
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,137,63,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Mary\'s Health Spa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,137,63,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Mary\'s <span class="text-[color:var(--accent-deep)]">Health Spa</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call to book" data-en="Call to book">Call to book</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call to book" data-en="Call to book">Call to book</a>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miramar, FL · Facial Studio" data-en="Miramar, FL · Facial Studio">Miramar, FL · Facial Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Your skin, read before it is treated." data-en="Your skin, read before it is treated.">Your skin, read before it is treated.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Water facials, dermabrasion" data-en="Water facials, dermabrasion">Water facials, dermabrasion</span><br /><span data-es="and cupping, done to " data-en="and cupping, done to ">and cupping, done to </span><span class="text-shine" data-es="glow" data-en="glow">glow</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    "data-es=\"Licensed esthetician Marilyn Leach runs a one-on-one suite inside Novus Salon Suites in Miramar: HydraFacial-style water treatments, Korean deep cleansing, diamond dermabrasion and cupping, backed by a wall of real training certificates.\" data-en=\"Licensed esthetician Marilyn Leach runs a one-on-one suite inside Novus Salon Suites in Miramar: HydraFacial-style water treatments, Korean deep cleansing, diamond dermabrasion and cupping, backed by a wall of real training certificates.\">Licensed esthetician Marilyn Leach runs a one-on-one suite inside Novus Salon Suites in Miramar: HydraFacial-style water treatments, Korean deep cleansing, diamond dermabrasion and cupping, backed by a wall of real training certificates.</p>")
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 29 reviews on Google" data-en="4.9 · 29 reviews on Google">4.9 · 29 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 354-1717" data-en="Call (786) 354-1717">Call (786) 354-1717</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-certificates.jpg" alt="The treatment room wall of training certificates at Mary\'s Health Spa, Miramar FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Suite 118" data-en="Suite 118">Suite 118</p>
            <p class="font-display text-lg">Novus Salon Suites</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="By appointment" data-en="By appointment">By appointment</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="29">29</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Water <span class="text-shine">&amp;</span> Facials</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Dermabrasion · Cupping" data-en="Dermabrasion · Cupping">Dermabrasion · Cupping</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">1:1</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Suite privada" data-en="Private suite">Private suite</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Miramar</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Miramar Pkwy" data-en="Miramar Pkwy">Miramar Pkwy</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Water Facial"),
    ("Hybrid Set", "Korean Deep Cleansing"),
    ("Volume Set", "Dermabrasion"),
    ("Mega Volume", "Cupping Therapy"),
    ("Bottom Lashes", "LED Light Therapy"),
    ("West Palm Beach, FL", "Miramar, FL"),
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
          <img src="assets/about-vanity.jpg" alt="The treatment vanity and tools at Mary's Health Spa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/gallery-led-therapy.jpg" alt="LED light therapy bed inside Mary's Health Spa treatment room" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One esthetician," data-en="One esthetician,">One esthetician,</span><br /><span class="text-shine" data-es="a wall of real training" data-en="a wall of real training">a wall of real training</span>')
rep("data-es=\"Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad.\" data-en=\"Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.\">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>",
    "data-es=\"Mary's Health Spa is the private suite of licensed esthetician Marilyn Leach, inside Novus Salon Suites on Miramar Parkway. The treatment room wall is lined with real certificates: lymphatic drainage, mesotherapy, eyebrow design and more.\" data-en=\"Mary's Health Spa is the private suite of licensed esthetician Marilyn Leach, inside Novus Salon Suites on Miramar Parkway. The treatment room wall is lined with real certificates: lymphatic drainage, mesotherapy, eyebrow design and more.\">Mary's Health Spa is the private suite of licensed esthetician Marilyn Leach, inside Novus Salon Suites on Miramar Parkway. The treatment room wall is lined with real certificates: lymphatic drainage, mesotherapy, eyebrow design and more.</p>")
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Clients describe Marilyn as attentive and informative, walking through every step before starting. The result: a 4.9-star rating across 29 Google reviews." data-en="Clients describe Marilyn as attentive and informative, walking through every step before starting. The result: a 4.9-star rating across 29 Google reviews.">Clients describe Marilyn as attentive and informative, walking through every step before starting. The result: a 4.9-star rating across 29 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="29">29</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">10+</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Certificaciones" data-en="Certifications">Certifications</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,137,63,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Marilyn Leach" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,137,63,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Marilyn Leach · <span class="text-[color:var(--ink-40)]" data-es="Licensed esthetician" data-en="Licensed esthetician">Licensed esthetician</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your visit, step" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="by step" data-en="by step">by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call to book" data-en="Call to book">Call to book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call Mary's Health Spa and Marilyn finds a time at her Novus Salon Suites room that works for you." data-en="Call Mary's Health Spa and Marilyn finds a time at her Novus Salon Suites room that works for you.">Call Mary's Health Spa and Marilyn finds a time at her Novus Salon Suites room that works for you.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Skin consult" data-en="Skin consult">Skin consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Marilyn explains each step before starting, so you know exactly what a water facial, dermabrasion or cupping session involves." data-en="Marilyn explains each step before starting, so you know exactly what a water facial, dermabrasion or cupping session involves.">Marilyn explains each step before starting, so you know exactly what a water facial, dermabrasion or cupping session involves.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The treatment" data-en="The treatment">The treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Soft, soothing music, a quiet room, and an unhurried facial, dermabrasion or cupping session from start to finish." data-en="Soft, soothing music, a quiet room, and an unhurried facial, dermabrasion or cupping session from start to finish.">Soft, soothing music, a quiet room, and an unhurried facial, dermabrasion or cupping session from start to finish.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Your next visit" data-en="Your next visit">Your next visit</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Marilyn lets you know what to expect for your skin and when it makes sense to come back for the next session." data-en="Marilyn lets you know what to expect for your skin and when it makes sense to come back for the next session.">Marilyn lets you know what to expect for your skin and when it makes sense to come back for the next session.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (sin menu de precios publicado -> "se cotiza, llama")
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Facials for" data-en="Facials for">Facials for</span> <span class="text-shine" data-es="every skin" data-en="every skin">every skin</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    "data-es=\"Every treatment is quoted to your skin and the service you choose. Call (786) 354-1717 and Marilyn will walk you through pricing.\" data-en=\"Every treatment is quoted to your skin and the service you choose. Call (786) 354-1717 and Marilyn will walk you through pricing.\">Every treatment is quoted to your skin and the service you choose. Call (786) 354-1717 and Marilyn will walk you through pricing.</p>")

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(184,137,63,0.4); box-shadow: 0 18px 50px rgba(46,39,25,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="HydraFacial-style Water Treatment" data-en="HydraFacial-style Water Treatment">HydraFacial-style Water Treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A multi-step water infusion facial for cleansing, exfoliating and hydrating in one visit." data-en="A multi-step water infusion facial for cleansing, exfoliating and hydrating in one visit.">A multi-step water infusion facial for cleansing, exfoliating and hydrating in one visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Deep clean" data-en="Deep clean">Deep clean</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Korean Deep Cleansing Facial" data-en="Korean Deep Cleansing Facial">Korean Deep Cleansing Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A thorough Korean-style cleansing routine, gentle enough for sensitive skin and done step by step." data-en="A thorough Korean-style cleansing routine, gentle enough for sensitive skin and done step by step.">A thorough Korean-style cleansing routine, gentle enough for sensitive skin and done step by step.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Resurface" data-en="Resurface">Resurface</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Diamond Dermabrasion" data-en="Diamond Dermabrasion">Diamond Dermabrasion</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diamond-tip microdermabrasion to resurface skin and smooth out texture." data-en="Diamond-tip microdermabrasion to resurface skin and smooth out texture.">Diamond-tip microdermabrasion to resurface skin and smooth out texture.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Recovery" data-en="Recovery">Recovery</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cupping Therapy" data-en="Cupping Therapy">Cupping Therapy</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Glass cupping to support circulation and lymphatic flow, on its own or paired with a facial." data-en="Glass cupping to support circulation and lymphatic flow, on its own or paired with a facial.">Glass cupping to support circulation and lymphatic flow, on its own or paired with a facial.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on the service and your skin. Call (786) 354-1717 for a quote." data-en="Pricing depends on the service and your skin. Call (786) 354-1717 for a quote.">Pricing depends on the service and your skin. Call (786) 354-1717 for a quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Inside the" data-en="Inside the">Inside the</span> <span class="text-shine" data-es="suite" data-en="suite">suite</span>')
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Tratamiento de agua HydraFacial" data-en="HydraFacial-style water treatment">HydraFacial-style water treatment</span><img src="assets/gallery-hydrafacial-treatment.jpg" alt="A client receiving a HydraFacial-style water treatment at Mary's Health Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Pared de certificaciones" data-en="The certificate wall">The certificate wall</span><img src="assets/hero-certificates.jpg" alt="A wall of real training certificates at Mary's Health Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Maquina de agua para facial" data-en="Water facial machine">Water facial machine</span><img src="assets/gallery-hydrafacial-machine.jpg" alt="The water facial machine used for treatments at Mary's Health Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Herramientas de cupping" data-en="Cupping tools">Cupping tools</span><img src="assets/gallery-cupping-tools.jpg" alt="Glass cupping tools used at Mary's Health Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Miramar" data-en="What Miramar">What Miramar</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 29 reviews on Google" data-en="4.9 out of 5 · 29 reviews on Google">4.9 out of 5 · 29 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"My daughter had a Korean deep facial cleansing treatment, and the experience was amazing from start to finish. Mary was friendly, professional, and attentive, taking the time to explain each step of the process and making her feel..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maria Azzollini</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The service was Excellent!!! Marylin is very knowledgeable and informative what kind of process I need to be done. I left so please and this is my second time and I will be returning to keep myself young :)"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Veronica Cadena</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mary was very supportive and I enjoyed the derma braze facial! Mary made sure I was very comfortable and relaxed the whole time! With soft, soothing music and a very quiet, calm atmosphere I may only regret.. not getting a facial sooner!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sandi Ehler</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=Mary%27s+Health+Spa+Miramar+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 29 reviews on Google" data-en="Read all 29 reviews on Google">Read all 29 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miramar</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,137,63,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + NEW_ADDR + ''' (inside Novus Salon Suites)</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,137,63,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,137,63,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Friday 10 AM to 6 PM, Saturday 9 AM to 7 PM. Closed Sunday." data-en="Monday to Friday 10 AM to 6 PM, Saturday 9 AM to 7 PM. Closed Sunday.">Monday to Friday 10 AM to 6 PM, Saturday 9 AM to 7 PM. Closed Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,137,63,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 354-1717" data-en="Call (786) 354-1717">Call (786) 354-1717</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,137,63,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See the spa's latest posts and send a DM with any questions before your visit." data-en="See the spa's latest posts and send a DM with any questions before your visit.">See the spa's latest posts and send a DM with any questions before your visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,137,63,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Mary's Health Spa, 12555 Miramar Pkwy, Miramar FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es-ignore-noop' if False else '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Your skin, read before it is treated." data-en="Your skin, read before it is treated.">Your skin, read before it is treated.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your next facial" data-en="Your next facial">Your next facial</span> <span class="text-shine" data-es="is one call away" data-en="is one call away">is one call away</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    "data-es-ignore" if False else '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (786) 354-1717 for a water facial, Korean deep cleansing, dermabrasion or cupping with Marilyn at Mary\'s Health Spa." data-en="Call (786) 354-1717 for a water facial, Korean deep cleansing, dermabrasion or cupping with Marilyn at Mary\'s Health Spa.">Call (786) 354-1717 for a water facial, Korean deep cleansing, dermabrasion or cupping with Marilyn at Mary\'s Health Spa.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 354-1717" data-en="Call (786) 354-1717">Call (786) 354-1717</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    "<span class=\"foot-mark\" aria-hidden=\"true\">Mary's Health Spa</span>")
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,158,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Mary's Health Spa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,158,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Mary's Health Spa</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Facial studio inside Novus Salon Suites, Miramar, FL. By appointment only." data-en="Facial studio inside Novus Salon Suites, Miramar, FL. By appointment only.">Facial studio inside Novus Salon Suites, Miramar, FL. By appointment only.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#e8cf9e]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#e8cf9e]" data-es="Call (786) 354-1717" data-en="Call (786) 354-1717">Call (786) 354-1717</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e8cf9e]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e8cf9e]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    "<p class=\"text-xs text-[color:var(--ink-40)]\">© 2026 Mary's Health Spa.</p>")
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf5ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Mary\'s Health Spa">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf5ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n  </a>')
print("BOOK-FLOAT done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", PATH)
