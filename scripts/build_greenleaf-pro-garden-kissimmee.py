#!/usr/bin/env python3
"""
Build script for output/greenleaf-pro-garden-kissimmee/index.html
Derived from templates/dark-v2/index.html (Pure Artistry skeleton) via anchored
transformation, per templates/SKELETONS-V2.md. Landscaping business, GreenPal-only,
no bookable menu, no own site -> VARIANTE ADAPTADA (FORGE-BRIEF 0.b): no fixed
prices (quote-based), no interactive map (mobile lawn-care crew, address is not a
public storefront), CTA -> real GreenPal profile + verified phone.
"""
import re

SLUG = "greenleaf-pro-garden-kissimmee"
SRC = "templates/dark-v2/index.html"
PATH = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    count = h.count(a)
    assert count >= n, f"NO MATCH (found {count}, need {n}): {a[:90]!r}"
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    count = h.count(a)
    if expect is not None:
        assert count == expect, f"COUNT MISMATCH (found {count}, expected {expect}): {a[:90]!r}"
    else:
        assert count >= 1, f"NO MATCH: {a[:90]!r}"
    h = h.replace(a, b)


def rep_re(pattern, repl, n=1, flags=re.S):
    global h
    new_h, cnt = re.subn(pattern, repl, h, count=n, flags=flags)
    assert cnt == n, f"REGEX MATCH COUNT {cnt} != {n}: {pattern[:90]!r}"
    h = new_h


GREENPAL = "https://www.yourgreenpal.com/greenleaf-pro-garden"
NEXTDOOR = "https://nextdoor.com/pages/greenleaf-pro-garden/"
TEL = "+14075531467"
TEL_DISPLAY = "(407) 553-1467"

