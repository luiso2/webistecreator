#!/usr/bin/env python3
"""Anchored-replacement build script for Imagine It Gardening (Pembroke Pines, FL).
Derives output/imagine-it-gardening-pembroke-pines/index.html from templates/light-v2/index.html
following templates/SKELETONS-V2.md's method. Business is EN-primary, GreenPal-sourced,
no phone/email/own-site (variante adaptada, FORGE-BRIEF 0.b): no bookable menu, no fixed
prices, no address map (mobile lawn crew, no public storefront). CTA -> real GreenPal profile.
"""
import re

SLUG = 'imagine-it-gardening-pembroke-pines'
PATH = f'output/{SLUG}/index.html'

h = open(PATH, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'ANCHOR NOT FOUND: ' + a[:120]
    h = h.replace(a, b, n)


GREENPAL = 'https://www.yourgreenpal.com/imagine-it-gardening'

# ---------------------------------------------------------------------------
# 1. Protect the Merktop badge (gold rgba(212,168,75,...) must survive palette swap)
# ---------------------------------------------------------------------------
badge_match = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_match, 'merktop badge block not found'
BADGE_TOKEN = '@@BADGE@@'
badge_block = badge_match.group(0)
h = h.replace(badge_block, BADGE_TOKEN, 1)

# ---------------------------------------------------------------------------
# 2. Global palette swap: Lash Bloom plum-pink -> Imagine It terracotta/clay
#    (distinct from every landscaping palette already used in output/: otech's
#    forest #3d6b2f, papa-green's turf #2b6a38, garden-now's green #45703a,
#    bonzai's sky blue #48a7d7, pride-landscaping's grass #55ca65, blue-ribbon's
#    blue hue208, and TODAY's valeria-teal #146b60 and rapalo-jade #4bd490.)
# ---------------------------------------------------------------------------
PALETTE = [
    ('#a04a72', '#b1502c'),   # accent-deep: plum -> terracotta
    ('#c47a9c', '#d98a54'),   # accent-mid: light plum -> warm clay/amber
    ('#f3e0ea', '#f3e4d5'),   # accent-soft / bg-2: pink tint -> warm sand
    ('#faf2f6', '#faf5ee'),   # bg: pink-white -> warm cream
    ('#33222c', '#2e2015'),   # ink: plum-black -> dark warm brown
    ('rgba(51,34,44', 'rgba(46,32,21'),      # ink rgba triplets (60/40 alpha variants keep suffix)
    ('rgba(160,74,114', 'rgba(177,80,44'),   # accent-deep rgba triplets
    ('#5f2c48', '#6b3018'),   # text-shine deep stop
    ('#c9789f', '#e0975f'),   # text-shine mid stop 1
    ('#b25a85', '#c66a35'),   # text-shine mid stop 2
    ('#7d3457', '#8a4420'),   # btn-3d gradient bottom / scroll-progress mid-dark
    ('#5c2140', '#5c2c12'),   # btn-3d shadow "sole"
    ('#dc9dbe', '#eab183'),   # scroll-progress light stop
    ('#f2d5e3', '#f5ddc4'),   # orb-a color
    ('#d9a8c2', '#e8b98a'),   # orb-b color
    ('#e5c1d4', '#eecca4'),   # orb-c color
]
for old, new in PALETTE:
    assert old in h, f'palette anchor missing: {old}'
    h = h.replace(old, new)

# dark-band section: distinct near-black terracotta-brown tones (mirrors valeria's own
# bespoke dark-teal set and otechlandscaping's dark-green set for the CTA-final/footer bands)
rep('background: linear-gradient(180deg, #2a1722 0%, #1f0f18 100%);',
    'background: linear-gradient(180deg, #241408 0%, #180d05 100%);')
rep('bg-[#1c0f16]', 'bg-[#180d06]')
# dark-band text-shine: warm amber glow variant (keep a soft cream orb as contrast accent)
rep(".dark-band .text-shine { background-image: linear-gradient(110deg, #f0bed7 0%, #f8dfeb 30%, #8fcdbf 52%, #f0bed7 75%, #f2cfe0 100%); }",
    ".dark-band .text-shine { background-image: linear-gradient(110deg, #f3d2a8 0%, #fbe9d3 30%, #e8b98a 52%, #f3d2a8 75%, #f5ddc4 100%); }")
rep(".dark-band .orb-b { background: radial-gradient(circle, rgba(185,138,128,0.14) 0%, transparent 70%); opacity: 1; }",
    ".dark-band .orb-b { background: radial-gradient(circle, rgba(217,138,84,0.16) 0%, transparent 70%); opacity: 1; }")
rep(".dark-band .btn-3d { background: linear-gradient(180deg, #fbeff5 0%, #efd0e0 48%, #d3a2bc 100%); color: #172a26; box-shadow: inset 0 1px 0 rgba(255,255,255,0.55), inset 0 -2px 5px rgba(125,52,87,0.35), 0 5px 0 #8a5573, 0 12px 24px rgba(0,0,0,0.45); }",
    ".dark-band .btn-3d { background: linear-gradient(180deg, #fdf3e7 0%, #f0dcbf 48%, #dcae82 100%); color: #2e2015; box-shadow: inset 0 1px 0 rgba(255,255,255,0.55), inset 0 -2px 5px rgba(138,68,32,0.35), 0 5px 0 #8a6142, 0 12px 24px rgba(0,0,0,0.45); }")
rep(".dark-band .btn-3d:hover { box-shadow: inset 0 1px 0 rgba(255,255,255,0.6), inset 0 -2px 5px rgba(125,52,87,0.35), 0 7px 0 #8a5573, 0 18px 34px rgba(0,0,0,0.55), 0 0 40px rgba(240,190,215,0.18); }",
    ".dark-band .btn-3d:hover { box-shadow: inset 0 1px 0 rgba(255,255,255,0.6), inset 0 -2px 5px rgba(138,68,32,0.35), 0 7px 0 #8a6142, 0 18px 34px rgba(0,0,0,0.55), 0 0 40px rgba(243,210,168,0.18); }")
rep(".dark-band .btn-3d:active { box-shadow: inset 0 1px 0 rgba(255,255,255,0.4), inset 0 -1px 3px rgba(125,52,87,0.4), 0 1px 0 #8a5573, 0 4px 10px rgba(0,0,0,0.4); }",
    ".dark-band .btn-3d:active { box-shadow: inset 0 1px 0 rgba(255,255,255,0.4), inset 0 -1px 3px rgba(138,68,32,0.4), 0 1px 0 #8a6142, 0 4px 10px rgba(0,0,0,0.4); }")
rep(".dark-band .btn-ghost { border-color: rgba(240,190,215,0.35); color: var(--ink); }",
    ".dark-band .btn-ghost { border-color: rgba(243,210,168,0.35); color: var(--ink); }")
rep(".dark-band .btn-ghost:hover { border-color: rgba(240,190,215,0.7); background: rgba(240,190,215,0.08); box-shadow: 0 10px 26px rgba(0,0,0,0.4); }",
    ".dark-band .btn-ghost:hover { border-color: rgba(243,210,168,0.7); background: rgba(243,210,168,0.08); box-shadow: 0 10px 26px rgba(0,0,0,0.4); }")
rep(".dark-band .stars { color: #f0bed7; text-shadow: 0 0 14px rgba(240,190,215,0.4); }",
    ".dark-band .stars { color: #f3d2a8; text-shadow: 0 0 14px rgba(243,210,168,0.4); }")
rep("--surface: rgba(255,255,255,0.05); --accent-ghost: rgba(233,205,186,0.16); color: var(--ink);",
    "--surface: rgba(255,255,255,0.05); --accent-ghost: rgba(217,138,84,0.2); color: var(--ink);")
rep("--ink: #f4f8f6; --ink-60: rgba(250,242,246,0.65); --ink-40: rgba(250,242,246,0.45);",
    "--ink: #faf3ea; --ink-60: rgba(250,243,234,0.65); --ink-40: rgba(250,243,234,0.45);")
rep(".foot-mark { position: absolute; left: 0; right: 0; bottom: -0.22em; z-index: 0; text-align: center; font-family: 'Playfair Display', serif; font-size: clamp(4rem, 15vw, 11rem); line-height: 1; white-space: nowrap; color: transparent; -webkit-text-stroke: 1px rgba(240,190,215,0.09); pointer-events: none; user-select: none; }",
    ".foot-mark { position: absolute; left: 0; right: 0; bottom: -0.22em; z-index: 0; text-align: center; font-family: 'Playfair Display', serif; font-size: clamp(4rem, 15vw, 11rem); line-height: 1; white-space: nowrap; color: transparent; -webkit-text-stroke: 1px rgba(243,210,168,0.09); pointer-events: none; user-select: none; }")

# restore protected badge
h = h.replace(BADGE_TOKEN, badge_block)

# ---------------------------------------------------------------------------
# 3. Globals: booking link -> GreenPal, IG link removed (no verified handle), logo image -> text monogram
# ---------------------------------------------------------------------------
old_booksy = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
assert h.count(old_booksy) > 0
h = h.replace(old_booksy, GREENPAL)

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<meta name="theme-color" content="#f6f1ea" />', '<meta name="theme-color" content="#f3e4d5" />')
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Imagine It Gardening · Lawn Care in Pembroke Pines, FL | 4.67 on GreenPal</title>'
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Imagine It Gardening, Pembroke Pines FL: lawn mowing, edging, hedge trimming and yard care across Miami-Dade. 4.67 rating across 85 GreenPal reviews, in business since 2010." />'
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Imagine It Gardening · Lawn Care in Pembroke Pines, FL" />'
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Lawn mowing, edging and hedge trimming across Miami-Dade. 4.67 rating, 85 reviews on GreenPal." />'
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/hero-driveway-lawn.jpg" />'
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect width=%22100%22 height=%22100%22 rx=%2222%22 fill=%22%23b1502c%22/%3E%3Ctext x=%2250%22 y=%2266%22 font-size=%2244%22 font-family=%22Georgia,serif%22 fill=%22%23faf5ee%22 text-anchor=%22middle%22%3EIIG%3C/text%3E%3C/svg%3E" />'
)

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert old_jsonld
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LandscapingBusiness",
    "name": "Imagine It Gardening",
    "founder": "Alejandro Hurtado",
    "description": "Lawn care and landscaping company serving Pembroke Pines and Miami-Dade County, FL: mowing, edging, hedge trimming and yard cleanup, booked and reviewed through GreenPal.",
    "areaServed": [
      { "@type": "City", "name": "Pembroke Pines" },
      { "@type": "AdministrativeArea", "name": "Miami-Dade County" }
    ],
    "address": { "@type": "PostalAddress", "addressLocality": "Pembroke Pines", "addressRegion": "FL", "postalCode": "33186", "addressCountry": "US" },
    "sameAs": ["https://www.yourgreenpal.com/imagine-it-gardening"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.67", "reviewCount": "85", "bestRating": "5" },
    "priceRange": "$20-$45",
    "foundingDate": "2010-02"
  }
  </script>'''
h = h[:old_jsonld.start()] + new_jsonld + h[old_jsonld.end():]

# ---------------------------------------------------------------------------
# 5. Language: business is EN-primary and light-v2 already defaults to EN -> no applyLang swap needed.
#    <html lang="en"> already correct in the copied skeleton.
# ---------------------------------------------------------------------------
mlang = re.search(r"applyLang\(lang === '(\w\w)' \? '\w\w' : '(\w\w)'\)", h)
assert mlang and mlang.group(2) == 'en', 'template default is not EN as expected'

# ---------------------------------------------------------------------------
# 6. PRELOADER
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">IIG</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Imagine It Gardening</span>')

# ---------------------------------------------------------------------------
# 7. NAV (logo image -> text monogram, no verified brand logo file)
# ---------------------------------------------------------------------------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,96,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(177,80,44,0.35)] bg-[rgba(177,80,44,0.1)] text-[color:var(--accent-deep)]">IIG</span>\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Imagine It <span class="text-[color:var(--accent-deep)]">Gardening</span></span>'
)
rep('<a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
    '<a class="nav-link" href="#experiencia" data-es="Nuestra Historia" data-en="Our Story">Our Story</a>')
rep('<a class="nav-link" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
    '<a class="nav-link" href="#metodo" data-es="Cómo Trabajamos" data-en="How We Work">How We Work</a>')
rep('<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>', '<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Services</a>', n=2)
rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>', '<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>', n=2)
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>', '<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>', n=2)
rep('<a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>',
    '<a class="nav-link" href="#ubicacion" data-es="Zona de Servicio" data-en="Service Area">Service Area</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="Nuestra Historia" data-en="Our Story">Our Story</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="Cómo Trabajamos" data-en="How We Work">How We Work</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Services</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>')
rep('<a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>',
    '<a class="py-3 px-3" href="#ubicacion" data-es="Zona de Servicio" data-en="Service Area">Service Area</a>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Cotización Gratis" data-en="Free Quote">Free Quote</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Cotización Gratis" data-en="Free Quote">Free Quote</a>')

# ---------------------------------------------------------------------------
# 8. HERO
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Pembroke Pines, FL · Cuidado de Jardines" data-en="Pembroke Pines, FL · Lawn &amp; Garden Care">Pembroke Pines, FL · Lawn &amp; Garden Care</p>'
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Imagínalo, y lo dejamos crecer." data-en="Imagine it, and we help it grow.">Imagine it, and we help it grow.</p>'
)
rep(
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="16 años cuidando" data-en="16 years caring for">16 years caring for</span><br /><span data-es="céspedes de " data-en="Pembroke Pines ">Pembroke Pines </span><span class="text-shine" data-es="Pembroke Pines" data-en="lawns">lawns</span>
        </h1>'''
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Alejandro Hurtado y su equipo cuidan céspedes y jardines en Pembroke Pines y todo Miami-Dade: corte, orillado, poda de arbustos y limpieza de patios, con más de una década de experiencia y 85 reseñas reales en GreenPal." data-en="Alejandro Hurtado and his crew take care of lawns and gardens across Pembroke Pines and Miami-Dade County: mowing, edging, hedge trimming and yard cleanup, backed by over a decade of experience and 85 real reviews on GreenPal.">Alejandro Hurtado and his crew take care of lawns and gardens across Pembroke Pines and Miami-Dade County: mowing, edging, hedge trimming and yard cleanup, backed by over a decade of experience and 85 real reviews on GreenPal.</p>'
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="4.67 · 85 reseñas en GreenPal" data-en="4.67 · 85 reviews on GreenPal">4.67 · 85 reviews on GreenPal</span>'
)
rep(
    '''<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
    '''<span data-es="Cotización Gratis" data-en="Get a Free Quote">Get a Free Quote</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg>
            <span data-es="Ver en GreenPal" data-en="See on GreenPal">See on GreenPal</span>
          </a>'''
)
rep(
    '''<div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>
          </div>''',
    '''<div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/hero-driveway-lawn.jpg" alt="Freshly mowed lawn and driveway at a Pembroke Pines home serviced by Imagine It Gardening" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Cotización" data-en="Quote">Quote</p>
            <p class="font-display text-lg" data-es="Estimado gratis" data-en="Free Estimate">Free Estimate</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Pembroke Pines, FL" data-en="Pembroke Pines, FL">Pembroke Pines, FL</p>
          </div>'''
)

# ---------------------------------------------------------------------------
# 9. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.67" data-decimals="2">4.67</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="85">85</span> <span data-es="reseñas en GreenPal" data-en="reviews on GreenPal">reviews on GreenPal</span></p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Mowing <span class="text-shine">&amp;</span> Trimming</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicio recurrente" data-en="Recurring service">Recurring service</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">2010</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="En el negocio desde" data-en="In business since">In business since</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">56<span class="text-shine">%</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientes recurrentes" data-en="Repeat clients">Repeat clients</p></div>'
)

# ---------------------------------------------------------------------------
# 10. MARQUEE (x2 blocks, 4 occurrences per word)
# ---------------------------------------------------------------------------
marquee_words = [
    ('Classic Set', 'Lawn Mowing'),
    ('Hybrid Set', 'Edging'),
    ('Volume Set', 'Hedge Trimming'),
    ('Mega Volume', 'Yard Cleanup'),
    ('Bottom Lashes', 'Landscaping'),
    ('West Palm Beach, FL', 'Pembroke Pines, FL'),
]
for old_w, new_w in marquee_words:
    old_span = f'<span class="marquee-word">{old_w}</span>'
    cnt = h.count(old_span)
    assert cnt == 4, f'expected 4 occurrences of {old_span!r}, found {cnt}'
    h = h.replace(old_span, f'<span class="marquee-word">{new_w}</span>')

# ---------------------------------------------------------------------------
# 11. LA EXPERIENCIA / OUR STORY
# ---------------------------------------------------------------------------
rep(
    '''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''',
    '''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/gallery-landscaping-bed.jpg" alt="Flower bed and mulch landscaping detail finished by Imagine It Gardening" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/gallery-mowing-action.jpg" alt="Imagine It Gardening crew mowing a backyard lawn in Miami-Dade" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>'''
)
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Nuestra historia" data-en="Our story">Our story</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Passion for landscaping" data-en="A passion for landscaping">A passion for landscaping</span><br /><span class="text-shine" data-es="que se nota" data-en="that shows in every yard">that shows in every yard</span></h2>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Imagine It Gardening es el negocio de Alejandro Hurtado, en el rubro del mantenimiento de jardines desde hace más de 12 años. Para él esto no es solo un trabajo: cada césped que corta y cada seto que da forma lleva su firma personal." data-en="Imagine It Gardening is Alejandro Hurtado&#39;s business, in the landscaping maintenance trade for over 12 years. For him this is not just a job: every lawn he mows and every hedge he shapes carries his personal touch.">Imagine It Gardening is Alejandro Hurtado&#39;s business, in the landscaping maintenance trade for over 12 years. For him this is not just a job: every lawn he mows and every hedge he shapes carries his personal touch.</p>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 4.67 de calificación en 85 reseñas verificadas en GreenPal, en el negocio desde febrero de 2010, con 56% de clientes que vuelven a contratarlo temporada tras temporada." data-en="The result: a 4.67 rating across 85 verified reviews on GreenPal, in business since February 2010, with 56% of clients coming back season after season.">The result: a 4.67 rating across 85 verified reviews on GreenPal, in business since February 2010, with 56% of clients coming back season after season.</p>'
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.67" data-decimals="2">4.67</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">GreenPal</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="85">85</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2010</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Desde" data-en="Since">Since</p></div>'
)
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,96,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>''',
    '''<img src="assets/raw/founder-alejandro.jpg" alt="Alejandro Hurtado, owner of Imagine It Gardening" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(177,80,44,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Alejandro Hurtado · <span class="text-[color:var(--ink-40)]" data-es="Dueño" data-en="Owner">Owner</span></span>'''
)

