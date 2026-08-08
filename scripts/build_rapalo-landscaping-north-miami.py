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

# ============================================================
# STEP 9: LA EXPERIENCIA (About Us)
# ============================================================
rep(
'''        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''',
'''        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-white-house-purple-door.jpg" alt="Manicured lawn and trimmed palms at a home serviced by Rapalo Landscaping" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-yard-cleanup.jpg" alt="Yard cleanup in progress by Rapalo Landscaping, patchy lawn area being restored" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>'''
)
rep(
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>',
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Nosotros" data-en="About us">About us</p>'
)
rep(
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un equipo local," data-en="A local crew,">A local crew,</span><br /><span class="text-shine" data-es="cuidado de verdad" data-en="care you can trust">care you can trust</span></h2>'
)
rep(
'<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
'<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Rapalo Landscaping es un equipo de jardineria local liderado por Breylin, sirviendo North Miami y North Miami Beach. Se encargan de todo: corte y bordes de cesped, siembra de plantas, deshierbe, poda y limpiezas de temporada, con un objetivo simple: un jardin sano y bonito sin complicaciones para ti." data-en="Rapalo Landscaping is a local gardening team led by Breylin, serving North Miami and North Miami Beach. They handle everything from lawn mowing and edging to planting, weeding, pruning and seasonal cleanups, all built around one simple goal: a healthy, beautiful yard without the hassle for you.">Rapalo Landscaping is a local gardening team led by Breylin, serving North Miami and North Miami Beach. They handle everything from lawn mowing and edging to planting, weeding, pruning and seasonal cleanups, all built around one simple goal: a healthy, beautiful yard without the hassle for you.</p>'
)
rep(
'<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
'<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Su politica es simple: si tu presupuesto cotizado no alcanza para el trabajo extra que encuentran, se detienen y lo dejan tal cual en vez de sumar costos sin avisarte primero. Tu sigues en control de cada trabajo. 4.76 de calificacion en 238 reseñas verificadas de GreenPal lo confirman." data-en="Their policy is simple: if your quoted budget does not cover extra work they find on-site, they pause and leave it as-is instead of adding costs without asking first. You stay in control of every job. A 4.76 rating across 238 verified GreenPal reviews backs it up.">Their policy is simple: if your quoted budget does not cover extra work they find on-site, they pause and leave it as-is instead of adding costs without asking first. You stay in control of every job. A 4.76 rating across 238 verified GreenPal reviews backs it up.</p>'
)
rep(
'''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
'''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.76" data-decimals="2">4.76</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">GreenPal</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="238">238</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="70">70</span>%</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Repiten" data-en="Repeat">Repeat</p></div>'''
)
rep(
'''            <img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,212,144,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
'''            <span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(75,212,144,0.3)] bg-[rgba(75,212,144,0.1)] text-[color:var(--accent-deep)]">R</span>
            <span class="text-sm font-light">Rapalo Landscaping · <span class="text-[color:var(--ink-40)]" data-es="North Miami, FL" data-en="North Miami, FL">North Miami, FL</span></span>'''
)

print("Experiencia OK")

# ============================================================
# STEP 10: EL METODO (How It Works)
# ============================================================
rep(
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Asi trabajamos" data-en="How it works">How it works</p>'
)
rep(
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Simple, de principio" data-en="Simple, start">Simple, start</span> <span class="text-shine" data-es="a fin" data-en="to finish">to finish</span></h2>'
)
rep(
'''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
'''          <h3 class="font-display text-xl mb-3" data-es="Pides tu cotizacion" data-en="Request your quote">Request your quote</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Escribes por GreenPal o llamas al (786) 641-9360 y cuentas el tamaño de tu patio y que necesitas." data-en="Message them on GreenPal or call (786) 641-9360 and tell them your yard size and what you need.">Message them on GreenPal or call (786) 641-9360 and tell them your yard size and what you need.</p>'''
)
rep(
'''          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
'''          <h3 class="font-display text-xl mb-3" data-es="Estimado en el sitio" data-en="On-site estimate">On-site estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Breylin visita tu patio y te da opciones segun tu presupuesto: nunca suman costos sin tu aprobacion primero." data-en="Breylin visits your yard and offers options that fit your budget: they never add costs without your approval first.">Breylin visits your yard and offers options that fit your budget: they never add costs without your approval first.</p>'''
)
rep(
'''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
'''          <h3 class="font-display text-xl mb-3" data-es="Hacen el trabajo" data-en="They do the work">They do the work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Corte, bordes, siembra, deshierbe o limpieza, con su propio equipo, en North Miami y North Miami Beach." data-en="Mowing, edging, planting, weeding or cleanup, with their own equipment, across North Miami and North Miami Beach.">Mowing, edging, planting, weeding or cleanup, with their own equipment, across North Miami and North Miami Beach.</p>'''
)
rep(
'''          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
'''          <h3 class="font-display text-xl mb-3" data-es="Cuidado continuo" data-en="Ongoing care">Ongoing care</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Reservas visitas puntuales o recurrentes, y puedes pausar o reprogramar cuando quieras, sin complicaciones." data-en="Book one-time or recurring visits, and skip or reschedule anytime, no hassle.">Book one-time or recurring visits, and skip or reschedule anytime, no hassle.</p>'''
)