# ============================================================
# STEP 1: Protect the Merktop badge block (stays gold, always)
# ============================================================
badge_re = re.compile(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", re.S)
m = badge_re.search(h)
assert m, "merktop badge block not found"
badge_block = m.group(0)
h = h[:m.start()] + "@@BADGE@@" + h[m.end():]

# ============================================================
# STEP 2: Palette - hue-rotate every gold/amber tone to olive-lime green
# (computed via HSL rotation, hue=88deg, preserving L/S so every gradient/
# shadow/glass-border relationship stays intact). Distinct from every other
# landscaping build in output/: otechlandscaping's forest #3d6b2f (light),
# papa-green-lawn-care-brandon's turf #2b6a38 (light), garden-now-landscaping
# -orlando's olive #45703a (light), pride-landscaping-cape-coral's bright grass
# #55ca65 (dark, hue~128), bonzailandscapingportstlucie's sky blue #48a7d7
# (dark), valeria-landscape-north-miami's teal #146b60 (light, hue~172),
# rapalo-landscaping-north-miami's jade #4bd490 (dark, hue~150). #94d44b
# (hue~88) is a distinct yellow-green olive-lime, not a repeat of any hex above.
# ============================================================
HEX_MAP = {
    "0c0905": "090c05", "0f0b07": "0b0f07", "100c05": "0b1005", "171207": "101707",
    "191307": "111907", "1c1408": "131c08", "241c0e": "1a240e", "6b5222": "496b22",
    "8a744a": "6c8a4a", "96742c": "65962c", "9a7431": "699a31", "b8934a": "85b84a",
    "bfa060": "93bf60", "c9a04a": "8ec94a", "c9ab6b": "9dc96b", "d4a84b": "94d44b",
    "e5c374": "b0e574", "e8c476": "b3e876", "e8cf96": "c2e896", "e9c3ab": "cce9ab",
    "ecd9a8": "cceca8", "f0dc9e": "caf09e", "f0dcae": "d1f0ae", "f4eee2": "ecf4e2",
    "f5efe3": "edf5e3", "f8eed3": "e7f8d3", "faf1dc": "ecfadc", "fbf6ea": "f3fbea",
}
RGB_MAP = {
    "110,85,35": "75,110,35", "122,90,30": "79,122,30", "15,11,7": "11,15,7",
    "180,140,60": "124,180,60", "185,138,128": "158,185,128", "212,168,75": "148,212,75",
    "232,207,150": "194,232,150", "232,210,160": "198,232,160", "244,238,226": "236,244,226",
    "245,239,227": "237,245,227", "27,21,14": "21,27,14", "36,28,20": "29,36,20",
    "54,42,38": "47,54,38", "80,58,18": "51,80,18",
}
for old, new in HEX_MAP.items():
    # some source colors (e.g. #D4A84B) only occur inside the protected badge
    # block and are legitimately absent from `h` at this point; skip those.
    h = h.replace("#" + old, "#" + new)
for old, new in RGB_MAP.items():
    h = h.replace("rgba(" + old, "rgba(" + new)

# Restore protected badge (always gold, per pipeline rule)
h = h.replace("@@BADGE@@", badge_block)

print("Palette OK")

# ============================================================
# STEP 3: HEAD (title, meta, og, icon, JSON-LD)
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Greenleaf Pro Garden · Lawn Care in Kissimmee, FL | 4.8 on GreenPal</title>'
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Greenleaf Pro Garden: lawn mowing, edging, bush trimming and mulch in Kissimmee and Orlando, FL. 4.8 rating across 73 GreenPal reviews. Free quotes." />'
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Greenleaf Pro Garden · Lawn Care in Kissimmee, FL" />'
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Lawn mowing, edging, bush trimming and mulch across Kissimmee and Orlando. 4.8 rating, 73 reviews on GreenPal." />'
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/hero-ranch-house-palm.jpg" />'
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect width=%22100%22 height=%22100%22 rx=%2222%22 fill=%22%2394d44b%22/%3E%3Ctext x=%2250%22 y=%2263%22 font-size=%2238%22 font-family=%22Georgia,serif%22 fill=%22%230b0f07%22 text-anchor=%22middle%22%3EGP%3C/text%3E%3C/svg%3E" />'
)

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LandscapingBusiness",
    "name": "Greenleaf Pro Garden",
    "description": "Lawn care and garden maintenance company serving Kissimmee and the greater Orlando area, FL: mowing, edging, bush trimming and mulch, booked and reviewed through GreenPal.",
    "telephone": "+1-407-553-1467",
    "address": { "@type": "PostalAddress", "streetAddress": "2611 Hawthorne Lane", "addressLocality": "Kissimmee", "addressRegion": "FL", "postalCode": "34743", "addressCountry": "US" },
    "areaServed": ["Kissimmee, FL", "Orlando, FL"],
    "sameAs": ["https://www.yourgreenpal.com/greenleaf-pro-garden", "https://nextdoor.com/pages/greenleaf-pro-garden/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.78", "reviewCount": "73", "bestRating": "5" },
    "priceRange": "$20-$45",
    "makesOffer": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Lawn Mowing & Edging" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Yard Cleanup" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bush Trimming" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Mulch" } }
    ]
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]

# ============================================================
# STEP 4: Language - business is EN-primary (GreenPal meta/FAQ/reviews all EN),
# dark-v2 template already defaults applyLang to EN and <html lang="en"> -> no swap needed.
# ============================================================
mlang = re.search(r"applyLang\(lang === '(\w\w)' \? '\w\w' : '(\w\w)'\)", h)
assert mlang and mlang.group(2) == 'en', 'template default is not EN as expected'

# ============================================================
# STEP 5: PRELOADER
# ============================================================
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">GP</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Greenleaf Pro Garden</span>')

# ============================================================
# STEP 6: NAV (logo image -> text monogram, no verified brand logo file;
# vendor-supplied profile image was an unusable low-angle selfie)
# ============================================================
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(148,212,75,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-lg ring-1 ring-[rgba(148,212,75,0.35)] bg-[rgba(148,212,75,0.1)] text-[color:var(--accent-deep)]">GP</span>\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Greenleaf <span class="text-[color:var(--accent-deep)]">Pro Garden</span></span>'
)
rep('<a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
    '<a class="nav-link" href="#experiencia" data-es="Nuestra Historia" data-en="Our Story">Our Story</a>')
rep('<a class="nav-link" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
    '<a class="nav-link" href="#metodo" data-es="Cómo Trabajamos" data-en="How It Works">How It Works</a>')