# ---------------------------------------------------------------------------
# 12. EL METODO / HOW WE WORK
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Cómo trabajamos" data-en="How it works">How it works</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Simple, de principio" data-en="Simple, start">Simple, start</span> <span class="text-shine" data-es="a fin" data-en="to finish">to finish</span></h2>'
)
old_step_blocks = [
    ('Reserva online', 'Book online', 'Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante.', 'Pick your set or fill on Booksy with clear price and duration, and confirm instantly.'),
    ('Mapeo del ojo', 'Eye mapping', 'Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen.', 'Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.'),
    ('Aplicación zen', 'The zen part', 'Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña.', 'You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.'),
    ('Plan de relleno', 'Fill plan', 'Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad.', 'You leave with your 2 or 3 week fill booked and loyalty points adding up.'),
]
new_titles_es = ['Cotización Gratis', 'Coordina tu Visita', 'Corte y Poda', 'Servicio Continuo']
new_titles_en = ['Request a Free Quote', 'Schedule Your Visit', 'Mowing &amp; Trimming', 'Ongoing, No Commitment']
new_texts_es = [
    'Escribe a través de GreenPal y cuéntanos el tamaño de tu propiedad. La mayoría recibe una cotización el mismo día.',
    'Sin mínimo de trabajo: coordinamos el día que te convenga, con servicio disponible todo el año, todos los días de la semana.',
    'Corte a la altura ideal, orillado, poda de setos y soplado de restos, dejando cada patio prolijo.',
    'Tú controlas el calendario: sin penalidad por pausar el servicio si solo necesitas unos meses.',
]
new_texts_en = [
    'Reach out through GreenPal and tell us the size of your property. Most requests get a quote the same day.',
    'No minimum job size: we coordinate a day that works for you, with service available year round, every day of the week.',
    'Mowing at the ideal height, edging, hedge trimming and blowing off clippings, leaving every yard tidy.',
    'You control the schedule: no penalty for pausing the service if you only need it for a few months.',
]
for i, (old_title_es, old_title_en, old_text_es, old_text_en) in enumerate(old_step_blocks):
    rep(f'data-es="{old_title_es}" data-en="{old_title_en}">{old_title_en}</h3>',
        f'data-es="{new_titles_es[i]}" data-en="{new_titles_en[i]}">{new_titles_en[i]}</h3>')
    rep(f'data-es="{old_text_es}" data-en="{old_text_en}">{old_text_en}</p>',
        f'data-es="{new_texts_es[i]}" data-en="{new_texts_en[i]}">{new_texts_en[i]}</p>')

