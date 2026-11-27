import re
import shutil

SLUG = "johncopperpainting-tallahassee"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/light/index.html", PATH)
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f"NO ANCHOR (found {c}, need {n}): " + a[:200]
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


TEL = "tel:+18503398575"
SMS = "sms:+18503398575"
MAPS_URL = ("https://www.google.com/maps/place/John+copper+painting/data="
            "!4m7!3m6!1s0x88ec4370c88d2305:0x33f0f46c815e859c!8m2!3d30.4507802!4d-84.088806"
            "!16s%2Fg%2F11s8m8rzsw!19sChIJBSONyHBD7IgRnIVegWz08DM"
            "?authuser=0&hl=en&g_ep=EgoyMDI2MTEyMy4wIJJjKgBIAVAD&rclk=1")

# ---------------------------------------------------------------------------
# 0. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 1. Paleta: mocha/gold (Amani) -> "copper" (terracotta/clay) - juego con el
#    nombre "Copper" del negocio, sobre base crema calida.
# ---------------------------------------------------------------------------
NEW_BG = "#f6f1e8"
NEW_BG2 = "#ece1d0"
NEW_INK = "#2e2420"
NEW_ACCENT_DEEP = "#9c4a30"
NEW_ACCENT_MID = "#c17a52"

HEX_PALETTE = [
    ("#f5f0e8", NEW_BG),
    ("#ece3d4", NEW_BG2),
    ("#32281f", NEW_INK),
    ("#8a6f4d", NEW_ACCENT_DEEP),
    ("#a8907a", NEW_ACCENT_MID),
    ("#b0916a", "#c98a63"),
    ("#5b473a", "#5a2e1d"),
    ("#a8845a", "#b8714a"),
    ("#e2d4bd", "#e8c9a8"),
    ("#c4ad93", "#d1946a"),
    ("#d3c1a6", "#e0b48c"),
    ("#6d5539", "#6b3220"),
    ("#4a3a26", "#4a2415"),
    ("#e8cfa6", "#e8b89a"),
    ("#f8ecd6", "#f8e3d6"),
    ("#c9ab7f", "#d9a77e"),
    ("#faf3e6", "#faf0e6"),
    ("#e8d9bf", "#e8cdb0"),
    ("#c9b393", "#c9a383"),
    ("#8a7358", "#8a6a4e"),
    ("#f3e3c2", "#f3d9c2"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(138,111,77", rgbstr(NEW_ACCENT_DEEP)),
    ("rgba(50,40,31", rgbstr(NEW_INK)),
    ("rgba(250,247,241", "rgba(250,245,237"),
    ("rgba(245,240,232", rgbstr(NEW_BG)),
    ("rgba(60,45,28", "rgba(74,36,21"),
    ("rgba(232,207,166", "rgba(232,184,154"),
    ("rgba(168,144,122", "rgba(180,140,110"),
    ("rgba(234,214,183", "rgba(232,184,154"),
    ("rgba(120,90,50", "rgba(138,100,70"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 2. Idioma: negocio EN -> default English, toggle muestra ES
# ---------------------------------------------------------------------------
rep('<html lang="es" class="scroll-smooth">', '<html lang="en" class="scroll-smooth">')
print("LANG done")

# ---------------------------------------------------------------------------
# 3. HEAD: title, meta, og, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Amani HeadSpa · Head Spa Holístico en Flagami, Miami | Rituales de bienestar para ti o en pareja</title>',
    '<title>John Copper Painting · Residential Painting in Tallahassee, FL | Free Estimates</title>')
rep('<meta name="description" content="Amani HeadSpa, Miami\'s Holistic Head Spa en Flagami. The Unwinding: rituales de 60 a 90 minutos con limpieza del cuero cabelludo, masaje terapéutico, mascarilla personalizada y piedras calientes. 4.9 en Google. Reserva online." />',
    '<meta name="description" content="John Copper Painting, Tallahassee FL: exterior &amp; interior painting, deck staining, cabinet refinishing and door restoration. 5.0 rating on Google. Call or text (850) 339-8575 for a free estimate." />')
rep('<meta property="og:title" content="Amani HeadSpa · Head Spa Holístico en Flagami, Miami" />',
    '<meta property="og:title" content="John Copper Painting · Residential Painting in Tallahassee, FL" />')
rep('<meta property="og:description" content="Rituales de bienestar para individuales y parejas. The Unwinding | 90min: $185. Reserva tu cita online." />',
    '<meta property="og:description" content="Exterior &amp; interior painting, deck staining, cabinet refinishing and door restoration. Free, honest estimates." />')
rep('<meta property="og:image" content="assets/raw/hero-1.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-1.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "John Copper Painting",
    "description": "Residential painting and refinishing company based in Tallahassee, FL: exterior and interior painting, deck and wood staining, cabinet refinishing and door restoration.",
    "telephone": "+1-850-339-8575",
    "address": { "@type": "PostalAddress", "streetAddress": "11371 Gordon St", "addressLocality": "Tallahassee", "addressRegion": "FL", "postalCode": "32317", "addressCountry": "US" },
    "areaServed": { "@type": "City", "name": "Tallahassee" },
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "11", "bestRating": "5" },
    "hasOfferCatalog": {
      "@type": "OfferCatalog",
      "name": "Painting and refinishing services",
      "itemListElement": [
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Exterior & Interior Painting" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Deck & Wood Staining" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cabinet Refinishing" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Door & Trim Restoration" } }
      ]
    }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
rep('<meta name="theme-color" content="#f5f0e8" />'.replace("#f5f0e8", NEW_BG),
    '<meta name="theme-color" content="' + NEW_BG + '" />')
print("HEAD done")

# ---------------------------------------------------------------------------
# 4. NAV
# ---------------------------------------------------------------------------
rep('<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-xl ring-1 ring-[rgba(138,111,77,0.35)] bg-[rgba(138,111,77,0.1)] text-[color:var(--accent-deep)]">A</span>'
    .replace("rgba(138,111,77", rgbstr(NEW_ACCENT_DEEP)),
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-xl ring-1 ring-[rgba(156,74,48,0.35)] bg-[rgba(156,74,48,0.1)] text-[color:var(--accent-deep)]">JC</span>')
rep('<span class="font-display text-xl tracking-[0.14em] uppercase">Amani <span class="text-[color:var(--ink-60)] text-sm font-sans font-light tracking-[0.2em] uppercase ml-1">HeadSpa</span></span>',
    '<span class="font-display text-xl tracking-[0.14em] uppercase">John Copper <span class="text-[color:var(--ink-60)] text-sm font-sans font-light tracking-[0.2em] uppercase ml-1">Painting</span></span>')
rep_all('<a class="nav-link" href="#experiencia">La Experiencia</a>',
        '<a class="nav-link" href="#experiencia" data-es="Nosotros" data-en="About">About</a>')
rep_all('<a class="nav-link" href="#ritual">El Ritual</a>',
        '<a class="nav-link" href="#metodo" data-es="Cómo Trabajamos" data-en="How We Work">How We Work</a>')
rep_all('<a class="nav-link" href="#servicios">Servicios</a>',
        '<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Services</a>')
rep_all('<a class="nav-link" href="#galeria">Galería</a>',
        '<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>')
rep_all('<a class="nav-link" href="#opiniones">Opiniones</a>',
        '<a class="nav-link" href="#opiniones" data-es="Reseñas" data-en="Reviews">Reviews</a>')
rep_all('<a class="nav-link" href="#ubicacion">Ubicación</a>',
        '<a class="nav-link" href="#ubicacion" data-es="Zona de Servicio" data-en="Service Area">Service Area</a>')
print("NAV LINKS done")

rep('''<a href="https://amaniheadspa.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          Reservar cita
        </a>
        <button id="menuBtn" class="md:hidden w-10 h-10 flex flex-col items-center justify-center gap-[5px]" aria-label="Abrir menú">''',
    '''<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Change language">ES</button>
        <a href="''' + TEL + '''" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span data-es="Llamar Ahora" data-en="Call Now">Call Now</span>
        </a>
        <button id="menuBtn" class="md:hidden w-10 h-10 flex flex-col items-center justify-center gap-[5px]" aria-label="Open menu">''')
print("NAV CTA done")

rep_all('''<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia">La Experiencia</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#ritual">El Ritual</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios">Servicios</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria">Galería</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones">Opiniones</a>
        <a class="py-3 px-3" href="#ubicacion">Ubicación</a>
        <a href="https://amaniheadspa.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2">Reservar cita</a>''',
    '''<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="Nosotros" data-en="About">About</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="Cómo Trabajamos" data-en="How We Work">How We Work</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Reseñas" data-en="Reviews">Reviews</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Zona de Servicio" data-en="Service Area">Service Area</a>
        <a href="''' + TEL + '''" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar Ahora" data-en="Call Now">Call Now</a>''')
print("MOBILE NAV done")

# ---------------------------------------------------------------------------
# 5. HERO
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6">Flagami · Miami\'s Holistic Head Spa</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Tallahassee, FL · Pintura Residencial" data-en="Tallahassee, FL · Residential Painting">Tallahassee, FL · Residential Painting</p>')
rep('<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms">The Unwinding empieza aquí.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pintura precisa, acabado de confianza." data-en="Precision painting, trusted finish.">Precision painting, trusted finish.</p>')
rep('''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          Suelta el estrés,<br /><span class="text-shine">renueva</span> cuerpo y mente
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pintura precisa," data-en="Precision paint,">Precision paint,</span><br /><span data-es="acabados que " data-en="finishes that ">finishes that </span><span class="text-shine" data-es="perduran" data-en="last">last</span>
        </h1>''')
rep('''<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms">
          Rituales de bienestar holístico en Flagami: limpieza profunda del cuero cabelludo, masaje terapéutico, mascarilla capilar personalizada y terapia de piedras calientes. Para ti, o en pareja.
        </p>''',
    '''<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="John Copper Painting aplica ojo de artesano en cada trabajo en Tallahassee: pintura interior y exterior, teñido de madera y terrazas, repintado de gabinetes y restauración de puertas. Preparación cuidadosa, precios honestos y un acabado hecho para durar." data-en="John Copper Painting brings a craftsman's eye to every job in Tallahassee: exterior and interior painting, deck and wood staining, cabinet refinishing and door restoration. Careful prep, honest pricing, and a finish built to last.">John Copper Painting brings a craftsman's eye to every job in Tallahassee: exterior and interior painting, deck and wood staining, cabinet refinishing and door restoration. Careful prep, honest pricing, and a finish built to last.</p>''')
rep('<span class="text-sm text-[color:var(--ink-60)]">4.9 · 73 reseñas en Google</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 11 reseñas en Google" data-en="5.0 · 11 reviews on Google">5.0 · 11 reviews on Google</span>')
rep('''<a href="https://amaniheadspa.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            Reservar cita
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="tel:+13057906977" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            (305) 790-6977
          </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar (850) 339-8575" data-en="Call (850) 339-8575">Call (850) 339-8575</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + SMS + '''" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <span data-es="Enviar Mensaje" data-en="Text for a Quote">Text for a Quote</span>
          </a>''')
rep('<img src="assets/raw/hero-1.jpg" alt="Aplicación de mascarilla facial con brocha durante un ritual en Amani HeadSpa" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="Painted deck addition on a Tallahassee home by John Copper Painting" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1">Ritual insignia</p>
            <p class="font-display text-lg">The Unwinding | 90min</p>
            <p class="text-sm text-[color:var(--ink-60)]">90 minutos · $185</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Cotizaciones" data-en="Estimates">Estimates</p>
            <p class="font-display text-lg" data-es="Gratis y honestas" data-en="Free &amp; honest">Free &amp; honest</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Llama o escribe cuando quieras" data-en="Call or text anytime">Call or text anytime</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 6. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('''<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="73">73</span> reseñas en Google</p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Rituales <span class="text-shine">en pareja</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Sesiones para dos</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">The <span class="text-shine">Unwinding</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Desde $130 · 60 min</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Flagami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">752 Flagami Blvd, Miami</p></div>''',
    '''<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="11">11</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl"><span data-es="Exterior e" data-en="Exterior &amp;">Exterior &amp;</span> <span class="text-shine" data-es="Interior" data-en="Interior">Interior</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Pintura y teñido" data-en="Painting &amp; staining">Painting &amp; staining</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span class="text-shine" data-es="Gratis" data-en="Free">Free</span> <span data-es="Cotizaciones" data-en="Estimates">Estimates</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Precios honestos y claros" data-en="Honest, upfront pricing">Honest, upfront pricing</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tallahassee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Condado de Leon, FL" data-en="Leon County, FL">Leon County, FL</p></div>''')
print("STRIP done")

# ---------------------------------------------------------------------------
# 7. MARQUEE (x2 bloques, cada palabra aparece 4 veces en total)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("The Unwinding", "Exterior Painting"),
    ("Rituales en Pareja", "Interior Painting"),
    ("Piedras Calientes", "Deck Staining"),
    ("Head Spa Holístico", "Cabinet Refinishing"),
    ("Flagami, Miami", "Tallahassee, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 8. LA EXPERIENCIA (About)
# ---------------------------------------------------------------------------
rep('''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/space-1.jpg" alt="Interior de Amani HeadSpa: paredes crema con nichos en arco, repisas de roble y camilla con textil acanalado" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/space-2.jpg" alt="Logo AMANI en serif dorado sobre pared crema, bajo lámpara escultural de yeso" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''',
    '''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/gmaps-3.jpg" alt="Freshly stained wood deck boards by John Copper Painting" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/gmaps-7.jpg" alt="Hand-finished wood door refinished by John Copper Painting" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''')
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5">La experiencia</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Nosotros" data-en="About">About</p>', n=1)
rep('''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms">Un refugio holístico<br /><span class="text-shine">en pleno Flagami</span></h2>''',
    '''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms" data-es="Oficio, con atención al <span class=&quot;text-shine&quot;>detalle</span>" data-en="Craftsmanship, with an eye for <span class=&quot;text-shine&quot;>detail</span>">Craftsmanship, with an eye for <span class="text-shine">detail</span></h2>''')
rep('''<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms">
          Amani es el head spa holístico de Miami: un espacio de calma cálida con paredes crema, arcos suaves, madera clara y luz tenue, pensado para que el tiempo se detenga. Cada ritual combina limpieza del cuero cabelludo, exfoliación, masaje terapéutico y mascarillas personalizadas.
        </p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms">
          Puedes vivirlo en solitario o compartirlo: las sesiones para dos son una de las experiencias más pedidas. Sales como lo promete su propio ritual: <em class="font-script text-[color:var(--accent-deep)]">refreshed, balanced, renewed</em>.
        </p>''',
    '''<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="John Copper Painting es una empresa de pintura y acabados con sede en Tallahassee, construida sobre una preparación cuidadosa y una ejecución limpia. Desde repintados completos de exteriores hasta la restauración de una sola puerta principal, cada trabajo recibe la misma atención: líneas de cinta rectas, superficies bien preparadas y un equipo que deja todo limpio al terminar." data-en="John Copper Painting is a Tallahassee-based painting and finishing company built on careful prep work and clean execution. From full exterior repaints to refinishing a single front door, every job gets the same attention: tape lines that stay straight, surfaces prepped right, and a crew that cleans up after itself.">John Copper Painting is a Tallahassee-based painting and finishing company built on careful prep work and clean execution. From full exterior repaints to refinishing a single front door, every job gets the same attention: tape lines that stay straight, surfaces prepped right, and a crew that cleans up after itself.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: una calificación perfecta de 5.0 estrellas en 11 reseñas de Google, cotizaciones gratis a domicilio, y dueños de casa que llaman primero a John Copper la próxima vez que algo necesita pintura, teñido o reparación." data-en="The result: a perfect 5.0-star rating across 11 Google reviews, free on-site estimates, and homeowners who call John Copper first the next time something needs a fresh coat, a stain, or a repair.">The result: a perfect 5.0-star rating across 11 Google reviews, free on-site estimates, and homeowners who call John Copper first the next time something needs a fresh coat, a stain, or a repair.</p>''')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">+<span data-count="3.9" data-decimals="1">3.9</span>K</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Instagram</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">60-90'</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">De ritual</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="11">11</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Cotizaciones" data-en="Estimates">Estimates</p></div>''')
rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-4">El equipo</p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-4" data-es="El equipo" data-en="The team">The team</p>')
rep('''<div class="flex flex-wrap gap-4">
            <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
              <img src="assets/raw/team-1.jpg" alt="Nilda Estevez, especialista de Amani HeadSpa" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,74,48,0.3)]" loading="lazy" />
              <span class="text-sm font-light">Nilda Estevez</span>
            </div>
            <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
              <img src="assets/raw/team-2.jpg" alt="Mireia Fenoy, especialista de Amani HeadSpa" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,74,48,0.3)]" loading="lazy" />
              <span class="text-sm font-light">Mireia Fenoy</span>
            </div>
            <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
              <img src="assets/raw/team-3.jpg" alt="Maria Gutierrez, especialista de Amani HeadSpa" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,74,48,0.3)]" loading="lazy" />
              <span class="text-sm font-light">Maria Gutierrez</span>
            </div>
            <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
              <img src="assets/raw/team-4.jpg" alt="Nildy Estevez, especialista de Amani HeadSpa" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(156,74,48,0.3)]" loading="lazy" />
              <span class="text-sm font-light">Nildy Estevez</span>
            </div>
          </div>''',
    '''<div class="flex flex-wrap gap-4">
            <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
              <span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-xs tracking-wide" style="background:var(--accent-ghost); color:var(--accent-deep); border:1px solid var(--accent-ghost)">JC</span>
              <span class="text-sm font-light">John Copper &middot; John Copper Painting</span>
            </div>
          </div>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 9. EL RITUAL -> COMO TRABAJAMOS
# ---------------------------------------------------------------------------
rep('<section id="ritual" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">',
    '<section id="metodo" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">')
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5">El ritual, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Cómo trabajamos" data-en="How we work">How we work</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms">Así se vive <span class="text-shine">The Unwinding</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms" data-es="Tu proyecto, de principio a <span class=&quot;text-shine&quot;>fin</span>" data-en="Your project, start to <span class=&quot;text-shine&quot;>finish</span>">Your project, start to <span class="text-shine">finish</span></h2>')
rep('''<p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3">Limpieza y exfoliación</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed">El ritual abre con una limpieza calmante y exfoliación del cuero cabelludo que estimula la circulación y cuida la salud capilar.</p>''',
    '''<p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Llama o Escribe" data-en="Call or Text">Call or Text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama o escribe al (850) 339-8575 y cuéntanos qué necesita pintura, teñido o reparación." data-en="Call or text (850) 339-8575 and tell us what needs painting, staining or fixing.">Call or text (850) 339-8575 and tell us what needs painting, staining or fixing.</p>''')
rep('''<p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3">Masaje terapéutico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed">Masaje craneal terapéutico, extendido al escote, que libera la tensión acumulada y te lleva a una relajación profunda.</p>''',
    '''<p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Cotización Gratis" data-en="Free Estimate">Free Estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Recorremos el trabajo contigo y te damos una cotización gratis y honesta antes de empezar." data-en="We walk the job with you and give a free, honest estimate before any work begins.">We walk the job with you and give a free, honest estimate before any work begins.</p>''')
rep('''<p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3">Mascarilla y piedras calientes</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed">Mascarilla capilar personalizada que nutre y restaura, mientras la terapia de piedras calientes relaja brazos y manos.</p>''',
    '''<p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Se Hace el Trabajo" data-en="The Work Gets Done">The Work Gets Done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Preparación cuidadosa, líneas limpias y materiales de calidad en cada trabajo, grande o pequeño." data-en="Careful prep, clean lines and quality materials on every job, big or small.">Careful prep, clean lines and quality materials on every job, big or small.</p>''')
rep('''<p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3">Cierre renovador</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed">Shampoo personalizado, masaje ligero de hombros y desenredado suave. Sales fresca, en equilibrio y renovada.</p>''',
    '''<p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Revisamos Juntos" data-en="Walk Results Together">Walk Results Together</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Antes de irnos, recorremos juntos el trabajo terminado para que sepas que quedó bien hecho." data-en="Before we leave, we walk through the finished work together so you know it was done right.">Before we leave, we walk through the finished work together so you know it was done right.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 10. SERVICIOS
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms">Elige tu <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms">Precios y duraciones publicados por Amani HeadSpa. Reserva online con confirmación inmediata.</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms" data-es="Servicios para <span class=&quot;text-shine&quot;>cada hogar</span>" data-en="Services for <span class=&quot;text-shine&quot;>every home</span>">Services for <span class="text-shine">every home</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Ningún proyecto es igual a otro. Cada trabajo recibe su propia cotización gratis y honesta antes de comenzar." data-en="No two projects are the same. Every job gets its own free, honest estimate before any work begins.">No two projects are the same. Every job gets its own free, honest estimate before any work begins.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:0ms; border-color: rgba(156,74,48,0.4); box-shadow: 0 18px 50px rgba(46,36,32,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pintura Exterior e Interior" data-en="Exterior &amp; Interior Painting">Exterior &amp; Interior Painting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Repintados completos de exterior, habitaciones interiores, molduras y preparación de superficies, para un acabado limpio y duradero." data-en="Full exterior repaints, interior rooms, trim and surface prep done right, for a clean finish that holds up.">Full exterior repaints, interior rooms, trim and surface prep done right, for a clean finish that holds up.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Cotización gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Vida al aire libre" data-en="Outdoor living">Outdoor living</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Teñido de Terrazas y Madera" data-en="Deck &amp; Wood Staining">Deck &amp; Wood Staining</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Teñido y sellado de terrazas, restauración de madera e impermeabilización para proteger superficies exteriores del sol y la lluvia de Florida." data-en="Deck staining and sealing, wood restoration and weatherproofing to protect outdoor surfaces from Florida sun and rain.">Deck staining and sealing, wood restoration and weatherproofing to protect outdoor surfaces from Florida sun and rain.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Cotización gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cocinas y baños" data-en="Kitchens &amp; baths">Kitchens &amp; baths</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Repintado de Gabinetes" data-en="Cabinet Refinishing">Cabinet Refinishing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pintura y repintado de gabinetes que transforma una cocina sin el costo de una remodelación completa." data-en="Cabinet painting and refinishing that transforms a kitchen without the cost of a full remodel.">Cabinet painting and refinishing that transforms a kitchen without the cost of a full remodel.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Cotización gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Detalle fino" data-en="Fine detail">Fine detail</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Restauración de Puertas y Molduras" data-en="Door &amp; Trim Restoration">Door &amp; Trim Restoration</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Restauración de puertas principales, molduras con vitral y trabajo de detalle para una primera impresión a la altura del resto de la casa." data-en="Front door refinishing, stained-glass trim and detail work for a first impression that matches the rest of the home.">Front door refinishing, stained-glass trim and detail work for a first impression that matches the rest of the home.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Cotización gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Pintura y Superficies" data-en="Paint &amp; Surfaces">Paint &amp; Surfaces</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Pintura interior" data-en="Interior painting">Interior painting</li>
            <li class="flex items-center gap-2" data-es="Pintura exterior" data-en="Exterior painting">Exterior painting</li>
            <li class="flex items-center gap-2" data-es="Molduras y zócalos" data-en="Trim &amp; baseboards">Trim &amp; baseboards</li>
            <li class="flex items-center gap-2" data-es="Preparación de superficies" data-en="Surface prep &amp; patching">Surface prep &amp; patching</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Madera y Teñido" data-en="Wood &amp; Staining">Wood &amp; Staining</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Teñido y sellado de terrazas" data-en="Deck staining &amp; sealing">Deck staining &amp; sealing</li>
            <li class="flex items-center gap-2" data-es="Restauración de puertas" data-en="Door refinishing">Door refinishing</li>
            <li class="flex items-center gap-2" data-es="Restauración de madera" data-en="Wood restoration">Wood restoration</li>
            <li class="flex items-center gap-2" data-es="Impermeabilización" data-en="Weatherproofing">Weatherproofing</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Gabinetes y Detalle" data-en="Cabinets &amp; Detail">Cabinets &amp; Detail</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Pintura de gabinetes" data-en="Cabinet painting">Cabinet painting</li>
            <li class="flex items-center gap-2" data-es="Repintado de cocina" data-en="Kitchen refinishing">Kitchen refinishing</li>
            <li class="flex items-center gap-2" data-es="Detalle fino de molduras" data-en="Fine trim detail">Fine trim detail</li>
            <li class="flex items-center gap-2" data-es="Asesoría de color" data-en="Color consultation">Color consultation</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8">Al reservar se solicita un depósito de $50 a $60 según el servicio.</p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="El precio depende del alcance y los materiales. Llama o escribe al (850) 339-8575 para una cotización gratis y honesta." data-en="Pricing depends on scope and materials. Call or text (850) 339-8575 for a free, honest estimate.">Pricing depends on scope and materials. Call or text (850) 339-8575 for a free, honest estimate.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 11. GALERIA
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms">Dentro del <span class="text-shine">spa</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms" data-es="Trabajos <span class=&quot;text-shine&quot;>recientes</span>" data-en="Recent <span class=&quot;text-shine&quot;>work</span>">Recent <span class="text-shine">work</span></h2>')
rep('''<a href="https://www.instagram.com/amaniheadspa/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @amaniheadspa
        </a>''',
    '''<a href="''' + TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span data-es="Llamar (850) 339-8575" data-en="Call (850) 339-8575">Call (850) 339-8575</span>
        </a>''')

OLD_GALLERY = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>\s*\n\n  <!-- MARQUEE -->',
    flags=re.S)
gm = OLD_GALLERY.search(h)
assert gm, "gallery grid not found"
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Pintura exterior en proceso" data-en="Exterior painting in progress">Exterior painting in progress</span><img src="assets/raw/gmaps-4.jpg" alt="John Copper Painting crew member painting exterior trim on a ladder" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Restauración de puerta" data-en="Door restoration">Door restoration</span><img src="assets/raw/gmaps-9.jpg" alt="Refinished front door with stained glass detail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:180ms"><span class="tile-cap" data-es="Repintado de porche y molduras" data-en="Porch &amp; trim repaint">Porch &amp; trim repaint</span><img src="assets/raw/gmaps-6.jpg" alt="Freshly painted covered porch with rocking chairs" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-[-2.5rem] img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Repintado de gabinetes" data-en="Cabinet refinishing">Cabinet refinishing</span><img src="assets/raw/gmaps-10.jpg" alt="Kitchen cabinets repainted in deep navy blue" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Repintado exterior completo" data-en="Full exterior repaint">Full exterior repaint</span><img src="assets/raw/gmaps-2.jpg" alt="Large farmhouse-style home with freshly painted wraparound porch" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Detalle de molduras exteriores" data-en="Exterior trim detail">Exterior trim detail</span><img src="assets/raw/gmaps-5.jpg" alt="Brick home with crisp white-painted window and door trim" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:360ms"><span class="tile-cap" data-es="Acabado de patio techado" data-en="Covered patio finish">Covered patio finish</span><img src="assets/raw/gmaps-8.jpg" alt="Covered patio with freshly painted tan exterior and white columns" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  <!-- MARQUEE -->'''
h = h[:gm.start()] + NEW_GALLERY + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 12. OPINIONES
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5">Opiniones</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms">Lo que dicen <span class="text-shine">nuestros clientes</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;4.9 de 5 · 73 reseñas en Google</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Reseñas" data-en="Reviews">Reviews</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms" data-es="Lo que dicen <span class=&quot;text-shine&quot;>los dueños de casa</span>" data-en="What <span class=&quot;text-shine&quot;>homeowners say</span>">What <span class="text-shine">homeowners say</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 11 reseñas en Google" data-en="5.0 of 5 · 11 reviews on Google">5.0 of 5 · 11 reviews on Google</span></p>')

OLD_SLIDES = re.compile(r'<div class="carousel-track">.*?</div>\s*</div>\s*(?=<div id="reviewDots")', flags=re.S)
sm_ = OLD_SLIDES.search(h)
assert sm_, "review slides not found"
NEW_SLIDES = '''<div class="carousel-track">
          <div class="carousel-slide">
            <figure class="glass glass-hover rounded-3xl p-8">
              <p class="stars text-sm mb-4">★★★★★</p>
              <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"One of the best experiences. John gave all pricing upfront. We have a mahogany front door that was in bad shape, he made it look brand new again! He also redid our cool deck at a third of the price of what I paid last time. John painted&hellip;"</blockquote>
              <figcaption class="text-sm"><span class="font-medium">Paula Burn</span> <span class="text-[color:var(--ink-40)]">&middot; Google</span></figcaption>
            </figure>
          </div>
          <div class="carousel-slide">
            <figure class="glass glass-hover rounded-3xl p-8">
              <p class="stars text-sm mb-4">★★★★★</p>
              <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mr. John was very professional and fair with his pricing. He did an exceptional job with the detail of the work. I had my garage floor painted and had done all the research. Then he showed up to give me a quote and told me all the steps he&hellip;"</blockquote>
              <figcaption class="text-sm"><span class="font-medium">Omar Quijada</span> <span class="text-[color:var(--ink-40)]">&middot; Google</span></figcaption>
            </figure>
          </div>
          <div class="carousel-slide">
            <figure class="glass glass-hover rounded-3xl p-8">
              <p class="stars text-sm mb-4">★★★★★</p>
              <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"John Copper and his team were a pleasure to have in our home. They are skilled artisans but also timely and reliable. John kept us apprised of what to expect and when at each stage of the job. We recommend him highly."</blockquote>
              <figcaption class="text-sm"><span class="font-medium">John Phelps</span> <span class="text-[color:var(--ink-40)]">&middot; Google</span></figcaption>
            </figure>
          </div>
        </div>
      </div>
      '''
h = h[:sm_.start()] + NEW_SLIDES + h[sm_.end():]

rep('<a href="https://www.google.com/maps/place/Amani+HeadSpa/@25.7629928,-80.3165977,17z/data=!3m1!4b1!4m6!3m5!1s0x88d9b9e5643c2807:0xbec5dea2b1e5c153!8m2!3d25.7629928!4d-80.3165977!16s%2Fg%2F11x6b88jdf" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2">Leer las 73 reseñas en Google</a>',
    '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 11 reseñas en Google" data-en="Read all 11 reviews on Google">Read all 11 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 13. UBICACION
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5">Visítanos</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Zona de Servicio" data-en="Service Area">Service Area</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms">Tu pausa queda <span class="text-shine">cerca</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms" data-es="Vamos a <span class=&quot;text-shine&quot;>tu casa</span>" data-en="We come to <span class=&quot;text-shine&quot;>you</span>">We come to <span class="text-shine">you</span></h2>')
rep('''<p class="font-medium mb-1">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">752 Flagami Blvd, Miami, FL 33144</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,111,77,0.4)]" href="https://www.google.com/maps/place/Amani+HeadSpa/@25.7629928,-80.3165977,17z/data=!3m1!4b1!4m6!3m5!1s0x88d9b9e5643c2807:0xbec5dea2b1e5c153!8m2!3d25.7629928!4d-80.3165977!16s%2Fg%2F11x6b88jdf" target="_blank" rel="noopener">Cómo llegar</a>'''.replace("rgba(138,111,77", rgbstr(NEW_ACCENT_DEEP)),
    '''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">11371 Gordon St, Tallahassee, FL 32317</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(156,74,48,0.4)]" href="''' + MAPS_URL + '''" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get Directions">Get Directions</a>''')
rep('''<p class="font-medium mb-1">Horario</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Lunes a Viernes: 10:00 AM a 7:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Sábado: 8:00 AM a 7:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Domingo: 8:00 AM a 5:00 PM</p>''',
    '''<p class="font-medium mb-1" data-es="Zona de Servicio" data-en="Service Area">Service Area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Tallahassee y el condado de Leon, FL" data-en="Tallahassee and surrounding Leon County, FL">Tallahassee and surrounding Leon County, FL</p>''')
rep('''<p class="font-medium mb-1">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Online: <a class="text-[color:var(--accent-deep)]" href="https://amaniheadspa.glossgenius.com" target="_blank" rel="noopener">amaniheadspa.glossgenius.com</a></p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Teléfono: <a class="text-[color:var(--accent-deep)]" href="tel:+13057906977">(305) 790-6977</a></p>''',
    '''<p class="font-medium mb-1" data-es="Contacto" data-en="Contact">Contact</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light"><span data-es="Llama o escribe" data-en="Call or text">Call or text</span>: <a class="text-[color:var(--accent-deep)]" href="''' + TEL + '''">(850) 339-8575</a></p>''')
rep('<iframe title="Mapa: Amani HeadSpa, 752 Flagami Blvd, Miami FL"\n          src="https://www.google.com/maps?q=Amani+HeadSpa,+752+Flagami+Blvd,+Miami,+FL+33144&output=embed"',
    '<iframe title="Map: John Copper Painting, 11371 Gordon St, Tallahassee FL"\n          src="https://www.google.com/maps?q=11371+Gordon+St,+Tallahassee,+FL+32317&output=embed"')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 14. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5">Fresca, en equilibrio, renovada.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Trabajo cuidadoso. Precios honestos." data-en="Careful work. Honest pricing.">Careful work. Honest pricing.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms">The Unwinding te está <span class="text-shine">esperando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms" data-es="Tu próximo proyecto empieza con una <span class=&quot;text-shine&quot;>cotización gratis</span>" data-en="Your next project starts with a <span class=&quot;text-shine&quot;>free estimate</span>">Your next project starts with a <span class="text-shine">free estimate</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms">Reserva tu ritual online en segundos, para ti o en pareja. Elige día, hora y especialista, y deja que Amani haga el resto.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Llama o escribe al (850) 339-8575 y cuéntanos sobre tu proyecto. Sin presión, sin sorpresas, solo una cotización honesta." data-en="Call or text (850) 339-8575 and tell us about your project. No pressure, no surprises, just an honest quote.">Call or text (850) 339-8575 and tell us about your project. No pressure, no surprises, just an honest quote.</p>')
rep('''<a href="https://amaniheadspa.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2">Reservar cita</a>
        <a href="tel:+13057906977" class="btn-ghost rounded-full px-10 py-4 text-sm">Llamar ahora</a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar Ahora" data-en="Call Now">Call Now</a>
        <a href="''' + SMS + '''" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Enviar Mensaje" data-en="Text Us">Text Us</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 15. FOOTER
# ---------------------------------------------------------------------------
rep('''<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-lg ring-1 ring-[rgba(232,207,166,0.35)] bg-[rgba(232,207,166,0.08)] text-[#e8cfa6]">A</span>
          <span class="font-display text-lg tracking-[0.12em] uppercase">Amani HeadSpa</span>'''.replace("rgba(232,207,166", "rgba(232,184,154").replace("#e8cfa6", "#e8b89a"),
    '''<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-lg ring-1 ring-[rgba(232,184,154,0.35)] bg-[rgba(232,184,154,0.08)] text-[#e8b89a]">JC</span>
          <span class="font-display text-lg tracking-[0.12em] uppercase">John Copper Painting</span>''')
rep('<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed">Miami\'s Holistic Head Spa. Wellness rituals para individuales y parejas: head spa + facials.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Pintura residencial, teñido y repintado en Tallahassee, FL. Preparación cuidadosa, precios honestos." data-en="Residential painting, staining and refinishing in Tallahassee, FL. Careful prep, honest pricing.">Residential painting, staining and refinishing in Tallahassee, FL. Careful prep, honest pricing.</p>')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3">Contacto</p>
        <p>752 Flagami Blvd, Miami, FL 33144</p>
        <p><a href="tel:+13057906977" class="hover:text-[#e8cfa6]">(305) 790-6977</a></p>
        <p><a href="mailto:amaniheadspa@gmail.com" class="hover:text-[#e8cfa6]">amaniheadspa@gmail.com</a></p>
        <p>Lun a Vie 10 AM a 7 PM · Sáb 8 AM a 7 PM · Dom 8 AM a 5 PM</p>'''.replace("#e8cfa6", "#e8b89a"),
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>11371 Gordon St, Tallahassee, FL 32317</p>
        <p><a href="''' + TEL + '''" class="hover:text-[#e8b89a]">(850) 339-8575</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3">Síguenos</p>
        <p><a href="https://www.instagram.com/amaniheadspa/" target="_blank" rel="noopener" class="hover:text-[#e8cfa6]">Instagram · @amaniheadspa</a></p>
        <p><a href="https://amaniheadspa.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#e8cfa6]">Reservas online · GlossGenius</a></p>'''.replace("#e8cfa6", "#e8b89a"),
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Zona de Servicio" data-en="Service Area">Service Area</p>
        <p data-es="Tallahassee, FL" data-en="Tallahassee, FL">Tallahassee, FL</p>
        <p data-es="Condado de Leon y alrededores" data-en="Leon County &amp; surrounding areas">Leon County &amp; surrounding areas</p>
        <p data-es="Lunes a domingo · Con cita" data-en="Monday to Sunday · By appointment">Monday to Sunday · By appointment</p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Amani HeadSpa. Todos los derechos reservados.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]"><span data-es="© 2026 John Copper Painting. Todos los derechos reservados." data-en="© 2026 John Copper Painting. All rights reserved.">© 2026 John Copper Painting. All rights reserved.</span></p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 16. Boton flotante (tel: en vez de calendario de reservas)
# ---------------------------------------------------------------------------
rep('''<a href="https://amaniheadspa.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f5f0e8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>'''.replace("#f5f0e8", NEW_BG),
    '''<a href="''' + TEL + '''" class="book-float" aria-label="Call John Copper Painting">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="''' + NEW_BG + '''" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
print("FLOAT BUTTON done")

# ---------------------------------------------------------------------------
# 17. Preloader (mono + wordmark)
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">A</span>', '<span class="pre-mono">JC</span>')
rep('<span class="pre-word">Amani HeadSpa</span>', '<span class="pre-word">John Copper Painting</span>')
print("PRELOADER done")

# ---------------------------------------------------------------------------
# 18. Script: insertar el mecanismo de Multilenguaje (data-es/data-en + toggle)
# ---------------------------------------------------------------------------
rep('''<script>
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;''',
    '''<script>
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    // Multilenguaje: data-es/data-en + toggle + localStorage + navigator.language
    const applyLang = l => {
      document.querySelectorAll('[data-es]').forEach(el => { el.innerHTML = el.dataset[l] || el.dataset.es; });
      document.documentElement.lang = l;
      try { localStorage.setItem('lang', l); } catch (e) {}
      document.getElementById('langToggle').textContent = l === 'es' ? 'EN' : 'ES';
    };
    let lang = 'en';
    try { lang = localStorage.getItem('lang') || (navigator.language || 'en').slice(0, 2); } catch (e) {}
    applyLang(lang === 'es' ? 'es' : 'en');
    document.getElementById('langToggle').addEventListener('click', () => applyLang(document.documentElement.lang === 'en' ? 'es' : 'en'));''')
print("I18N SCRIPT done")

open(PATH, "w", encoding="utf-8").write(h)
print("WROTE", PATH, len(h), "bytes")
