#!/usr/bin/env python3
"""
Build script for output/rapalo-landscaping-north-miami/index.html
Derived from templates/dark-v2/index.html (Pure Artistry skeleton) via anchored
transformation, per templates/SKELETONS-V2.md. Landscaping business, GreenPal-only,
no bookable menu -> VARIANTE ADAPTADA (FORGE-BRIEF 0.b): no fixed prices (quote-based),
no map (no public storefront, service comes to the customer), CTA -> real GreenPal profile.
"""
import re, sys

SLUG = "rapalo-landscaping-north-miami"
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

# ============================================================
# STEP 1: Protect the Merktop badge block (stays gold, always)
# ============================================================
badge_re = re.compile(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", re.S)
m = badge_re.search(h)
assert m, "merktop badge block not found"
badge_block = m.group(0)
h = h[:m.start()] + "@@BADGE@@" + h[m.end():]

# ============================================================
# STEP 2: Palette - hue-rotate every gold/amber tone to jade green
# (computed via HSL rotation, hue=150deg, preserving L/S -> keeps all
# gradient/shadow relationships intact). Distinct from otechlandscaping's
# forest #3d6b2f (light), pride-landscaping's bright #55ca65 (dark) and
# bonzai's blue #48a7d7 (dark).
# ============================================================
HEX_MAP = {
    "6b5222": "226b47", "d4a84b": "4bd490", "e9c3ab": "abe9ca", "8a744a": "4a8a6a",
    "1c1408": "081c12", "f5efe3": "e3f5ec", "f0dc9e": "9ef0c7", "e8cf96": "96e8bf",
    "e8c476": "76e8af", "e5c374": "74e5ad", "c9a04a": "4ac98a", "9a7431": "319a66",
    "96742c": "2c9661", "0f0b07": "070f0b", "fbf6ea": "eafbf2", "faf1dc": "dcfaeb",
    "f8eed3": "d3f8e5", "f4eee2": "e2f4eb", "f0dcae": "aef0cf", "ecd9a8": "a8ecca",
    "c9ab6b": "6bc99a", "bfa060": "60bf90", "b8934a": "4ab881", "241c0e": "0e2419",
    "191307": "071910", "171207": "07170f", "100c05": "05100b", "0c0905": "050c09",
}
RGB_MAP = {
    "212,168,75": "75,212,144", "232,207,150": "150,232,191", "245,239,227": "227,245,236",
    "80,58,18": "18,80,49", "110,85,35": "35,110,73", "54,42,38": "38,54,46",
    "36,28,20": "20,36,28", "27,21,14": "14,27,20", "244,238,226": "226,244,235",
    "232,210,160": "160,232,196", "185,138,128": "128,185,156", "180,140,60": "60,180,120",
    "15,11,7": "7,15,11", "122,90,30": "30,122,76",
}
for old, new in HEX_MAP.items():
    h = h.replace("#" + old, "#" + new)
for old, new in RGB_MAP.items():
    h = h.replace("rgba(" + old, "rgba(" + new)

# Restore protected badge (always gold, per pipeline rule)
h = h.replace("@@BADGE@@", badge_block)

# theme-color meta uses old bg hex already mapped above (0f0b07 -> 070f0b): fine.

print("Palette OK")

# ============================================================
# STEP 3: HEAD (title, meta, og, icon, JSON-LD)
# ============================================================
rep(
'<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
'<title>Rapalo Landscaping · Lawn Care in North Miami, FL | 4.76 on GreenPal</title>'
)
rep(
'<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
'<meta name="description" content="Rapalo Landscaping, North Miami &amp; North Miami Beach FL: lawn mowing, edging, planting and yard cleanup. 4.76 rating across 238 reviews on GreenPal. Free on-site quotes." />'
)
rep(
'<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
'<meta property="og:title" content="Rapalo Landscaping · North Miami, FL" />'
)
rep(
'<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
'<meta property="og:description" content="Lawn care and yard maintenance in North Miami, FL. 4.76 rating, 238 reviews on GreenPal." />'
)
rep(
'<meta property="og:image" content="assets/raw/bk-1.jpg" />',
'<meta property="og:image" content="assets/raw/hero-white-house-purple-door.jpg" />'
)
rep(
'<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
'<link rel="icon" type="image/jpeg" href="assets/raw/hero-white-house-purple-door.jpg" />'
)

OLD_JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Pure Artistry",
    "description": "Hair studio in Orlando, FL: silk press, loc retwists and interlocks, knotless braids, K-Tip and microlink extensions, keratin treatments.",
    "address": { "@type": "PostalAddress", "streetAddress": "80 W Grant St, Suite 111, Studio 156", "addressLocality": "Orlando", "addressRegion": "FL", "postalCode": "32806", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando", "https://www.instagram.com/pure.artistrysk/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "234", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Silk Press" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full-head Loc Retwist" } },
      { "@type": "Offer", "price": "400", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Small Knotless Braids" } },
      { "@type": "Offer", "price": "750", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "K-Tip Extensions" } }
    ] }
  }
  </script>'''
NEW_JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LandscapingBusiness",
    "name": "Rapalo Landscaping",
    "legalName": "Rapalo Landscaping LLC",
    "description": "Lawn care and landscaping company serving North Miami and North Miami Beach, FL: mowing, edging, planting and design, weeding and yard cleanup.",
    "telephone": "+1-786-641-9360",
    "address": { "@type": "PostalAddress", "streetAddress": "3546 NW 99th St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33147", "addressCountry": "US" },
    "areaServed": ["North Miami, FL", "North Miami Beach, FL"],
    "sameAs": ["https://www.yourgreenpal.com/rapalo-landscaping"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.76", "reviewCount": "238", "bestRating": "5" },
    "makesOffer": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Lawn Care" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Planting & Design" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Yard Maintenance" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Free Consultation" } }
    ]
  }
  </script>'''
