#!/usr/bin/env python3
"""Anchored-replacement build script for Valeria Landscape (North Miami, FL).
Derives output/valeria-landscape-north-miami/index.html from templates/light-v2/index.html
following templates/SKELETONS-V2.md's method. Business is EN-primary, GreenPal-sourced,
no phone/email/own-site (variante adaptada, FORGE-BRIEF 0.b): no bookable menu, no fixed
prices, no address map. CTA -> real GreenPal profile.
"""
import re

SLUG = 'valeria-landscape-north-miami'
PATH = f'output/{SLUG}/index.html'

h = open(PATH, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'ANCHOR NOT FOUND: ' + a[:120]
    h = h.replace(a, b, n)


GREENPAL = 'https://www.yourgreenpal.com/valeria-landscape-se'

# ---------------------------------------------------------------------------
# 1. Protect the Merktop badge (gold rgba(212,168,75,...) must survive palette swap)
# ---------------------------------------------------------------------------
badge_match = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_match, 'merktop badge block not found'
BADGE_TOKEN = '@@BADGE@@'
badge_block = badge_match.group(0)
h = h.replace(badge_block, BADGE_TOKEN, 1)

# ---------------------------------------------------------------------------
# 2. Global palette swap: Lash Bloom plum-pink -> Valeria teal
# ---------------------------------------------------------------------------
PALETTE = [
    ('#a04a72', '#146b60'),   # accent-deep
    ('#c47a9c', '#4fae9c'),   # accent-mid
    ('#f3e0ea', '#e2eeea'),   # accent-soft / bg-2
    ('#faf2f6', '#f4f8f6'),   # bg
    ('#33222c', '#172a26'),   # ink
    ('rgba(51,34,44', 'rgba(23,42,38'),      # ink rgba triplets (60/40 alpha variants keep suffix)
    ('rgba(160,74,114', 'rgba(20,107,96'),   # accent-deep rgba triplets
    ('#5f2c48', '#0c352f'),   # text-shine deep stop
    ('#c9789f', '#3f9384'),   # text-shine mid stop 1
    ('#b25a85', '#268172'),   # text-shine mid stop 2
    ('#7d3457', '#0e453c'),   # btn-3d gradient bottom / scroll-progress mid-dark
    ('#5c2140', '#08251f'),   # btn-3d shadow "sole"
    ('#dc9dbe', '#7fcabb'),   # scroll-progress light stop
    ('#f2d5e3', '#cdeae2'),   # orb-a color
    ('#d9a8c2', '#8fcdbf'),   # orb-b color
    ('#e5c1d4', '#bfe4da'),   # orb-c color
]
for old, new in PALETTE:
    assert old in h, f'palette anchor missing: {old}'
    h = h.replace(old, new)

# dark-band section: distinct near-black teal tones (mirrors otechlandscaping's own dark-green bespoke set)
rep('background: linear-gradient(180deg, #2a1722 0%, #1f0f18 100%);',
    'background: linear-gradient(180deg, #0d211d 0%, #071613 100%);')
rep('bg-[#1c0f16]', 'bg-[#0a1a17]')
# dark-band text-shine: teal glow variant (keep pink orb-a as warm contrast accent like otech precedent)
rep(".dark-band .text-shine { background-image: linear-gradient(110deg, #f0bed7 0%, #f8dfeb 30%, #8fcdbf 52%, #f0bed7 75%, #f2cfe0 100%); }",
    ".dark-band .text-shine { background-image: linear-gradient(110deg, #bdeadd 0%, #e6f7f2 30%, #8fcdbf 52%, #bdeadd 75%, #cdeae2 100%); }")
rep(".dark-band .orb-b { background: radial-gradient(circle, rgba(185,138,128,0.14) 0%, transparent 70%); opacity: 1; }",
    ".dark-band .orb-b { background: radial-gradient(circle, rgba(79,174,156,0.16) 0%, transparent 70%); opacity: 1; }")
rep(".dark-band .btn-3d { background: linear-gradient(180deg, #fbeff5 0%, #efd0e0 48%, #d3a2bc 100%); color: #172a26; box-shadow: inset 0 1px 0 rgba(255,255,255,0.55), inset 0 -2px 5px rgba(125,52,87,0.35), 0 5px 0 #8a5573, 0 12px 24px rgba(0,0,0,0.45); }",
    ".dark-band .btn-3d { background: linear-gradient(180deg, #eefbf6 0%, #cdeadf 48%, #96cdbc 100%); color: #172a26; box-shadow: inset 0 1px 0 rgba(255,255,255,0.55), inset 0 -2px 5px rgba(14,69,60,0.35), 0 5px 0 #4f8577, 0 12px 24px rgba(0,0,0,0.45); }")
rep(".dark-band .btn-3d:hover { box-shadow: inset 0 1px 0 rgba(255,255,255,0.6), inset 0 -2px 5px rgba(125,52,87,0.35), 0 7px 0 #8a5573, 0 18px 34px rgba(0,0,0,0.55), 0 0 40px rgba(240,190,215,0.18); }",
    ".dark-band .btn-3d:hover { box-shadow: inset 0 1px 0 rgba(255,255,255,0.6), inset 0 -2px 5px rgba(14,69,60,0.35), 0 7px 0 #4f8577, 0 18px 34px rgba(0,0,0,0.55), 0 0 40px rgba(189,234,221,0.18); }")
rep(".dark-band .btn-3d:active { box-shadow: inset 0 1px 0 rgba(255,255,255,0.4), inset 0 -1px 3px rgba(125,52,87,0.4), 0 1px 0 #8a5573, 0 4px 10px rgba(0,0,0,0.4); }",
    ".dark-band .btn-3d:active { box-shadow: inset 0 1px 0 rgba(255,255,255,0.4), inset 0 -1px 3px rgba(14,69,60,0.4), 0 1px 0 #4f8577, 0 4px 10px rgba(0,0,0,0.4); }")
rep(".dark-band .btn-ghost { border-color: rgba(240,190,215,0.35); color: var(--ink); }",
    ".dark-band .btn-ghost { border-color: rgba(189,234,221,0.35); color: var(--ink); }")
rep(".dark-band .btn-ghost:hover { border-color: rgba(240,190,215,0.7); background: rgba(240,190,215,0.08); box-shadow: 0 10px 26px rgba(0,0,0,0.4); }",
    ".dark-band .btn-ghost:hover { border-color: rgba(189,234,221,0.7); background: rgba(189,234,221,0.08); box-shadow: 0 10px 26px rgba(0,0,0,0.4); }")
rep(".dark-band .stars { color: #f0bed7; text-shadow: 0 0 14px rgba(240,190,215,0.4); }",
    ".dark-band .stars { color: #bdeadd; text-shadow: 0 0 14px rgba(189,234,221,0.4); }")
# book-float background/shadow already covered by the global PALETTE swap above
# (accent-deep/mid, #5c2140 sole shadow, and ink rgba triplet all already replaced).
rep("--surface: rgba(255,255,255,0.05); --accent-ghost: rgba(233,205,186,0.16); color: var(--ink);",
    "--surface: rgba(255,255,255,0.05); --accent-ghost: rgba(79,174,156,0.2); color: var(--ink);")
rep("--ink: #f4f8f6; --ink-60: rgba(250,242,246,0.65); --ink-40: rgba(250,242,246,0.45);",
    "--ink: #f2faf8; --ink-60: rgba(242,250,248,0.65); --ink-40: rgba(242,250,248,0.45);")
rep(".foot-mark { position: absolute; left: 0; right: 0; bottom: -0.22em; z-index: 0; text-align: center; font-family: 'Playfair Display', serif; font-size: clamp(4rem, 15vw, 11rem); line-height: 1; white-space: nowrap; color: transparent; -webkit-text-stroke: 1px rgba(240,190,215,0.09); pointer-events: none; user-select: none; }",
    ".foot-mark { position: absolute; left: 0; right: 0; bottom: -0.22em; z-index: 0; text-align: center; font-family: 'Playfair Display', serif; font-size: clamp(4rem, 15vw, 11rem); line-height: 1; white-space: nowrap; color: transparent; -webkit-text-stroke: 1px rgba(189,234,221,0.09); pointer-events: none; user-select: none; }")

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
rep('<meta name="theme-color" content="#f6f1ea" />', '<meta name="theme-color" content="#e2eeea" />')
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Valeria Landscape · Lawn Care in North Miami, FL | 4.8 on GreenPal</title>'
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Valeria Landscape Service Corp: lawn mowing, edging, yard cleanup and debris removal in North Miami and across Miami-Dade, FL. 4.8 rating across 98 GreenPal reviews." />'
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Valeria Landscape · Lawn Care in North Miami, FL" />'
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Lawn mowing, edging and yard cleanup across Miami-Dade. 4.8 rating, 98 reviews on GreenPal." />'
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/hero-house-cleared-yard.jpg" />'
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect width=%22100%22 height=%22100%22 rx=%2222%22 fill=%22%23146b60%22/%3E%3Ctext x=%2250%22 y=%2266%22 font-size=%2252%22 font-family=%22Georgia,serif%22 fill=%22%23f4f8f6%22 text-anchor=%22middle%22%3EV%3C/text%3E%3C/svg%3E" />'
)

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert old_jsonld
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LandscapingBusiness",
    "name": "Valeria Landscape",
    "legalName": "Valeria Landscape Service Corp",
    "description": "Lawn care and landscaping company serving North Miami and Miami-Dade County, FL: mowing, edging, trimming and yard cleanup, booked and reviewed through GreenPal.",
    "areaServed": [
      { "@type": "City", "name": "North Miami" },
      { "@type": "AdministrativeArea", "name": "Miami-Dade County" }
    ],
    "address": { "@type": "PostalAddress", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33196", "addressCountry": "US" },
    "sameAs": ["https://www.yourgreenpal.com/valeria-landscape-se"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "98", "bestRating": "5" },
    "priceRange": "$20-$50"
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
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">VL</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Valeria Landscape</span>')

# ---------------------------------------------------------------------------
# 7. NAV (logo image -> text monogram, like otechlandscaping precedent, no verified brand logo file)
# ---------------------------------------------------------------------------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,96,0.35)]" />\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-lg ring-1 ring-[rgba(20,107,96,0.35)] bg-[rgba(20,107,96,0.1)] text-[color:var(--accent-deep)]">VL</span>\n        <span class="font-display text-xl tracking-[0.1em] uppercase">Valeria <span class="text-[color:var(--accent-deep)]">Landscape</span></span>'
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
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="North Miami, FL · Cuidado de Césped" data-en="North Miami, FL · Lawn Care">North Miami, FL · Lawn Care</p>'
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu césped, cuidado de principio a fin." data-en="Your yard, cared for from start to finish.">Your yard, cared for from start to finish.</p>'
)
rep(
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Cuidado de césped" data-en="Lawn care your">Lawn care your</span><br /><span data-es="en el que puedes " data-en="North Miami yard can ">North Miami yard can </span><span class="text-shine" data-es="confiar" data-en="rely on">rely on</span>
        </h1>'''
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="David Rodriguez Boza y su equipo cuidan céspedes en North Miami y en todo Miami-Dade: corte, orillado, recorte y limpieza de hojas, cada trabajo cotizado según el tamaño de tu propiedad." data-en="David Rodriguez Boza and his crew take care of lawns across North Miami and Miami-Dade County: mowing, edging, trimming and yard cleanup, every job quoted to the size of your property.">David Rodriguez Boza and his crew take care of lawns across North Miami and Miami-Dade County: mowing, edging, trimming and yard cleanup, every job quoted to the size of your property.</p>'
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="4.8 · 98 reseñas en GreenPal" data-en="4.8 · 98 reviews on GreenPal">4.8 · 98 reviews on GreenPal</span>'
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
          <a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
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
            <img src="assets/raw/hero-house-cleared-yard.jpg" alt="Freshly cleared yard and driveway serviced by Valeria Landscape in North Miami, FL" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Cotización" data-en="Quote">Quote</p>
            <p class="font-display text-lg" data-es="Estimado gratis" data-en="Free Estimate">Free Estimate</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="North Miami, FL" data-en="North Miami, FL">North Miami, FL</p>
          </div>'''
)

