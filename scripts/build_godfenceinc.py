#!/usr/bin/env python3
"""Derivacion anclada: templates/light-v2 -> output/god-fence-inc.

GOD FENCE INC, Hialeah/North Miami area FL. Fence and gate installation.
Datos VERIFICADOS (2026-10-28) via Google Maps (scripts/maps_discover.py +
maps_research.py), nada inventado:
- Nombre: "God Fence Inc" (titulo de la ficha de Google Maps)
- Direccion real: 3789 W 18th Ave, Hialeah, FL 33012
- Telefono real: +1 786-216-4089
- Rating 5.0, 154 reviews en Google (ficha publica)
- Horarios reales: Lun-Sab 8AM-8PM, Domingo cerrado
- SIN website propio: verificado con maps_discover.py (ficha sin boton de website) +
  WebSearch ("God Fence Inc" Hialeah/Miami Florida instagram/facebook/email) sin resultados
- SIN Instagram/Facebook/email publico encontrado -> outreach pending_manual (solo telefono)
- Servicios reales inferidos de 3 reviews verbatim de Google + fotos propias de la ficha:
  aluminum privacy fencing (horizontal slat), PVC/vinyl gates (double gate, keypad lock),
  vertical aluminum fencing con remates festoneados, mailbox posts a juego.
  Tecnico nombrado en una resena (Nora, truncada por Google): Osmany.
- 2 reviews verbatim completas usables (Sandalio Carmona, Sulay Mengana). La tercera
  (Nora) esta truncada por Google con "..." a media frase: se omite como cita pero su
  dato (el nombre "Osmany") se usa en el copy de Nosotros, ya que es visible sin truncar.
- SIN precios publicos -> cards de servicio sin precio ("Call for a quote")

Paleta: steel/graphite (acero), distinta de terracota (miami-painting-florida) y de las
paletas de belleza ya usadas en el registro (coral, caramelo, esmeralda, teal, violeta,
rosa, gold).
"""
import re

SLUG = "god-fence-inc"
PATH = f"output/{SLUG}/index.html"
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


TEL = "tel:+17862164089"
MAPS_URL = "https://www.google.com/maps/place/God+Fence+Inc/data=!4m7!3m6!1s0x88d9bbb0d1d9f841:0xe08756139270f602!8m2!3d25.85619!4d-80.3183983!16s%2Fg%2F11r97d7f4v!19sChIJQfjZ0bC72YgRAvZwkhNWh-A?authuser=0&hl=en&g_ep=EgoyMDI2MTAyMC4wIJJjKgBIAVAD&rclk=1"
MAPS_EMBED = "https://www.google.com/maps?q=3789+W+18th+Ave,+Hialeah,+FL+33012&output=embed"
MAPS_DIR = "https://www.google.com/maps?q=3789+W+18th+Ave,+Hialeah,+FL+33012"