rep(OLD_JSONLD, NEW_JSONLD)

print("Head OK")

# ============================================================
# STEP 4: Preloader
# ============================================================
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">R</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Rapalo Landscaping</span>')

print("Preloader OK")

# ============================================================
# STEP 5: NAV (logo -> monogram, wordmark, links, CTA, mobile menu)
# ============================================================
rep(
'''<a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,212,144,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>
      </a>''',
'''<a href="#top" class="flex items-center gap-3">
        <span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-lg ring-1 ring-[rgba(75,212,144,0.35)] bg-[rgba(75,212,144,0.1)] text-[color:var(--accent-deep)]">R</span>
        <span class="font-display text-xl tracking-[0.1em] uppercase">Rapalo <span class="text-[color:var(--accent-deep)]">Landscaping</span></span>
      </a>'''
)

rep(
'''        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>
        <a class="nav-link" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>
        <a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>
        <a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>
        <a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>
        <a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>
      </nav>''',
'''        <a class="nav-link" href="#experiencia" data-es="Nosotros" data-en="About Us">About Us</a>
        <a class="nav-link" href="#metodo" data-es="Cómo Trabajamos" data-en="How It Works">How It Works</a>
        <a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="nav-link" href="#opiniones" data-es="Reseñas" data-en="Reviews">Reviews</a>
        <a class="nav-link" href="#ubicacion" data-es="Contacto" data-en="Contact">Contact</a>
      </nav>'''
)

rep(
'''        <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''',
'''        <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Cotización Gratis" data-en="Free Quote">Free Quote</span>
        </a>'''
)

rep(
'''        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>
        <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>''',
'''        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="Nosotros" data-en="About Us">About Us</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="Cómo Trabajamos" data-en="How It Works">How It Works</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Reseñas" data-en="Reviews">Reviews</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Contacto" data-en="Contact">Contact</a>
        <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Cotización Gratis" data-en="Free Quote">Free Quote</a>'''
)

print("Nav OK")

