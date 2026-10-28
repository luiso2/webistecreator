#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2 -> output/jusel-finish-carpentry.

JUSEL FINISH CARPENTRY LLC, Brandon/Tampa Bay area FL. Finish carpentry, custom
shelving, trim, cabinetry. Datos VERIFICADOS (2026-10-28) via Google Maps
(maps_discover.py + maps_research.py), nada inventado:
- Nombre: "Jusel Finish Carpentry LLC"
- Rating 5.0, 24 reviews en Google
- Telefono real: +1 813-648-0643
- Horarios reales: todos los dias 6AM-8PM... en realidad 6AM-6PM los 7 dias (ficha Maps)
- SIN direccion publica en la ficha (address: null) -> sin mapa inventado
- SIN website propio (verificado con maps_discover.py + WebSearch sin resultados)
- SIN Instagram/Facebook/email publico encontrado (WebSearch negativo)
- Lider: "Jusel" (carpintero), pareja/coordinadora "Diana", nombrados en resenas reales
- 2 reviews verbatim completas (allison perez, Emily Petronis); una 3a (Jon Behr) estaba
  truncada por Google con "..." y se omite
- Servicios derivados de resenas + fotos propias: floating shelves, shoe molding/trim,
  tile backsplash, tongue-and-groove ceiling/beams, outdoor entertainment centers,
  kitchen cabinets, closet shelving. SIN precios publicos -> "Call for a quote".
