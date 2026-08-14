import re
import shutil

SLUG = "tno-painting-handyman-lakeland"
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


def hx(hexcode):
    hexcode = hexcode.lstrip('#')
    return tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4))


def rgbstr(hexcode):
    r, g, b = hx(hexcode)
    return f"rgba({r},{g},{b}"


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> hunter green / warm ivory (TNO Painting
#    and Handyman). Trade/craftsman palette: deep forest green for trust and
#    quality-work association with paint/greenery, on a warm canvas-cream
#    base. Distinct from steel-blue-navy (serrano/invictus) and copper-rust
#    (239-handyman-can-capecoral) already used for other handyman builds.
# ---------------------------------------------------------------------------
NEW_ACCENT_DEEP = "#2f6b3f"
NEW_ACCENT_MID = "#5f9468"
NEW_BG = "#f5f3e9"
NEW_BG2 = "#e6e4d4"
NEW_INK = "#23281e"

HEX_PALETTE = [
    ("#a04a72", NEW_ACCENT_DEEP),   # accent-deep
    ("#5c2140", "#16281a"),         # btn-3d sole darkest
    ("#f0bed7", "#b9dcb9"),         # dark-band shine/orb/stars accent
    ("#faf2f6", NEW_BG),            # bg
    ("#c47a9c", NEW_ACCENT_MID),    # accent-mid
    ("#8a5573", "#1f4a2a"),         # dark-band btn shadow deep
    ("#f3e0ea", NEW_BG2),           # bg-2 / accent-soft
    ("#d9a8c2", "#a7c9a8"),         # orb-b
    ("#7d3457", "#245536"),         # dark mid
    ("#5f2c48", "#1a3d24"),         # step-num gradient end
    ("#33222c", NEW_INK),           # ink
    ("#fbf3f8", "#f3f7ee"),         # tile-cap text near-white
    ("#fbeff5", "#eef5ea"),         # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#d7e8d3"),         # dark-band shimmer 3rd stop
    ("#f6f1ea", "#f1efe2"),         # theme-color meta
    ("#f2d5e3", "#dbe6d4"),         # orb-a
    ("#f2cfe0", "#c9dec5"),         # dark-band shimmer last stop
    ("#efd0e0", "#cfe2cb"),         # dark-band btn-3d gradient mid
    ("#e5c1d4", "#b9d6b6"),         # orb-c pale
    ("#dc9dbe", "#7fb384"),         # scroll-progress end stop
    ("#d3a2bc", "#a8cba6"),         # dark-band btn-3d gradient end light
    ("#c9789f", "#4f8a58"),         # shimmer stop
    ("#b25a85", "#3a7a45"),         # shimmer stop
    ("#2a1722", "#0e1f10"),         # cta-final bg gradient start
    ("#1f0f18", "#08120a"),         # cta-final bg gradient end
    ("#1c0f16", "#0a1509"),         # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", rgbstr(NEW_ACCENT_DEEP)),   # accent-deep alpha
    ("rgba(51,34,44", rgbstr(NEW_INK)),              # ink alpha
    ("rgba(240,190,215", rgbstr("#b9dcb9")),         # dark-band light accent alpha
    ("rgba(70,25,50", rgbstr("#16281a")),            # btn-3d darkest inset shadow
    ("rgba(250,242,246", rgbstr(NEW_BG)),            # bg alpha (nav scrolled)
    ("rgba(125,52,87", rgbstr("#245536")),           # dark mid alpha
    ("rgba(253,246,250", rgbstr("#fdfbf3")),         # surface alpha
    ("rgba(40,16,30", rgbstr("#08120a")),            # tile-cap gradient dark
    ("rgba(233,205,186", rgbstr("#d8e4d2")),         # dark-band accent-ghost
    ("rgba(185,138,128", rgbstr("#3f7a4a")),         # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel:. IG real (@tnopaintinghandyman).
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+12677261015"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/tnopaintinghandyman/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@tnopaintinghandyman"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_FB_URL = "https://www.facebook.com/TNOHandyman/"
NEW_MAPS = "https://www.google.com/maps?q=Lakeland,+FL"
REVIEWS_URL = "https://reviews.birdeye.com/tno-painting-and-handyman-services-llc-156203833001459"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>TNO Painting and Handyman · Painting &amp; Handyman in Lakeland, FL | 4.7 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="TNO Painting and Handyman Service LLC, serving Lakeland, Winter Haven and Polk County FL since 2016: interior and exterior painting, handyman repairs, flooring and remodeling. 4.7 stars on Google. Free estimates, call (267) 726-1015." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="TNO Painting and Handyman · Lakeland, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Painting, handyman repairs, flooring and remodeling across Lakeland &amp; Polk County since 2016. 4.7 on Google. Free estimates." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-pavers.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />\n  ', '')
print("HEAD meta done")

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "TNO Painting and Handyman Service LLC",
    "description": "Painting and handyman company serving Lakeland, Winter Haven and Polk County, FL since 2016: interior and exterior painting, drywall repair, flooring and tile, bathroom and bedroom remodeling, and general handyman repairs.",
    "address": { "@type": "PostalAddress", "addressLocality": "Lakeland", "addressRegion": "FL", "addressCountry": "US" },
    "areaServed": "Lakeland, Winter Haven &amp; Polk County, FL",
    "telephone": "+1-267-726-1015",
    "sameAs": ["https://www.instagram.com/tnopaintinghandyman/", "https://www.facebook.com/TNOHandyman/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "39", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Painting and handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Interior &amp; Exterior Painting" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Handyman Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Flooring &amp; Tile" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Remodeling &amp; Renovations" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD JSON-LD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (ya es el default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. NAV (monograma de texto en vez de logo foto: no hay logo limpio real)
# ---------------------------------------------------------------------------
MONO_SPAN = ('<span class="w-10 h-10 rounded-full flex items-center justify-center font-display '
             'text-xs tracking-wide" style="background:var(--accent-ghost); color:var(--accent-deep); '
             'border:1px solid var(--accent-ghost))">TP</span>').replace("))", ")")
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,107,63,0.35)]" />',
    MONO_SPAN)
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">TNO <span class="text-[color:var(--accent-deep)]">Painting</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">TP</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">TNO Painting</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Free Estimate" data-en="Free Estimate">Free Estimate</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Free Estimate" data-en="Free Estimate">Free Estimate</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Lakeland, FL · Painting &amp; Handyman" data-en="Lakeland, FL · Painting &amp; Handyman">Lakeland, FL · Painting &amp; Handyman</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Quality work you can trust." data-en="Quality work you can trust.">Quality work you can trust.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Painting and handyman work" data-en="Painting and handyman work">Painting and handyman work</span><br /><span data-es="Lakeland homes " data-en="Lakeland homes ">Lakeland homes </span><span class="text-shine" data-es="can count on" data-en="can count on">can count on</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="TNO Painting and Handyman has been fixing, painting and renovating homes across Lakeland, Winter Haven and Polk County since 2016. From a full room repaint to bathroom remodels, flooring and general repairs, the TNO team shows up, gives a free estimate, and gets the job done right." data-en="TNO Painting and Handyman has been fixing, painting and renovating homes across Lakeland, Winter Haven and Polk County since 2016. From a full room repaint to bathroom remodels, flooring and general repairs, the TNO team shows up, gives a free estimate, and gets the job done right.">TNO Painting and Handyman has been fixing, painting and renovating homes across Lakeland, Winter Haven and Polk County since 2016. From a full room repaint to bathroom remodels, flooring and general repairs, the TNO team shows up, gives a free estimate, and gets the job done right.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.7 · 39 reviews on Google" data-en="4.7 · 39 reviews on Google">4.7 · 39 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (267) 726-1015" data-en="Call (267) 726-1015">Call (267) 726-1015</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-pavers.jpg" alt="A paver walkway installed by TNO Painting and Handyman" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Estimates" data-en="Estimates">Estimates</p>
            <p class="font-display text-lg" data-es="Free &amp; honest" data-en="Free &amp; honest">Free &amp; honest</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Call or text anytime" data-en="Call or text anytime">Call or text anytime</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="39">39</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl"><span data-es="Since" data-en="Since">Since</span> <span class="text-shine">2016</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Serving Lakeland &amp; Polk County" data-en="Serving Lakeland &amp; Polk County">Serving Lakeland &amp; Polk County</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine" data-es="Free" data-en="Free">Free</span> <span data-es="Estimates" data-en="Estimates">Estimates</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Honest, upfront pricing" data-en="Honest, upfront pricing">Honest, upfront pricing</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Lakeland</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Polk County, FL" data-en="Polk County, FL">Polk County, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Interior Painting"),
    ("Hybrid Set", "Exterior Painting"),
    ("Volume Set", "Handyman Repairs"),
    ("Mega Volume", "Flooring &amp; Tile"),
    ("Bottom Lashes", "Remodeling"),
    ("West Palm Beach, FL", "Lakeland, FL"),
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
          <img src="assets/about-team-work.jpg" alt="The TNO Painting and Handyman team installing safety railing on a commercial job" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Painting and repairs," data-en="Painting and repairs,">Painting and repairs,</span><br /><span class="text-shine" data-es="done the right way" data-en="done the right way">done the right way</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="TNO Painting and Handyman Service LLC has served Lakeland, Winter Haven and the surrounding Polk County area since 2016. The team, managed by Tiffari Bucknor, handles everything from interior and exterior painting to drywall repair, flooring and full bathroom remodels, with technicians like Shane and Osari doing the hands-on work on site." data-en="TNO Painting and Handyman Service LLC has served Lakeland, Winter Haven and the surrounding Polk County area since 2016. The team, managed by Tiffari Bucknor, handles everything from interior and exterior painting to drywall repair, flooring and full bathroom remodels, with technicians like Shane and Osari doing the hands-on work on site.">TNO Painting and Handyman Service LLC has served Lakeland, Winter Haven and the surrounding Polk County area since 2016. The team, managed by Tiffari Bucknor, handles everything from interior and exterior painting to drywall repair, flooring and full bathroom remodels, with technicians like Shane and Osari doing the hands-on work on site.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.7-star rating across 39 Google reviews, a free estimate on every job, and homeowners who call TNO first the next time something needs fixing, painting or replacing." data-en="The result: a 4.7-star rating across 39 Google reviews, a free estimate on every job, and homeowners who call TNO first the next time something needs fixing, painting or replacing.">The result: a 4.7-star rating across 39 Google reviews, a free estimate on every job, and homeowners who call TNO first the next time something needs fixing, painting or replacing.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="39">39</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2016</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Serving since" data-en="Serving since">Serving since</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,107,63,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    MONO_SPAN.replace('w-10 h-10', 'blur-up w-10 h-10') + '\n            <span class="text-sm font-light">Tiffari Bucknor · <span class="text-[color:var(--ink-40)]" data-es="Manager, TNO Painting and Handyman" data-en="Manager, TNO Painting and Handyman">Manager, TNO Painting and Handyman</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your project, start" data-en="Your project, start">Your project, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or text" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or text (267) 726-1015 with what needs fixing, painting or remodeling, and the TNO team will talk through the job with you." data-en="Call or text (267) 726-1015 with what needs fixing, painting or remodeling, and the TNO team will talk through the job with you.">Call or text (267) 726-1015 with what needs fixing, painting or remodeling, and the TNO team will talk through the job with you.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Free estimate" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="You get a free, honest estimate for the work before anything begins, so there are no surprises." data-en="You get a free, honest estimate for the work before anything begins, so there are no surprises.">You get a free, honest estimate for the work before anything begins, so there are no surprises.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The work gets done" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="From a single repair to a full room repaint or remodel, TNO handles the job with the same care every time." data-en="From a single repair to a full room repaint or remodel, TNO handles the job with the same care every time.">From a single repair to a full room repaint or remodel, TNO handles the job with the same care every time.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Walk the results together" data-en="Walk the results together">Walk the results together</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Before the team leaves, you walk through the finished work together, so you know it was done right." data-en="Before the team leaves, you walk through the finished work together, so you know it was done right.">Before the team leaves, you walk through the finished work together, so you know it was done right.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; solo nombres, sin precios inventados)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine">every home</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="No two projects are the same, so every job gets its own free, honest estimate by phone, before any work begins." data-en="No two projects are the same, so every job gets its own free, honest estimate by phone, before any work begins.">No two projects are the same, so every job gets its own free, honest estimate by phone, before any work begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:0ms; border-color: rgba(47,107,63,0.4); box-shadow: 0 18px 50px rgba(35,40,30,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Interior &amp; Exterior Painting" data-en="Interior &amp; Exterior Painting">Interior &amp; Exterior Painting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full interior and exterior painting, drywall repair and patching, baseboards and surface refinishing for a fresh, clean finish." data-en="Full interior and exterior painting, drywall repair and patching, baseboards and surface refinishing for a fresh, clean finish.">Full interior and exterior painting, drywall repair and patching, baseboards and surface refinishing for a fresh, clean finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Everyday fixes" data-en="Everyday fixes">Everyday fixes</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Handyman Repairs" data-en="Handyman Repairs">Handyman Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Light fixtures, ceiling fans, blinds, curtain rods, door weather stripping, electrical outlets and TV mounting: the everyday fixes every home eventually needs." data-en="Light fixtures, ceiling fans, blinds, curtain rods, door weather stripping, electrical outlets and TV mounting: the everyday fixes every home eventually needs.">Light fixtures, ceiling fans, blinds, curtain rods, door weather stripping, electrical outlets and TV mounting: the everyday fixes every home eventually needs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Flooring" data-en="Flooring">Flooring</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Flooring &amp; Tile" data-en="Flooring &amp; Tile">Flooring &amp; Tile</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tile and wood flooring installation and refinishing, plus garage floor coatings that hold up to daily use." data-en="Tile and wood flooring installation and refinishing, plus garage floor coatings that hold up to daily use.">Tile and wood flooring installation and refinishing, plus garage floor coatings that hold up to daily use.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Bigger projects" data-en="Bigger projects">Bigger projects</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Remodeling &amp; Renovations" data-en="Remodeling &amp; Renovations">Remodeling &amp; Renovations</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Bathroom remodeling, bedroom renovations and office space renovations, plus roof and shingle repairs." data-en="Bathroom remodeling, bedroom renovations and office space renovations, plus roof and shingle repairs.">Bathroom remodeling, bedroom renovations and office space renovations, plus roof and shingle repairs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Free estimate" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Paint &amp; Surfaces" data-en="Paint &amp; Surfaces">Paint &amp; Surfaces</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Interior painting" data-en="Interior painting">Interior painting</li>
            <li class="flex items-center gap-2" data-es="Exterior painting" data-en="Exterior painting">Exterior painting</li>
            <li class="flex items-center gap-2" data-es="Drywall repair &amp; patching" data-en="Drywall repair &amp; patching">Drywall repair &amp; patching</li>
            <li class="flex items-center gap-2" data-es="Baseboards &amp; refinishing" data-en="Baseboards &amp; refinishing">Baseboards &amp; refinishing</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Repairs &amp; Install" data-en="Repairs &amp; Install">Repairs &amp; Install</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Light fixtures &amp; ceiling fans" data-en="Light fixtures &amp; ceiling fans">Light fixtures &amp; ceiling fans</li>
            <li class="flex items-center gap-2" data-es="Blinds &amp; curtain rods" data-en="Blinds &amp; curtain rods">Blinds &amp; curtain rods</li>
            <li class="flex items-center gap-2" data-es="Door weather stripping" data-en="Door weather stripping">Door weather stripping</li>
            <li class="flex items-center gap-2" data-es="TV mounting &amp; outlets" data-en="TV mounting &amp; outlets">TV mounting &amp; outlets</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Flooring &amp; Remodel" data-en="Flooring &amp; Remodel">Flooring &amp; Remodel</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Tile &amp; wood flooring" data-en="Tile &amp; wood flooring">Tile &amp; wood flooring</li>
            <li class="flex items-center gap-2" data-es="Garage floor coatings" data-en="Garage floor coatings">Garage floor coatings</li>
            <li class="flex items-center gap-2" data-es="Bathroom &amp; bedroom remodeling" data-en="Bathroom &amp; bedroom remodeling">Bathroom &amp; bedroom remodeling</li>
            <li class="flex items-center gap-2" data-es="Roof &amp; shingle repair" data-en="Roof &amp; shingle repair">Roof &amp; shingle repair</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on scope and materials. Call (267) 726-1015 for a free, honest estimate." data-en="Pricing depends on scope and materials. Call (267) 726-1015 for a free, honest estimate.">Pricing depends on scope and materials. Call (267) 726-1015 for a free, honest estimate.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex; 3 fotos reales curadas)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="projects" data-en="projects">projects</span>')
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Renovación de fachada, terminada" data-en="Exterior renovation, finished right">Exterior renovation, finished right</span><img src="assets/gallery-exterior-stonework.jpg" alt="A finished stone facade and garage door renovation by TNO Painting and Handyman" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Antes: mesa desgastada" data-en="Before: worn patio table">Before: worn patio table</span><img src="assets/gallery-table-before.jpg" alt="A weathered patio table before refinishing by TNO Painting and Handyman" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Después: renovada" data-en="After: refinished and revived">After: refinished and revived</span><img src="assets/gallery-table-after.jpg" alt="The same patio table refinished and revived by TNO Painting and Handyman" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Lakeland" data-en="What Lakeland">What Lakeland</span> <span class="text-shine" data-es="homeowners say" data-en="homeowners say">homeowners say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.7 out of 5 · 39 reviews on Google" data-en="4.7 out of 5 · 39 reviews on Google">4.7 out of 5 · 39 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"TNO has provided me with phenomenal services! Mr. Bucknor is very patient, trustworthy, professional, understanding, and affordable."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Henreta Jarrett</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña verificada" data-en="Verified review">Verified review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"This company took very good care of us. He was fast and knowledgeable and even gave my husband some info we could use."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Michelle Cain</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña verificada" data-en="Verified review">Verified review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Shane and Osari were both very professional and courteous. They were very efficient but took care to get everything just right."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Kim George</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña verificada" data-en="Verified review">Verified review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read more reviews" data-en="Read more reviews">Read more reviews</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (sin direccion fija: se muestra como area de servicio)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Lakeland, FL</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,107,63,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Service area" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="TNO Painting and Handyman works by appointment across Lakeland, Winter Haven and the surrounding Polk County area." data-en="TNO Painting and Handyman works by appointment across Lakeland, Winter Haven and the surrounding Polk County area.">TNO Painting and Handyman works by appointment across Lakeland, Winter Haven and the surrounding Polk County area.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,107,63,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="View on map" data-en="View on map">View on map</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,107,63,0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Estimates" data-en="Estimates">Estimates</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Every job starts with a free, honest estimate over the phone before any work begins." data-en="Every job starts with a free, honest estimate over the phone before any work begins.">Every job starts with a free, honest estimate over the phone before any work begins.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,107,63,0.4)]" href="''' + NEW_TEL + '''" data-es="Call (267) 726-1015" data-en="Call (267) 726-1015">Call (267) 726-1015</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,107,63,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See recent jobs from the TNO team and message any questions before you call." data-en="See recent jobs from the TNO team and message any questions before you call.">See recent jobs from the TNO team and message any questions before you call.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,107,63,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: TNO Painting and Handyman service area, Lakeland FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Quality work you can trust." data-en="Quality work you can trust.">Quality work you can trust.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your next project," data-en="Your next project,">Your next project,</span> <span class="text-shine" data-es="handled right" data-en="handled right">handled right</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call or text (267) 726-1015 for a free, honest estimate on your painting, repair or remodeling project." data-en="Call or text (267) 726-1015 for a free, honest estimate on your painting, repair or remodeling project.">Call or text (267) 726-1015 for a free, honest estimate on your painting, repair or remodeling project.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (267) 726-1015" data-en="Call (267) 726-1015">Call (267) 726-1015</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">TNO</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(185,220,185,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    MONO_SPAN.replace('w-10 h-10', 'w-9 h-9') + '''
          <span class="font-display text-lg tracking-[0.1em] uppercase">TNO Painting &amp; Handyman</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Painting &amp; handyman services in Lakeland, Winter Haven and Polk County, FL. Free estimates." data-en="Painting &amp; handyman services in Lakeland, Winter Haven and Polk County, FL. Free estimates.">Painting &amp; handyman services in Lakeland, Winter Haven and Polk County, FL. Free estimates.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[#b9dcb9]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p data-es="Lakeland, FL &amp; Polk County" data-en="Lakeland, FL &amp; Polk County">Lakeland, FL &amp; Polk County</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#b9dcb9]" data-es="Call (267) 726-1015" data-en="Call (267) 726-1015">Call (267) 726-1015</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#b9dcb9]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#b9dcb9]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#b9dcb9]">Facebook · TNO Painting and Handyman</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 TNO Painting and Handyman Service LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar (icono de telefono en vez de calendario)
# ---------------------------------------------------------------------------
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f5f3e9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>''',
    '''<a href="''' + NEW_TEL + '''" class="book-float" aria-label="Call TNO Painting and Handyman">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f5f3e9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
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
    "4.7 · 39 reviews on Google": "4.7 · 39 reseñas en Google",
    "4.7 out of 5 · 39 reviews on Google": "4.7 de 5 · 39 reseñas en Google",
    "Bathroom &amp; bedroom remodeling": "Remodelación de baño y dormitorio",
    "Bigger projects": "Proyectos grandes",
    "Blinds &amp; curtain rods": "Persianas y cortineros",
    "Call": "Llamar",
    "Call (267) 726-1015": "Llama al (267) 726-1015",
    "Call or text (267) 726-1015 for a free, honest estimate on your painting, repair or remodeling project.":
        "Llama o escribe al (267) 726-1015 para una cotización gratis y honesta para tu proyecto de pintura, reparación o remodelación.",
    "Free estimate": "Cotización gratis",
    "Call or text": "Llama o escribe",
    "Estimates": "Cotizaciones",
    "Free &amp; honest": "Gratis y honesta",
    "Call or text anytime": "Llama o escribe cuando quieras",
    "Contact": "Contacto",
    "Door weather stripping": "Sellado de puertas",
    "Drywall repair &amp; patching": "Reparación de paredes de yeso",
    "Baseboards &amp; refinishing": "Zócalos y refinado de superficies",
    "Everyday fixes": "Arreglos cotidianos",
    "Exterior painting": "Pintura exterior",
    "Interior painting": "Pintura interior",
    "Flooring": "Pisos",
    "Flooring &amp; Remodel": "Pisos y Remodelación",
    "Flooring &amp; Tile": "Pisos y Azulejos",
    "Follow": "Síguenos",
    "Follow on Instagram": "Síguenos en Instagram",
    "Painting &amp; handyman services in Lakeland, Winter Haven and Polk County, FL. Free estimates.":
        "Servicios de pintura y reparaciones del hogar en Lakeland, Winter Haven y el condado de Polk, FL. Cotizaciones gratis.",
    "Lakeland, FL · Painting &amp; Handyman": "Lakeland, FL · Pintura y Reparaciones",
    "Garage floor coatings": "Recubrimiento de pisos de garaje",
    "Handyman Repairs": "Reparaciones del Hogar",
    "Honest, upfront pricing": "Precios honestos y claros",
    "Instagram &amp; Facebook": "Instagram y Facebook",
    "Interior &amp; Exterior Painting": "Pintura Interior y Exterior",
    "Full interior and exterior painting, drywall repair and patching, baseboards and surface refinishing for a fresh, clean finish.":
        "Pintura interior y exterior completa, reparación de paredes de yeso, zócalos y refinado de superficies para un acabado fresco y limpio.",
    "Light fixtures, ceiling fans, blinds, curtain rods, door weather stripping, electrical outlets and TV mounting: the everyday fixes every home eventually needs.":
        "Lámparas, ventiladores de techo, persianas, cortineros, sellado de puertas, tomacorrientes e instalación de televisores: los arreglos cotidianos que toda casa necesita tarde o temprano.",
    "Tile and wood flooring installation and refinishing, plus garage floor coatings that hold up to daily use.":
        "Instalación y refinado de pisos de azulejo y madera, más recubrimientos de piso de garaje que resisten el uso diario.",
    "Bathroom remodeling, bedroom renovations and office space renovations, plus roof and shingle repairs.":
        "Remodelación de baños, renovación de dormitorios y espacios de oficina, más reparación de techos y tejas.",
    "Light fixtures &amp; ceiling fans": "Lámparas y ventiladores de techo",
    "Most requested": "Lo más solicitado",
    "Paint &amp; Surfaces": "Pintura y Superficies",
    "Call or text (267) 726-1015 with what needs fixing, painting or remodeling, and the TNO team will talk through the job with you.":
        "Llama o escribe al (267) 726-1015 con lo que necesitas reparar, pintar o remodelar, y el equipo de TNO hablará contigo sobre el trabajo.",
    "TNO Painting and Handyman has been fixing, painting and renovating homes across Lakeland, Winter Haven and Polk County since 2016. From a full room repaint to bathroom remodels, flooring and general repairs, the TNO team shows up, gives a free estimate, and gets the job done right.":
        "TNO Painting and Handyman lleva desde 2016 reparando, pintando y renovando casas en Lakeland, Winter Haven y el condado de Polk. Desde repintar un cuarto completo hasta remodelaciones de baño, pisos y reparaciones generales, el equipo de TNO llega, da una cotización gratis, y hace el trabajo bien.",
    "Remodeling &amp; Renovations": "Remodelación y Renovaciones",
    "Repairs &amp; Install": "Reparaciones e Instalación",
    "Roof &amp; shingle repair": "Reparación de techo y tejas",
    "Serving Lakeland &amp; Polk County": "Sirviendo a Lakeland y el condado de Polk",
    "Since": "Desde",
    "Painting and handyman work": "El trabajo de pintura y reparaciones",
    "Lakeland homes ": "que las casas de Lakeland ",
    "can count on": "pueden confiar",
    "The result: a 4.7-star rating across 39 Google reviews, a free estimate on every job, and homeowners who call TNO first the next time something needs fixing, painting or replacing.":
        "El resultado: una calificación de 4.7 estrellas en 39 reseñas de Google, cotización gratis en cada trabajo, y dueños de casa que llaman primero a TNO la próxima vez que algo necesita reparación, pintura o reemplazo.",
    "The work gets done": "El trabajo se hace",
    "From a single repair to a full room repaint or remodel, TNO handles the job with the same care every time.":
        "Desde una sola reparación hasta repintar un cuarto completo o una remodelación, TNO maneja el trabajo con el mismo cuidado siempre.",
    "TV mounting &amp; outlets": "Instalación de TV y tomacorrientes",
    "Tile &amp; wood flooring": "Pisos de azulejo y madera",
    "View on map": "Ver en el mapa",
    "Walk the results together": "Revisan los resultados juntos",
    "Before the team leaves, you walk through the finished work together, so you know it was done right.":
        "Antes de que el equipo se vaya, revisan juntos el trabajo terminado, para que sepas que quedó bien hecho.",
    "What Lakeland": "Lo que dicen los",
    "homeowners say": "dueños de casa en Lakeland",
    "You get a free, honest estimate for the work before anything begins, so there are no surprises.":
        "Recibes una cotización gratis y honesta para el trabajo antes de empezar, sin sorpresas.",
    "Your next project,": "Tu próximo proyecto,",
    "handled right": "bien hecho",
    "Your project, start": "Tu proyecto, de inicio",
    "to finish": "hasta el final",
    "Free": "Gratis",
    "Free Estimate": "Cotización Gratis",
    "Estimates": "Cotizaciones",
    "Serving since": "Sirviendo desde",
    "Painting and repairs,": "Pintura y reparaciones,",
    "done the right way": "hechas bien",
    "TNO Painting and Handyman Service LLC has served Lakeland, Winter Haven and the surrounding Polk County area since 2016. The team, managed by Tiffari Bucknor, handles everything from interior and exterior painting to drywall repair, flooring and full bathroom remodels, with technicians like Shane and Osari doing the hands-on work on site.":
        "TNO Painting and Handyman Service LLC ha servido a Lakeland, Winter Haven y el área circundante del condado de Polk desde 2016. El equipo, dirigido por la gerente Tiffari Bucknor, maneja todo, desde pintura interior y exterior hasta reparación de paredes, pisos y remodelaciones de baño completas, con técnicos como Shane y Osari haciendo el trabajo manual en el sitio.",
    "Manager, TNO Painting and Handyman": "Gerente, TNO Painting and Handyman",
    "No two projects are the same, so every job gets its own free, honest estimate by phone, before any work begins.":
        "Ningún proyecto es igual a otro, así que cada trabajo recibe su propia cotización gratis y honesta por teléfono, antes de comenzar.",
    "Pricing depends on scope and materials. Call (267) 726-1015 for a free, honest estimate.":
        "El precio depende del alcance y los materiales. Llama al (267) 726-1015 para una cotización gratis y honesta.",
    "Quality work you can trust.": "Trabajo de calidad en el que puedes confiar.",
    "Read more reviews": "Lee más reseñas",
    "Real": "Trabajo",
    "projects": "real",
    "Reseña verificada": "Reseña verificada",
    "Verified review": "Reseña verificada",
    "Serving": "Sirviendo a",
    "Service area": "Área de servicio",
    "TNO Painting and Handyman works by appointment across Lakeland, Winter Haven and the surrounding Polk County area.":
        "TNO Painting and Handyman trabaja con cita previa en Lakeland, Winter Haven y el área circundante del condado de Polk.",
    "Every job starts with a free, honest estimate over the phone before any work begins.":
        "Cada trabajo comienza con una cotización gratis y honesta por teléfono antes de empezar.",
    "See recent jobs from the TNO team and message any questions before you call.":
        "Mira trabajos recientes del equipo de TNO y escribe cualquier duda antes de llamar.",
    "Services for": "Servicios para",
    "Polk County, FL": "Condado de Polk, FL",
    "Exterior renovation, finished right": "Renovación de fachada, terminada",
    "Before: worn patio table": "Antes: mesa de patio desgastada",
    "After: refinished and revived": "Después: renovada",
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