# ============================================================
# STEP 6: HERO
# ============================================================
rep(
'<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
'<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="North Miami, FL · Lawn &amp; Yard Care" data-en="North Miami, FL · Lawn &amp; Yard Care">North Miami, FL · Lawn &amp; Yard Care</p>'
)
rep(
'<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
'<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Un jardin sano, sin complicaciones." data-en="A healthy yard, without the hassle.">A healthy yard, without the hassle.</p>'
)
rep(
'''        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>
        </h1>''',
'''        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Tu cesped y jardin," data-en="Your yard, cared for">Your yard, cared for</span><br /><span data-es="cuidados " data-en="the ">the </span><span class="text-shine" data-es="de verdad" data-en="right way">right way</span>
        </h1>'''
)
rep(
'<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
'<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Breylin y el equipo de Rapalo Landscaping se encargan de todo: corte y bordes de cesped, siembra de plantas, deshierbe y limpiezas de temporada en North Miami y North Miami Beach, con 4.76 de calificacion en 238 reseñas de GreenPal." data-en="Breylin and the Rapalo Landscaping crew handle it all: mowing and edging, planting, weeding and seasonal cleanups across North Miami and North Miami Beach, with a 4.76 rating across 238 reviews on GreenPal.">Breylin and the Rapalo Landscaping crew handle it all: mowing and edging, planting, weeding and seasonal cleanups across North Miami and North Miami Beach, with a 4.76 rating across 238 reviews on GreenPal.</p>'
)
rep(
'<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
'<span class="text-sm text-[color:var(--ink-60)]" data-es="4.76 · 238 reseñas en GreenPal" data-en="4.76 · 238 reviews on GreenPal">4.76 · 238 reviews on GreenPal</span>'
)
rep(
'''          <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>''',
'''          <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Pedir cotizacion en GreenPal" data-en="Get a quote on GreenPal">Get a quote on GreenPal</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="tel:+17866419360" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            (786) 641-9360
          </a>'''
)
rep(
'<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
'<img src="assets/raw/hero-white-house-purple-door.jpg" alt="Freshly mowed lawn with trimmed palms in front of a home serviced by Rapalo Landscaping in North Miami" class="blur-up w-full h-full object-cover" />'
)
rep(
'''            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
'''            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Cotizacion" data-en="Quote">Quote</p>
            <p class="font-display text-lg" data-es="Estimado gratis" data-en="Free estimate">Free estimate</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="North Miami, FL" data-en="North Miami, FL">North Miami, FL</p>'''
)

print("Hero OK")

# ============================================================
# STEP 7: STRIP DE CONFIANZA
# ============================================================
rep(
'<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
'<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.76" data-decimals="2">4.76</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="238">238</span> <span data-es="reseñas en GreenPal" data-en="reviews on GreenPal">reviews on GreenPal</span></p></div>'
)
rep(
'<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
'<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Lawn <span class="text-shine">&amp;</span> Yard</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Corte · Bordes · Siembra" data-en="Mowing · Edging · Planting">Mowing · Edging · Planting</p></div>'
)
rep(
'<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
'<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-count="70">70</span>%</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientes que repiten" data-en="Repeat clients">Repeat clients</p></div>'
)
rep(
'<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
'<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl" data-es="North Miami" data-en="North Miami">North Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Zona de servicio" data-en="Service area">Service area</p></div>'
)

print("Strip OK")

# ============================================================
# STEP 8: MARQUEE (2 marquees x 2 seqs = 4 occurrences per word)
# ============================================================
MARQUEE_WORDS = [
    ("Silk Press", "Lawn Mowing"),
    ("Loc Retwist", "Edging"),
    ("Knotless Braids", "Planting &amp; Design"),
    ("K-Tip Extensions", "Weeding"),
    ("Keratin", "Yard Cleanup"),
    ("Orlando, FL", "North Miami, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)

print("Marquee OK")

open(PATH, "w", encoding="utf-8").write(h)
print("Checkpoint 3 written (+marquee)")