rep('<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>', '<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Services</a>', n=1)
rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>', '<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>', n=1)
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>', '<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>', n=1)
rep('<a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>',
    '<a class="nav-link" href="#ubicacion" data-es="Zona de Servicio" data-en="Service Area">Service Area</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="Nuestra Historia" data-en="Our Story">Our Story</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="Cómo Trabajamos" data-en="How It Works">How It Works</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Services</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>')
rep('<a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>',
    '<a class="py-3 px-3" href="#ubicacion" data-es="Zona de Servicio" data-en="Service Area">Service Area</a>')
rep(
    '<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n        </a>',
    f'<a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>\n          <span data-es="Cotización Gratis" data-en="Free Quote">Free Quote</span>\n        </a>'
)
rep(
    f'<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    f'<a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Cotización Gratis" data-en="Free Quote">Free Quote</a>'
)

# ============================================================
# STEP 7: HERO
# ============================================================
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Kissimmee, FL · Cuidado de Jardines" data-en="Kissimmee, FL · Lawn &amp; Garden Care">Kissimmee, FL · Lawn &amp; Garden Care</p>'
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu césped, en buenas manos." data-en="Your yard, in good hands.">Your yard, in good hands.</p>'
)
rep(
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Corte, limpieza y" data-en="Mowing, cleanup and">Mowing, cleanup and</span><br /><span data-es="buena imagen para tu " data-en="curb appeal for your ">curb appeal for your </span><span class="text-shine" data-es="jardín en Kissimmee" data-en="Kissimmee yard">Kissimmee yard</span>
        </h1>'''
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Emmanuel Rodriguez y el equipo de Greenleaf Pro Garden cuidan céspedes en Kissimmee y Orlando: corte, orillado, recorte de arbustos y mantillo, con los recortes triturados y devueltos al césped en cada visita." data-en="Emmanuel Rodriguez and the Greenleaf Pro Garden crew take care of lawns across Kissimmee and Orlando: mowing, edging, bush trimming and mulch, with clippings mulched back into the lawn on every visit.">Emmanuel Rodriguez and the Greenleaf Pro Garden crew take care of lawns across Kissimmee and Orlando: mowing, edging, bush trimming and mulch, with clippings mulched back into the lawn on every visit.</p>'
)
rep(
    '''<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>
        </div>''',
    '''<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.8 · 73 reseñas en GreenPal" data-en="4.8 · 73 reviews on GreenPal">4.8 · 73 reviews on GreenPal</span>
        </div>'''
)
rep(
    f'''<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>''',
    f'''<a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Cotización Gratis" data-en="Get a Free Quote">Get a Free Quote</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="tel:{TEL}" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span data-es="{TEL_DISPLAY}" data-en="{TEL_DISPLAY}">{TEL_DISPLAY}</span>
          </a>'''
)
rep(
    '''<div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>
          </div>''',
    '''<div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/hero-ranch-house-palm.jpg" alt="Freshly mowed lawn and clean driveway at a Kissimmee-area home serviced by Greenleaf Pro Garden" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Cotización" data-en="Quote">Quote</p>
            <p class="font-display text-lg" data-es="Estimado gratis" data-en="Free Estimate">Free Estimate</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Kissimmee, FL" data-en="Kissimmee, FL">Kissimmee, FL</p>
          </div>'''
)

# ============================================================
# STEP 8: STRIP DE CONFIANZA
# ============================================================
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.78" data-decimals="1">4.8</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="73">73</span> <span data-es="reseñas en GreenPal" data-en="reviews on GreenPal">reviews on GreenPal</span></p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Mowing <span class="text-shine">&amp;</span> Cleanup</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicio recurrente" data-en="Recurring service">Recurring service</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">2026</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Fundado en" data-en="Founded in">Founded in</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Kissimmee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Zona de servicio" data-en="Service area">Kissimmee &amp; Orlando, FL</p></div>'
)

# ============================================================
# STEP 9: MARQUEE (x2 blocks, 4 occurrences per word)
# ============================================================
marquee_words = [
    ('Silk Press', 'Lawn Mowing'),
    ('Loc Retwist', 'Edging'),
    ('Knotless Braids', 'Bush Trimming'),
    ('K-Tip Extensions', 'Mulching'),
    ('Keratin', 'Yard Cleanup'),
    ('Orlando, FL', 'Kissimmee, FL'),
]
for old_w, new_w in marquee_words:
    old_span = f'<span class="marquee-word">{old_w}</span>'
    cnt = h.count(old_span)
    assert cnt == 4, f'expected 4 occurrences of {old_span!r}, found {cnt}'
    h = h.replace(old_span, f'<span class="marquee-word">{new_w}</span>')

# ============================================================
# STEP 10: LA EXPERIENCIA / OUR STORY
# ============================================================
rep(
    '''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''',
    '''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/about-townhome-walkway.jpg" alt="Freshly mowed front yard and walkway at a Kissimmee townhome serviced by Greenleaf Pro Garden" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-cul-de-sac-tan-house.jpg" alt="Mowed lawn on a cul-de-sac lot in the Kissimmee area" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>'''
)
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Nuestra historia" data-en="Our story">Our story</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un equipo local" data-en="A local crew">A local crew</span><br /><span class="text-shine" data-es="que cuida tu jardín bien" data-en="that treats your yard right">that treats your yard right</span></h2>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Greenleaf Pro Garden es el negocio de Emmanuel Rodriguez, atendiendo a familias en Kissimmee y en toda el área de Orlando desde marzo de 2026." data-en="Greenleaf Pro Garden is run by Emmanuel Rodriguez, serving homeowners across Kissimmee and the greater Orlando area since March 2026.">Greenleaf Pro Garden is run by Emmanuel Rodriguez, serving homeowners across Kissimmee and the greater Orlando area since March 2026.</p>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 4.8 de calificación en 73 reseñas verificadas en GreenPal, recortes triturados y devueltos al césped en cada visita, y un calendario que puedes pausar cuando quieras, sin penalidad." data-en="The result: a 4.8 rating across 73 verified reviews on GreenPal, clippings mulched back into the lawn on every visit, and a schedule you can pause anytime, no penalty.">The result: a 4.8 rating across 73 verified reviews on GreenPal, clippings mulched back into the lawn on every visit, and a schedule you can pause anytime, no penalty.</p>'
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.78" data-decimals="1">4.8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">GreenPal</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="73">73</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2026</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Fundado" data-en="Founded">Founded</p></div>'
)
rep(
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(148,212,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(148,212,75,0.3)] bg-[rgba(148,212,75,0.1)] text-[color:var(--accent-deep)]">ER</span>
            <span class="text-sm font-light">Emmanuel Rodriguez · <span class="text-[color:var(--ink-40)]" data-es="Dueño" data-en="Owner">Owner</span></span>
          </div>'''
)

