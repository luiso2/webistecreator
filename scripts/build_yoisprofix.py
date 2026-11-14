import re
import shutil

SLUG = "yois-pro-fix"
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
# 2. Paleta: plum-pink (lashbloom) -> teal-blue (Yois Pro Fix, su propio azul de marca)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#145c74"),
    ("#5c2140", "#0c2d38"),
    ("#f0bed7", "#a9d1de"),
    ("#faf2f6", "#f2f7f8"),
    ("#c47a9c", "#3f8aa3"),
    ("#8a5573", "#1c5163"),
    ("#f3e0ea", "#dcebef"),
    ("#d9a8c2", "#78afc2"),
    ("#7d3457", "#164555"),
    ("#5f2c48", "#0e3947"),
    ("#33222c", "#1c282b"),
    ("#fbf3f8", "#f2f9fb"),
    ("#fbeff5", "#eaf6fa"),
    ("#f8dfeb", "#cde6ee"),
    ("#f6f1ea", "#eaf3f6"),
    ("#f2d5e3", "#cde4ec"),
    ("#f2cfe0", "#c2e0e9"),
    ("#efd0e0", "#c8e2eb"),
    ("#e5c1d4", "#a9d1de"),
    ("#dc9dbe", "#579cb3"),
    ("#d3a2bc", "#8ebdcd"),
    ("#c9789f", "#3d859c"),
    ("#b25a85", "#1f657d"),
    ("#2a1722", "#0b242c"),
    ("#1f0f18", "#07181e"),
    ("#1c0f16", "#08171d"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(20,92,116"),
    ("rgba(51,34,44", "rgba(28,40,43"),
    ("rgba(240,190,215", "rgba(169,209,222"),
    ("rgba(70,25,50", "rgba(12,45,56"),
    ("rgba(250,242,246", "rgba(242,247,248"),
    ("rgba(125,52,87", "rgba(22,69,85"),
    ("rgba(253,246,250", "rgba(242,249,251"),
    ("rgba(40,16,30", "rgba(11,36,44"),
    ("rgba(233,205,186", "rgba(169,209,222"),
    ("rgba(185,138,128", "rgba(63,138,163"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform ni IG -> tel: y mailto:
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+17862707121"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_MAIL_URL = "mailto:yois.profix@gmail.com"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_MAIL_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_MAIL_LABEL = "yois.profix@gmail.com"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_MAIL_LABEL)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=Kendall,+FL"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Yois Pro Fix · Property Repairs in Kendall, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Yois Pro Fix, Kendall FL: HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs. 5.0 stars across 17 Google reviews. Call or email for a free quote." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Yois Pro Fix · Property Repairs in Kendall, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="HVAC, electrical, plumbing, flooring, painting and structural repairs. 5.0 on Google with 17 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-levelwork.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Yois Pro Fix",
    "description": "Property repair company serving Kendall, FL and Miami-Dade County: HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs, available 24/7.",
    "areaServed": "Kendall, FL",
    "telephone": "+1-786-270-7121",
    "email": "yois.profix@gmail.com",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "17", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Property repair services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "HVAC &amp; Duct Cleaning" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Electrical" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plumbing" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Flooring &amp; Painting" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Structural Repairs" } }
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
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,92,116,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Yois Pro Fix" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,92,116,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Yois <span class="text-[color:var(--accent-deep)]">Pro Fix</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">YPF</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Yois Pro Fix</span>')
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
    'data-es="Kendall, FL · Property Repairs" data-en="Kendall, FL · Property Repairs">Kendall, FL · Property Repairs</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Professional property repairs." data-en="Professional property repairs.">Professional property repairs.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="HVAC, electrical, plumbing" data-en="HVAC, electrical, plumbing">HVAC, electrical, plumbing</span><br /><span data-es="and more, fixed " data-en="and more, fixed ">and more, fixed </span><span class="text-shine" data-es="right" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs, all from one team available 24/7 across Kendall and Miami-Dade. A straight quote before any work begins, every time." data-en="HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs, all from one team available 24/7 across Kendall and Miami-Dade. A straight quote before any work begins, every time.">HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs, all from one team available 24/7 across Kendall and Miami-Dade. A straight quote before any work begins, every time.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 17 reviews on Google" data-en="5.0 · 17 reviews on Google">5.0 · 17 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_MAIL_LABEL + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (786) 270-7121" data-en="Call (786) 270-7121">Call (786) 270-7121</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_MAIL_URL + '''" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
            ''' + NEW_MAIL_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-levelwork.jpg" alt="A Yois Pro Fix technician leveling a wall before painting in Kendall, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Available" data-en="Available">Available</p>
            <p class="font-display text-lg">24/7</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="By phone or email" data-en="By phone or email">By phone or email</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="17">17</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">HVAC <span class="text-shine">&amp;</span> Electrical</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Plomeria · Pisos · Pintura" data-en="Plumbing · Flooring · Paint">Plumbing · Flooring · Paint</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">24/7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Availability" data-en="Availability">Availability</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Kendall</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Miami-Dade, FL" data-en="Miami-Dade, FL">Miami-Dade, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "HVAC &amp; Duct Cleaning"),
    ("Hybrid Set", "Electrical"),
    ("Volume Set", "Plumbing"),
    ("Mega Volume", "Flooring &amp; Painting"),
    ("Bottom Lashes", "Structural Repairs"),
    ("West Palm Beach, FL", "Kendall, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (1 sola foto real disponible para esta seccion -> grid 1 col)
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
          <img src="assets/about-team.jpg" alt="The Yois Pro Fix team installing window blinds in a Kendall home" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One team," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="every repair handled" data-en="every repair handled">every repair handled</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Yois Pro Fix is a Kendall-based property repair team covering HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs. One call or email gets a straight answer on the job and the price, before any work starts." data-en="Yois Pro Fix is a Kendall-based property repair team covering HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs. One call or email gets a straight answer on the job and the price, before any work starts.">Yois Pro Fix is a Kendall-based property repair team covering HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs. One call or email gets a straight answer on the job and the price, before any work starts.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a perfect 5.0 rating across 17 Google reviews, and 24/7 availability for the repairs that cannot wait." data-en="The result: a perfect 5.0 rating across 17 Google reviews, and 24/7 availability for the repairs that cannot wait.">The result: a perfect 5.0 rating across 17 Google reviews, and 24/7 availability for the repairs that cannot wait.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="17">17</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Disponibilidad" data-en="Availability">Availability</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,92,116,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Yois Pro Fix" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,92,116,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yois Pro Fix · <span class="text-[color:var(--ink-40)]" data-es="Property repair team" data-en="Property repair team">Property repair team</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your project, start" data-en="Your project, start">Your project, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or email" data-en="Call or email">Call or email</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Reach out by phone or email with what needs fixing, and the team will talk through the job with you." data-en="Reach out by phone or email with what needs fixing, and the team will talk through the job with you.">Reach out by phone or email with what needs fixing, and the team will talk through the job with you.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Honest quote" data-en="Honest quote">Honest quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a clear, upfront price for the work, no surprises once the job is underway." data-en="You get a clear, upfront price for the work, no surprises once the job is underway.">You get a clear, upfront price for the work, no surprises once the job is underway.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The work gets done" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="From an electrical fix to a full flooring job, Yois Pro Fix handles it with the same care every time." data-en="From an electrical fix to a full flooring job, Yois Pro Fix handles it with the same care every time.">From an electrical fix to a full flooring job, Yois Pro Fix handles it with the same care every time.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walk the results together" data-en="Walk the results together">Walk the results together</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Before the team leaves, you walk through the finished work together, so you know it was done right." data-en="Before the team leaves, you walk through the finished work together, so you know it was done right.">Before the team leaves, you walk through the finished work together, so you know it was done right.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Servicios para" data-en="Services for">Services for</span> <span class="text-shine" data-es="cada propiedad" data-en="every property">every property</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two jobs are the same, so every project gets its own honest quote by phone or email, before any work begins." data-en="No two jobs are the same, so every project gets its own honest quote by phone or email, before any work begins.">No two jobs are the same, so every project gets its own honest quote by phone or email, before any work begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Climate control" data-en="Climate control">Climate control</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="HVAC &amp; Duct Cleaning" data-en="HVAC &amp; Duct Cleaning">HVAC &amp; Duct Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="AC and duct cleaning and repair, vent inspection and the everyday HVAC maintenance that keeps a Florida home comfortable." data-en="AC and duct cleaning and repair, vent inspection and the everyday HVAC maintenance that keeps a Florida home comfortable.">AC and duct cleaning and repair, vent inspection and the everyday HVAC maintenance that keeps a Florida home comfortable.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(20,92,116,0.4); box-shadow: 0 18px 50px rgba(28,40,43,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Electrical &amp; Plumbing" data-en="Electrical &amp; Plumbing">Electrical &amp; Plumbing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Outlet and fixture work, wiring fixes, leak repair and the plumbing and electrical jobs homeowners call about most." data-en="Outlet and fixture work, wiring fixes, leak repair and the plumbing and electrical jobs homeowners call about most.">Outlet and fixture work, wiring fixes, leak repair and the plumbing and electrical jobs homeowners call about most.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Finishes" data-en="Finishes">Finishes</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Flooring &amp; Painting" data-en="Flooring &amp; Painting">Flooring &amp; Painting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Flooring installs and repair, interior and exterior painting, drywall patching and wall mounting done clean." data-en="Flooring installs and repair, interior and exterior painting, drywall patching and wall mounting done clean.">Flooring installs and repair, interior and exterior painting, drywall patching and wall mounting done clean.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Bigger projects" data-en="Bigger projects">Bigger projects</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Structural Repairs" data-en="Structural Repairs">Structural Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Ceiling and framing repair, exterior structural fixes and the bigger jobs that need more than a quick patch." data-en="Ceiling and framing repair, exterior structural fixes and the bigger jobs that need more than a quick patch.">Ceiling and framing repair, exterior structural fixes and the bigger jobs that need more than a quick patch.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Mechanical" data-en="Mechanical">Mechanical</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="HVAC &amp; AC repair" data-en="HVAC &amp; AC repair">HVAC &amp; AC repair</li>
            <li class="flex items-center gap-2" data-es="Duct cleaning" data-en="Duct cleaning">Duct cleaning</li>
            <li class="flex items-center gap-2" data-es="Electrical" data-en="Electrical">Electrical</li>
            <li class="flex items-center gap-2" data-es="Plumbing" data-en="Plumbing">Plumbing</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Finishes" data-en="Finishes">Finishes</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Flooring" data-en="Flooring">Flooring</li>
            <li class="flex items-center gap-2" data-es="Interior &amp; exterior painting" data-en="Interior &amp; exterior painting">Interior &amp; exterior painting</li>
            <li class="flex items-center gap-2" data-es="Drywall patching" data-en="Drywall patching">Drywall patching</li>
            <li class="flex items-center gap-2" data-es="Wall &amp; TV mounting" data-en="Wall &amp; TV mounting">Wall &amp; TV mounting</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Structural" data-en="Structural">Structural</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Structural repairs" data-en="Structural repairs">Structural repairs</li>
            <li class="flex items-center gap-2" data-es="Ceiling &amp; vent repair" data-en="Ceiling &amp; vent repair">Ceiling &amp; vent repair</li>
            <li class="flex items-center gap-2" data-es="Exterior &amp; concrete work" data-en="Exterior &amp; concrete work">Exterior &amp; concrete work</li>
            <li class="flex items-center gap-2" data-es="General property repairs" data-en="General property repairs">General property repairs</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and materials. Call (786) 270-7121 or email for a free quote." data-en="Pricing depends on scope and materials. Call (786) 270-7121 or email for a free quote.">Pricing depends on scope and materials. Call (786) 270-7121 or email for a free quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="work" data-en="work">work</span>')
rep('''<a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_MAIL_LABEL + '''
        </a>''',
    '''<a href="''' + NEW_MAIL_URL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
          ''' + NEW_MAIL_LABEL + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Instalacion de rejilla de ventilacion de AC" data-en="AC vent grille install, Kendall FL">AC vent grille install, Kendall FL</span><img src="assets/gallery-ceiling-vent.jpg" alt="A Yois Pro Fix technician installing an AC vent grille in a Kendall home" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Montaje de cuadro en pared" data-en="Wall art hung level">Wall art hung level</span><img src="assets/gallery-wall-art.jpg" alt="Framed artwork mounted level on an interior wall by Yois Pro Fix" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Trabajo exterior y techo" data-en="Exterior &amp; roofline work">Exterior &amp; roofline work</span><img src="assets/gallery-exterior.jpg" alt="Exterior roofline repair work done by Yois Pro Fix" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Reparacion de techo en proceso" data-en="Ceiling repair in progress">Ceiling repair in progress</span><img src="assets/gallery-ceiling-repair.jpg" alt="A ceiling repair job in progress by Yois Pro Fix" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Demolicion de concreto exterior" data-en="Exterior concrete demo">Exterior concrete demo</span><img src="assets/gallery-concrete-demo.jpg" alt="Exterior concrete demolition work by Yois Pro Fix" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Kendall" data-en="What Kendall">What Kendall</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 17 reviews on Google" data-en="5.0 out of 5 · 17 reviews on Google">5.0 out of 5 · 17 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Exellent service, very professional and reliable. Highly recomended this company 100%"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Aroldo Delgado</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always gets the job done great prices and excellent work highly recommended !"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tatiana Montenegro</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Really impressed! They showed up on time, fixed the problem fast, and left everything spotless. Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yiosniel</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=Yois+Pro+Fix+Kendall+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 17 reviews on Google" data-en="Read all 17 reviews on Google">Read all 17 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (sin direccion fija: area de servicio)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Kendall, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,92,116,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Yois Pro Fix works across Kendall, FL and the greater Miami-Dade area, 24 hours a day, 7 days a week." data-en="Yois Pro Fix works across Kendall, FL and the greater Miami-Dade area, 24 hours a day, 7 days a week.">Yois Pro Fix works across Kendall, FL and the greater Miami-Dade area, 24 hours a day, 7 days a week.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,92,116,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,92,116,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Availability" data-en="Availability">Availability</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open 24 hours, every day of the week, for calls and quote requests." data-en="Open 24 hours, every day of the week, for calls and quote requests.">Open 24 hours, every day of the week, for calls and quote requests.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,92,116,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (786) 270-7121" data-en="Call (786) 270-7121">Call (786) 270-7121</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,92,116,0.4)]" href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener">''' + NEW_MAIL_LABEL + '''</a>
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
              <p class="font-medium mb-1" data-es="Email" data-en="Email">Email</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Send photos of the job and get a written quote back by email." data-en="Send photos of the job and get a written quote back by email.">Send photos of the job and get a written quote back by email.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,92,116,0.4)]" href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener">''' + NEW_MAIL_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Yois Pro Fix service area, Kendall FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Professional property repairs." data-en="Professional property repairs.">Professional property repairs.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call fixes" data-en="One call fixes">One call fixes</span> <span class="text-shine" data-es="it all" data-en="it all">it all</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (786) 270-7121 or email for a free, honest quote on your HVAC, electrical, plumbing, flooring, painting or structural repair. Available 24/7." data-en="Call (786) 270-7121 or email for a free, honest quote on your HVAC, electrical, plumbing, flooring, painting or structural repair. Available 24/7.">Call (786) 270-7121 or email for a free, honest quote on your HVAC, electrical, plumbing, flooring, painting or structural repair. Available 24/7.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (786) 270-7121" data-en="Call (786) 270-7121">Call (786) 270-7121</a>
        <a href="''' + NEW_MAIL_URL + '''" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Email Yois Pro Fix" data-en="Email Yois Pro Fix">Email Yois Pro Fix</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Yois Pro Fix</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,209,222,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Yois Pro Fix" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,209,222,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Yois Pro Fix</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Property repairs serving Kendall, FL and Miami-Dade. Available 24/7." data-en="Property repairs serving Kendall, FL and Miami-Dade. Available 24/7.">Property repairs serving Kendall, FL and Miami-Dade. Available 24/7.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#a9d1de]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Kendall, FL &amp; Miami-Dade" data-en="Kendall, FL &amp; Miami-Dade">Kendall, FL &amp; Miami-Dade</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#a9d1de]" data-es="Call (786) 270-7121" data-en="Call (786) 270-7121">Call (786) 270-7121</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_MAIL_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9d1de]">Instagram · ''' + NEW_MAIL_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact us" data-en="Contact us">Contact us</p>
        <p><a href="''' + NEW_MAIL_URL + '''" class="hover:text-[#a9d1de]">Email · ''' + NEW_MAIL_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Yois Pro Fix.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Call Yois Pro Fix">')
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
    "HVAC, electrical, plumbing": "HVAC, electricidad, plomeria",
    "and more, fixed ": "y mas, arreglado ",
    "right": "bien",
    "Professional property repairs.": "Reparaciones profesionales de propiedades.",
    "Kendall, FL · Property Repairs": "Kendall, FL · Reparaciones de Propiedades",
    "HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs, all from one team available 24/7 across Kendall and Miami-Dade. A straight quote before any work begins, every time.":
        "HVAC y limpieza de ductos, electricidad, plomeria, pisos, pintura y reparaciones estructurales, todo de un mismo equipo disponible 24/7 en Kendall y Miami-Dade. Una cotizacion clara antes de empezar cualquier trabajo, siempre.",
    "5.0 · 17 reviews on Google": "5.0 · 17 resenas en Google",
    "Call (786) 270-7121": "Llama al (786) 270-7121",
    "Available": "Disponible",
    "By phone or email": "Por telefono o correo",
    "Availability": "Disponibilidad",
    "Miami-Dade, FL": "Miami-Dade, FL",
    "One team,": "Un equipo,",
    "every repair handled": "cada reparacion resuelta",
    "Yois Pro Fix is a Kendall-based property repair team covering HVAC and duct cleaning, electrical, plumbing, flooring, painting and structural repairs. One call or email gets a straight answer on the job and the price, before any work starts.":
        "Yois Pro Fix es un equipo de reparaciones con base en Kendall que cubre HVAC y limpieza de ductos, electricidad, plomeria, pisos, pintura y reparaciones estructurales. Una llamada o correo basta para recibir una respuesta clara sobre el trabajo y el precio, antes de empezar.",
    "The result: a perfect 5.0 rating across 17 Google reviews, and 24/7 availability for the repairs that cannot wait.":
        "El resultado: una calificacion perfecta de 5.0 en 17 resenas de Google, y disponibilidad 24/7 para las reparaciones que no pueden esperar.",
    "Property repair team": "Equipo de reparaciones",
    "Your project, start": "Tu proyecto, de inicio",
    "to finish": "hasta el final",
    "Call or email": "Llama o escribe",
    "Reach out by phone or email with what needs fixing, and the team will talk through the job with you.":
        "Comunicate por telefono o correo con lo que necesitas reparar, y el equipo hablara contigo sobre el trabajo.",
    "Honest quote": "Cotizacion honesta",
    "You get a clear, upfront price for the work, no surprises once the job is underway.":
        "Recibes un precio claro y directo por el trabajo, sin sorpresas una vez que empieza.",
    "The work gets done": "El trabajo se hace",
    "From an electrical fix to a full flooring job, Yois Pro Fix handles it with the same care every time.":
        "Desde un arreglo electrico hasta un trabajo completo de pisos, Yois Pro Fix lo maneja con el mismo cuidado siempre.",
    "Walk the results together": "Revisan los resultados juntos",
    "Before the team leaves, you walk through the finished work together, so you know it was done right.":
        "Antes de que el equipo se vaya, revisan juntos el trabajo terminado, para que sepas que quedo bien hecho.",
    "No two jobs are the same, so every project gets its own honest quote by phone or email, before any work begins.":
        "Ningun trabajo es igual a otro, asi que cada proyecto recibe su propia cotizacion honesta por telefono o correo, antes de comenzar.",
    "Climate control": "Climatizacion",
    "HVAC &amp; Duct Cleaning": "HVAC y Limpieza de Ductos",
    "AC and duct cleaning and repair, vent inspection and the everyday HVAC maintenance that keeps a Florida home comfortable.":
        "Limpieza y reparacion de AC y ductos, inspeccion de rejillas y el mantenimiento de HVAC que mantiene comoda una casa en Florida.",
    "Call for a quote": "Llama para cotizar",
    "Call": "Llamar",
    "Most requested": "Lo mas solicitado",
    "Electrical &amp; Plumbing": "Electricidad y Plomeria",
    "Outlet and fixture work, wiring fixes, leak repair and the plumbing and electrical jobs homeowners call about most.":
        "Trabajo de tomacorrientes y accesorios, arreglos de cableado, reparacion de fugas y los trabajos de plomeria y electricidad que mas piden los clientes.",
    "Finishes": "Acabados",
    "Flooring &amp; Painting": "Pisos y Pintura",
    "Flooring installs and repair, interior and exterior painting, drywall patching and wall mounting done clean.":
        "Instalacion y reparacion de pisos, pintura interior y exterior, parcheo de paredes y montaje en pared hecho con limpieza.",
    "Bigger projects": "Proyectos grandes",
    "Structural Repairs": "Reparaciones Estructurales",
    "Ceiling and framing repair, exterior structural fixes and the bigger jobs that need more than a quick patch.":
        "Reparacion de techos y estructuras, arreglos estructurales exteriores y los trabajos grandes que necesitan mas que un parche rapido.",
    "Mechanical": "Mecanico",
    "HVAC &amp; AC repair": "HVAC y reparacion de AC",
    "Duct cleaning": "Limpieza de ductos",
    "Electrical": "Electricidad",
    "Plumbing": "Plomeria",
    "Flooring": "Pisos",
    "Interior &amp; exterior painting": "Pintura interior y exterior",
    "Drywall patching": "Parcheo de paredes",
    "Wall &amp; TV mounting": "Montaje en pared y TV",
    "Structural": "Estructural",
    "Structural repairs": "Reparaciones estructurales",
    "Ceiling &amp; vent repair": "Reparacion de techos y rejillas",
    "Exterior &amp; concrete work": "Trabajo exterior y de concreto",
    "General property repairs": "Reparaciones generales de propiedad",
    "Pricing depends on scope and materials. Call (786) 270-7121 or email for a free quote.":
        "El precio depende del alcance y los materiales. Llama al (786) 270-7121 o escribe por correo para una cotizacion gratis.",
    "Real": "Trabajo",
    "work": "real",
    "What Kendall": "Lo que dicen los",
    "customers say": "clientes en Kendall",
    "Read all 17 reviews on Google": "Lee las 17 resenas en Google",
    "Serving": "Sirviendo a",
    "Service area": "Area de servicio",
    "Yois Pro Fix works across Kendall, FL and the greater Miami-Dade area, 24 hours a day, 7 days a week.":
        "Yois Pro Fix trabaja en Kendall, FL y el area metropolitana de Miami-Dade, las 24 horas, los 7 dias de la semana.",
    "View on map": "Ver en el mapa",
    "Open 24 hours, every day of the week, for calls and quote requests.":
        "Abierto las 24 horas, todos los dias de la semana, para llamadas y cotizaciones.",
    "Email": "Correo",
    "Send photos of the job and get a written quote back by email.":
        "Envia fotos del trabajo y recibe una cotizacion por escrito por correo.",
    "One call fixes": "Una llamada arregla",
    "it all": "todo",
    "Call (786) 270-7121 or email for a free, honest quote on your HVAC, electrical, plumbing, flooring, painting or structural repair. Available 24/7.":
        "Llama al (786) 270-7121 o escribe por correo para una cotizacion gratis y honesta de tu reparacion de HVAC, electricidad, plomeria, pisos, pintura o estructura. Disponible 24/7.",
    "Email Yois Pro Fix": "Escribele a Yois Pro Fix",
    "Property repairs serving Kendall, FL and Miami-Dade. Available 24/7.":
        "Reparaciones de propiedades en Kendall, FL y Miami-Dade. Disponible 24/7.",
    "Contact": "Contacto",
    "Kendall, FL &amp; Miami-Dade": "Kendall, FL y Miami-Dade",
    "Contact us": "Contactanos",
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