# ---------------------------------------------------------------------------
# 13. SERVICIOS (variante adaptada: sin precios fijos, cotizacion, CTA GreenPal)
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que" data-en="What we">What we</span> <span class="text-shine" data-es="hacemos" data-en="do">do</span></h2>'
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cada propiedad es distinta: el precio se cotiza según el tamaño y lo que necesites, sin sorpresas." data-en="Every property is different: pricing is quoted based on size and what you need, no surprises.">Every property is different: pricing is quoted based on size and what you need, no surprises.</p>'
)

services_grid = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert services_grid, 'services grid anchor not found'
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte y Orillado" data-en="Lawn Mowing &amp; Edging">Lawn Mowing &amp; Edging</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte a la altura ideal, orillado y recorte de bordes, con soplado de restos en calles y entradas en cada visita." data-en="Mowing at the ideal height, clean edging and line trimming, with clippings blown off driveways and walkways on every visit.">Mowing at the ideal height, clean edging and line trimming, with clippings blown off driveways and walkways on every visit.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(177,80,44,0.4); box-shadow: 0 18px 50px rgba(46,32,21,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Su especialidad" data-en="His specialty">His specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Poda de Setos" data-en="Hedge Trimming">Hedge Trimming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Formas prolijas y parejas en cada seto: Alejandro se especializa personalmente en este trabajo de detalle." data-en="Clean, even shapes on every hedge: this is the detail work Alejandro personally specializes in.">Clean, even shapes on every hedge: this is the detail work Alejandro personally specializes in.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Limpieza" data-en="Cleanup">Cleanup</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Limpieza de Patio" data-en="Yard Cleanup">Yard Cleanup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Retiro de hojas y restos vegetales, para propiedades residenciales y comerciales que necesitan un repaso a fondo." data-en="Leaf and debris removal, for residential and commercial properties that need a deeper pass front and back.">Leaf and debris removal, for residential and commercial properties that need a deeper pass front and back.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Flexible" data-en="Flexible">Flexible</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Servicio Recurrente" data-en="Recurring Service">Recurring Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sin contrato largo ni penalidad: tú controlas el calendario, ya sea por temporada o todo el año, los 7 días." data-en="No long contract and no penalty: you control the schedule, whether it is seasonal or year round, 7 days a week.">No long contract and no penalty: you control the schedule, whether it is seasonal or year round, 7 days a week.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

services_note = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert services_note
h = h[:services_note.start()] + services_note.group(1) + '<span data-es="Trabajos residenciales y comerciales. Cada visita se cotiza según el tamaño de tu propiedad." data-en="Residential and commercial jobs. Every visit is quoted based on the size of your property.">Residential and commercial jobs. Every visit is quoted based on the size of your property.</span>' + services_note.group(2) + h[services_note.end():]

# ---------------------------------------------------------------------------
# 14. GALERIA (8 real, curated, watermark-cropped photos -> 2x4 grid, no wide tile)
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Jardines" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="yards">yards</span></h2>'
)
rep(
    '''<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>''',
    '''<a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg>
          <span data-es="Ver en GreenPal" data-en="See on GreenPal">See on GreenPal</span>
        </a>'''
)