# ============================================================
# STEP 11: EL METODO / HOW IT WORKS
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Cómo trabajamos" data-en="How it works">How it works</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Simple, de principio" data-en="Simple, start">Simple, start</span> <span class="text-shine" data-es="a fin" data-en="to finish">to finish</span></h2>'
)
step_blocks = [
    ('Reserva online', 'Book online',
     'Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante.',
     'Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.',
     'Cotización Gratis', 'Request a Free Quote',
     'Escribe a través de GreenPal y cuéntanos sobre tu propiedad. La mayoría de las solicitudes reciben respuesta rápido.',
     'Reach out through GreenPal and tell us about your property. Most requests get a response quickly.'),
    ('Consulta capilar', 'Hair consult',
     'Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad.',
     'Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.',
     'Coordina tu Visita', 'Schedule Your Visit',
     'Elige el día que te convenga: servicio disponible los 7 días de la semana, todo el año.',
     'Pick a day that works for you: service is available seven days a week, year round.'),
    ('Manos a la obra', 'The work',
     'Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros.',
     'From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.',
     'Corte, Orillado y Limpieza', 'Mowing, Edging &amp; Cleanup',
     'Corte, orillado, recorte de arbustos y mantillo, con los recortes triturados y devueltos al césped para un corte más saludable.',
     'Mowing, edging, bush trimming and mulch, with clippings mulched back into the lawn for a healthier cut.'),
    ('El toque final', 'The finish',
     'Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada.',
     'You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.',
     'Pausa Cuando Quieras', 'Pause Anytime',
     'Salta o reprograma cualquier visita desde tu panel de GreenPal, sin penalidad, cuando lo necesites.',
     'Skip or reschedule any visit from your GreenPal dashboard, no penalty, whenever you need to.'),
]
for old_title_es, old_title_en, old_text_es, old_text_en, new_title_es, new_title_en, new_text_es, new_text_en in step_blocks:
    rep(f'data-es="{old_title_es}" data-en="{old_title_en}">{old_title_en}</h3>',
        f'data-es="{new_title_es}" data-en="{new_title_en}">{new_title_en}</h3>')
    rep(f'data-es="{old_text_es}" data-en="{old_text_en}">{old_text_en}</p>',
        f'data-es="{new_text_es}" data-en="{new_text_en}">{new_text_en}</p>')