"""
import re

SLUG = "jusel-finish-carpentry"
PATH = f"output/{SLUG}/index.html"
h = open(PATH, encoding="utf-8").read()

TEL = "tel:+18136480643"
MAPS_URL = "https://www.google.com/maps/place/Jusel+Finish+Carpentry+LLC/data=!4m7!3m6!1s0x5b95b95e0fe285b:0xcc935a1fbbb1702e!8m2!3d27.9175306!4d-82.515625!16s%2Fg%2F11tp7ww6tq!19sChIJWyj-4JVbuQURLnCxux9ak8w?authuser=0&hl=en&g_ep=EgoyMDI2MTAyMC4wIJJjKgBIAVAD&rclk=1"


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


def rx(pattern, new, flags=re.S):
    global h
    m = re.search(pattern, h, flags=flags)
    assert m, "REGEX NO MATCH: " + pattern[:140]
    h = h[:m.start()] + new + h[m.end():]


# ---------------------------------------------------------------------------
# 1. Paleta: dorado (pureartistry) -> copper/walnut (madera, carpinteria)
#    accent-deep #c17a3d, accent-mid #a9683a. Distinto del dorado champan original.
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#d4a84b", "#c17a3d"),   # accent-deep
    ("#b8934a", "#a9683a"),   # accent-mid
    ("#f0dc9e", "#e8b37e"),   # text-shine light stop / shimmer
    ("#9a7431", "#7a4a22"),   # text-shine dark stop
    ("#e5c374", "#d6975c"),   # text-shine mid stop
    ("#e8c476", "#d99a5e"),   # btn-3d gradient start
    ("#c9a04a", "#bd7c3e"),   # btn-3d gradient mid
    ("#96742c", "#6e431f"),   # btn-3d gradient end
    ("#6b5222", "#4f2f16"),   # btn-3d sole shadow
    ("#e9c3ab", "#e3b98f"),   # footer link hover
    ("#e8cf96", "#e0b07e"),   # dark-band text-shine light
    ("#f8eed3", "#f6e6d2"),   # dark-band text-shine lightest
    ("#bfa060", "#b4824f"),   # dark-band text-shine mid
    ("#faf1dc", "#f8ecd8"),   # dark-band btn-3d gradient start
    ("#ecd9a8", "#e9cba3"),   # dark-band btn-3d gradient mid
    ("#c9ab6b", "#c99f6e"),   # dark-band btn-3d gradient end
    ("#8a744a", "#8a6540"),   # dark-band btn-3d shadow
    ("#232016", "#231a12"),   # (noop-safe guard, see below if absent)
]
# Algunas entradas de arriba pueden no existir si el valor exacto difiere; cada
# reemplazo real se valida por separado abajo para no abortar todo el script
# por una entrada decorativa.
for old, new in HEX_PALETTE:
    c = h.count(old)
    if c:
        h = h.replace(old, new)
    else:
        print(f"(paleta) aviso: '{old}' no encontrado, se omite")

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(193,122,61"),   # accent-deep alpha (glass borders, badges)
    ("rgba(122,90,30", "rgba(110,67,31"),     # orb-b
    ("rgba(180,140,60", "rgba(189,124,62"),   # orb-c
    ("rgba(232,207,150", "rgba(224,176,126"), # dark-band accent-ghost / orb-a
    ("rgba(110,85,35", "rgba(110,67,31"),     # dark-band btn-3d shadow alpha
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    if c:
        h = h.replace(old, new)
    else:
        print(f"(paleta rgba) aviso: '{old}' no encontrado, se omite")
print("PALETTE done")

# ---------------------------------------------------------------------------
# 2. GLOBALES: Booksy -> tel:, IG -> Google Maps listing
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
c = h.count(OLD_BOOK)
assert c >= 8, c
h = h.replace(OLD_BOOK, TEL)

OLD_IG = "https://www.instagram.com/pure.artistrysk/"
c = h.count(OLD_IG)
assert c >= 3, c
h = h.replace(OLD_IG, MAPS_URL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 3. HEAD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Jusel Finish Carpentry LLC · Finish Carpentry in Brandon, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Jusel Finish Carpentry LLC, Brandon FL: custom floating shelves, trim, cabinetry, tile backsplash and tongue-and-groove ceilings. 5.0 stars across 24 Google reviews. Call (813) 648-0643." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Jusel Finish Carpentry LLC · Finish Carpentry in Brandon, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Custom carpentry, shelving, trim and cabinetry. 5.0 on Google. Call (813) 648-0643." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-1.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-1.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = f'''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "GeneralContractor",
    "name": "Jusel Finish Carpentry LLC",
    "description": "Finish carpentry contractor serving the Brandon and Tampa Bay, FL area: custom floating shelves, trim, cabinetry, tile backsplash installation and tongue-and-groove ceilings.",
    "areaServed": "Brandon and Tampa Bay, FL",
    "telephone": "+1-813-648-0643",
    "image": "assets/raw/gmaps-1.jpg",
    "sameAs": ["{MAPS_URL}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "24", "bestRating": "5" }},
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Finish carpentry services", "itemListElement": [
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Custom Floating Shelves" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Trim &amp; Shoe Molding" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Tile Backsplash Installation" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Tongue-and-Groove Ceilings &amp; Beams" }} }}
    ] }}
  }}
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 4. Idioma: EN -> se queda en default
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 5. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">JF</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Jusel Finish Carpentry</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(193,122,61,0.35)]" />',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(193,122,61,0.35)] bg-[rgba(193,122,61,0.1)] text-[color:var(--accent-deep)]">JF</span>')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-base sm:text-xl tracking-[0.04em] sm:tracking-[0.1em] uppercase whitespace-nowrap">Jusel <span class="text-[color:var(--accent-deep)]">Finish Carpentry</span></span>')
print("NAV BRAND done")

for old, new in [
    ('data-es="La Experiencia" data-en="The Experience">La Experiencia</a>', 'data-es="About Us" data-en="About Us">About Us</a>'),
    ('data-es="El Método" data-en="The Method">El Método</a>', 'data-es="How We Work" data-en="How We Work">How We Work</a>'),
    ('data-es="Servicios" data-en="Services">Servicios</a>', 'data-es="Servicios" data-en="Services">Services</a>'),
    ('data-es="Galería" data-en="Gallery">Galería</a>', 'data-es="Galería" data-en="Gallery">Gallery</a>'),
    ('data-es="Opiniones" data-en="Reviews">Opiniones</a>', 'data-es="Reviews" data-en="Reviews">Reviews</a>'),
    ('data-es="Ubicación" data-en="Location">Ubicación</a>', 'data-es="Contact" data-en="Contact">Contact</a>'),
]:
    rep_all(old, new, expect=2)
print("NAV LINKS done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call Now" data-en="Call Now">Call Now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call Now" data-en="Call Now">Call Now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 6. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio',
    'data-es="Brandon, FL · Finish Carpentry" data-en="Brandon, FL · Finish Carpentry">Brandon, FL · Finish Carpentry')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Built in, built right." data-en="Built in, built right.">Built in, built right.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Custom carpentry," data-en="Custom carpentry,">Custom carpentry,</span><br /><span data-es="finished with " data-en="finished with ">finished with </span><span class="text-shine" data-es="real craft" data-en="real craft">real craft</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Jusel Finish Carpentry LLC construye estantes flotantes a medida, molduras, gabinetes y techos de madera en toda el area de Brandon y Tampa Bay. Jusel y su equipo trabajan con la atencion al detalle que describen sus clientes, con 5.0 perfecto en Google." data-en="Jusel Finish Carpentry LLC builds custom floating shelves, trim, cabinetry and wood ceilings across the Brandon and Tampa Bay area. Jusel and his crew work with the attention to detail clients describe, holding a perfect 5.0 on Google.">Jusel Finish Carpentry LLC builds custom floating shelves, trim, cabinetry and wood ceilings across the Brandon and Tampa Bay area. Jusel and his crew work with the attention to detail clients describe, holding a perfect 5.0 on Google.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 24 reseñas en Google" data-en="5.0 · 24 reviews on Google">5.0 · 24 reviews on Google</span>')
rx(r'<a href="tel:\+18136480643" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\s*<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>.*?</a>\s*<a href="' + re.escape(MAPS_URL) + r'" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">.*?@pure\.artistrysk\s*</a>',
   f'''<a href="{TEL}" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (813) 648-0643" data-en="Call (813) 648-0643">Call (813) 648-0643</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <span data-es="Google Maps" data-en="Google Maps">Google Maps</span>
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="Kitchen cabinets and tile backsplash finished by Jusel Finish Carpentry" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Direct Line" data-en="Direct Line">Direct Line</p>
            <p class="font-display text-lg">(813) 648-0643</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Brandon, FL" data-en="Brandon, FL">Brandon, FL</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 7. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="24">24</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Trim <span class="text-shine">&amp;</span> Shelves</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cabinets · Backsplash" data-en="Cabinets · Backsplash">Cabinets · Backsplash</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Jusel <span class="text-shine">&amp;</span> Diana</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Equipo nombrado en reseñas" data-en="Team named in reviews">Team named in reviews</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Brandon</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Tampa Bay area, FL" data-en="Tampa Bay area, FL">Tampa Bay area, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 8. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Floating Shelves"),
    ("Loc Retwist", "Trim &amp; Molding"),
    ("Knotless Braids", "Tile Backsplash"),
    ("K-Tip Extensions", "Tongue-and-Groove Ceilings"),
    ("Keratin", "Custom Cabinetry"),
    ("Orlando, FL", "Brandon, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 9. LA EXPERIENCIA -> ABOUT US
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-6.jpg" alt="Kitchen backsplash and cabinets finished by Jusel Finish Carpentry" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-9.jpg" alt="Floating maple shelves installed beside a kitchen range by Jusel Finish Carpentry" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="About Us" data-en="About Us">About Us</p>')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="A crew that" data-en="A crew that">A crew that</span><br /><span class="text-shine" data-es="shows up and finishes" data-en="shows up and finishes">shows up and finishes</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Jusel Finish Carpentry LLC es un equipo de carpinteria de acabados que trabaja en el area de Brandon y Tampa Bay. Jusel, junto con Diana, cubre desde estantes flotantes a medida y molduras hasta gabinetes de cocina y techos de madera machihembrada." data-en="Jusel Finish Carpentry LLC is a finish carpentry crew working across the Brandon and Tampa Bay area. Jusel, together with Diana, covers everything from custom floating shelves and trim to kitchen cabinets and tongue-and-groove wood ceilings.">Jusel Finish Carpentry LLC is a finish carpentry crew working across the Brandon and Tampa Bay area. Jusel, together with Diana, covers everything from custom floating shelves and trim to kitchen cabinets and tongue-and-groove wood ceilings.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Honesto, confiable y atento a los detalles: asi describen los clientes el trabajo de Jusel en sus reseñas de Google. Ese enfoque sostiene el 5.0 perfecto en 24 reseñas." data-en="Honest, reliable and attentive to detail: that is how clients describe Jusel''s work in their Google reviews. That approach is what holds the perfect 5.0 across 24 reviews.">Honest, reliable and attentive to detail: that is how clients describe Jusel''s work in their Google reviews. That approach is what holds the perfect 5.0 across 24 reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="24">24</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">6-6</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Abierto los 7 dias" data-en="Open 7 days">Open 7 days</p></div>''')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(193,122,61,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
    '''<span class="blur-up loaded w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(193,122,61,0.3)] bg-[rgba(193,122,61,0.1)] text-[color:var(--accent-deep)]">JF</span>
            <span class="text-sm font-light">Jusel &amp; Diana · <span class="text-[color:var(--ink-40)]" data-es="Finish Carpentry" data-en="Finish Carpentry">Finish Carpentry</span></span>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 10. EL METODO -> HOW WE WORK
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="How we work, step by step" data-en="How we work, step by step">How we work, step by step</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="The job," data-en="The job,">The job,</span> <span class="text-shine" data-es="done with care" data-en="done with care">done with care</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call or Request Service" data-en="Call or Request Service">Call or Request Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama al (813) 648-0643 y describe el proyecto, de unos estantes flotantes a un techo completo de madera." data-en="Call (813) 648-0643 and describe the project, from a set of floating shelves to a full wood ceiling.">Call (813) 648-0643 and describe the project, from a set of floating shelves to a full wood ceiling.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="On-Site Look" data-en="On-Site Look">On-Site Look</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Jusel revisa el espacio en persona y propone el acabado que mejor encaja, tal como describen las reseñas de clientes." data-en="Jusel looks at the space in person and proposes the finish that fits best, just like real client reviews describe.">Jusel looks at the space in person and proposes the finish that fits best, just like real client reviews describe.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Honest Craftsmanship" data-en="Honest Craftsmanship">Honest Craftsmanship</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Molduras, estantes, gabinetes o techos, construidos con la atencion al detalle que clientes reales describen como honesta y confiable." data-en="Trim, shelving, cabinetry or ceilings, built with the attention to detail real clients describe as honest and reliable.">Trim, shelving, cabinetry or ceilings, built with the attention to detail real clients describe as honest and reliable.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Done on Time" data-en="Done on Time">Done on Time</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El proyecto se entrega en el plazo acordado, el mismo punto que clientes reales resaltan en sus reseñas de Google." data-en="The project wraps on the timeline agreed, the same point real clients highlight in their Google reviews.">The project wraps on the timeline agreed, the same point real clients highlight in their Google reviews.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 11. SERVICIOS (sin precios publicos)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Finish carpentry," data-en="Finish carpentry,">Finish carpentry,</span> <span class="text-shine" data-es="done right" data-en="done right">done right</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Cada proyecto se cotiza segun el alcance y los materiales. Llama al (813) 648-0643 para un presupuesto." data-en="Every project is quoted based on scope and materials. Call (813) 648-0643 for an estimate.">Every project is quoted based on scope and materials. Call (813) 648-0643 for an estimate.</p>')

NEW_SERVICES_GRID = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(193,122,61,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Custom Floating Shelves" data-en="Custom Floating Shelves">Custom Floating Shelves</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Estantes a medida para laundry, cocina o sala, construidos y montados a la medida exacta del espacio." data-en="Built-to-size shelving for laundry rooms, kitchens and living spaces, built and mounted to the exact fit of the space.">Built-to-size shelving for laundry rooms, kitchens and living spaces, built and mounted to the exact fit of the space.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="{TEL}" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Finishing" data-en="Finishing">Finishing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Trim &amp; Shoe Molding" data-en="Trim &amp; Shoe Molding">Trim &amp; Shoe Molding</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Molduras y remates que terminan un espacio, instalados con precision en cada esquina y union." data-en="Trim and shoe molding that finish a room, installed with precision at every corner and seam.">Trim and shoe molding that finish a room, installed with precision at every corner and seam.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="{TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Kitchens &amp; Baths" data-en="Kitchens &amp; Baths">Kitchens &amp; Baths</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tile Backsplash &amp; Cabinets" data-en="Tile Backsplash &amp; Cabinets">Tile Backsplash &amp; Cabinets</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Instalacion de backsplash y trabajo de gabinetes que transforma una cocina de principio a fin." data-en="Backsplash installation and cabinet work that transforms a kitchen from start to finish.">Backsplash installation and cabinet work that transforms a kitchen from start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="{TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Statement Ceilings" data-en="Statement Ceilings">Statement Ceilings</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tongue-and-Groove Ceilings" data-en="Tongue-and-Groove Ceilings">Tongue-and-Groove Ceilings</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Techos y vigas machihembradas que le dan caracter a una entrada o espacio exterior, mas centros de entretenimiento a medida." data-en="Tongue-and-groove ceilings and beams that give an entryway or outdoor space real character, plus custom entertainment centers.">Tongue-and-groove ceilings and beams that give an entryway or outdoor space real character, plus custom entertainment centers.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for a quote" data-en="Call for a quote">Call for a quote</p></div>
            <a href="{TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
rx(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', NEW_SERVICES_GRID)

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Do not see your project on the list? Call and we will talk it through." data-en="Do not see your project on the list? Call and we will talk it through.">Do not see your project on the list? Call and we will talk it through.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 12. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="work" data-en="work">work</span>')
rx(re.escape(f'<a href="{MAPS_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">') + r'.*?@pure\.artistrysk\s*</a>',
   f'''<a href="{MAPS_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
          <span data-es="See on Google Maps" data-en="See on Google Maps">See on Google Maps</span>
        </a>''')

def _tile(i, img, clases, delay, cap_es, cap_en, alt):
    lazy = '' if i == 0 else ' loading="lazy"'
    return (f'<div class="frame zoomable {clases} img-reveal"{delay}><span class="tile-cap" data-es="{cap_es}" data-en="{cap_en}">{cap_es}</span>'
            f'<img src="assets/raw/{img}" alt="{alt}" class="blur-up w-full h-full object-cover"{lazy} /></div>')

TILES = [
    ("gmaps-6.jpg", "col-span-2 aspect-[16/9]", "", "Kitchen, finished", "Kitchen, finished", "Kitchen with range hood, tile backsplash and cabinets finished by Jusel Finish Carpentry"),
    ("gmaps-1.jpg", "aspect-[3/4]", ' style="transition-delay:90ms"', "Cabinets &amp; lighting", "Cabinets &amp; lighting", "Second kitchen angle with pendant lighting finished by Jusel Finish Carpentry"),
    ("gmaps-3.jpg", "aspect-[3/4]", ' style="transition-delay:150ms"', "Custom closet", "Custom closet", "Walk-in closet with custom shelving and drawers by Jusel Finish Carpentry"),
    ("gmaps-7.jpg", "aspect-[3/4] lg:mt-10", ' style="transition-delay:120ms"', "Floating shelves", "Floating shelves", "Floating corner shelves installed in a laundry room by Jusel Finish Carpentry"),
    ("gmaps-9.jpg", "aspect-[3/4]", ' style="transition-delay:210ms"', "Backsplash &amp; shelves", "Backsplash &amp; shelves", "Tile backsplash with floating maple shelves installed by Jusel Finish Carpentry"),
    ("gmaps-4.jpg", "aspect-[3/4] lg:mt-10", ' style="transition-delay:300ms"', "Outdoor ceiling fan", "Outdoor ceiling fan", "Large outdoor ceiling fan installed in a wood tongue-and-groove ceiling by Jusel Finish Carpentry"),
]
NEW_GALLERY = ('<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">\n        '
    + '\n        '.join(_tile(i, *t) for i, t in enumerate(TILES))
    + '\n      </div>\n    </div>\n  </section>')
rx(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', NEW_GALLERY)
print("GALERIA done")

# ---------------------------------------------------------------------------
# 13. OPINIONES (2 reviews reales; la 3a estaba truncada por Google)
# ---------------------------------------------------------------------------
rep('data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    'data-es="What" data-en="What">What</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 24 reseñas en Google" data-en="5.0 out of 5 · 24 reviews on Google">5.0 out of 5 · 24 reviews on Google</span>')

NEW_REVIEWS = '''<div class="grid sm:grid-cols-2 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Fantastic craftsmanship. Jusel installed shoe molding, made custom, floating shelves for the laundry room and installed a tile backsplash with mural. We are so pleased with his work. Honest, reliable and attention to details. Absolutely, would highly recommend."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Allison</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Jusel and his team are amazing! I love the tongue and groove ceiling and beams he installed in the front our house. He also built a custom outdoor entertainment center for us. I highly recommend Jusel. He is reliable, honest and fair. I will definitely be using him again!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>'''
rx(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10 reveal">)', NEW_REVIEWS)

rx(re.escape(TEL) + r'" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3\.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
   f'{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="See all 24 reviews on Google" data-en="See all 24 reviews on Google">See all 24 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 14. UBICACION -> CONTACT (sin direccion publica: sin mapa, foto en su lugar)
# ---------------------------------------------------------------------------
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>', 'data-es="Contact" data-en="Contact">Contact</p>')
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Brandon</span>')

rx(r'<div>\s*<p class="reveal text-xs tracking-\[0\.35em\] uppercase text-\[color:var\(--accent-deep\)\] mb-5" data-es="Contact" data-en="Contact">Contact</p>.*?</div>\s*</div>\s*</div>\s*<div class="frame map-frame reveal min-h-\[380px\]" style="transition-delay:180ms">.*?</div>\s*</section>',
   f'''<div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Contact" data-en="Contact">Contact</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Brandon</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Phone" data-en="Phone">Phone</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Direct call or text, no middlemen, no forms." data-en="Direct call or text, no middlemen, no forms.">Direct call or text, no middlemen, no forms.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(193,122,61,0.4)]" href="{TEL}">(813) 648-0643</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Open every day, 6AM to 6PM, per the public Google listing." data-en="Open every day, 6AM to 6PM, per the public Google listing.">Open every day, 6AM to 6PM, per the public Google listing.</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Google Listing" data-en="Google Listing">Google Listing</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See the full review history and real client photos on the public Google Business profile." data-en="See the full review history and real client photos on the public Google Business profile.">See the full review history and real client photos on the public Google Business profile.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(193,122,61,0.4)]" href="{MAPS_URL}" target="_blank" rel="noopener" data-es="See Google listing" data-en="See Google listing">See Google listing</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame zoomable img-reveal min-h-[380px] h-full max-h-[560px] lg:max-h-none" style="transition-delay:180ms">
        <img src="assets/raw/gmaps-10.jpg" alt="Entryway flooring finished by Jusel Finish Carpentry" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>
    </div>
  </section>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 15. CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Built in, built right." data-en="Built in, built right.">Built in, built right.</p>')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Your project" data-en="Your project">Your project</span> <span class="text-shine" data-es="starts with a call" data-en="starts with a call">starts with a call</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Llama al (813) 648-0643 y cuentanos el proyecto. Jusel responde con un presupuesto claro, sin compromiso." data-en="Call (813) 648-0643 and tell us about the project. Jusel will come back with a clear estimate, no strings attached.">Call (813) 648-0643 and tell us about the project. Jusel will come back with a clear estimate, no strings attached.</p>')
rx(re.escape(TEL) + r'" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
   f'{TEL}" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (813) 648-0643" data-en="Call (813) 648-0643">Call (813) 648-0643</a>')
rx(re.escape(MAPS_URL) + r'" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
   f'{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="See on Google Maps" data-en="See on Google Maps">See on Google Maps</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 16. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Jusel Finish Carpentry</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(224,176,126,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>''',
    '''<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(224,176,126,0.35)] bg-[rgba(224,176,126,0.12)]">JF</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">Jusel Finish Carpentry</span>''')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.',
    'data-es="Finish carpentry serving Brandon and the Tampa Bay area, FL." data-en="Finish carpentry serving Brandon and the Tampa Bay area, FL.">Finish carpentry serving Brandon and the Tampa Bay area, FL.')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>Brandon, FL &amp; Tampa Bay area</p>')
rx(re.escape(TEL) + r'" target="_blank" rel="noopener" class="hover:text-\[#e3b98f\]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a>',
   f'{TEL}" class="hover:text-[#e3b98f]" data-es="Call · (813) 648-0643" data-en="Call · (813) 648-0643">Call · (813) 648-0643</a>')
rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Listing" data-en="Listing">Listing</p>')
rx(re.escape(MAPS_URL) + r'" target="_blank" rel="noopener" class="hover:text-\[#e3b98f\]">Instagram · @pure\.artistrysk</a>',
   f'{MAPS_URL}" target="_blank" rel="noopener" class="hover:text-[#e3b98f]">Google Maps · 5.0 (24)</a>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Jusel Finish Carpentry LLC.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 17. Boton flotante: de reserva a llamada
# ---------------------------------------------------------------------------
rx(re.escape(TEL) + r'" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">.*?<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>\s*</a>',
   f'''{TEL}" class="book-float" aria-label="Call Jusel Finish Carpentry">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>
    <span class="book-float-label" data-es="Call Now" data-en="Call Now">Call Now</span>
  </a>''')
print("BOOK-FLOAT done")

open(PATH, 'w', encoding='utf-8').write(h)
print(f'{SLUG}: derivacion completa ->', PATH)