print("Metodo OK")

# ============================================================
# STEP 11: SERVICIOS (VARIANTE ADAPTADA: no fixed prices, quote-based)
# ============================================================
rep(
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>',
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>'
)
rep(
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que" data-en="What they">What they</span> <span class="text-shine" data-es="hacemos" data-en="do">do</span></h2>'
)
rep(
'<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
'<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cada patio se cotiza segun tamaño y lo que necesite. Escribenos y pide tu cotizacion gratis." data-en="Every yard is quoted based on size and what it needs. Get in touch for a free quote.">Every yard is quoted based on size and what it needs. Get in touch for a free quote.</p>'
)

SERVICES_RE = r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)'
SERVICES_NEW = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(75,212,144,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte &amp; Bordes" data-en="Lawn Care">Lawn Care</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte, bordes y fertilizacion para un cesped parejo y fresco en cada visita." data-en="Mowing, edging and fertilizing for a fresh, even cut on every visit.">Mowing, edging and fertilizing for a fresh, even cut on every visit.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotizacion" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diseño" data-en="Design">Design</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Siembra &amp; Diseño" data-en="Planting &amp; Design">Planting &amp; Design</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Flores, arbustos y plantas elegidas segun el espacio y la luz de tu jardin." data-en="Flowers, shrubs and greenery chosen for your yard's space and sunlight.">Flowers, shrubs and greenery chosen for your yard's space and sunlight.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotizacion" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mantenimiento" data-en="Maintenance">Maintenance</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cuidado del Jardin" data-en="Yard Maintenance">Yard Maintenance</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Deshierbe, poda y retiro de escombros para mantener todo prolijo durante el año." data-en="Weeding, pruning and debris removal to keep things tidy year round.">Weeding, pruning and debris removal to keep things tidy year round.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotizacion" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sin costo" data-en="No cost">No cost</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Consulta Gratis" data-en="Free Consultation">Free Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una visita al sitio para evaluar tu jardin y encontrar opciones segun tu presupuesto." data-en="An on-site visit to assess your yard and find options that fit your budget.">An on-site visit to assess your yard and find options that fit your budget.</p>
          <div class="mt-auto">
            <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir cotizacion" data-en="Get a quote">Get a quote</a>
          </div>
        </div>
      </div>
      '''
rep_re(SERVICES_RE, SERVICES_NEW, n=1)

rep(
'<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
'<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="¿Necesitas algo que no esta en la lista? Preguntanos igual: cotizan segun lo que tu patio necesite." data-en="Need something not on this list? Ask anyway: they quote based on what your yard actually needs.">Need something not on this list? Ask anyway: they quote based on what your yard actually needs.</span></p>'
)

print("Servicios OK")

# ============================================================
# STEP 12: GALERIA (4 real curated photos: 1 wide + 3 tiles, no reuse
# within the grid; DESIGN.md prefers fewer real tiles over padding)
# ============================================================
rep(
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>',
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galeria" data-en="Gallery">Gallery</p>'
)
rep(
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Cespedes" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lawns">lawns</span></h2>'
)
rep(
'''        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @pure.artistrysk
        </a>''',
'''        <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          Rapalo Landscaping on GreenPal
        </a>'''
)

GALLERY_RE = r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>'
GALLERY_NEW = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Entrada y carport" data-en="Driveway &amp; carport">Driveway &amp; carport</span><img src="assets/raw/gallery-carport-driveway-strips.jpg" alt="Mowed lawn with clean driveway edging at a carport home serviced by Rapalo Landscaping" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cesped y palmeras" data-en="Lawn &amp; palms">Lawn &amp; palms</span><img src="assets/raw/gallery-white-house-palm.jpg" alt="Freshly mowed lawn with palm trees in front of a white house" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Trabajo terminado" data-en="Finished job">Finished job</span><img src="assets/raw/gallery-driveway-minivan.jpg" alt="Mowed lawn and driveway at a North Miami home after a Rapalo Landscaping visit" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Bordes y seto" data-en="Edging &amp; hedge">Edging &amp; hedge</span><img src="assets/raw/gallery-carport-hedge.jpg" alt="Trimmed hedge and mowed lawn next to a carport" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
rep_re(GALLERY_RE, GALLERY_NEW, n=1)

print("Galeria OK")

# ============================================================
# STEP 13: OPINIONES (real verbatim quotes from GreenPal)
# ============================================================
rep(
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Reseñas" data-en="Reviews">Reviews</p>'
)
rep(
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>',
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What North Miami">Lo que dicen</span> <span class="text-shine" data-es="en North Miami" data-en="says">says</span></h2>'
)
rep(
'<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
'<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.76 de 5 · 238 reseñas verificadas en GreenPal" data-en="4.76 out of 5 · 238 verified reviews on GreenPal">4.76 out of 5 · 238 verified reviews on GreenPal</span></p>'
)
rep(
'''        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
'''        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Used Rapalo Landscaping and they came in and did a great job"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jannette Rodriguez</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>'''
)
rep(
'''        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
'''        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Thank you, Breylin! You always do great work and leave a beautiful yard behind :-)"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mercedes Cordero</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>'''
)
rep(
'''        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
'''        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great communication as always and excellent work."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rene Ferretti</span> <span class="text-[color:var(--ink-40)]">· GreenPal</span></figcaption>
        </figure>'''
)
rep(
'<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
'<a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 238 reseñas en GreenPal" data-en="Read all 238 reviews on GreenPal">Read all 238 reviews on GreenPal</a>'
)

print("Opiniones OK")

# ============================================================
# STEP 14: UBICACION -> CONTACTO (VARIANTE ADAPTADA: no public storefront
# address to visit, so no map; real photo instead, per FORGE-BRIEF 0.b)
# ============================================================
rep(
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visítanos</p>',
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Contacto" data-en="Contact">Contact</p>'
)
rep(
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
'<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Trabajamos en" data-en="Serving">Serving</span> <span class="text-shine" data-es="North Miami" data-en="North Miami, FL">North Miami, FL</span></h2>'
)
rep(
'''            <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,144,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
'''            <p class="font-medium mb-1" data-es="Cotizacion gratis" data-en="Free quote">Free quote</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Pide tu cotizacion gratis por GreenPal o llama al (786) 641-9360. Suelen responder rapido." data-en="Request your free quote through GreenPal or call (786) 641-9360. They usually respond quickly.">Request your free quote through GreenPal or call (786) 641-9360. They usually respond quickly.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,144,0.4)]" href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener">Rapalo Landscaping on GreenPal</a>'''
)
rep(
'''            <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,144,0.4)]" href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
'''            <p class="font-medium mb-1" data-es="Reseñas verificadas" data-en="Verified reviews">Verified reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="4.76 de calificacion en 238 reseñas de GreenPal, ademas de 5.0 en Angi y HomeAdvisor." data-en="4.76 rating from 238 reviews on GreenPal, plus a 5.0 rating on Angi and HomeAdvisor.">4.76 rating from 238 reviews on GreenPal, plus a 5.0 rating on Angi and HomeAdvisor.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,144,0.4)]" href="https://www.homeadvisor.com/rated.rapalolandscaping.145086278.html" target="_blank" rel="noopener">Rapalo Landscaping on HomeAdvisor</a>'''
)
rep(
'''            <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,144,0.4)]" href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener">@pure.artistrysk</a>''',
'''            <p class="font-medium mb-1" data-es="Zona de servicio" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="North Miami, North Miami Beach y alrededores." data-en="North Miami, North Miami Beach and the surrounding area.">North Miami, North Miami Beach and the surrounding area.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,212,144,0.4)]" href="https://www.google.com/maps/place/North+Miami,+FL" target="_blank" rel="noopener" data-es="Ver zona" data-en="See area">See area</a>'''
)
# Icon for the "Verified reviews" card: swap the map-pin icon for a shield icon
rep(
'''            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reseñas verificadas" data-en="Verified reviews">Verified reviews</p>''',
'''            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reseñas verificadas" data-en="Verified reviews">Verified reviews</p>'''
)
# Map iframe -> real photo (no public storefront address to visit; FORGE-BRIEF 0.b)
rep(
'''      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
'''      <div class="frame zoomable img-reveal reveal min-h-[380px]" style="transition-delay:180ms">
        <img src="assets/raw/gallery-white-house-palm.jpg" alt="Freshly mowed lawn with palm trees at a home in North Miami serviced by Rapalo Landscaping" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>'''
)

print("Ubicacion OK")

# ============================================================
# STEP 15: CTA FINAL
# ============================================================
rep(
'<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
'<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Un jardin sano, sin complicaciones." data-en="A healthy yard, without the hassle.">A healthy yard, without the hassle.</p>'
)
rep(
'<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
'<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu jardin" data-en="Your yard">Your yard</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>'
)
rep(
'<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
'<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Pide tu cotizacion gratis hoy por GreenPal. Sin costos ocultos sin tu aprobacion, solo un jardin bien cuidado." data-en="Get your free quote today through GreenPal. No hidden costs added without your approval, just a well kept yard.">Get your free quote today through GreenPal. No hidden costs added without your approval, just a well kept yard.</p>'
)
rep(
'''        <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
'''        <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Pedir cotizacion en GreenPal" data-en="Get a quote on GreenPal">Get a quote on GreenPal</a>
        <a href="tel:+17866419360" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm">(786) 641-9360</a>'''
)