# ============================================================
# STEP 12: SERVICIOS (variante adaptada: sin precios fijos, cotizacion, CTA GreenPal)
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que" data-en="What we">What we</span> <span class="text-shine" data-es="hacemos" data-en="do">do</span></h2>'
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cada propiedad es distinta: el precio se cotiza según el tamaño y lo que necesites, sin sorpresas." data-en="Every property is different: pricing is quoted based on size and what you need, no surprises.">Every property is different: pricing is quoted based on size and what you need, no surprises.</p>'
)

services_grid = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert services_grid, 'services grid anchor not found'
NEW_SERVICES = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(148,212,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y Orillado" data-en="Lawn Mowing &amp; Edging">Lawn Mowing &amp; Edging</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte regular a la altura correcta con orillado limpio, recortes triturados y devueltos al césped para un pasto más saludable en cada visita." data-en="Regular mowing at the right height with clean edging, clippings mulched back into the lawn for healthier turf on every visit.">Regular mowing at the right height with clean edging, clippings mulched back into the lawn for healthier turf on every visit.</p>
          <div class="mt-auto">
            <a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Repaso a fondo" data-en="Deeper pass">Deeper pass</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Limpieza de Patio" data-en="Yard Cleanup">Yard Cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Limpieza de patio para despejar restos y poner propiedades descuidadas de nuevo en forma." data-en="Yard cleanup service to clear debris and get overgrown properties back in shape.">Yard cleanup service to clear debris and get overgrown properties back in shape.</p>
          <div class="mt-auto">
            <a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Detalle" data-en="Detail work">Detail work</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Recorte de Arbustos" data-en="Bush Trimming">Bush Trimming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Recorte de arbustos y setos para mantener la propiedad prolija entre cortes de césped." data-en="Bush and shrub trimming to keep the property neat and tidy between mows.">Bush and shrub trimming to keep the property neat and tidy between mows.</p>
          <div class="mt-auto">
            <a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Jardines" data-en="Garden beds">Garden beds</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Mantillo" data-en="Mulch">Mulch</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Servicio de mantillo para camas de jardín y áreas ajardinadas, renovado cuando lo necesites." data-en="Mulch service for garden beds and landscaping, refreshed on request.">Mulch service for garden beds and landscaping, refreshed on request.</p>
          <div class="mt-auto">
            <a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    f'<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: recortes mulcheados en cada visita y pausa de servicio sin penalidad cuando la necesites. Cotización y disponibilidad en GreenPal." data-en="Also: clippings mulched on every visit and pause your service with no penalty whenever you need to. Quotes and availability on GreenPal.">Also: clippings mulched on every visit and pause your service with no penalty whenever you need to. Quotes and availability on GreenPal.</span></p>'
)