gallery_grid = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert gallery_grid, 'gallery grid anchor not found'
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal"><span class="tile-cap" data-es="Jardín en flor" data-en="Landscaping bed">Landscaping bed</span><img src="assets/raw/gallery-landscaping-bed.jpg" alt="Flower bed and mulch landscaping detail finished by Imagine It Gardening" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Equipo en acción" data-en="Crew at work">Crew at work</span><img src="assets/raw/gallery-mowing-action.jpg" alt="Imagine It Gardening crew member mowing a backyard lawn" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[4/3] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Fachada prolija" data-en="Porch &amp; lawn">Porch &amp; lawn</span><img src="assets/raw/gallery-porch-lawn.jpg" alt="Freshly mowed front lawn and porch at a Miami-Dade home" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Entrada despejada" data-en="Driveway &amp; garage">Driveway &amp; garage</span><img src="assets/raw/gallery-driveway-garage.jpg" alt="Mowed lawn and driveway in front of a home garage serviced by Imagine It Gardening" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Patio trasero" data-en="Backyard corner">Backyard corner</span><img src="assets/raw/gallery-backyard-corner.jpg" alt="Mowed backyard corner with paver walkway" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[4/3] lg:mt-10 img-reveal" style="transition-delay:330ms"><span class="tile-cap" data-es="Corte parejo" data-en="Even cut">Even cut</span><img src="assets/raw/gallery-driveway-car.jpg" alt="Even mowed lawn along a paved driveway in Miami-Dade" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:390ms"><span class="tile-cap" data-es="Detalle de césped" data-en="Lawn detail">Lawn detail</span><img src="assets/raw/gallery-lawn-texture.jpg" alt="Close-up of a freshly mowed lawn edge in Pembroke Pines" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]