# ---------------------------------------------------------------------------
# 9. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="98">98</span> <span data-es="reseñas en GreenPal" data-en="reviews on GreenPal">reviews on GreenPal</span></p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Mowing <span class="text-shine">&amp;</span> Cleanup</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicio recurrente" data-en="Recurring service">Recurring service</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">2023</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Fundado en" data-en="Founded in">Founded in</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">North Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Zona de servicio" data-en="Service area">Miami-Dade County, FL</p></div>'
)

# ---------------------------------------------------------------------------
# 10. MARQUEE (x2 blocks, 4 occurrences per word)
# ---------------------------------------------------------------------------
marquee_words = [
    ('Classic Set', 'Lawn Mowing'),
    ('Hybrid Set', 'Edging'),
    ('Volume Set', 'Yard Cleanup'),
    ('Mega Volume', 'Leaf Removal'),
    ('Bottom Lashes', 'Trimming'),
    ('West Palm Beach, FL', 'North Miami, FL'),
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
          <img src="assets/raw/gallery-front-yard-cleared.jpg" alt="Front yard mowed and cleared at a North Miami home serviced by Valeria Landscape" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/gallery-driveway-cleared.jpg" alt="Driveway and yard cleared of debris at a Miami property" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>'''
)
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Nuestra historia" data-en="Our story">Our story</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un equipo local" data-en="A local crew">A local crew</span><br /><span class="text-shine" data-es="que cuida tu propiedad" data-en="that treats your property right">that treats your property right</span></h2>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Valeria Landscape Service Corp fue fundada en 2023 por David Rodriguez Boza, quien creció entre el paisajismo de Miami y convirtió esa pasión en un negocio propio de cuidado de céspedes." data-en="Valeria Landscape Service Corp was founded in 2023 by David Rodriguez Boza, who grew up around Miami&#39;s lush landscaping and turned that passion into his own lawn care business.">Valeria Landscape Service Corp was founded in 2023 by David Rodriguez Boza, who grew up around Miami&#39;s lush landscaping and turned that passion into his own lawn care business.</p>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 4.8 de calificación en 98 reseñas verificadas en GreenPal, clientes recurrentes en North Miami y un servicio que se agenda según tu propio horario, sin compromisos largos." data-en="The result: a 4.8 rating across 98 verified reviews on GreenPal, repeat clients across North Miami, and service scheduled around you, with no long-term commitment required.">The result: a 4.8 rating across 98 verified reviews on GreenPal, repeat clients across North Miami, and service scheduled around you, with no long-term commitment required.</p>'
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">GreenPal</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="98">98</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2023</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Fundado" data-en="Founded">Founded</p></div>'
)
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,96,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>''',
    '''<img src="assets/raw/founder-david.jpg" alt="David Rodriguez Boza, owner of Valeria Landscape" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,96,0.3)]" loading="lazy" />
            <span class="text-sm font-light">David Rodriguez Boza · <span class="text-[color:var(--ink-40)]" data-es="Dueño" data-en="Owner">Owner</span></span>'''
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
steps = [
    ('01', 'Reserva online', 'Book online', 'Request a Free Quote',
     'Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante.',
     'Pick your set or fill on Booksy with clear price and duration, and confirm instantly.',
     'Escribe a través de GreenPal y cuéntanos el tamaño de tu propiedad. La mayoría recibe una cotización el mismo día.',
     'Reach out through GreenPal and tell us the size of your property. Most requests get a quote the same day.'),
    ('02', 'Mapeo del ojo', 'Eye mapping', 'Schedule Your Visit',
     'Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen.',
     'Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.',
     'Sin mínimo de trabajo: coordinamos el día que te convenga, con servicio disponible todo el año.',
     'No minimum job size: we coordinate a day that works for you, with service available year round.'),
    ('03', 'Aplicación zen', 'The zen part', 'Mowing, Edging & Cleanup',
     'Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña.',
     'You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.',
     'Corte, orillado, recorte y soplado de restos en calles y entradas, dejando la propiedad lista.',
     'Mowing, edging, trimming and blowing off clippings from driveways and walkways, leaving the property clean.'),
    ('04', 'Plan de relleno', 'Fill plan', 'Ongoing, No Commitment',
     'Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad.',
     'You leave with your 2 or 3 week fill booked and loyalty points adding up.',
     'Tú controlas el calendario: sin penalidad por pausar el servicio si solo necesitas unos meses.',
     'You control the schedule: no penalty for pausing the service if you only need it for a few months.'),
]
old_step_blocks = [
    ('Reserva online', 'Book online', 'Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante.', 'Pick your set or fill on Booksy with clear price and duration, and confirm instantly.'),
    ('Mapeo del ojo', 'Eye mapping', 'Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen.', 'Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.'),
    ('Aplicación zen', 'The zen part', 'Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña.', 'You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.'),
    ('Plan de relleno', 'Fill plan', 'Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad.', 'You leave with your 2 or 3 week fill booked and loyalty points adding up.'),
]
new_titles_es = ['Cotización Gratis', 'Coordina tu Visita', 'Corte y Limpieza', 'Servicio Continuo']
new_titles_en = ['Request a Free Quote', 'Schedule Your Visit', 'Mowing & Cleanup', 'Ongoing, No Commitment']
new_texts_es = [
    'Escribe a través de GreenPal y cuéntanos el tamaño de tu propiedad. La mayoría recibe una cotización el mismo día.',
    'Sin mínimo de trabajo: coordinamos el día que te convenga, con servicio disponible todo el año.',
    'Corte, orillado, recorte y soplado de restos en calles y entradas, dejando la propiedad lista.',
    'Tú controlas el calendario: sin penalidad por pausar el servicio si solo necesitas unos meses.',
]
new_texts_en = [
    'Reach out through GreenPal and tell us the size of your property. Most requests get a quote the same day.',
    'No minimum job size: we coordinate a day that works for you, with service available year round.',
    'Mowing, edging, trimming and blowing off clippings from driveways and walkways, leaving the property clean.',
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
            <a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(20,107,96,0.4); box-shadow: 0 18px 50px rgba(23,42,38,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Reseñas lo confirman" data-en="Reviews confirm it">Reviews confirm it</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Limpieza y Recogida de Hojas" data-en="Yard Cleanup &amp; Leaf Removal">Yard Cleanup &amp; Leaf Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Limpieza de patio y recogida de hojas y restos vegetales, para propiedades que necesitan un repaso a fondo." data-en="Yard cleanup and leaf and debris removal, for properties that need a deeper pass front and back.">Yard cleanup and leaf and debris removal, for properties that need a deeper pass front and back.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Detalle" data-en="Detail work">Detail work</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Recorte y Soplado" data-en="Trimming &amp; Blow-off">Trimming &amp; Blow-off</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Recorte de línea junto a bordes y cercas, con soplado de superficies duras para dejar todo prolijo." data-en="Line trimming along edges and fences, with hard surfaces blown clean so nothing is left scattered.">Line trimming along edges and fences, with hard surfaces blown clean so nothing is left scattered.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Flexible" data-en="Flexible">Flexible</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Servicio Recurrente" data-en="Recurring Service">Recurring Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sin contrato largo ni penalidad: tú controlas el calendario, ya sea por temporada o todo el año." data-en="No long contract and no penalty: you control the schedule, whether it is seasonal or year round.">No long contract and no penalty: you control the schedule, whether it is seasonal or year round.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

services_note = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert services_note
h = h[:services_note.start()] + services_note.group(1) + '<span data-es="Cada trabajo se cotiza según el tamaño de tu propiedad. Escríbenos por GreenPal." data-en="Every job is quoted based on the size of your property. Reach out through GreenPal.">Every job is quoted based on the size of your property. Reach out through GreenPal.</span>' + services_note.group(2) + h[services_note.end():]

# ---------------------------------------------------------------------------
# 14. GALERIA (only 4 real, curated, watermark-cropped photos available -> 2x2/1x4 grid, no wide tile)
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Céspedes" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="yards">yards</span></h2>'
)
rep(
    '''<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>''',
    '''<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg>
          <span data-es="Ver en GreenPal" data-en="See on GreenPal">See on GreenPal</span>
        </a>'''
)

gallery_grid = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert gallery_grid, 'gallery grid anchor not found'
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal"><span class="tile-cap" data-es="Patio delantero limpio" data-en="Yard cleared">Yard cleared</span><img src="assets/raw/gallery-front-yard-cleared.jpg" alt="Front yard mowed and cleared at a North Miami property" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Entrada despejada" data-en="Driveway cleared">Driveway cleared</span><img src="assets/raw/gallery-driveway-cleared.jpg" alt="Driveway and yard cleared of debris in Miami" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[4/3] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Terreno esquinero" data-en="Corner lot mowed">Corner lot mowed</span><img src="assets/raw/gallery-corner-lot-cleared.jpg" alt="Corner lot lawn mowed and cleared near North Miami" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Lateral prolijo" data-en="Side yard cleared">Side yard cleared</span><img src="assets/raw/gallery-side-yard-cleared.jpg" alt="Side yard cleared and tidy at a Miami-Dade property" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]

# ---------------------------------------------------------------------------
# 15. OPINIONES (4 real verbatim GreenPal quotes, expand grid to fit all 4)
# ---------------------------------------------------------------------------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span></h2>'
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.8 de 5 · 98 reseñas verificadas en GreenPal" data-en="4.8 out of 5 · 98 verified reviews on GreenPal">4.8 out of 5 · 98 verified reviews on GreenPal</span></p>'
)

reviews_grid = re.search(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10 reveal">)', h, flags=re.S)
assert reviews_grid, 'reviews grid anchor not found'
NEW_REVIEWS = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="stars text-sm mb-4">★★★★☆</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Overall very good service did a nice job I would have liked to have seen the leaves in my back yard removed but other than that very happy with the job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">James Tejada</span> <span class="text-[color:var(--ink-40)]">· North Miami, FL · GreenPal</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Thank you very much I really appreciate your service."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carissa Thompson</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Nice work."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Matthew Collins</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Gracias David."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sed Gaines</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep(
    '<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 98 reseñas en GreenPal" data-en="Read all 98 reviews on GreenPal">Read all 98 reviews on GreenPal</a>'
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
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Servimos" data-en="Serving">Serving</span> <span class="text-shine">North Miami &amp; Miami-Dade</span></h2>'
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="North Miami y zonas cercanas, con cobertura en todo Miami-Dade County, FL." data-en="North Miami and nearby neighborhoods, with coverage across Miami-Dade County, FL.">North Miami and nearby neighborhoods, with coverage across Miami-Dade County, FL.</p>
            </div>'''
)
rep(
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Cotización gratis" data-en="Free quote">Free quote</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Pide tu cotización por GreenPal, sin compromiso. Suelen responder el mismo día." data-en="Request your quote through GreenPal, no obligation. They usually respond the same day.">Request your quote through GreenPal, no obligation. They usually respond the same day.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" data-es="Pedir cotización" data-en="Get a quote">Get a quote</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.8 de calificación con 98 reseñas de clientes reales en GreenPal." data-en="A 4.8 rating from 98 real customer reviews on GreenPal.">A 4.8 rating from 98 real customer reviews on GreenPal.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,96,0.4)]" href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener">Valeria Landscape on GreenPal</a>
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
        <img src="assets/raw/gallery-corner-lot-cleared.jpg" alt="Corner lot lawn mowed and cleared near North Miami, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>'''
)

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu césped, cuidado de principio a fin." data-en="Your yard, cared for from start to finish.">Your yard, cared for from start to finish.</p>'
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
    '<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Cotización Gratis" data-en="Request a Free Quote">Request a Free Quote</a>'
)
rep(
    '<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Ver Reseñas en GreenPal" data-en="See Reviews on GreenPal">See Reviews on GreenPal</a>'
)

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-base ring-1 ring-[rgba(189,234,221,0.35)] bg-[rgba(189,234,221,0.08)]">VL</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">Valeria Landscape</span>'''
)
rep(
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Cuidado de césped y jardinería en North Miami y Miami-Dade County, FL." data-en="Lawn care and landscaping in North Miami and Miami-Dade County, FL.">Lawn care and landscaping in North Miami and Miami-Dade County, FL.</p>'
)
rep(
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p data-es="North Miami &amp; Miami-Dade County, FL" data-en="North Miami &amp; Miami-Dade County, FL">North Miami &amp; Miami-Dade County, FL</p>
        <p><a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="hover:text-[#bdeadd]" data-es="Cotización gratis · GreenPal" data-en="Free quote · GreenPal">Free quote · GreenPal</a></p>'''
)
rep(
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reseñas" data-en="Reviews">Reviews</p>
        <p><a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="hover:text-[#bdeadd]">GreenPal · 4.8 · 98 reviews</a></p>'''
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Valeria Landscape.</p>')
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Valeria Landscape</span>')

# ---------------------------------------------------------------------------
# 19. Floating booking button
# ---------------------------------------------------------------------------
rep(
    '<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://www.yourgreenpal.com/valeria-landscape-se" target="_blank" rel="noopener" class="book-float" aria-label="Get a free quote on GreenPal">'
)
rep(
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f4f8f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>',
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f4f8f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>'
)

# ---------------------------------------------------------------------------
# Write out
# ---------------------------------------------------------------------------
open(PATH, 'w', encoding='utf-8').write(h)
print('Build OK ->', PATH)