# ============================================================
# STEP 13: GALERIA
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Jardines" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="yards">yards</span></h2>'
)
rep(
    f'''<a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @pure.artistrysk
        </a>''',
    f'''<a href="{GREENPAL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg>
          <span data-es="Ver en GreenPal" data-en="See on GreenPal">See on GreenPal</span>
        </a>'''
)
gallery_grid = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*(?=</div>\s*</section>\s*<!-- MARQUEE -->)', h, flags=re.S)
assert gallery_grid, 'gallery grid anchor not found'
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Buena imagen" data-en="Fresh curb appeal">Fresh curb appeal</span><img src="assets/raw/gallery-two-story-curved-driveway.jpg" alt="Two-story Kissimmee-area home with a mowed lawn and curved driveway serviced by Greenleaf Pro Garden" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Bordes limpios" data-en="Clean edges">Clean edges</span><img src="assets/raw/gallery-pink-house-palm-patio.jpg" alt="Home with a palm tree and freshly edged lawn serviced in the Kissimmee area" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Líneas de corte" data-en="Sharp mow lines">Sharp mow lines</span><img src="assets/raw/gallery-yellow-house-mow-lines.jpg" alt="Lawn with crisp mowing lines at a Kissimmee-area property" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="De la calle a la puerta" data-en="Driveway to curb">Driveway to curb</span><img src="assets/raw/gallery-green-house-driveway.jpg" alt="Home with a mowed lawn and clean driveway serviced by Greenleaf Pro Garden" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Listo para el cul-de-sac" data-en="Cul-de-sac ready">Cul-de-sac ready</span><img src="assets/raw/about-cul-de-sac-tan-house.jpg" alt="Mowed lawn on a cul-de-sac lot in the Kissimmee area" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Aceras prolijas" data-en="Tidy sidewalks">Tidy sidewalks</span><img src="assets/raw/gallery-tan-house-palm-sidewalk.jpg" alt="Palm tree and mowed lawn along a sidewalk at a Kissimmee-area home" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]

# ============================================================
# STEP 14: OPINIONES / REVIEWS (only 2 real quotes with body text found on
# GreenPal's own live JSON-LD out of the 20 shown -- kept to a real 2-card
# grid per pipeline rule against fabricating quotes. Grid changed from
# sm:grid-cols-3 to sm:grid-cols-2 and the 3rd figure removed.)
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen los" data-en="What Kissimmee">What Kissimmee</span> <span class="text-shine" data-es="vecinos de Kissimmee" data-en="homeowners say">homeowners say</span></h2>'
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.8 de 5 · 73 reseñas verificadas en GreenPal" data-en="4.8 out of 5 · 73 verified reviews on GreenPal">4.8 out of 5 · 73 verified reviews on GreenPal</span></p>'
)
reviews_grid = re.search(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)', h, flags=re.S)
assert reviews_grid, 'reviews grid anchor not found'
NEW_REVIEWS = '''<div class="grid sm:grid-cols-2 gap-5 items-stretch max-w-2xl mx-auto">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Good job"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Marissa Camohoy</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Completed the service, thank you."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rj Temple</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
      </div>'''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep(
    f'<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    f'<a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 73 reseñas en GreenPal" data-en="Read all 73 reviews on GreenPal">Read all 73 reviews on GreenPal</a>'
)

# ============================================================
# STEP 15: UBICACION / SERVICE AREA (variante adaptada: mobile lawn-care
# crew, address is not a public storefront -> real photo instead of an
# interactive map, per FORGE-BRIEF 0.b)
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Zona de servicio" data-en="Service area">Service area</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Atendemos" data-en="Serving">Serving</span> <span class="text-shine" data-es="Kissimmee y Orlando" data-en="Kissimmee &amp; Orlando">Kissimmee &amp; Orlando</span></h2>'
)
rep(
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(148,212,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Área de servicio" data-en="Coverage area">Coverage area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Kissimmee, Orlando y comunidades cercanas de los condados de Osceola y Orange, FL. El equipo va a tu propiedad, sin local al que visitar." data-en="Kissimmee, Orlando and nearby Osceola &amp; Orange County neighborhoods, FL. The crew comes to your property, there is no storefront to visit.">Kissimmee, Orlando and nearby Osceola &amp; Orange County neighborhoods, FL. The crew comes to your property, there is no storefront to visit.</p>
            </div>
          </div>'''
)
rep(
    f'''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(148,212,75,0.4)]" href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>''',
    f'''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Cotización" data-en="Get a quote">Get a quote</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Escribe por GreenPal con tu dirección y lo que necesitas. La mayoría de las solicitudes reciben respuesta rápido." data-en="Message through GreenPal with your address and what you need done. Most requests get a response quickly.">Message through GreenPal with your address and what you need done. Most requests get a response quickly.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(148,212,75,0.4)]" href="{GREENPAL}" target="_blank" rel="noopener" data-es="Pedir cotización en GreenPal" data-en="Get a quote on GreenPal">Get a quote on GreenPal</a>
            </div>
          </div>'''
)
rep(
    f'''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(148,212,75,0.4)]" href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener">@pure.artistrysk</a>
            </div>
          </div>''',
    f'''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Llamar o enviar mensaje" data-en="Call or text">Call or text</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Número verificado, disponible los 7 días de la semana de 7am a 10pm." data-en="Verified number, available seven days a week from 7am to 10pm.">Verified number, available seven days a week from 7am to 10pm.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(148,212,75,0.4)]" href="tel:{TEL}">{TEL_DISPLAY}</a>
            </div>
          </div>'''
)
rep(
    '''<div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div class="frame reveal min-h-[380px] zoomable img-reveal" style="transition-delay:180ms">
        <img src="assets/raw/hero-ranch-house-palm.jpg" alt="Freshly mowed lawn serviced by Greenleaf Pro Garden in the Kissimmee area" class="blur-up w-full h-full object-cover min-h-[380px]" loading="lazy" />
      </div>'''
)