print("CTA final OK")

# ============================================================
# STEP 16: FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Rapalo</span>')
rep(
'''        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,232,191,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
'''        <div class="flex items-center gap-3 mb-4">
          <span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(150,232,191,0.35)] bg-[rgba(75,212,144,0.1)] text-[color:var(--accent-deep)]">R</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">Rapalo Landscaping</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Cuidado de cesped y jardines en North Miami y North Miami Beach, FL. Cotizacion gratis." data-en="Lawn care and yard maintenance in North Miami and North Miami Beach, FL. Free quotes.">Lawn care and yard maintenance in North Miami and North Miami Beach, FL. Free quotes.</p>'''
)
rep(
'''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="hover:text-[#abe9ca]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
'''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>North Miami, FL, United States</p>
        <p><a href="tel:+17866419360" class="hover:text-[#abe9ca]">(786) 641-9360</a></p>
        <p><a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="hover:text-[#abe9ca]" data-es="Cotizacion gratis en GreenPal" data-en="Free quote on GreenPal">Free quote on GreenPal</a></p>'''
)
rep(
'''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="hover:text-[#abe9ca]">Instagram · @pure.artistrysk</a></p>''',
'''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Tambien verificados en" data-en="Also verified on">Also verified on</p>
        <p><a href="https://www.homeadvisor.com/rated.rapalolandscaping.145086278.html" target="_blank" rel="noopener" class="hover:text-[#abe9ca]">HomeAdvisor · 5.0</a></p>
        <p><a href="https://www.angi.com/companylist/us/fl/miami/rapalo-landscaping-reviews-1.htm" target="_blank" rel="noopener" class="hover:text-[#abe9ca]">Angi · 5.0</a></p>'''
)
rep(
'<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
'<p class="text-xs text-[color:var(--ink-40)]">© 2026 Rapalo Landscaping.</p>'
)

print("Footer OK")

# ============================================================
# STEP 17: Floating book button + icon color (uses accent-deep-on-dark hex)
# ============================================================
rep(
'''  <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#081c12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>''',
'''  <a href="https://www.yourgreenpal.com/rapalo-landscaping" target="_blank" rel="noopener" class="book-float" aria-label="Get a free quote on GreenPal">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#081c12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>'''
)

print("Floating button OK")

# ============================================================
# STEP 18: Any leftover Booksy/Pure Artistry/Orlando/Instagram references
# (safety net; should be zero after the above, asserted for certainty)
# ============================================================
for leftover in ["Pure Artistry", "pure.artistrysk", "booksy.com", "Booksy", "Orlando", "silk press", "Silk Press", "K-Tip"]:
    assert leftover not in h, f"LEFTOVER FOUND: {leftover!r}"

open(PATH, "w", encoding="utf-8").write(h)
print("BUILD COMPLETE:", PATH)