# ---------------------------------------------------------------------------
# 15. OPINIONES (real GreenPal quotes; only 4 non-empty text quotes exist across
#     the 20 reviews exposed via JSON-LD, so 4-card grid, same pattern as valeria)
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span></h2>'
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★☆</span> &nbsp;<span data-es="4.67 de 5 · 85 reseñas verificadas en GreenPal" data-en="4.67 out of 5 · 85 verified reviews on GreenPal">4.67 out of 5 · 85 verified reviews on GreenPal</span></p>'
)

reviews_grid = re.search(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10 reveal">)', h, flags=re.S)
assert reviews_grid, 'reviews grid anchor not found'
NEW_REVIEWS = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Alex did an excellent job overall."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rosy M. Dabalsa</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Good."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rebecca Shafee</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Great job!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tilah Properties</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Thanks."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Peter Nunez</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep(
    '<a href="' + GREENPAL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + GREENPAL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 85 reseñas en GreenPal" data-en="Read all 85 reviews on GreenPal">Read all 85 reviews on GreenPal</a>'
)

# ---------------------------------------------------------------------------
# 16. UBICACION -> ZONA DE SERVICIO (variante adaptada: sin mapa de direccion, foto real en vez de mapa)
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Zona de servicio" data-en="Service area">Service area</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Servimos" data-en="Serving">Serving</span> <span class="text-shine">Pembroke Pines &amp; Miami-Dade</span></h2>'
)
rep(
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Área de trabajo" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Pembroke Pines y alrededores: Kendall, Richmond Heights, Pinecrest, Homestead, Doral, Coral Gables, Little Havana, Miramar, Hialeah, Miami Shores y Coconut Grove." data-en="Pembroke Pines and nearby areas: Kendall, Richmond Heights, Pinecrest, Homestead, Doral, Coral Gables, Little Havana, Miramar, Hialeah, Miami Shores and Coconut Grove.">Pembroke Pines and nearby areas: Kendall, Richmond Heights, Pinecrest, Homestead, Doral, Coral Gables, Little Havana, Miramar, Hialeah, Miami Shores and Coconut Grove.</p>
            </div>'''
)
rep(
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="''' + GREENPAL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Cotización gratis" data-en="Free quote">Free quote</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Pide tu cotización por GreenPal, sin compromiso. Alejandro responde y disponibilidad todos los días de 7am a 10pm." data-en="Request your quote through GreenPal, no obligation. Alejandro responds and is available every day from 7am to 10pm.">Request your quote through GreenPal, no obligation. Alejandro responds and is available every day from 7am to 10pm.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
            </div>'''
)
rep(
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>
            </div>''',
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reseñas verificadas" data-en="Verified reviews">Verified reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.67 de calificación con 85 reseñas de clientes reales en GreenPal." data-en="A 4.67 rating from 85 real customer reviews on GreenPal.">A 4.67 rating from 85 real customer reviews on GreenPal.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener">Imagine It Gardening on GreenPal</a>
            </div>'''
)
# Replace the map iframe block with a real curated photo (variante adaptada: no address-based map)
rep(
    '''<div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div class="frame zoomable img-reveal reveal min-h-[380px]" style="transition-delay:180ms">
        <img src="assets/raw/gallery-driveway-garage.jpg" alt="Mowed lawn and driveway serviced by Imagine It Gardening in Miami-Dade County, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>'''
)

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Imagínalo, y lo dejamos crecer." data-en="Imagine it, and we help it grow.">Imagine it, and we help it grow.</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo corte" data-en="Your next mow">Your next mow</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Escríbenos por GreenPal hoy: cotización gratis, sin compromiso, según el tamaño de tu propiedad." data-en="Reach out through GreenPal today: a free, no-obligation quote based on the size of your property.">Reach out through GreenPal today: a free, no-obligation quote based on the size of your property.</p>'
)
rep(
    '<a href="' + GREENPAL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + GREENPAL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Cotización Gratis" data-en="Request a Free Quote">Request a Free Quote</a>'
)
rep(
    '<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Ver Reseñas en GreenPal" data-en="See Reviews on GreenPal">See Reviews on GreenPal</a>'
)

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(243,210,168,0.35)] bg-[rgba(243,210,168,0.08)]">IIG</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">Imagine It Gardening</span>'''
)
rep(
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Cuidado de césped y jardinería en Pembroke Pines y Miami-Dade County, FL." data-en="Lawn care and landscaping in Pembroke Pines and Miami-Dade County, FL.">Lawn care and landscaping in Pembroke Pines and Miami-Dade County, FL.</p>'
)
rep(
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + GREENPAL + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p data-es="Pembroke Pines &amp; Miami-Dade County, FL" data-en="Pembroke Pines &amp; Miami-Dade County, FL">Pembroke Pines &amp; Miami-Dade County, FL</p>
        <p><a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="hover:text-[#f3d2a8]" data-es="Cotización gratis · GreenPal" data-en="Free quote · GreenPal">Free quote · GreenPal</a></p>'''
)
rep(
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reseñas" data-en="Reviews">Reviews</p>
        <p><a href="https://www.yourgreenpal.com/imagine-it-gardening" target="_blank" rel="noopener" class="hover:text-[#f3d2a8]">GreenPal · 4.67 · 85 reviews</a></p>'''
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Imagine It Gardening.</p>')
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Imagine It Gardening</span>')

# ---------------------------------------------------------------------------
# 19. Floating booking button
# ---------------------------------------------------------------------------
rep(
    '<a href="' + GREENPAL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + GREENPAL + '" target="_blank" rel="noopener" class="book-float" aria-label="Get a free quote on GreenPal">'
)

# ---------------------------------------------------------------------------
# Write out
# ---------------------------------------------------------------------------
open(PATH, 'w', encoding='utf-8').write(h)
print('Build OK ->', PATH)