# ---------------------------------------------------------------------------
# 1. Paleta: plum-pink (lashbloom) -> steel/graphite (God Fence Inc)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#3a4750"),
    ("#5c2140", "#1c2529"),
    ("#f0bed7", "#b8c4c8"),
    ("#faf2f6", "#f3f4f2"),
    ("#c47a9c", "#6b8089"),
    ("#8a5573", "#445257"),
    ("#f3e0ea", "#e4e7e6"),
    ("#d9a8c2", "#93a8ac"),
    ("#7d3457", "#4a5a60"),
    ("#5f2c48", "#2e383c"),
    ("#33222c", "#262f33"),
    ("#fbf3f8", "#f4f6f5"),
    ("#fbeff5", "#eef1f0"),
    ("#f8dfeb", "#c7d2d4"),
    ("#f6f1ea", "#eef0ee"),
    ("#f2d5e3", "#c3cdd0"),
    ("#f2cfe0", "#bcc9cc"),
    ("#efd0e0", "#d7dedf"),
    ("#e5c1d4", "#a9b8bb"),
    ("#dc9dbe", "#90a3a8"),
    ("#d3a2bc", "#9fb0b4"),
    ("#c9789f", "#5c6f74"),
    ("#b25a85", "#475458"),
    ("#2a1722", "#151c1e"),
    ("#1f0f18", "#0e1314"),
    ("#1c0f16", "#0d1213"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(58,71,80"),
    ("rgba(51,34,44", "rgba(38,47,51"),
    ("rgba(240,190,215", "rgba(184,196,200"),
    ("rgba(70,25,50", "rgba(28,37,41"),
    ("rgba(250,242,246", "rgba(243,244,242"),
    ("rgba(125,52,87", "rgba(74,90,96"),
    ("rgba(253,246,250", "rgba(244,246,245"),
    ("rgba(40,16,30", "rgba(21,28,30"),
    ("rgba(233,205,186", "rgba(184,196,200"),
    ("rgba(185,138,128", "rgba(68,82,87"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 2. GLOBALES: sin booking, sin IG -> tel: en todos lados
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c >= 8, c
h = h.replace(OLD_BOOK, TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, MAPS_URL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 3. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>God Fence Inc · Fence &amp; Gate Installation in Hialeah, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="God Fence Inc, Hialeah FL: aluminum privacy fencing, PVC and vinyl gates, and custom gates with keypad locks. 5.0 stars across 154 Google reviews. Call (786) 216-4089." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="God Fence Inc · Fence &amp; Gate Installation in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Aluminum privacy fencing, PVC/vinyl gates and keypad gate locks. 5.0 on Google. Call (786) 216-4089." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-9.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-9.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "God Fence Inc",
    "description": "Fence and gate installation contractor serving Hialeah and the Miami-Dade, FL area: aluminum privacy fencing, PVC and vinyl gates, and custom gates with keypad locks.",
    "address": { "@type": "PostalAddress", "streetAddress": "3789 W 18th Ave", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33012", "addressCountry": "US" },
    "areaServed": "Miami-Dade County, FL",
    "telephone": "+1-786-216-4089",
    "image": "assets/raw/gmaps-9.jpg",
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "08:00", "closes": "20:00" }
    ],
    "sameAs": ["''' + MAPS_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "154", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Fence &amp; gate services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Aluminum Privacy Fencing" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "PVC &amp; Vinyl Gates" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Custom Gates with Keypad Locks" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Mailbox Posts &amp; Finishing" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 4. Idioma: negocio EN -> se queda en EN (default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 5. NAV (sin logo real -> monograma GF)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(58,71,80,0.35)]" />',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(58,71,80,0.35)] bg-[rgba(58,71,80,0.1)] text-[color:var(--accent-deep)]">GF</span>')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-base sm:text-xl tracking-[0.04em] sm:tracking-[0.1em] uppercase whitespace-nowrap">God <span class="text-[color:var(--accent-deep)]">Fence Inc</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">GF</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">God Fence Inc</span>')
print("NAV done")

for old, new in [
    ('data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
     'data-es="Nosotros" data-en="About Us">About Us</a>'),
    ('data-es="El Método" data-en="The Method">El Método</a>',
     'data-es="Cómo Trabajamos" data-en="How We Work">How We Work</a>'),
    ('data-es="Servicios" data-en="Services">Servicios</a>',
     'data-es="Servicios" data-en="Services">Services</a>'),
    ('data-es="Galería" data-en="Gallery">Galería</a>',
     'data-es="Galería" data-en="Gallery">Gallery</a>'),
    ('data-es="Opiniones" data-en="Reviews">Opiniones</a>',
     'data-es="Opiniones" data-en="Reviews">Reviews</a>'),
    ('data-es="Ubicación" data-en="Location">Ubicación</a>',
     'data-es="Contacto" data-en="Contact">Contact</a>'),
]:
    rep_all(old, new, expect=2)
print("NAV LINKS done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar Ahora" data-en="Call Now">Call Now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar Ahora" data-en="Call Now">Call Now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 6. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Fence &amp; Gate Installation" data-en="Hialeah, FL · Fence &amp; Gate Installation">Hialeah, FL · Fence &amp; Gate Installation</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Built to last, installed right." data-en="Built to last, installed right.">Built to last, installed right.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Your fence," data-en="Your fence,">Your fence,</span><br /><span data-es="installed by " data-en="installed by ">installed by </span><span class="text-shine" data-es="God Fence" data-en="God Fence">God Fence</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="God Fence Inc instala cercas de privacidad en aluminio, portones de PVC y vinil, y portones personalizados con cerradura de teclado en Hialeah y el area de Miami-Dade. Un 5.0 perfecto en 154 reseñas de Google, con Osmany y el equipo haciendo el trabajo en sitio." data-en="God Fence Inc installs aluminum privacy fencing, PVC and vinyl gates, and custom gates with keypad locks across Hialeah and the Miami-Dade area. A perfect 5.0 across 154 Google reviews, with Osmany and the crew doing the work on site.">God Fence Inc installs aluminum privacy fencing, PVC and vinyl gates, and custom gates with keypad locks across Hialeah and the Miami-Dade area. A perfect 5.0 across 154 Google reviews, with Osmany and the crew doing the work on site.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 154 reseñas en Google" data-en="5.0 · 154 reviews on Google">5.0 · 154 reviews on Google</span>')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>\n            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>\n          </a>\n          <a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n            @_lashbloom\n          </a>',
    '<a href="' + TEL + '" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n            <span data-es="Call (786) 216-4089" data-en="Call (786) 216-4089">Call (786) 216-4089</span>\n            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>\n          </a>\n          <a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">\n            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>\n            <span data-es="Google Maps" data-en="Google Maps">Google Maps</span>\n          </a>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-9.jpg" alt="Black vertical-slat aluminum fence and gate with keypad lock installed by God Fence Inc" class="blur-up w-full h-full object-cover" />')
rep('<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Volume Full Set</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Direct Line" data-en="Direct Line">Direct Line</p>\n            <p class="font-display text-lg">(786) 216-4089</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Hialeah, FL" data-en="Hialeah, FL">Hialeah, FL</p>')
print("HERO done")

# ---------------------------------------------------------------------------
# 7. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="154">154</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fence <span class="text-shine">&amp;</span> Gates</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Aluminio · PVC · Vinil" data-en="Aluminum · PVC · Vinyl">Aluminum · PVC · Vinyl</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Osmany <span class="text-shine">&amp;</span> Crew</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Equipo nombrado en las reseñas" data-en="Crew named in the reviews">Crew named in the reviews</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Miami-Dade County, FL" data-en="Miami-Dade County, FL">Miami-Dade County, FL</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 8. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Aluminum Privacy Fencing"),
    ("Hybrid Set", "PVC Gates"),
    ("Volume Set", "Vinyl Fencing"),
    ("Mega Volume", "Keypad Gate Locks"),
    ("Bottom Lashes", "Custom Gates"),
    ("West Palm Beach, FL", "Hialeah, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 9. LA EXPERIENCIA (Nosotros)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-4.jpg" alt="Osmany and the God Fence Inc crew next to a finished white aluminum gate" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-3.jpg" alt="God Fence Inc crew installing a gate on site in Hialeah" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="Nosotros" data-en="About Us">About Us</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="A crew that" data-en="A crew that">A crew that</span><br /><span class="text-shine" data-es="shows up and finishes" data-en="shows up and finishes">shows up and finishes</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="God Fence Inc instala cercas y portones en Hialeah y el area de Miami-Dade. Osmany, el instalador que los clientes nombran directamente en sus reseñas, y su equipo se encargan de todo, desde un solo portón hasta la línea completa de la propiedad." data-en="God Fence Inc installs fencing and gates across Hialeah and the Miami-Dade area. Osmany, the installer clients name directly in their reviews, and his crew handle everything from a single gate to a full property fence line.">God Fence Inc installs fencing and gates across Hialeah and the Miami-Dade area. Osmany, the installer clients name directly in their reviews, and his crew handle everything from a single gate to a full property fence line.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Los clientes destacan un acabado limpio y profesional, y un equipo que cumple el plazo aunque el trabajo se complique en el camino. Ese enfoque es lo que mantiene a God Fence Inc en un 5.0 perfecto en 154 reseñas de Google." data-en="Clients highlight a clean, professional finish and a crew that stays on schedule even when a job runs into surprises along the way. That focus is what keeps God Fence Inc at a perfect 5.0 across 154 Google reviews.">Clients highlight a clean, professional finish and a crew that stays on schedule even when a job runs into surprises along the way. That focus is what keeps God Fence Inc at a perfect 5.0 across 154 Google reviews.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="154">154</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>\n          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="1 Día" data-en="1 Day">1 Day</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Instalación típica" data-en="Typical install">Typical install</p></div>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(58,71,80,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="blur-up loaded w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(58,71,80,0.3)] bg-[rgba(58,71,80,0.1)] text-[color:var(--accent-deep)]">GF</span>\n            <span class="text-sm font-light">Osmany &amp; Crew · <span class="text-[color:var(--ink-40)]" data-es="Instaladores de cercas" data-en="Fence installers">Fence installers</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 10. EL METODO -> COMO TRABAJAMOS
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Cómo trabajamos, paso a paso" data-en="How we work, step by step">How we work, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="The job," data-en="The job,">The job,</span> <span class="text-shine" data-es="done right" data-en="done right">done right</span>')
rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Llama o pide servicio" data-en="Call or Request Service">Call or Request Service</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama al (786) 216-4089 y describe el proyecto, de un solo portón a una línea de cerca completa." data-en="Call (786) 216-4089 and describe the project, from a single gate to a full fence line.">Call (786) 216-4089 and describe the project, from a single gate to a full fence line.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Evaluación en el sitio" data-en="On-Site Evaluation">On-Site Evaluation</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El equipo mide la propiedad y revisa opciones de material: aluminio, PVC o vinil, además de herrajes como cerraduras de teclado." data-en="The crew measures the property and goes over material options: aluminum, PVC or vinyl, plus hardware like keypad locks.">The crew measures the property and goes over material options: aluminum, PVC or vinyl, plus hardware like keypad locks.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Instalación" data-en="Installation">Installation</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Postes, paneles y portones se instalan con el acabado limpio y profesional que describen las reseñas de clientes." data-en="Posts, panels and gates go in with the clean, professional finish clients describe in their reviews.">Posts, panels and gates go in with the clean, professional finish clients describe in their reviews.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Revisión final" data-en="Walkthrough &amp; Finish">Walkthrough &amp; Finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El equipo recorre contigo la cerca terminada antes de cerrar el trabajo, muchas veces en un solo día." data-en="The crew walks the finished fence line with you before wrapping up, often completing the job in a single day.">The crew walks the finished fence line with you before wrapping up, often completing the job in a single day.</p>')
print("METODO done")

# ---------------------------------------------------------------------------
# 11. SERVICIOS (sin precios publicos)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Fencing &amp; gates" data-en="Fencing &amp; gates">Fencing &amp; gates</span> <span class="text-shine" data-es="done right" data-en="done right">done right</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Cada instalación se cotiza según los pies lineales y el material. Llama al (786) 216-4089 para un presupuesto." data-en="Every job is quoted based on linear footage and material. Call (786) 216-4089 for an estimate.">Every job is quoted based on linear footage and material. Call (786) 216-4089 for an estimate.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(58,71,80,0.4); box-shadow: 0 18px 50px rgba(38,47,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cerca de privacidad en aluminio" data-en="Aluminum Privacy Fencing">Aluminum Privacy Fencing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cerca de aluminio con paneles horizontales que resiste el clima de Florida, instalada en linderos y patios laterales." data-en="Horizontal-slat aluminum privacy fencing that holds up to Florida weather, installed along property lines and side yards.">Horizontal-slat aluminum privacy fencing that holds up to Florida weather, installed along property lines and side yards.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Se cotiza, llámanos" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Portones" data-en="Gates">Gates</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Portones de PVC y vinil" data-en="PVC &amp; Vinyl Gates">PVC &amp; Vinyl Gates</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Portones dobles y sencillos de PVC o vinil, construidos panel por panel para igualar el resto de la cerca." data-en="Double and single PVC/vinyl gates, built panel by panel to match the rest of the fence line.">Double and single PVC/vinyl gates, built panel by panel to match the rest of the fence line.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Se cotiza, llámanos" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Seguridad" data-en="Security">Security</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Portones con cerradura de teclado" data-en="Custom Gates with Keypad Locks">Custom Gates with Keypad Locks</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Portones equipados con cerradura electrónica de teclado para acceso controlado sin llave física." data-en="Gates fitted with electronic keypad locks for controlled access without a physical key.">Gates fitted with electronic keypad locks for controlled access without a physical key.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Se cotiza, llámanos" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Detalles" data-en="Detail work">Detail work</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Postes de buzón y remates" data-en="Mailbox Posts &amp; Finishing">Mailbox Posts &amp; Finishing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Postes de buzón a juego y detalles finales que amarran toda la instalación." data-en="Matching mailbox posts and finishing touches that tie the whole installation together.">Matching mailbox posts and finishing touches that tie the whole installation together.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Se cotiza, llámanos" data-en="Call for a quote">Call for a quote</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="¿No ves tu proyecto en la lista? Llama y lo describimos juntos." data-en="Do not see your project on the list? Call and we will talk it through.">Do not see your project on the list? Call and we will talk it through.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 12. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="fences">fences</span>')
rep('<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n          @_lashbloom\n        </a>',
    '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>\n          <span data-es="Ver en Google Maps" data-en="See on Google Maps">See on Google Maps</span>\n        </a>')
TILES = [
    ('gmaps-2.jpg', 'col-span-2 aspect-[16/9]', '', 'Double gate, finished', 'Double gate, finished', 'Finished white PVC double gate with keypad lock installed by God Fence Inc'),
    ('gmaps-5.jpg', 'aspect-[3/4]', ' style="transition-delay:90ms"', 'Privacy fencing', 'Privacy fencing', 'Gray aluminum horizontal privacy fence along a Hialeah home'),
    ('gmaps-7.jpg', 'aspect-[3/4]', ' style="transition-delay:150ms"', 'Scalloped fence line', 'Scalloped fence line', 'Scalloped-top vertical fence panel installed by God Fence Inc'),
    ('gmaps-6.jpg', 'aspect-[3/4] lg:mt-10', ' style="transition-delay:120ms"', 'Front yard fence', 'Front yard fence', 'Light gray aluminum fence along a home front yard'),
    ('gmaps-8.jpg', 'aspect-[3/4]', ' style="transition-delay:210ms"', 'Mailbox post', 'Mailbox post', 'Matching white mailbox post built by God Fence Inc'),
]
rx = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
m2 = rx.search(h)
assert m2, "gallery grid not found"


def _tile(i, img, clases, delay, cap_es, cap_en, alt):
    lazy = '' if i == 0 else ' loading="lazy"'
    return (f'<div class="frame zoomable {clases} img-reveal"{delay}><span class="tile-cap" data-es="{cap_es}" data-en="{cap_en}">{cap_es}</span>'
            f'<img src="assets/raw/{img}" alt="{alt}" class="blur-up w-full h-full object-cover"{lazy} /></div>')


NEW_GALLERY = ('<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">\n        '
    + '\n        '.join(_tile(i, *tile) for i, tile in enumerate(TILES))
    + '\n      </div>\n    </div>\n  </section>')
h = h[:m2.start()] + NEW_GALLERY + h[m2.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 13. OPINIONES (2 reviews reales verbatim completas; una 3a -Nora- estaba
#     truncada por Google y se omite como cita, solo se usa su dato del
#     nombre del instalador en la seccion Nosotros)
# ---------------------------------------------------------------------------
rep('data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    'data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span>')
rep('<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 154 reseñas en Google" data-en="5.0 out of 5 · 154 reviews on Google">5.0 out of 5 · 154 reviews on Google</span>')

reviews_re = re.compile(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10 reveal">)', flags=re.S)
m3 = reviews_re.search(h)
assert m3, "reviews grid not found"
NEW_REVIEWS = '''<div class="grid sm:grid-cols-2 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great experience! God Fence Inc did an amazing job on my fence. The work came out beautiful, clean, and professional. Highly recommend them to anyone looking for quality fence installation!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sandalio</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Super happy with my new front fence from God Fence Inc! The whole process was smooth, and the crew was very friendly and efficient. They ran into a couple of challenges but still managed to finish everything in just one day. You can tell they really care about their work. Highly recommend!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sulay</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>'''
h = h[:m3.start()] + NEW_REVIEWS + h[m3.end():]

rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver las 154 reseñas en Google" data-en="See all 154 reviews on Google">See all 154 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 14. UBICACION (direccion real -> mapa real)
# ---------------------------------------------------------------------------
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>', 'data-es="Contacto" data-en="Contact">Contact</p>')
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Serving" data-en="Serving">Serving</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">3789 W 18th Ave, Hialeah, FL 33012</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    'href="' + MAPS_DIR + '" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>')
rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(58,71,80,0.4)]" href="''' + TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Telefono" data-en="Phone">Phone</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Llamada o mensaje de texto directo, sin intermediarios ni formularios." data-en="Direct call or text, no middlemen, no forms.">Direct call or text, no middlemen, no forms.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(58,71,80,0.4)]" href="''' + TEL + '''">(786) 216-4089</a>
            </div>
          </div>''')
rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(58,71,80,0.4)]" href="''' + MAPS_URL + '''" target="_blank" rel="noopener">@_lashbloom</a>
            </div>
          </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sabado 8AM a 8PM, domingo cerrado, segun la ficha publica de Google." data-en="Monday to Saturday 8AM to 8PM, Sunday closed, per the public Google listing.">Monday to Saturday 8AM to 8PM, Sunday closed, per the public Google listing.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(58,71,80,0.4)]" href="''' + MAPS_URL + '''" target="_blank" rel="noopener" data-es="Ver ficha en Google" data-en="See Google listing">See Google listing</a>
            </div>
          </div>''')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="' + MAPS_EMBED + '"')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: God Fence Inc, 3789 W 18th Ave, Hialeah FL"')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 15. CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Built to last, installed right." data-en="Built to last, installed right.">Built to last, installed right.</p>')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Your fence" data-en="Your fence">Your fence</span> <span class="text-shine" data-es="starts with a call" data-en="starts with a call">starts with a call</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Llama al (786) 216-4089 y cuentale al equipo lo que necesitas, de un solo portón a una línea de cerca completa. Osmany y el equipo responden con un plan claro." data-en="Call (786) 216-4089 and tell the crew what you need, from a single gate to a full fence line. Osmany and the team will come back with a clear plan.">Call (786) 216-4089 and tell the crew what you need, from a single gate to a full fence line. Osmany and the team will come back with a clear plan.</p>')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + TEL + '" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar (786) 216-4089" data-en="Call (786) 216-4089">Call (786) 216-4089</a>')
rep('<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Ver en Google Maps" data-en="See on Google Maps">See on Google Maps</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 16. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">God Fence</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(184,196,200,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(184,196,200,0.35)] bg-[rgba(184,196,200,0.12)]">GF</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">God Fence Inc</span>''')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.',
    'data-es="Instalación de cercas y portones en Hialeah, FL." data-en="Fence and gate installation in Hialeah, FL.">Fence and gate installation in Hialeah, FL.')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>3789 W 18th Ave, Hialeah, FL 33012</p>')
rep('<p><a href="' + TEL + '" target="_blank" rel="noopener" class="hover:text-[#b8c4c8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + TEL + '" class="hover:text-[#b8c4c8]" data-es="Llamar · (786) 216-4089" data-en="Call · (786) 216-4089">Call · (786) 216-4089</a></p>')
rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n        <p><a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="hover:text-[#b8c4c8]">Instagram · @_lashbloom</a></p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Ficha" data-en="Listing">Listing</p>\n        <p><a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="hover:text-[#b8c4c8]">Google Maps · 5.0 (154)</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 God Fence Inc.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 17. Boton flotante: de calendario a llamada
# ---------------------------------------------------------------------------
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f3f4f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
    '<a href="' + TEL + '" class="book-float" aria-label="Call God Fence Inc">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f3f4f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>\n  </a>')
print("BOOK-FLOAT done")

open(PATH, 'w', encoding='utf-8').write(h)
print(f'{SLUG}: derivacion completa ->', PATH)