# ============================================================
# STEP 16: CTA FINAL
# ============================================================
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu césped, en buenas manos." data-en="Your yard, in good hands.">Your yard, in good hands.</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo corte" data-en="Your next mow">Your next mow</span> <span class="text-shine" data-es="a un mensaje de distancia" data-en="is one message away">is one message away</span></h2>'
)
rep(
    f'<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    f'<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Pide tu cotización gratis en GreenPal, o llama o escribe al {TEL_DISPLAY} para cuidado de céspedes en Kissimmee y Orlando." data-en="Get a free quote through GreenPal, or call or text {TEL_DISPLAY} for lawn care across Kissimmee and Orlando.">Get a free quote through GreenPal, or call or text {TEL_DISPLAY} for lawn care across Kissimmee and Orlando.</p>'
)
rep(
    f'''<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    f'''<a href="{GREENPAL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Cotización Gratis" data-en="Get a Free Quote">Get a Free Quote</a>
        <a href="tel:{TEL}" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="{TEL_DISPLAY}" data-en="Call {TEL_DISPLAY}">Call {TEL_DISPLAY}</a>'''
)

# ============================================================
# STEP 17: FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Greenleaf Pro Garden</span>')
rep(
    '''<div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(194,232,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<div class="flex items-center gap-3 mb-4">
          <span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(194,232,150,0.35)] bg-[rgba(194,232,150,0.1)] text-[color:var(--accent-deep)]">GP</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">Greenleaf Pro Garden</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Cuidado de césped y jardines en Kissimmee y Orlando, FL. Por cotización a través de GreenPal." data-en="Lawn and garden care across Kissimmee and Orlando, FL. By free quote through GreenPal.">Lawn and garden care across Kissimmee and Orlando, FL. By free quote through GreenPal.</p>'''
)
rep(
    f'''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="hover:text-[#cce9ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    f'''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>2611 Hawthorne Lane, Kissimmee, FL 34743</p>
        <p><a href="tel:{TEL}" class="hover:text-[#cce9ab]">{TEL_DISPLAY}</a></p>
        <p><a href="{GREENPAL}" target="_blank" rel="noopener" class="hover:text-[#cce9ab]" data-es="Cotización online · GreenPal" data-en="Online quotes · GreenPal">Online quotes · GreenPal</a></p>'''
)
rep(
    f'''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="hover:text-[#cce9ab]">Instagram · @pure.artistrysk</a></p>''',
    f'''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Encuéntranos" data-en="Find us">Find us</p>
        <p><a href="{GREENPAL}" target="_blank" rel="noopener" class="hover:text-[#cce9ab]">GreenPal · Greenleaf Pro Garden</a></p>
        <p><a href="{NEXTDOOR}" target="_blank" rel="noopener" class="hover:text-[#cce9ab]">Nextdoor · Greenleaf Pro Garden</a></p>'''
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Greenleaf Pro Garden.</p>')

# ============================================================
# STEP 18: Floating booking button -> GreenPal
# ============================================================
rep(
    '<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#131c08" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
    f'<a href="{GREENPAL}" target="_blank" rel="noopener" class="book-float" aria-label="Get a free quote on GreenPal">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#131c08" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>'
)

# ============================================================
# WRITE OUTPUT
# ============================================================
open(PATH, "w", encoding="utf-8").write(h)
print(f"Wrote {PATH} ({len(h)} bytes)")
